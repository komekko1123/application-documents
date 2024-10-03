from socket import *
import os
from tools import *
import time


def make_response(request, headers=None):
  status = 200
  datapath = os.path.dirname(os.path.abspath(__file__))


  if request.method not in CanUse_methods :
    return bad_request().encoding()
  if request.http_version != 'HTTP/1.1':
    return HTTP_V_N_S().encoding()
  
  if request.method == 'DELETE' :
    if checkNotHtml(request) == True :
      return bad_request().encoding()
    try:
      response_delete_message = deleteData(request)
    except Exception: # 沒有可刪的檔案(file not exist)
      return Page_Not_Found().encoding()
    return response_delete_message.encoding()
  
  elif request.method == 'PUT':
    if checkNotHtml(request) == True :
      return bad_request().encoding()
    else:
      data = PutFuction(request)
      response_message = data.encoding()
    return response_message

  if checkNotHtml(request) == False:
    try:
      route, methods = routes.get(request.path)
    except TypeError:
      return Page_Not_Found().encoding()
    if request.method not in methods:
      return bad_request().encoding()  
    data = route(request)
  else:
    try:
      data = render_template(request.path)
    except Exception: # 沒有可刪的檔案
      return Page_Not_Found().encoding()
  if checkConditionalHeaders(request) == True:
    data = ConditionalGet(request)


  if isinstance(data, Response):
    response_message = data.encoding()
  else:
    response = Response(data, headers=headers, status=status, method = request.method)
    response_message = response.encoding()
  return response_message

def process_connection(connectionSocket):
  request_bytes = b''
  chunk = b''
  while True:
    try:
      connectionSocket.settimeout(1.0)
      chunk = connectionSocket.recv(512) 
    except BlockingIOError:
      pass
    except timeout:
      print("timeout")
      request_bytes += chunk
      connectionSocket.settimeout(None)
      break  
    request_bytes += chunk
    
    if len(chunk) <= 0 :
      break 

  if len(request_bytes) == 0 :
    return
  print(request_bytes)
  try:
    request_message = request_bytes.decode('UTF-8')
    request = Request(request_message)
    response_bytes = make_response(request)
    connectionSocket.sendall(response_bytes)
  except UnicodeDecodeError:
    #request_array = bytearray(request_bytes)
    index = request_bytes.index(b'\r\n\r\n')
    print(index)
    request_body = request_bytes[index+4:]
    request_bytes = request_bytes[0:index]
    request_message = request_bytes.decode('UTF-8')
    request = Request(request_message)
    request.body = request_body
    response_bytes = make_response(request)
    connectionSocket.sendall(response_bytes)
  connectionSocket.close()

def main():
  serverName = 'localhost'
  serverPort = 6771
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('',serverPort)) #前面是ip
  serverSocket.listen(3) # 讓幾個人收聽
  while True:
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    process_connection(connectionSocket)
    connectionSocket.close()

if __name__ == '__main__':
  main()

