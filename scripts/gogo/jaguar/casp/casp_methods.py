from __future__ import print_function

import sys
import datetime
import json

#import jwt
import requests
from socketIO_client import SocketIO, LoggingNamespace

requests.packages.urllib3.disable_warnings() # silence unsigned SSL cert warnings

AUTH_LABELS = []
AUTH_GROUPS = []
PASSWORD = "sharedsecret"
METHOD = 'http'
#SERVER = 'localhost'
SERVER = '192.168.1.15'
PORT = 3001
CONFIG_JSON = 'config.json'

def get_all_labels_groups():
    global AUTH_LABELS, AUTH_GROUPS, CONFIG_JSON
    with open(CONFIG_JSON, 'r') as f:
        cj = json.load(f)
    AUTH_LABELS = []
    AUTH_GROUPS = []
    for name, lbl in cj['labels'].items():
        AUTH_LABELS.append(name)
        AUTH_LABELS.append(str(lbl['config']['label']))
    for name, lbl in cj['labelgroups'].items():
        AUTH_GROUPS.append(name)

def new_auth_token(labels=None, labelgroup=None, timeoutInMinutes=400000, payload=None):
    if payload is None:
        if labels is None:
            if not AUTH_LABELS:
                get_all_labels_groups()
            labels = AUTH_LABELS
        if labelgroup is None:
            if not AUTH_GROUPS:
                get_all_labels_groups()
            labelgroup = AUTH_GROUPS
        payload = {
            "iss"         : "gogo" ,
            "appname"     : "PyClient",
            "version"     : "0.0.1",
            "apitype"     : ["poll", "sample", "stopsample", "stop", "stream", "stopstream"],
            "labels"      : labels,
            "labelgroup"  : labelgroup,
        }
        
    # lower-case these lists
    for key in ("apitype", "labels", "labelgroup"):
        for i in range(len(payload[key])):
            payload[key][i] = payload[key][i].lower()

    payload["iat"] = datetime.datetime.now() # issued at
    payload["exp"] = payload["iat"] + datetime.timedelta(minutes=timeoutInMinutes) # expires
    
    return jwt.encode(payload, PASSWORD, algorithm='HS256')

def get_session_token(authentication_token):
    url = "%s://%s:%d/api/a429/v1/authenticate" % (METHOD, SERVER, PORT)
    r = requests.post(url, data={'token': authentication_token}, verify=False)
    try:
        j = r.json()
    except ValueError:
        print("Not JSON:", r)
        return None
    if j.get('success'):
        return j.get('token')
    #print(j, file=sys.stderr)
    return None

# curl -k https://localhost:3000/api/a429/v1/poll/verticalacceleration?token=
def poll(label, stoken):
    url = "%s://%s:%d/api/a429/v1/poll/%s" % (METHOD, SERVER, PORT, label)
    data = {'token': stoken} if stoken else {}
    r = requests.post(url, data=data, verify=False)
    obj = r
    try:
        obj = r.json()
    except ValueError:
        print("Not JSON:", r)
    return obj

def stream(labels, stoken, fmt="{glabel} {time} {cdata} {rdata} {alabelno}", duration=10000):
    request = {'label': labels}
    if stoken:
        request['token'] = stoken
    socket_io_generic('stream', request, duration, fmt=fmt)

def sample(labels, intervalms, stoken, fmt="{glabel} {time} {cdata} {rdata} {alabelno}", duration=10000):
    request = {'label': labels, 'interval': intervalms}
    if stoken:
        request['token'] = stoken
    socket_io_generic('sample', request, duration, fmt=fmt)

def socket_io_generic(message, request, duration,
                      fmt):
    def on_stream_response(data):
        # yield data # would have to use a thread and a queue instead.
        # See http://stackoverflow.com/questions/9968592/turn-functions-with-a-callback-into-python-generators
        if 'glabel' in data:
            if fmt == 'raw':
                print(repr(data))
            else:
                print(fmt.format(**data))
        else:
            print('raw:', data)

    def on_unauthorized_response(*args):
        print('unauthorized:', "\n".join([repr(x) for x in args]))
            
    #print(request)
    server = METHOD + '://' + SERVER

    with SocketIO(server, PORT, LoggingNamespace, verify=False) as socketIO:
        socketIO.on('response', on_stream_response)
        socketIO.on('sampler', on_stream_response)
        socketIO.on('unauthorized', on_unauthorized_response)
        socketIO.emit(message, request)
        socketIO.wait(seconds=duration)
        print("Sending stop"+message, file=sys.stderr)
        socketIO.emit('stop'+message, request)
        socketIO.wait(seconds=1)

