import argparse
from sys import exit
import socket
from urllib.parse import urlparse

# Global variables 
delimiter = ":"
response_string = ''

# Argparse stuff 
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('command', type=str, choices=['help', 'help_get', 'help_post', 'get', 'post'])
parser.add_argument('-v',dest='verbose', action='store_true')
parser.add_argument('-h', dest='header', help='Associates headers to HTTP request with the format \'key:value\'', action='append')
parser.add_argument('-d', dest='data', type = str)
parser.add_argument('-f', dest = 'file', type=str)
parser.add_argument('-o', dest='filename')
parser.add_argument('-u',dest='url', type=str, help="url")
args = parser.parse_args()
print(args)
print("\n")



# Help functions
def help_response():
    response_string = '\nhttpc is a curl-like application but supports HTTP protocol only.\nUsage:\n\thttpc.py command ' \
             '[arguments]\nThe commands are:\n\tget\texecutes a HTTP GET request and prints the response.\n\tpost\t' \
             'executes a HTTP POST request and prints the response.\n\thelp\tprints this screen.\n\n' \
             'Use "httpc help [command]" for more information about a command.\n'
    return response_string


def help_get_response():
    response_string = '\nusage: httpc get [-v] [-h key:value] URL\n\nGet executes a HTTP GET request for a given URL.\n\t-v' \
             '\t\tPrints the detail of the response such as protocol, status, and headers.\n\t-h key:value\t' \
             'Associates headers to HTTP Request with the format "key:value".\n'
    return response_string


def help_post_response():
    response_string = '\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n\nPost executes a HTTP ' \
             'POST request for a given URL with inline data or from file.\n\t-v\t\tPrints the detail of the ' \
             'response such as protocol, status, and headers.\n\t-h key:value\tAssociates headers to HTTP Request ' \
             'with the format "key:value".\n\t-d string\tAssociates an inline data to the body HTTP POST request.' \
             '\n\t-f file\t\tAssociates the content of a file to the body HTTP POST request.\n\nEither [-d] or [-f] ' \
             'can be used but not both.'
    return response_string





def get_request_output(url, h):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url.netloc, 80))
    headers = ''
    
    if h:
        for i in range(len(args.header)):
            headers += args.header[i] +'\r\n'

        if delimiter not in args.header[i]:
            print("One or multiple headers do not follow the proper key:value format")
            exit()

        else:
         response_string = "GET " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                      + url.netloc + "\r\n" + headers + "\r\n\r\n"
    else:
        response_string = "GET " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                  + url.netloc + "\r\n\r\n"

    request = response_string.encode()
    sock.send(request)
    response = sock.recv(4096).decode("utf-8")
    sock.close()
    
    return response

def post_request_output(url, h, d, f):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((url.netloc, 80))

    data = None
    headers = ''

    if d:
        data = "Content-Length:" + str(len(d)) + "\r\n\r\n" + d

    elif f:
        file = open(f, 'r')
        d = file.read()
        file.close()
        data = "Content-Length:" + str(len(d)) + "\r\n\r\n" + d
        

    if h:
        for i in range(len(args.header)):
            headers += args.header[i] +'\r\n'

        if delimiter not in args.header[i]:
            print("One or multiple headers do not follow the proper key:value format")
            exit()

        if data:
                response_string = "POST " + url.path + "?" + url.query.replace("%26", "&") + \
                                          " HTTP/1.1\r\nHost: " + url.netloc + "\r\n" + headers + data + "\r\n"
                print('in data')
    
    else:
            response_string = "POST " + url.path + "?" + url.query.replace("%26", "&") + " HTTP/1.1\r\nHost: " \
                                  + url.netloc + "\r\n" + data + "\r\n"
            print("We are here")

    request = response_string.encode()
    sock.send(request)
    response = sock.recv(4096).decode("utf-8")
    sock.close()
    return response

def get_request(url, v, h, o):
    response = get_request_output(url, h)
    status_code = int(response.split("HTTP/")[1].split()[1]) # getting the initial status code number
    
    # WHILE REDIRECTION STATUS CODE
    while (status_code >= 300 and status_code <= 399):
        redirected_url = urlparse(response.split("Location:")[1].split()[0]) 
        response = get_request_output(redirected_url, h) 
        status_code = int(response.split("HTTP/")[1].split()[1]) 
        
    file = None

    if o:
        if v:
            file = open(o, 'w')
            file.write(response)
        else:
            file = open(o, 'w')
            try:
                index = response.index('{')
                file.write(response[index:])
            except ValueError:
                file.write(response)
    else:
        if v:
            print(response)
        else:
            try:
                index = response.index('{')
                print(response[index:])
            except ValueError:
                print(response)

def post_request(url, v, h, d, f, o):
    response = post_request_output(url, h, d, f)
    status_code = int(response.split("HTTP/")[1].split()[1]) # getting the initial status code number
    
    # WHILE REDIRECTION STATUS CODE
    while (status_code >= 300 and status_code <= 399):
        redirected_url = urlparse(response.split("Location:")[1].split()[0]) # getting redirection url
        response = post_request_output(redirected_url, h, d, f)
        status_code = int(response.split("HTTP/")[1].split()[1]) # getting the status code number

    file_to_write = None
  
    if o:
        if v:
            file_to_write = open(o, 'w')
            file_to_write.write(response)
        else:
            file_to_write = open(o, 'w')
            try:
                index = response.index('{')
                file_to_write.write(response[index:])
            except ValueError:
                file_to_write.write(response)
    else:

        if v:
            print(response)
        else:
            try:
                index = response.index('{')
                print(response[index:])
            except ValueError:
                print(response)



# Checks all the commands defined from argparse and creates the appropriate request 
if args.command == 'help':
        print(help_response())
elif args.command == 'help_post':
        print(help_post_response())
elif args.command == "help_get":
            print(help_get_response())

elif args.command == 'get':
    if args.data or args.file:
        print('Cannot have -d or -f in the get command. Please verify your syntax. ')
        exit()

    elif args.url:
        response_url = args.url.replace("'", "")
        parsed_response_url = urlparse(response_url)
        get_request(parsed_response_url, args.verbose, args.header, args.filename)

    else:
        print('Error: no URL has been specified. URL is required after "get"')
        exit()

elif args.command == 'post':
    if args.data and args.file:
       print("Error: -d and -f can't be used in the same post command. Please verify your syntax.")
       exit()

    elif args.data == None and args.file ==None:
        print("Atleast one of -d or -f should be in a post command. Please verify your syntax.")
        exit()

    elif args.url:
        response_url = args.url.replace("'", "")
        parsed_response_url = urlparse(response_url)
        post_request(parsed_response_url, args.verbose, args.header, args.data, args.file, args.filename)
    
    else:
        print('Error: no URL has been specified. URL is required after "post"')
        exit()
    

