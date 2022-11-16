import os
import re
import sys
import cmd
import argparse
import socket
import threading
import json
from HttpServer import HttpRequestParser, FileOperation
#from FileManager import FileManager

## Global variables for the program
RESPONSE_STRING = ''
BODY = ''
METHOD = ''
OPERATION = ''
DATA = ''
HEADER = ''
REQUEST_STRING = ''
REQUEST_RESPONSE = ''
CONTENT_TYPE = ''
HTTP_VERSION = '1.1'
FILE = ''
FILE_CONTENT = ''
HOST = 'localhost'
PORT = 8080
DIRECTORY = os.getcwd()
BUFFER_SIZE = 1024
CLIENT_RESPONSE =''
SERVER_RESPONSE = ''
GET = 0
GET_FILES = 1
GET_FILE = 2
POST = 3
DOWNLOAD = 4
POST_FILE = 5
INVALID = 6
STATUS_CODE = '404'


## Argparse commands
parser = argparse.ArgumentParser(description = 'httpfs is a simple file server', conflict_handler = 'resolve')
parser.add_argument('-v','--verbose',help='Prints debugging messages', action='store_true' )
parser.add_argument('-p','--port',help='Specifies the port number that the server will listen and serve at.\n \
                                    Default is 8080.', type=int, default=PORT )
parser.add_argument('-d','--dir',help='Specifies the directory that the server will use to read/write \
                                    requested files.', default='data' )
args = parser.parse_args()



# fm = FileManager()


def get_all_files(directory):
  files_list = []
  STATUS_CODE = ''

  for root, dirs, files in os.walk(directory):
    for file in files:
      location = root + '/' + file
      files_list.append(location[(len(directory) +1):])
    
    # if '__pycache__' in dirs:
    #   dirs.remove('__pycache__')
  STATUS_CODE = '200'
  return files_list, STATUS_CODE

def checkAccess(file, directory):
  files_list = []
  STATUS_CODE = ''

  if re.match(r'\.\.\/', file):
    STATUS_CODE - '400'
    response_string = f'[Error Code - 400]: Cannot access files from this {directory} ' 

  elif directory != 'data':
    STATUS_CODE = 400
    response_string = '[Error Code -400]: Not the data directory, hence cannot access'

    response_string = response_string
  else:
    if re.match(r'\/', file):
      file = file.split('/')[-1]
      directory = file.split('/')[-2]

    files_list =  get_all_files(directory)

  return files_list, file, directory, STATUS_CODE

def get_file(file, directory):

  files_list = checkAccess(file, directory) 
  STATUS_CODE =''
  response_string = ''

  if file in files_list:
    try:
      print("Attempting to read files from the directory...\n")
      with open(directory + '/' + file, 'r', errors = 'ignore') as f:
        response_string = f.read()
     
      if response_string is not None:
       STATUS_CODE = '200'
       response_string = f'[Success Code - 200]: Successfully got \'{file}\''  

      else:
       STATUS_CODE = '404'
       response_string = '[Error Code - 404]: ' + f'Unable to find file in the directory {directory}'

    except FileNotFoundError:
       STATUS_CODE = '404'
       response_string = '[Error Code - 404]: ' + f'Unable to find file in the directory {directory}'


    finally:
      print("Finished attempting to read")
        
  

  return response_string, STATUS_CODE

def post_file(file, directory, content):
  files_list = checkAccess(file, directory)
  STATUS_CODE =''

  if len(files_list) > 0:
    try:
      print("Attempting to write to a file.....\n")
      with open(directory + '/'+ file, 'w') as f:
        f.write(content)
    
    except IOError as e:
      print(e)
      STATUS_CODE = '400'
      response_string = f'[Error Code - 400]: Unable to write content in this {directory}'
    
    else:
      STATUS_CODE = '200'
      response_string = f'[Success Code - 200]: Successful in writing to \'{directory}/{file}\''

    finally:
      print("Finished attempting to write to a file....\n")

  else:
    STATUS_CODE = '404'
    response_string = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'

  return response_string, STATUS_CODE

  
def splitRequest(request):
  global CONTENT_TYPE, HEADER, FILE, METHOD, OPERATION, BODY, RESOURCE, http_version
  CONTENT_TYPE = 'application/json'


  HEADER, BODY = request.split('\r\n\r\n')

  header_arr = HEADER.split('\r\n')

  METHOD, RESOURCE, http_version = header_arr[0].split(' ')

  for string in header_arr[1:]:
    if re.match(r'Content-Type', string):
      CONTENT_TYPE = string.split(':')[1]
    
    elif re.match(r'Content-Disposition', string):
      OPERATION = DOWNLOAD
      if re.match(r'/(.+)', RESOURCE):
        FILE = RESOURCE[1:]

  callRequest()



