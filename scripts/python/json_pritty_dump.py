import json
import argparse

USAGE = 'Usage: json_pritty_dump.py [-s <input json string>] ||' \
        ' [-i <input json file] [-o <input json file>]'

def json_file_formatter(in_file):
    with open(in_file, "r") as json_file:
        data = json.load(json_file)
        formatted = json.dumps(data, indent=4, sort_keys=True)
    return formatted

def json_string_formatter(json_string):
    data = json.loads(json_string)
    return json.dumps(data, indent=4, sort_keys=True)

def write_to_file(input, output_file):
    with open(output_file, "w"):
        output_file.writelines(input)



if __name__ == '__main__':

    #Define Arguments
    parser = argparse.ArgumentParser(description='JSON Pretty Dump')
    parser.add_argument('-i', '--inputf', dest='in_file', type=str, default=None,
                        help='Input json text')
    parser.add_argument('-o', '--outputf', dest='out_file', type=str, default=None,
                        help='Output json text in pretty format.')
    parser.add_argument('-s', '--inputs', dest='in_string', type=str, default=None,
                        help='Input json string.')

    #Parse arguments
    args = parser.parse_args()
    if not args.in_file and not args.in_string:
        print("JSON string or file to not provided")
        exit(1)

    if args.in_file and args.in_string:
        print("Use either JSON string or file options not both")
        exit(1)

    if args.in_file:
        formatted = json_file_formatter(args.in_file)

    if args.in_string:
        formatted = json_string_formatter(args.in_string)

    if args.out_file:
        write_to_file(formatted, args.out_string)

    print(formatted)
