import http.client
from http import HTTPStatus
from urllib import request, parse

def send_get(url,path,data):
  conn = http.client.HTTPConnection(url)
  conn.request("GET",path)
  r1 = conn.getresponse()
  print(r1.status, r1.reason)
  data1 = r1.read()
  print(data1)
  conn.close()

def send_post(url,path,data,header):
  conn = http.client.HTTPConnection(url)
  conn.request("POST",path,data,header)
  r1 = conn.getresponse()
  print(r1.status, r1.reason)
  data1 = r1.read()
  print(data1)
  conn.close()

def send_head(url,path,data,header):
  conn = http.client.HTTPConnection(url)
  conn.request("HEAD",path,data,header)
  r1 = conn.getresponse()
  print(r1.status, r1.reason)
  data1 = r1.headers
  print(data1)
  conn.close()

def send_put(url,path,filedata,header):
  conn = http.client.HTTPConnection(url)
  conn.request("PUT",path,filedata,header)
  r1 = conn.getresponse()
  print(r1.status, r1.reason)
  data1 = r1.read()
  print(data1)
  conn.close()
  
def send_delete(url,path,data,headers):
  conn = http.client.HTTPConnection(url)
  conn.request("DELETE",path)
  r1 = conn.getresponse()
  print(r1.status, r1.reason)
  data1 = r1.headers
  print(data1)
  conn.close()

if __name__ == '__main__':
  url = "192.168.1.109:6771"  
  data = { 'mypostdata': 'hello world', }
  datas = parse.urlencode(data).encode('utf-8')
  headers = {"Content-Type": "application/x-www-form-urlencoded","Accept":"text/html"}
  print("----- Send get test:-----")
  send_get(url,path="/mynet",data=None)
  send_get(url,path="/mynet",data=None)
  # print("----- Send post test:-----")
  # send_post(url,path="/mynet",data=datas,header=headers)
  # print("----- Send head test:-----")
  # send_head(url,path="/mynet",data=datas,header=headers)
  # print("----- Send put test:-----")
  # send_put(url,path="/mynet",data=None,header=headers)