def callRequest():
  global OPERATION, METHOD, RESOURCE, PARAM, FILE, BODY, DATA, DOWNLOAD
  
  if METHOD == "GET" and OPERATION != DOWNLOAD:
    if re.match(r'/get', RESOURCE):
      if RESOURCE in ['/get', '/get?']:
        PARAM = ''
      
      else:
        temp_location = RESOURCE.split('?')[-1]
        characters = {}
        for item in temp_location.split('&'):
          key, value = item.split('=')
          characters[key] = value
      
        PARAM = characters
      OPERATION = GET
    
    elif RESOURCE == '/':
      OPERATION = GET_FILES
    
    elif re.match(r'/(.+)', RESOURCE):
      OPERATION = GET_FILE
      FILE = RESOURCE[1:]
      
    else:
      OPERATION =  INVALID

  elif METHOD == "POST":
    if RESOURCE == '/post':
       DATA = BODY
       OPERATION = POST
    
    else:
      if re.match(r'/(.+)', RESOURCE):
        OPERATION = POST_FILE
        DATA = BODY
        FILE = RESOURCE[1:]
      else:
        OPERATION = INVALID
  elif OPERATION == DOWNLOAD:
    pass
  else:
    OPERATION = INVALID

def runServer(host, port, directory):
  listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if os.access(directory, os.R_OK & os.W_OK):
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
    print("[Error] Connection closed, access to directory denied:", directory)


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
        response = "HTTP1.0/ 404 Not Found\r\nContext-Type: application/json\r\n\r\nNo Response"
        # GET request

        # Basic GET
        if OPERATION == GET:
            response = _generate_full_response_by_type(request_parser, PARAM, '200')
        # GET file list
        elif OPERATION == GET_FILES:    
            # return a list of current files in the data directory
            array = get_all_files(dir_path)
            files_list = array[0]
            status_code = array[1]
            
            print(f'files list is : {files_list}')
            response = _generate_full_response_by_type(request_parser,files_list, status_code)
        # Get File Content
        elif OPERATION == GET_FILE:
            array = get_file(request_parser.fileName, dir_path)
            file_content = array[0]
            status_code = array[1]
            response = _generate_full_response_by_type(request_parser, file_content, status_code)
        # Get Download
        elif OPERATION == DOWNLOAD:
            file_content = "Save me!"
            response = _generate_full_response_by_type(request_parser, file_content, '200')
        # Post Resource
        elif OPERATION == POST:
            response = _generate_full_response_by_type(request_parser, DATA, '200')

        # Post /bar
        elif OPERATION == POST_FILE:
            array = post_file(request_parser.fileName, dir_path, DATA)
            content_response = array[0]
            status_code = array[1]
            response = _generate_full_response_by_type(request_parser, content_response, status_code)
        # operation is invalid
        else:
            response = _generate_full_response_by_type(request_parser, 'Invalid Request', '400')

        return response
    

def _generate_full_response_by_type(request_parser, response_body, status_code):
        # default return JSON format of response body
        body_output = {}
        status_message = ''
        STATUS_CODE = status_code
        # GET Methods
        if OPERATION == GET:
          body_output['args'] = PARAM
          STATUS_CODE = '200'  
        elif OPERATION == GET_FILE:
          if STATUS_CODE == '400':
            STATUS_CODE = '400'
            body_output['Error'] = response_body
          elif STATUS_CODE == '404':
            STATUS_CODE = '404'
            body_output['Error'] = response_body
          else:
            body_output['content'] = response_body
        elif OPERATION == GET_FILES:
            STATUS_CODE = '200'
            body_output['files'] = response_body
        
        # Download
        elif OPERATION == DOWNLOAD:
            STATUS_CODE = '200'
            body_output['Download Info'] = response_body
        # POST methods
        elif OPERATION == POST:
            STATUS_CODE = '200'
            body_output['data'] = response_body
        elif OPERATION == POST_FILE:
            if STATUS_CODE == '404':
                STATUS_CODE = '404'
                body_output['Error'] = response_body
            
            elif STATUS_CODE == '400':
              STATUS_CODE = '400'
              body_output['Error'] = response_body

            else:
                STATUS_CODE = '200'
                body_output['Info'] = response_body
        # Check Http Version
        elif http_version != 'HTTP/1.1':
            # 505 : HTTP Version Not Support
            STATUS_CODE = '505'
        else:
            body_output['Invalid'] = response_body
        content = json.dumps(body_output)

        STATUS_CODE = STATUS_CODE
        print(STATUS_CODE)

        if STATUS_CODE == '200':
          status_message = ':OK'

        elif STATUS_CODE == '301':
          status_message = ':Moved Permanently'

        elif STATUS_CODE == '400':
          status_message = ':Bad Request'

        elif STATUS_CODE == '404':
          status_message = ':Not Found'

        elif STATUS_CODE == '505':
          status_message = ':HTTP Version Not Support'

        
        print(STATUS_CODE)


        response_header = http_version + ' ' + str(STATUS_CODE) + ' ' + \
            status_message + '\r\n' + \
            'Content-Length: ' + str(len(content)) + '\r\n' + \
            'Content-Type: ' + CONTENT_TYPE + '\r\n'
        # Content-Disposition
        if OPERATION == DOWNLOAD:
            response_header += f'Content-Disposition: attachment; filename={FILE} \r\n'
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
    runServer(HOST, args.port, args.dir)

  except KeyboardInterrupt:
    print("\nGOODBYE")
    sys.exit(0)

main()