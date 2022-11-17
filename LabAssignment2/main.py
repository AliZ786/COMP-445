import os
import re
import argparse
import socket
import threading
import json


## Global variables for the program
BODY = ''
REQUEST_TYPE = ''
CALLED_REQUEST = ''
DATA = ''
HEADER = ''
CONTENT_TYPE = ''
HTTP_VERSION = '1.1'
FILE = ''
FILE_CONTENT = ''
HOST = 'localhost'
PORT = 8080
BUFFER_SIZE = 1024
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
                                    requested files.', default='./data' )
args = parser.parse_args()




def get_All_Files(directory):
  files_list = []
  STATUS_CODE = ''
  dir_list = []

  for root, dirs, files in os.walk(directory):
    for file in files:
      location = root + '/' + file
      files_list.append(location[(len(directory) +1):])

    for i in range (len(dirs)):
      dir_list.append(dirs[i])


  
  print(f'List of directories in {directory}: {dir_list}')

  STATUS_CODE = '200'
  return files_list, STATUS_CODE 

def check_Access(file, directory):
  files_list = []
  STATUS_CODE = ''

  if re.match(r'\.\.\/', file):
    STATUS_CODE - '400'
    RESPONSE_STRING = f'[Error Code - 400]: Cannot access files from this {directory} ' 

  elif directory != 'data':
    STATUS_CODE = 400
    RESPONSE_STRING= '[Error Code -400]: Not the data directory, hence cannot access'

    RESPONSE_STRING = RESPONSE_STRING
  else:
    if re.match(r'\/', file):
      file = file.split('/')[-1]
      directory = file.split('/')[-2]

    files_list =  get_All_Files(directory)

  return files_list, file, directory, STATUS_CODE

def get_file(file, directory):

  files_list = check_Access(file, directory) 
  STATUS_CODE =''
  RESPONSE_STRING = ''

  if file in files_list:
    try:
      print("Attempting to read files from the directory...\n")
      with open(directory + '/' + file, 'r', errors = 'ignore') as f:
        RESPONSE_STRING = f.read()
     
      if RESPONSE_STRING is not None:
       STATUS_CODE = '200'
       RESPONSE_STRING = f'[Success Code - 200]: Successfully got \'{file}\''  

      else:
       STATUS_CODE = '404'
       RESPONSE_STRING = '[Error Code - 404]: ' + f'Unable to find file in the directory {directory}'

    except FileNotFoundError:
       STATUS_CODE = '404'
       RESPONSE_STRING = '[Error Code - 404]: ' + f'Unable to find file in the directory {directory}'


    finally:
      print("Finished attempting to read")
        
  

  return RESPONSE_STRING, STATUS_CODE

def post_file(file, directory, content):
  files_list = check_Access(file, directory)
  STATUS_CODE =''

  if len(files_list) > 0:
    try:
      print("Attempting to write to a file.....\n")
      with open(directory + '/'+ file, 'w') as f:
        f.write(content)
    
    except IOError as e:
      print(e)
      STATUS_CODE = '400'
      RESPONSE_STRING = f'[Error Code - 400]: Unable to write content in this {directory}'
    
    else:
      STATUS_CODE = '200'
      RESPONSE_STRING = f'[Success Code - 200]: Successful in writing to \'{directory}/{file}\''

    finally:
      print("Finished attempting to write to a file....\n")

  else:
    STATUS_CODE = '404'
    RESPONSE_STRING = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'

  return RESPONSE_STRING, STATUS_CODE

  
def splitRequest(request):
  global CONTENT_TYPE, HEADER, FILE, REQUEST_TYPE, CALLED_REQUEST, BODY, REQUEST_STRING, HTTP_VERSION
  CONTENT_TYPE = 'application/json'


  HEADER, BODY = request.split('\r\n\r\n')

  header_arr = HEADER.split('\r\n')

  REQUEST_TYPE, REQUEST_STRING, HTTP_VERSION = header_arr[0].split(' ')

  for string in header_arr[1:]:
    if re.match(r'Content-Type', string):
      CONTENT_TYPE = string.split(':')[1]
    
    elif re.match(r'Content-Disposition', string):
      CALLED_REQUEST = DOWNLOAD
      if re.match(r'/(.+)', REQUEST_STRING):
        FILE = REQUEST_STRING[1:]

  callRequest()



def callRequest():
  global CALLED_REQUEST, REQUEST_TYPE, REQUEST_STRING, DEFAULT_GET, FILE, BODY, DATA, DOWNLOAD
  
  if REQUEST_TYPE == "GET" and CALLED_REQUEST != DOWNLOAD:
    if re.match(r'/get', REQUEST_STRING):
      if REQUEST_STRING in ['/get', '/get?']:
        DEFAULT_GET = ''
      
      else:
        temp_location = REQUEST_STRING.split('?')[-1]
        characters = {}
        for item in temp_location.split('&'):
          key, value = item.split('=')
          characters[key] = value
      
        DEFAULT_GET = characters
      CALLED_REQUEST = GET
    
    elif REQUEST_STRING == '/':
      CALLED_REQUEST = GET_FILES
    
    elif re.match(r'/(.+)', REQUEST_STRING):
      CALLED_REQUEST = GET_FILE
      FILE = REQUEST_STRING[1:]
      
    else:
      CALLED_REQUEST =  INVALID

  elif REQUEST_TYPE == "POST":
    if REQUEST_STRING == '/post':
       DATA = BODY
       CALLED_REQUEST = POST
    
    else:
      if re.match(r'/(.+)', REQUEST_STRING):
        CALLED_REQUEST = POST_FILE
        DATA = BODY
        FILE = REQUEST_STRING[1:]
      else:
        CALLED_REQUEST = INVALID
  elif CALLED_REQUEST == DOWNLOAD:
    pass
  else:
    CALLED_REQUEST = INVALID

