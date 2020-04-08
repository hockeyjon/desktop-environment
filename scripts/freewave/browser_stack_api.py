import argparse
import json
import requests
import sys
from requests.auth import HTTPBasicAuth

USAGE = "\nUsage: browser_stack_api.py [scope] [id]\n" \
        "    scope: Scope of BrowserStack information to retrieve\n" \
        "           valid values are 'projects', 'build', 'session'\n" \
        "    id: id number for corresponding scope\n"


BROWSERSTACK_USER = "jonathankopp1"
BROWSERSTACK_PW = "jYFogzD3Pz4DcB4xAxhT"
NOT_FOUND = "The page you are looking for can't be found"
ACCESS_DENIED = "Access denied"

AUTHENTICATOR = HTTPBasicAuth(BROWSERSTACK_USER, BROWSERSTACK_PW)
BASE_URL = 'https://api.browserstack.com/automate'




def get_browser_stack_info(url):
    r = requests.get(url, auth=AUTHENTICATOR)
    return _format_response(r)


def _format_response(response):

    if not response.status_code == 200:
        print("HTTP status code: {}".format(response.status_code))
        if NOT_FOUND in response.text:
            error_msg = NOT_FOUND
        if ACCESS_DENIED in response.text:
            error_msg = ACCESS_DENIED
        else:
            output_file = "error.html"
            error_msg = "Unknown reason. See {} for details.".format(output_file)
            with open(output_file, "w") as f:
                f.writelines(response.text)
        response_text = error_msg
    else:
        try:
            data = json.loads(response.text)
            response_text = json.dumps(data, indent=4, sort_keys=True)
        except json.decoder.JSONDecodeError:
            response_text = "JSONDecodeError raised when parsing response:\n" + response.text

    return response_text

def browser_stack_url_builder(scope, id=None, limit=None, offset=None):
    """
    Builds the BrowserStack API call based on scope of the request

    Args:
        scope (str): type of API call to make.  Valid values are "projects",
        "project", "builds", "build", "sessions", "session". API calls in
        plural grammar are intened to not require a corresponding ID.

        id (str): optional id of corresponing scope to query.  id is required
        for any scope in singular grammar (i.e., project, build, session)

        limit (int): optional limit parameter to be used in query

        offset (int): optional offset parameter to be used in query

    Returns:
        BrowserStack API URL

    Raises:
        ValueError if parameters are invalid
    """
    url = "https://api.browserstack.com/automate/"

    if not scope in ["projects", "project", "builds", "build", "sessions", "session"]:
        raise ValueError("Invalid scope: {}".format(scope))

    if scope in ["project", "build", "session", "sessions"]:
        if not id:
            raise ValueError("No id provided for scope: {}".format(scope))
        if scope == "sessions":
            url = url + "builds/{}/sessions.json".format(id)
        else:
            url = url + scope + "s/{}.json".format(id)
    else:
        url = url + scope + ".json"

    if limit:
        url = url + "?limit={}".format(limit)

    if offset:
        offset_param = "offset={}".format(offset)
        if not limit:
            url = url + "?" + offset_param
        else:
            url = url + "&" + offset_param

    return url

if __name__ == '__main__':
    response_text = "Missing or unknown arguements.\n\n" + USAGE
    parser = argparse.ArgumentParser(description='JSON Pretty Dump')
    parser.add_argument('-s', '--scope', dest='scope', type=str, default=None,
                        help='Get BrowserStack API call based on scope')
    parser.add_argument('-i', '--id', dest='id', type=str, default=None,
                        help='Id of browser stack scope')
    parser.add_argument('-l', '--limit', dest='limit', type=int, default=None,
                        help='value of limit paramater to add to API URL')
    parser.add_argument('-o', '--offset', dest='offset', type=int, default=None,
                        help='value of limit paramater to add to API URL')
    parser.add_argument('-u', '--url', dest='url', type=str, default=None,
                        help='Get BrowserStack API call using raw URL.')
    parser.add_argument('-e', '--egrep', dest='egrep_vals', type=str, default=None,
                        help='comma delimited list of values to egrep on')
    parser.add_argument('-c', '--count', dest='count_val', type=str, default=None,
                        help='Sting to count number of occurances of')
    parser.add_argument('-f', '--first', dest='first', type=str, default=None,
                        help='Sting to count number of occurances of')
    args = parser.parse_args()

    #URL
    if args.scope:
        url = browser_stack_url_builder(args.scope, id=args.id, limit=args.limit, offset=args.offset)
    if args.url:
        url = args.url

    raw_text = get_browser_stack_info(url)

    if args.egrep_vals:
        response_text = ""
        egrep_list = args.egrep_vals.split(",")
        lines = raw_text.splitlines()
        for line in lines:
            for val in egrep_list:
                if val in line:
                    response_text = response_text + line + "\n"
    else:
        response_text = raw_text

    if args.count_val:
        count = 0
        lines = raw_text.splitlines()
        for line in lines:
            if args.count_val in line:
                count = count + 1
        response_text = response_text + '\t{c} lines with "{v}" were found.\n'.format(c=count, v=args.count_val)

    response_text = response_text + "\tURL: " + url + "\n\n"
    print(response_text)




