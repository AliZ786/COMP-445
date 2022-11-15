import os
import re
import sys
import cmd
import argparse
import socket
import threading
import json
from HttpServer import HttpRequestParser, FileOperation
from FileManager import FileManager

## Global variables for the program
RESPONSE_STRING = ''
METHOD = ''
DATA = ''
header = ''
request_string = ''
request_response = ''
content_type = ''
http_version = '1.1'
file = ''
file_content = ''
host = 'localhost'
client_response =''
server_response = ''
get = 0
getFiles = 1
getFile = 2
post = 3
download = 4
postFile = 5


## Argparse commands
parser = argparse.ArgumentParser(description = 'httpfs is a simple file server', conflict_handler = 'resolve')
parser.add_argument('-v','--verbose',help='Prints debugging messages', action='store_true' )
parser.add_argument('-p','--port',help='Specifies the port number that the server will listen and serve at.\n \
                                    Default is 8080.', type=int, default=8080 )
parser.add_argument('-d','--dir',help='Specifies the directory that the server will use to read/write \
                                    requested files.', default='data' )
args = parser.parse_args()



fm = FileManager()


def get_all_files(directory):
  files_list = []

  for root, dirs, files in os.walk(directory):
    for file in files:
      location = root + '/' + file
      files_list.append(location[(len(directory) +1):])
    
    # if '__pycache__' in dirs:
    #   dirs.remove('__pycache__')
  fm.status = '200'
  print(f"[Status Code - 200]: Able to get files from {directory}")
  return files_list

def checkAccess(file, directory):
  files_list = []

  if re.match(r'\.\.\/', file):
    fm.status = '400'
    response_string = f'[Error Code - 400]: Cannot access files from this {directory} ' 

  elif directory != 'data':
    fm.status = '400'
    response_string = '[Error Code -400]: Not the data directory, hence cannot access'

    response_string = response_string
  else:
    if re.match(r'\/', file):
      file = file.split('/')[-1]
      directory = file.split('/')[-2]

    files_list =  get_all_files(directory)

  return files_list, file, directory

def get_file(file, directory):

  files_list, file, directory = checkAccess(file, directory)  

  if len(files_list) >0:
    if file in files_list:
      try:
        print("Attempting to read files from the directory...\n")
        with open(directory + '/' + file, 'r') as f:
          response_string = f.read()
      
      finally:
        print("Finished attempting to read the files....")

      fm.status = '200'
      response_string = '[Success Code - 200]: '+response_string

    else:
      fm.status = '404'
      response_string = '[Error Code - 404]: ' + f'Unable to find file in the {directory}'

  else:
    fm.status= '404'
    response_string = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'


  return response_string

# def post_file(file, directory, content):
#   files_list, file, directory = checkAccess(file, directory)

#   if len(files_list) > 0:
#     try:
#       print("Attempting to write to a file.....\n")
#       with open(directory + '/'+ file, 'w') as f:
#         f.write(content)
    
#     except IOError as e:
#       print(e)
#       response_string = f'[Error Code - 400]: Unable to write content in this {directory}'
    
#     else:
#       response_string = f'[Success Code - 200]: Successful in writing to \'{directory}/{file}\''

#     finally:
#       print("Finished attempting to write to a file....\n")

#   else:
#     response_string = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'

#   return response_string

  
# def splitRequest(request):
#   content_type = 'application/json'

#   header, request_response = request.split('\r\n\r\n')

#   header_arr = header.split('\r\n')

#   method, request_string, http_version = header_arr[0].split(' ')

#   for string in header_arr[1:]:
#     if re.match(r'Content-Type', string):
#       content_type = string.split(':')[1]
    
#     elif re.match(r'Content-Disposition', string):
#       data = checkRequest('dowload')
#       if re.match(r'/(.+)', request_string):
#         file = request_string[1:]

#   callRequest()

# def callRequest():

#   data = ''
#   file_content = ''
#   if method == "GET":
#     if re.match(r'/get', request_string):
#       if request_string in ['/get', '/get?']:
#         temp_string = ''
      
#       else:
#         temp_location = request_string.split('?')[-1]
#         characters = {}
#         for item in temp_location.split('&'):
#           key, value = item.split('=')
#           characters[key] = value
        
#         temp_string = characters

#       data = checkRequest("defaultGet")
    
#     elif request_string == '/':
#       data = checkRequest('getFiles')
    
#     elif re.match(r'/(.+)', request_string):
#       data = checkRequest('getFile')
#       file = request_string[1:]
      
#     else:
#       data = checkRequest('invalid')

#   elif method == "POST":
#     if request_string == '/post':
#        file_content = request_response
#        data = checkRequest('defaultPost')
    
#     elif re.match(r'/(.+)', request_string):
#       data = checkRequest('postFile')
#       file_content = request_response
#       file = request_string[1:]

#   else:
#     file = checkRequest('invalid')

#   return data, file, file_content

def runServer(host, port, directory):
  listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if os.access(directory, os.R_OK,os.W_OK):
    try:
      ip_address = socket.gethostbyname(host)
      listener.bind((host, port))
      listener.listen(6)
      print(f'Server is listening at port number {port}\n')

      while True:
        conn, addr = listener.accept()
        threading.Thread(target= handle_client, args = (conn, addr, directory)).start()
      
    except KeyboardInterrupt:
      listener.close()
  else:
    print("[Error] Connection closed, access to directory denied:", d)