def runServer(host, port, directory):
  listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  if os.access(directory, os.R_OK & os.W_OK):
      try:
        listener.bind((host, port))
        listener.listen(6)
        print(f'Server is listening at port number {port}\n')

        while True:
          conn, addr = listener.accept()
          threading.Thread(target= runClient, args = (conn, addr, directory)).start()
        
      except KeyboardInterrupt:
        print("\nYou have chosen to end the connection. Goodbye")
        listener.close()
  else:
      print("[Error] Connection closed, access to directory denied:", directory)


def runClient(conn, addr, directory):
  print(f'New client from address number {addr}\n')

  try:
    cont = b''
    while True:
      buffer_content = conn.recv(BUFFER_SIZE)
      cont += buffer_content

      if len(buffer_content) < BUFFER_SIZE:
        break
      
    client_response = cont.decode('utf-8')
    print(client_response)
    print(f'Client response received is " \n{client_response}')


    split_request = splitRequest(client_response)

    server_response = processRequest(split_request, directory)
    
    conn.sendall(server_response.encode('utf-8'))

  finally:
    conn.close()
    print(f'Client with the address number {addr} has been disconnected')
    
def processRequest(response, dir_path):
  # A file manager
  response = "HTTP1.0/ 404 Not Found\r\nContext-Type: application/json\r\n\r\nNo Response"
  # GET request

  # Basic GET
  if CALLED_REQUEST == GET:
    response = returnRequest(DEFAULT_GET, '200')
  # GET file list
  elif CALLED_REQUEST == GET_FILES:    
  # return a list of current files in the data directory
    array = get_All_Files(dir_path)
    files_list = array[0]
    status_code = array[1]
            
    print(f'files list is : {files_list}')
    response = returnRequest(files_list, status_code)
  # Get File Content
  elif CALLED_REQUEST == GET_FILE:
    array = get_file(FILE, dir_path)
    file_content = array[0]
    status_code = array[1]
    response = returnRequest(file_content, status_code)
  # Get Download
  elif CALLED_REQUEST == DOWNLOAD:
    file_content = "Save me!"
    response = returnRequest(file_content, '200')
  # Post Resource
  elif CALLED_REQUEST == POST:
    response = returnRequest(DATA, '200')

  # Post /bar
  elif CALLED_REQUEST == POST_FILE:
    array = post_file(FILE, dir_path, DATA)
    content_response = array[0]
    status_code = array[1]
    response = returnRequest(content_response, status_code)
  # operation is invalid
  else:
    response = returnRequest('Invalid Request', '400')

  return response
    

def returnRequest(response_body, status_code):
  # default return JSON format of response body
  body_output = {}
  status_message = ''
  STATUS_CODE = status_code

  # GET Methods
  if CALLED_REQUEST == GET:
    body_output['args'] = DEFAULT_GET
    STATUS_CODE = '200'  
  elif CALLED_REQUEST == GET_FILE:
    if STATUS_CODE == '400':
      STATUS_CODE = '400'
      body_output['Error'] = response_body
    elif STATUS_CODE == '404':
      STATUS_CODE = '404'
      body_output['Error'] = response_body
    else:
      body_output['content'] = response_body
  elif CALLED_REQUEST == GET_FILES:
    STATUS_CODE = '200'
    body_output['files'] = response_body
        
  elif CALLED_REQUEST == DOWNLOAD:
    STATUS_CODE = '200'
    body_output['Download Info'] = response_body

  elif CALLED_REQUEST == POST:
    STATUS_CODE = '200'
    body_output['data'] = response_body
  elif CALLED_REQUEST == POST_FILE:
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
  elif HTTP_VERSION != 'HTTP/1.1':
  # 505 : HTTP Version Not Support
    STATUS_CODE = '505'
  else:
    body_output['Invalid'] = response_body
  content = json.dumps(body_output)

  STATUS_CODE = STATUS_CODE

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

        


  response_header = HTTP_VERSION + ' ' + str(STATUS_CODE) + ' ' + \
    status_message + '\r\n' + \
    'Content-Length: ' + str(len(content)) + '\r\n' + \
    'Content-Type: ' + CONTENT_TYPE + '\r\n'
  # Content-Disposition
  if CALLED_REQUEST == DOWNLOAD:
     response_header += f'Content-Disposition: attachment; filename={FILE} \r\n'
  response_header += 'Connection: close' + '\r\n\r\n'
  full_response = response_header + content

  print(f'Response sent to the server would be: \n{full_response}')

  return full_response     

  

if (__name__ == '__main__'):
  runServer(HOST, args.port, args.dir)