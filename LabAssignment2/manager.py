import os
import re

class Manager:
 
  def __init__(self):
    self.status_code = ''
    self.request_response = ''


  def checkFiles(self, f, dir):
    files_list = []

    # Checks if the start of the string is a proper directory or not
    if re.match(r'\./.\/'. f):
      self.status_code = "400"
      self.request_response = "Directory is " + dir + "which is outside of the server"

    elif dir != "data":
      self.status_code = "400"
      self.request_response = "Directory is not the data directory"

    else:
      if re.match(r'\/',f):
        dir = f.split('/')[-2]
        f = f.split('/')[-1]

      files_list = self.totalFiles(dir)

    return files_list, dir, f
  
  def totalFiles(self, dir):
    files_list = []
    for root, files in os.walk(dir):

      for file in files:
        location = root + '/' + file
        files_list.append(location[(len(dir) +1):])

        self.status_code = '200'
        print(files_list + self.status_code)

    return files_list


  def get_response(self, f, dir):
    files_list, f, dir = self.checkFiles(f, dir)

    if len(files_list) > 0:
      if f in files_list:
        try:
          print("Attempting to read the files....")
          print()
          with open(dir + '/' + f, 'r') as fOpen:
            request_response = fOpen.read()
            
        finally:
          print("Finished attempting to read the files....")

        self.status_code = '200'
        self.request_response = request_response

      else:
        self.status_code = "404"
        self.request_response = "No file was found"

    else:
      self.status_code = "404"
      self.request_response ="There were no file in the current " + dir

    return self.request_response

  def post_response(self, f, dir, request):

    files_list, f, dir = self.checkFiles(f, dir)
    if len(files_list) > 0:
      try:
        print("Attempting to read files........")
        print()
        with open(dir + '/' + f, 'w') as fOpen:
          print("Will begin writing to file " +f)
          fOpen.write(request)

      except IOError as IOerr:
        self.status_code = "400"
        self.request_response =f'Could not write request to \'{dir}/{f}\', We have error of type {IOerr} '

      else:
        self.status_code = "200"
        self.request_response =  f'Attempting to write request into \'{dir}/{f}\', was a success. '
      finally:
        print("Finished attempting to read the files....")

    else:
      self.status_code = "400"
      self.request_response = f"Failed to write request to  \'{dir}/{f}\', the directory does not exist "

    return self.request_response







    

