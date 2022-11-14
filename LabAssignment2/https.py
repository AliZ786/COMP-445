import sys
import cmd
import argparse
import re
import socket
from server import Server
from manager import Manager

response_string = ''


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("command", type=str, choices = ["?"])
args = parser.parse_args()
print(args)

def get_help_response():
  response_string = '\nhttps is a simple file server.\n' \
                    'usage: httfs [-v] [-p PORT] [-d PATH-TO-DIR]\n' \
                     '-v Print debugging messages.\n' \
                     '-p Specifies the port number that the server will listen and serve at. Default is 8080.\n' \
                     '-d Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.'
  
  return response_string


if args.command == "?":
  print(get_help_response())



