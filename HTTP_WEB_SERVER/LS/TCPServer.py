from socket import *
serverName = '192.168.1.109'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort)) #前面是ip
serverSocket.listen(1) # 讓幾個人收聽
print('The server is ready to receive')
while True:
  if serverSocket.accept():
    print("accept")
  connectionSocket, addr = serverSocket.accept()
  sentence = connectionSocket.recv(1024).decode()
  capitalizedSentence = sentence.upper()
  print(capitalizedSentence,addr)
  connectionSocket.send(capitalizedSentence.encode())
  connectionSocket.close()