def handle_client(conn, addr, directory):
  print(f'New client from address number {addr}\n')

  try:
    cont = b''
    while True:
      buffer_content = conn.recv(1024)
      cont += buffer_content

      if len(buffer_content) < 1024:
        break
      
    client_response = cont.decode('utf-8')
    print(client_response)
    print(f'Client response received is " \n{client_response}')


    split_response = HttpRequestParser(client_response)

    server_response = _get_response(split_response, directory)
    
    conn.sendall(server_response.encode('utf-8'))

  finally:
    conn.close()
    print(f'Client with the address number {addr} has been disconnected')
    
def _get_response(request_parser, dir_path):
        # A file manager
        file_manager = FileManager()
        response = "HTTP1.0/ 404 Not Found\r\nContext-Type: application/json\r\n\r\nNo Response"
        # GET request

        # Basic GET
        if request_parser.operation == get:
            response = _generate_full_response_by_type(request_parser, request_parser.param, file_manager)
        # GET file list
        elif request_parser.operation == getFiles:    
            # return a list of current files in the data directory
            files_list = get_all_files(dir_path)
            print(f'files list is : {files_list}')
            response = _generate_full_response_by_type(request_parser,files_list,file_manager)
        # Get File Content
        elif request_parser.operation == getFile:
            file_content = get_file(request_parser.fileName, dir_path)
            response = _generate_full_response_by_type(request_parser, file_content, file_manager)
        # Get Download
        elif request_parser.operation == download:
            file_content = "Save me!"
            response = _generate_full_response_by_type(request_parser, file_content, file_manager)
        # Post Resource
        elif request_parser.operation == post:
            response = _generate_full_response_by_type(request_parser, request_parser.data, file_manager)

        # Post /bar
        elif request_parser.operation == postFile:
            content_response = file_manager.post_file_content(request_parser.fileName, dir_path, request_parser.data)
            response = _generate_full_response_by_type(request_parser, content_response, file_manager)
        # operation is invalid
        else:
            response = _generate_full_response_by_type(request_parser, 'Invalid Request', file_manager)

        return response
    

def _generate_full_response_by_type(request_parser, response_body, file_manager):
        # default return JSON format of response body
        body_output = {}
        status_message = ''
        # GET Methods
        if request_parser.operation == FileOperation.GetResource:
            body_output['args'] = request_parser.param
            fm.status = '200'
        elif request_parser.operation == FileOperation.GetFileList:
            body_output['files'] = response_body
        elif request_parser.operation == FileOperation.GetFileContent:
            if fm.status in ['400','404']:
                body_output['Error'] = response_body
            else:
                body_output['content'] = response_body
        # Download
        elif request_parser.operation == FileOperation.Download:
            fm.status = '200'
            body_output['Download Info'] = response_body
        # POST methods
        elif request_parser.operation == FileOperation.PostResource:
            body_output['data'] = response_body
        elif request_parser.operation == FileOperation.PostFileContent:
            if fm.status in ['400','404']:
                body_output['Error'] = response_body
            else:
                body_output['Info'] = response_body
        # Check Http Version
        elif request_parser.version != 'HTTP/1.0':
            # 505 : HTTP Version Not Support
            fm.status == '505'
        else:
            body_output['Invalid'] = response_body
        # set header info
        body_output['headers'] = request_parser.dict_header_info
        # set json format
        content = json.dumps(body_output)

        if fm.status == '200':
          status_message = ':OK'

        elif fm.status == '301':
          status_message = ':Moved Permanently'

        elif fm.status == '400':
          status_message = ':Bad Request'

        
        elif fm.status == '404':
          status_message = ':Not Found'

        elif fm.status == '505':
          status_message = ':HTTP Version Not Support'

        



        response_header = request_parser.version + ' ' + str(fm.status) + ' ' + \
            status_message + '\r\n' + \
            'Content-Length: ' + str(len(content)) + '\r\n' + \
            'Content-Type: ' + request_parser.contentType + '\r\n'
        # Content-Disposition
        if request_parser.operation == FileOperation.Download:
            response_header += f'Content-Disposition: attachment; filename={request_parser.fileName} \r\n'
        response_header += 'Connection: close' + '\r\n\r\n'
        full_response = response_header + content

        print(f'Server send Response to client:\n{full_response}')

        return full_response


# def returnRequest(splitResponse, directory):

#   body_output = {}
#   full_response = ''
#   FileManager()

#   if splitResponse == FileOperation.GetResource:
#     FileManager.get_file_content()
#     body_output['args'] = request_response

#   elif splitResponse == FileOperation.GetFileList:
#     FileManager.get_files_list_in_dir()
#     body_output['files'] = request_response

#   elif splitResponse == FileOperation.GetFileContent:
#     FileManager.get_file_content()
#     body_output['content'] = request_response

  
#   elif splitResponse == FileOperation.PostResource:
#     FileManager.post_file_content()
#     body_output['data'] = request_response

#   elif splitResponse == FileOperation.PostFileContent:
#     FileManager.post_file_content()
#     body_output['Info'] = request_response

#   elif splitResponse == FileOperation.Download:
#     FileManager.get_file_content()
#     body_output['Download Info'] = request_response
    

#   elif http_version != 'HTTP/1.0':
#     print("Error code -505")

#   else:
#     body_output['Invalid'] = request_response

#   content = json.dumps(body_output)

  
#   response_header = http_version +  ' ' +  '\r\n' + \
#             'Content-Length: ' + str(len(content)) + '\r\n' + \
#             'Content-Type: ' + content_type+ '\r\n'

#   if splitResponse == FileOperation.Download:
#     response_header += f'Content-Disposition: attachment; filename={file} \r\n'
#     response_header += 'Connection: close' + '\r\n\r\n'
#     full_response = response_header + content

#     print(full_response)

#   return full_response


def main():
  try:
    runServer(host, args.port, args.dir)

  except KeyboardInterrupt:
    print("\nGOODBYE")
    sys.exit(0)





main()
    




