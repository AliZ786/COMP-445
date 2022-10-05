
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






parser = argparse.ArgumentParser(description='httpc is a curl-like application but supports HTTP protocol only.')
parser.add_argument('command', type=str, help=help_method())
parser.add_argument('-gh', '--gethelp', help=help_get_method(), action="store_true")
parser.add_argument('-ph', '--posthelp', help=help_post_method(), action="store_true")
args = parser.parse_args()

if args.command == 'help':
    if args.gethelp:
        print(help_get_method())
    elif args.posthelp:
        print(help_post_method())
    else:
        print(help_method())

# elif args.command == 'get':
#     print('in get')

# elif args.command == 'post':
#     print('in post')
