from socket import *
import sys #打開終端program
import threading
import os
import random
import string
status_code ={
  200:"200 ok",
  301:"301 Move Permanently",
  400:"400 Bad Request",
  404:"404 Not Found",
  505:"505 HTTP Version Not Supported",
}

methods = ['GET', 'POST', 'PUT', 'HEAD', 'DELETE',]


user_database = {
    "user": "password123",
    "alice": "alice123",
    "aa" : "a1",

}

session_store = {}

def add_cookie(headers, key, value):
  if 'Set-Cookie' in headers:
    headers['Set-Cookie'] += f', {key}={value}'
  else:
    headers['Set-Cookie'] = f'{key}={value}'

def generate_session_id():
   return ''.join(random.choices(string.ascii_letters + string.digits, k=32))


def Parse_header(message):
  if message == '':
    return '','',{} # no header
  request_line, request_header = message.split('\r\n', 1)
  # line = 'GET /index HTTP/1.1' -> ['GET', '/index', 'HTTP/1.1'] ; header = ....
  method, path, http_version = request_line.split()  # http用不到
  headers = {} #用字典存值
  for header in request_header.split('\r\n'):
   # print("i :", header.split(': ', 1))
    if header == '':
      break
    k, v = header.split(': ', 1) # xx: 1
    headers[k] = v
  return method, path, http_version, headers

def ResponseM(body,Request_headers,status,method):
  Response_headers = {
      'Content-Type': 'text/html; charset=utf-8',
      'File-Size': len(body),
     # 'Authorization': 'true'
  }
  #if status == 301:
    #send_response(301)
		#send_header('Location', location))  
  for rq_key,rq_value in Request_headers.items():
    if rq_key == 'Cookie': # set cookie進去裡面
      rq_key = 'Set-Cookie'
    if rq_key not in Response_headers: 
      Response_headers[rq_key] = rq_value
  if method == 'PUT':
    Response_headers.clear()

  header_str = f'HTTP/1.1 {status_code.get(status,"")}\r\n'   
  for key,value in Response_headers.items():
    header_str += ''.join(f'{key}: {value}\r\n') #.join就是類似c的append \r\n = \n
  response_message = header_str + '\r\n' + str(body)
  return response_message.encode('utf-8')

def make_response(method,path,header,str):
  status = 200
  file_content = ''
  datapath = os.path.dirname(os.path.abspath(__file__))
  if path == '/':
    path = '/mynet.html'
  path = datapath + path
  if method == 'GET' or method == 'POST':  
    if os.path.isfile(path):
      with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    else:
      status = 404  
  elif method == 'DELETE':
    if os.path.isfile(path):
      with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
      status = 200  
    else:
      status = 404  
  elif method == 'HEAD': #就print header就好  
    if os.path.isfile(path):
      status = 200  
      with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
      file_content = ""
    else:
      status = 404  
  elif method == 'PUT':  # 
    if os.path.isfile(path):
      with open(path, 'r', encoding='utf-8') as file:
        file_content = file.read()
      status = 200  
    else:
      status = 404  
  else:
    status = 405
    file_content = 'Method Not Allowed'     
  
  if str != '':
    file_content = file_content + ' ' + str  
  response_message = ResponseM(file_content,header,status,method)
  return response_message

def process_connection(connectionSocket):
  request_bytes = b''
  authication = False
  while True:
    chunk = connectionSocket.recv(4096)
    request_bytes += chunk
    if b'\r\n\r\n' in request_bytes:
      break
    if len(chunk) < 4096:
      break
  request_message = request_bytes.decode('utf-8')   
  method, path, header = Parse_header(request_message)
  cookies = header.get('Cookie', '').split('; ')
  session_id = str('?')
  for cookie in cookies:
    if cookie.startswith('session_id='):
     session_id = cookie.split('=')[1] # 第二個元素 就是=後面的id(cookie)
     break

  with open('cookie.txt', 'r') as file:
    cookie_txt = file.read()
    for session_line in cookie_txt.split('\n'):
      sid = session_line.split(' ')[0]
      sname = session_line.split(' ')[-1] # 1會out of range??
      session_store[sid] = sname  
    if session_id in session_store:
      authication = True
    file.close()

  if  method == 'POST' and path == '/login.html' :
        username = header.get('username', '')
        password = header.get('password', '')  
        if username in user_database and user_database[username] == password and authication == False:
            session_id = generate_session_id()
            session_store[session_id] = username
            add_cookie(header, 'session_id', session_id) #server裡面創cookie
            with open('cookie.txt', 'a+') as file:
              file.write(str(session_id)+' '+str(username)+'\n')
              file.close()  
           #   path = '/mynet.html'
            response_encode_message = make_response(method, path, header, 'Login successful')
            print("驗證成功(註冊cookie)")

        elif  username in user_database and user_database[username] == password and authication == True:
         # path = '/mynet.html'  
          response_encode_message = make_response(method, path, header, 'Login successful')
          print("驗證成功(已有cookie)")
        else:
            response_encode_message = make_response(method, path, header, 'Invalid credentials')
  elif method == 'GET' and path == '/login.html':
    response_encode_message = make_response(method, path, header, '')   
  else: 
        if authication == True and method == 'GET':
            print('驗證成功!: ',method)
            response_encode_message = make_response(method, path, header, f'Welcome, {session_store[session_id]}!')
        elif authication == True and method == 'HEAD':
            print('驗證成功!: ',method)
            response_encode_message = make_response(method, path, header, '')   
        else:
            print('驗證失敗!')
            response_encode_message = 'Session expired or invalid. Please login again'.encode('utf-8')
            #response_encode_message = make_response(method, path, header, 'Session expired or invalid. Please login again')


  #response_encode_message = make_response(method,path,header,' ')
  connectionSocket.send(response_encode_message)
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
