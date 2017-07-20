"""
Script to be called with arguements.  Syntax:

python offloadWsiReport.py -p 8087 -t turbulance

"""


# Python Imports
import requests
import argparse


global WSI_END_POINT
global GET_REPORT_BASE_URL

def send_wsiReport(type):
    # Create and send/export mock WSI TAPS report to GATE-BSG
    turbulance_report = '{"taps": "QU ATLDDDL\\n.GOGOAIR 201631\\nDFD\\nFI ' \
                        'GS0001/AN 19079CC\\nDT GGO GOGO 201631 D02A\\n- TRP ' \
                        '163111  39.9181 -105.1144 1311 1310.7 -1230 -1452395 '\
                        '-14.52395 XXXXXX XXXXXX 3.999  3.999 XXXXX XXXXX XX ' \
                        '00 XX XX XXX 4 -1452395", ' \
                        '"serial": "34110002T0024"}'
    heartbeat_report = '{"taps": "QU ATLDDDL\\n.GOGOAIR 201643\\nDFD\\nFI ' \
                       'GS0001/AN 19079CC\\nDT GGO GOGO 201643 D04A\\n- TRP ' \
                       '164334  39.9181 -105.1144 1311 1310.7 -1230 -1452395' \
                       ' -14.52395 XXXXXX XXXXXX 1.000  1.000 XXXXX XXXXX XX ' \
                       'XX XX XX XXX 8 -1452395", ' \
                       '"serial": "34110002T0024"}'

    if type == "turbulance":
        report = turbulance_report
    else:
        report = heartbeat_report
    print "sending WSI report to {}".format(WSI_END_POINT)
    resp = requests.post(WSI_END_POINT, data=report)
    return resp




if __name__ == '__main__':

    #Define Arguments
    parser = argparse.ArgumentParser(description='WSI offload test')
    parser.add_argument('-p', '--port', dest='port', type=int,
                        help='Port to send HTTP POST messages to.')
    parser.add_argument('-t', '--type', dest='type', type=str,
                        help='Type of WSI report to send.')

    #Parse arguments
    args = parser.parse_args()

    #Use arguments
    BSG_BASE_URL = "http://52.38.114.180:" + str(args.port)
    WSI_END_POINT = BSG_BASE_URL + "/wsi"
    GET_REPORT_BASE_URL = BSG_BASE_URL + "/api/wsi/getLastReport"
    httpResp = send_wsiReport(args.type)
