from socket import *
import sys #打開終端program
import os 

serverName = '192.168.1.119'
serverPort = 6771
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort)) #前面是ip
serverSocket.listen(1) # 讓幾個人收聽

def create_response(status_code, content_type, content):
    response = "HTTP/1.1 {0}\r\n".format(status_code)
    response += "Content-Type: "    + content_type + "\r\n"
    response += "Content-Length: " + str(len(content)) + "\r\n"
    response += "\r\n" + content
    return response


def handle_request(request_data):
    try:
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0].split(' ')
        request_method = request_line[0] #哪個方法
        file_path = request_line[1]

        # Handle GET request
        if request_method == 'GET':
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_content = file.readlines()
                return 200, 'OK', file_content
            else:
                return 404, 'Not Found', b'404 Not Found'
        
        # Handle DELETE request
        elif request_method == 'DELETE':
            if os.path.exists(file_path):
                os.remove(file_path)
                return 200, 'OK', b'File deleted successfully'
            else:
                return 404, 'Not Found', b'404 Not Found'
        
        # Handle POST, PUT, and HEAD requests (placeholders)
        elif request_method == 'POST' :
            content_length = int(request_data.split('Content-Length: ')[1].split('\r\n')[0])
            body = request_data.split('\r\n\r\n')[1][:content_length]
            # Process the POST data here (in this example, just echoing back the data)
            response_content = b"Received POST data: " + body.encode()
            return create_response("200 OK", "text/plain", response_content)
        
        elif request_method == 'PUT' :
           content_length = int(request_data.split("Content-Length: ")[1].split("\n")[0])
           put_data = client_socket.recv(content_length)
           with open(path[1:], "wb") as file:
             file.write(put_data)
          response_header = "HTTP/1.1 200 OK\n\n"
            response_data = b"File Updated Successfully"
        elif request_method == "HEAD":
            response_header = "HTTP/1.1 200 OK\nContent-Length: 0\n\n"
            response_data = b""
        # Invalid request method
        else:
            return 400, 'Bad Request', b'400 Bad Request'

    except Exception as e:
        response_header = "HTTP/1.1 505 HTTP Version Not Supported\n\n"
        response_data = b"505 HTTP Version Not Supported"


while True:
  print("Ready to serve...")
  connectionSocket, addr = serverSocket.accept()
  try:
    message = connectionSocket.recv(2048).decode() #decode好像不影響
    status_code, = handle_request(message)
    filename = message.split()[1]
    f = open(filename[1:],encoding="utf-8") #改成utf-8很重要
    outputdata = f.readlines() # 用read會跑不出照片故用readlines
    # send one http header line into socket
    okmessage = 'http 200 ok \n\n'
    connectionSocket.send(okmessage.encode())
    for i in range(0, len(outputdata)):
      connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())
  except IOError:
    #Send response message for file not found
    errormessage = 'http 404 error \n\n'
    connectionSocket.send(errormessage.encode())
    #Close client socket
    connectionSocket.close()
    break
serverSocket.close()

sys.exit()#Terminate the program after sending the corresponding data    