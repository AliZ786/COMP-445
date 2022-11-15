import os
import re
import sys
import cmd
import argparse
import socket


## Global variables for the program
response_string = ''
method = ''
data = ''
header = ''
request_string = ''
request_response = ''
content_type = ''
http_version = '1.1'
file = ''
file_content = ''





def get_all_files(directory):
  files_list = []

  for root, files in os.walk(directory):
    for file in files:
      location = root + '/' + file
      files_list.append(location[(len(directory)):])

 
  print("[Status Code]: " + 200 + "Able to get files from " + directory)
  return files_list

def checkAccess(file, directory):
  files_list = []

  if re.match(r'\.\.\/', file):
    
    response_string = f'[Error Code - 400]: Cannot access files from this {directory} ' 

  elif directory != 'data':
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

      response_string = '[Success Code - 200]: '+response_string

    else:
      response_string = '[Error Code - 404]: ' + f'Unable to find file in the {directory}'

  else:
    response_string = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'


  return response_string

def post_file(file, directory, content):
  files_list, file, directory = checkAccess(file, directory)

  if len(files_list) > 0:
    try:
      print("Attempting to write to a file.....\n")
      with open(directory + '/'+ file, 'w') as f:
        f.write(content)
    
    except IOError as e:
      print(e)
      response_string = f'[Error Code - 400]: Unable to write content in this {directory}'
    
    else:
      response_string = f'[Success Code - 200]: Successful in writing to \'{directory}/{file}\''

    finally:
      print("Finished attempting to write to a file....\n")

  else:
    response_string = '[Error Code - 404]: ' + f'The {directory} does not contain any files.'

  return response_string


def checkRequest(request):

  
    if request == "getFiles":
        print("Getting all files from the directory.....\n")
    
    elif request == "defaultGet":
      print("Getting directory....\n")
    
    elif request == "defaultPost":
      print("Posting to default directory....\n")

    elif request == "postFile":
        print("Posting content for file.....\n")

    elif request == "getFile":
        print("Getting specific file from the command.....\n")

    elif request =="download":
        print("Downloading content.....\n")
    
    else:
      print("Request is invalid....\n")
        

    return request


def splitRequest(request):
  content_type = 'application/json'

  header, request_response = request.split('\r\n\r\n')

  header_arr = header.split('\r\n')

  method, request_string, http_version - header_arr[0].split('')

  for string in header_arr[1:]:
    if re.match(r'Content-Type', string):
      content_type = string.split(':')[1]
    
    elif re.match(r'Content-Disposition', string):
      data = checkRequest('dowload')
      if re.match(r'/(.+)', request_string):
        file = request_string[1:]

  callRequest()

def callRequest():
  if method == "GET":
    if re.match(r'/get', request_string):
      if request_string in ['/get', '/get?']:
        temp_string = ''
      
      else:
        temp_location = request_string.split('?')[-1]
        characters = {}
        for item in temp_location.split('&'):
          key, value = item.split('=')
          characters[key] = value
        
        temp_string = characters

      data = checkRequest("defaultGet")
    
    elif request_string == '/':
      data = checkRequest('getFiles')
    
    elif re.match(r'/(.+)', request_string):
      data = checkRequest('getFile')
      file = request_string[1:]
      
    else:
      data = checkRequest('invalid')

  elif method == "POST":
    if request_string == '/post':
       file_content = request_response
       data = checkRequest('defaultPost')
    
    elif re.match(r'/(.+)', request_string):
      data = checkRequest('postFile')
      file_content = request_response
      file = request_string[1:]

  else:
    file = checkRequest('invalid')

  return data, file, file_content






