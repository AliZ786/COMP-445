import re

class Server:




  def __init__(self, request):

    self.method = []
    self.content = 'Empty content'
    self.request_response = 'No response'
    self.request_header, self.request_body = request.split('\r\n\r\n')

    header = self.request_header.split('\r\n')
    
    self.method, self.http_version, self.request_string = header[0].split(' ')


    for currentLine in header:
      if re.match(r'Content-Type', currentLine):
        self.content = currentLine.split(":")[1]

      elif re.match(r'Content-Dispostion', currentLine):
        self.request_response = self.call_request("download")

        if re.match(r'/(.+)', self.request_string):
                    # ignore the first '/'
                    self.f = self.request_string[1:]


      self.call_method()


  def call_request(request):

    match request:
      case "getFiles":
        print("Getting all files from the directory.....")
        print()

      case "postFile":
        print("Posting content for file.....")
        print()

      case "getFile":
        print("Getting specific file from the command.....")
        print()

      case "invalid":
        print("Invalid command")

      case "download":
        print("Downloading content.....")
        print()

    return request


  def call_method(self):
    
    if self.method == "GET" and self.request_response != self.call_request("download"):

      if self.request_string == '/':
        self.request_response = self.call_request("getFiles")

      elif re.match(r'/(.+)', self.request_string):
        self.request_response = self.call_request("getFile")
                    # ignore the first '/'
        self.f = self.request_string[1:]
                    
      else:
        self.request_response = self.call_request("invalid")

    elif self.method == "POST":
      














  




    
    


