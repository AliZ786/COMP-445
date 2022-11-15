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

  