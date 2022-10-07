import argparse
from sys import exit
import socket
from urllib.parse import urlparse


def help_output():
    output = '\nhttpc is a curl-like application but supports HTTP protocol only.\nUsage:\n\thttpc.py command ' \
             '[arguments]\nThe commands are:\n\tget\texecutes a HTTP GET request and prints the response.\n\tpost\t' \
             'executes a HTTP POST request and prints the response.\n\thelp\tprints this screen.\n\n' \
             'Use "httpc help [command]" for more information about a command.\n'
    return output


def help_get_output():
    output = '\nusage: httpc get [-v] [-h key:value] URL\n\nGet executes a HTTP GET request for a given URL.\n\t-v' \
             '\t\tPrints the detail of the response such as protocol, status, and headers.\n\t-h key:value\t' \
             'Associates headers to HTTP Request with the format "key:value".\n'
    return output


def help_post_output():
    output = '\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n\nPost executes a HTTP ' \
             'POST request for a given URL with inline data or from file.\n\t-v\t\tPrints the detail of the ' \
             'response such as protocol, status, and headers.\n\t-h key:value\tAssociates headers to HTTP Request ' \
             'with the format "key:value".\n\t-d string\tAssociates an inline data to the body HTTP POST request.' \
             '\n\t-f file\t\tAssociates the content of a file to the body HTTP POST request.\n\nEither [-d] or [-f] ' \
             'can be used but not both.'
    return output


def help_command():
    if args.arg2 == 'get':
        print(help_get_output())
    elif args.arg2 == 'post':
        print(help_post_output())
    else:
        if not args.arg2:
            print(help_output())
        else:
            print("Error: Unknown second argument. Options are 'get' or 'post' after 'help'")


def get_request(url, v, h):

    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((url.netloc, 80))

    if h:
        if ':' not in h:
            print("Error: please format the header (-h) in the form of 'key:value'.")
            return
        else:
            concatenated_url_string = "GET " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                      + url.netloc + "\r\n" + h + "\r\n\r\n"
    else:
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
    


def post_request(url, v, h):
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    skt.connect((url.netloc, 80))
  

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


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('command', type=str, help=help_output(), choices=['help', 'get', 'post'])
parser.add_argument('arg2', type=str)
parser.add_argument('-v', '--verbose', action="store_true")
parser.add_argument('-h', '--header')
parser.add_argument('-d', '--data')
parser.add_argument('-f', '--file')
parser.add_argument('-o', '--filename')
args = parser.parse_args()

if args.command == 'help':
    help_command()

elif args.command == 'get':
    
    if args.arg2:
        unquoted_url = args.arg2.replace("'", "")
        parsed_url = urlparse(unquoted_url)
        get_request(parsed_url, args.verbose, args.header)
    else:
        print('Error: no URL has been specified. URL is required after "get"')
        exit()

elif args.command == 'post':
   
    unquoted_url = args.arg2.replace("'", "")
    parsed_url = urlparse(unquoted_url)
    post_request(parsed_url, args.verbose, args.header)