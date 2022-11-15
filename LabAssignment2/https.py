import sys
import cmd
import argparse
import re
import socket
from server import Server
from manager import Manager

response_string = ''


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-v", dest="verbose", help="print debugging messages", action="store_true", required = False)
parser.add_argument("-p", dest="port", type=int, help="specifies port number server will listen on", default = 8080)
parser.add_argument("-d", dest="directory", type=str, help="specifies the directory", default = "./data")
args = parser.parse_args()
print(args)




def get_help_response():
  response_string = '\nhttps is a simple file server.\n' \
                    'usage: httfs [-v] [-p PORT] [-d PATH-TO-DIR]\n' \
                     '-v Print debugging messages.\n' \
                     '-p Specifies the port number that the server will listen and serve at. Default is 8080.\n' \
                     '-d Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.'
  
  return response_string


def run_server():
  

