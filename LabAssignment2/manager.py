import os
import re
import threading

class Manager:
  status_code = ""
  request_response = ""
  status_list = {}
  

  def __init__(self):
    self.status_code = ''
    self.request_response = ''
    
  
  def totalFiles(self, directory):
    files_list = []
    for root, files in os.walk(directory):

      for file in files:
        location = root + '/' + file
        files_list.append(location[len(directory) +1:])

        self.status_code = '200'
        print(files_list + self.status_code)




    

