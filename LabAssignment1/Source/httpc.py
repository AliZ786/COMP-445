import argparse
from sys import exit
import socket
from urllib.parse import urlparse

def help_method():
    string = '\nhttpc is a curl-like application but supports HTTP protocol only.\nUsage:\n\thttpc.py command [arguments]\n' + \
           'The commands are:\n\tget\texecutes a HTTP GET request and prints the response.\n\tpost\texecutes a HTTP' + \
           ' POST request and prints the response.\n\thelp\tprints this screen.\n\n' + \
           'Use "httpc help [command]" for more information about a command.'
    return string


def help_get_method():
  string = '\nusage: httpc get [-v] [-h key:value] URL\nGet executes a HTTP GET request for a given URL.\n\t-v\t' + \
               '\tPrints the detail of the response such as protocol, status, and headers.\n\t-h key:value\tAssociates ' \
               'headers to HTTP Request with the format "key:value".'
  return string

def help_post_method():
    string = '\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\nPost executes a HTTP POST ' \
                'request for a given URL with inline data or from file.\n\t-v\t\tPrints the detail of the response such ' \
                'as protocol, status, and headers.\n\t-h key:value\tAssociates headers to HTTP Request with the format ' \
                '"key:value".\n\t-d string\tAssociates an inline data to the body HTTP POST request.\n\t-f file\t\t' \
                'Associates the content of a file to the body HTTP POST request.\n\nEither [-d] or [-f] can be used ' \
                'but not both.'
    return string


def get_request(url, v):

    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((url.netloc, 80))


    concatenated_url_string = "GET " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                  + url.netloc + "\r\n\r\n"

    request = concatenated_url_string.encode()
    skt.send(request)
    file = None


    if v:
        print(skt.recv(4096).decode("utf-8"))
    else:
        response = skt.recv(4096).decode("utf-8")
        try:
            index = response.index('{')
            print(response[index:])
        except ValueError:
            print(response)

    skt.close()
    if file:
        file.close()

def post_method(url, v, h):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((url.netloc, 80))


    concatenated_url_string = "POST " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                      + url.netloc + "\r\n" + "\r\n\r\n"

    request = concatenated_url_string.encode()
    skt.send(request)

    if h:
        if ':' not in h:
            print("Error: please format the header (-h) in the form of 'key:value'.")
            return
        else:
            concatenated_url_string = "POST " + url.path + "?" + url.query.replace("%26", "&") + \
                                          " HTTP/1.1\r\nHost: " + url.netloc + "\r\n" + h + "\r\n\r\n"
    else:
        concatenated_url_string = "POST " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                      + url.netloc + "\r\n" + "\r\n\r\n"

    request = concatenated_url_string.encode()
    skt.send(request)

    if v:
            print(skt.recv(4096).decode("utf-8"))
    else:
            response = skt.recv(4096).decode("utf-8")
            try:
                index = response.index('{')
                print(response[index:])
            except ValueError:
                print(response)

    skt.close()





parser = argparse.ArgumentParser(description='httpc is a curl-like application but supports HTTP protocol only.')
parser.add_argument('command', type=str, help=help_method())
parser.add_argument('arg2', type=str)
parser.add_argument('-gh', '--gethelp', help=help_get_method(), action="store_true")
parser.add_argument('-ph', '--posthelp', help=help_post_method(), action="store_true")

parser.add_argument('-v', '--verbose', action="store_true")
parser.add_argument('-h', '--header')
args = parser.parse_args()

if args.command == 'help':
    if args.gethelp:
        print(help_get_method())
    elif args.posthelp:
        print(help_post_method())
    else:
        print(help_method())

elif args.command == 'get':
    if args.arg2:
        unquoted_url = args.arg2.replace("'", "")
        parsed_url = urlparse(unquoted_url)
        get_request(parsed_url, args.verbose)
    else:
        print('Error: no URL has been specified. URL is required after "get"')
        exit()

elif args.command == 'post':
    if args.arg2:
        unquoted_url = args.arg2.replace("'", "")
        parsed_url = urlparse(unquoted_url)
        post_method(parsed_url, args.verbose, args.headers)
    else:
        print('Error: no URL has been specified. URL is required after "post"')
        exit()
    
