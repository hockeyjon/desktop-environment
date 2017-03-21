#!/usr/bin/python

from __future__ import print_function

import sys
import os
import argparse
import time

import casp_methods

help_desc = """
A CASP client
Use -t to get a session token, or re-use one by setting STOKEN in environment:
 $ export STOKEN=`./client.py -t`
Requires exactly one "action" argument: -A | -t | -p <labels> | -s <labels> | -a <labels>
Multiple labels are separated with '+'. The label 'all' is all labels from config.json.
By default, auth token authenticates all labels, which requires reading config.json.
  So if requesting tokens, implicitly or explicitly, and you have not provided --labels,
  you will want to provide --json or set LABELCONFIG.
"""

parser = argparse.ArgumentParser(description=help_desc)
parser.add_argument('-A', '--auth-token', action='store_true',
                    help='Get a new authentication token only')
parser.add_argument('-t', '--sess-token', action='store_true',
                    help='Get a new session token only')
parser.add_argument('-n', '--no-token', action='store_true',
                    help='Do not pass a token with the request')
parser.add_argument('-p', '--poll', action='store', help='Perform polling on <poll> labels. Use "all" for all labels.')
parser.add_argument('-s', '--stream', action='store', help='stream <stream> labels')
parser.add_argument('-a', '--sample', action='store', help='sample <stream> labels')

# Optional:
parser.add_argument('-P', '--port', action='store', type=int, default=3000)
parser.add_argument('-S', '--server', action='store', default='localhost')
parser.add_argument('-i', '--interval', action='store', type=int,
                    help='Interval in ms to poll at. Default is to poll once only.')
parser.add_argument('-d', '--duration', action='store', type=int, default=200000,
                    help='Duration in seconds for sampling or streaming')
parser.add_argument('-f', '--format', action='store', default='{glabel} {time} {cdata} {rdata} {alabelno}',
                    help='Format of printout or "raw"')
parser.add_argument('-l', '--labels', action='store', help='Specify labels for auth token ("+" separates multiple)')
parser.add_argument('-g', '--labelgroup', action='store', help='Specify label groups for auth token ("+" separator)')
parser.add_argument('-j', '--json', action='store', help='config file for all labels and groups (env: LABELCONFIG)',
                    default='config.json')
args = parser.parse_args()

# Ensure just one "action" requested
one_true = {False: 0, True: 1}
action_count = (one_true[args.auth_token] +
                one_true[args.sess_token] +
                one_true[args.poll is not None] +
                one_true[args.stream is not None] +
                one_true[args.sample is not None])
if action_count != 1:
    print("Need exactly one action argument: -A | -t | -p <labels> | -s <labels> | -a <labels>",
          file=sys.stderr)
    #print("  Found " + repr(action_count), file=sys.stderr)
    sys.exit(1)

#print(args)

def all_if_all(label):
    return "+".join(casp_methods.AUTH_LABELS) if label == "all" else label

at = None
def get_auth_token():
    global at
    if at is None:
        labels = None # None -> all labels
        groups = None # same
        if args.labels is not None: # null string => True in this case -- no labels
            labels = args.labels.split('+')
            groups = [] # specifying labels implies specifying groups as well
        if args.labelgroup is not None:
            groups = args.labelgroup.split('+')
        at = casp_methods.new_auth_token(labels, groups)

if args.json:
    casp_methods.CONFIG_JSON = args.json
elif 'LABELCONFIG' in os.environ:
    casp_methods.CONFIG_JSON = os.environ['LABELCONFIG']

casp_methods.SERVER = args.server
casp_methods.PORT = args.port

######### Here's where the stuff happens:

if args.auth_token:
    get_auth_token()
    print(at)
    sys.exit(0)

if args.no_token:
    st = None
else:
    st = os.environ.get('STOKEN')
    if args.sess_token or not st:
        get_auth_token()
        #print(at)
        st = casp_methods.get_session_token(at)
        if args.sess_token:
            print(st)
            sys.exit(0)
            time.sleep(1.1)

if args.poll:
    while True:
        j = casp_methods.poll(all_if_all(args.poll), st)
        if j:
            #print('raw:', j)
            try:
                for data in j:
                    if args.format == 'raw':
                        # raw is not actually raw but essentially equivalent. json -> python repr
                        print(repr(data))
                    else:
                        print(args.format.format(**data))
                        #print(data.get('glabel'), data.get("alabelno"), data.get("time"), data.get("rdata"), data.get("cdata"))
            except:
                # something different
                print('raw:', j)
        if args.interval:
            time.sleep(args.interval / 1000.)
        else:
            break
    sys.exit(0) # unreachable

if args.stream:
    casp_methods.stream(all_if_all(args.stream), st,
                        fmt=args.format,
                        duration=args.duration)

if args.sample:
    interval = args.interval if args.interval else 1000
    casp_methods.sample(all_if_all(args.sample), interval, st,
                        fmt=args.format,
                        duration=args.duration)
