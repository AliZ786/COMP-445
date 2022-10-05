
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




parser = argparse.ArgumentParser(description='httpc is a curl-like application but supports HTTP protocol only.')
parser.add_argument('command', type=str, help=help_method())
parser.add_argument('-gh', '--gethelp', help='get', action="store_true")
parser.add_argument('-ph', '--posthelp', help='post', action="store_true")
args = parser.parse_args()

if args.command == 'help':
    if args.gethelp:
        print("get")
    elif args.posthelp:
        print("post")
    else:
        print(help_method())

# elif args.command == 'get':
#     print('in get')

# elif args.command == 'post':
#     print('in post')
