import os
import random
import string
import time
from datetime import datetime
status_reply ={
  200:"ok",
  201:"created",
  204:"No Content",
  206:"Partial Content",
  301:"Move Permanently",
  304:"Not Modified",
  400:"Bad Request",
  401:"Unauthorized",
  404:"Not Found",
  412:"Precondition Failed",
  416:"Range Not Satisfiable",
  505:"HTTP Version Not Supported",
}
CanUse_methods=['GET','POST','PUT','DELETE','HEAD']

def timereply(request):
  l_m_timestamp = os.path.getmtime(os.path.dirname(request.path))
  last_modified_datetime = datetime.fromtimestamp(l_m_timestamp)
  lmt_datetime = last_modified_datetime.strftime("%a, %d %b %Y %H:%M:%S")
  return lmt_datetime

class Request(object):

    def __init__(self, request_message):
        method, path, http_version, headers, args, form, body = self.parse_data(request_message)
        self.method = method  
        self.path = path  
        self.http_version = http_version
        self.headers = headers  
        self.args = args  
        self.form = form  
        self.body = body
    def parse_data(self, data):
        if '\r\n\r\n' in data:
          header, body = data.split('\r\n\r\n', 1)
        else:
          header,body = data,''    
        method, path, http_version, headers, args = self._parse_header(header)
        form = self._path_body(body)

        return method, path, http_version, headers, args, form, body

    def _parse_header(self, data):
        try:
          request_line, request_header = data.split('\r\n', 1)
        except:
          request_line = data 
        method, path_query, http_version = request_line.split()
        path, args = self._parse_path(path_query)

        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(': ', 1)
            headers[k] = v

        return method, path, http_version, headers, args

    @staticmethod
    def _parse_path(data):
        args = {}
        # get的東西用form接
        if '?' not in data:
            path, query = data, ''
        else:
            try:
              path, query = data.split('?', 1)
              for q in query.split('&'):
                  k, v = q.split('=', 1)
                  args[k] = v
            except:
              path, query = data, ''       
        return path, args

    @staticmethod
    def _path_body(data):
        form = {}
        if data:
             # POST 的東西用args接
            try:
              for b in data.split('&'):
                k, v = b.split('=', 1)
                # 前端form會被自動編碼，要自己url解碼
                form[k] = custom_unquote(v)
            except Exception:
              return data
        return form

class Response(object):
    def __init__(self, body, headers=None, status = 200, method =''):
        Response_header = {
          'Content-Type': 'text/html; charset=utf-8',
          'File_size': len(body),
        }
        if headers is not None:
          for rq_key,rq_value in headers.items():
            Response_header[rq_key] = rq_value
        self.headers = Response_header
        self.method = method  
        self.status = status
        self.body = body

    def encoding(self):
      header_str = f'HTTP/1.1 {self.status} {status_reply.get(self.status,"")}\r\n'   
      for key,value in self.headers.items():
        header_str += ''.join(f'{key}: {value}\r\n') #.join就是類似c的append \r\n = \n
      if self.method == 'HEAD':
        response_message = header_str + '\r\n' + str('')
        return response_message.encode('utf-8')  
      if isinstance(self.body,bytes):
        header_str = header_str.encode('utf-8')
        response_message = header_str + b'\r\n' + self.body 
        return response_message
      else:
        response_message = header_str + '\r\n' + str(self.body)
      return response_message.encode('utf-8')

def generate_session_id():
   return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def check_user(request):
  fileStr = str('')
  authication = False
  cookies = request.headers.get('Cookie', '')
  username = request.headers.get('username', '')
  sp_cookie = cookies.split('=')[-1]
  with open('cookie.txt', 'r') as file: #打開user資料夾
    cookie_data = file.read()
    for cookie_line in cookie_data.split('\n'):
      sname = cookie_line.split(' ')[0]
      scookie = cookie_line.split(' ')[-1] # 1會out of range??
      if( sname == '' or scookie == ''):
        continue
      if sp_cookie == scookie or username == sname:
        authication = True
    file.close()     
  return authication  

def render_template(template):
    datapath = os.path.dirname(os.path.abspath(__file__))
    path = datapath + template
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def redirect(url, status=301, cookies=None):
    headers = {
        'Location': url,
    }
    body = ''
    if cookies != None:
     headers['Set-Cookie'] = f'session_id={cookies}'
    return Response(body, headers=headers, status=status)


def custom_unquote(encoded_str):
    encoded_str = encoded_str.replace('+', ' ')
    parts = encoded_str.split('%')
    if len(parts) == 1:
        return encoded_str
    result = [parts[0]]
    for item in parts[1:]:
        try:
            char = chr(int(item[:2], 16)) ##轉char 2C = ,
            result.append(char + item[2:]) ##  2C後的編碼   
        except ValueError:
            result.append('%' + item)
    
    return ''.join(result)



def index(request):
  if check_user(request):
    data = render_template('/index.html')  
    return Response(body=data, status=200, method = request.method)
  else:
    return Response(body="authentication failed",status=401)      

def register(request):
  fileStr = str('')
  user_store= dict()
  if check_user(request):
    return redirect('/index')
  if request.method == 'POST':
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if not username or not password:
      return '無效帳號或密碼'.encode('utf-8')
    with open('user.txt', 'a+') as file:
      file.seek(0) #先放到開始的位
      for user_line in file.read().split('\n'):
        sname = user_line.split(' ')[0]
        spw = user_line.split(' ')[-1] # 1會out of range??
        user_store[sname] = spw  
      if username in user_store: #帳號存在  
        file.close()
        return 'user exist'.encode('utf-8') 
      else:
        file.seek(2) #放到最後寫資料進去
        file.write(str(username)+' '+str(password)+'\n')
      file.close()
    return redirect('/login') 
  return render_template('/register.html')

def login(request):
  fileStr = str('')
  user_store= dict()
  cookie_store= dict()
  if check_user(request):
    return redirect('/index')
  if request.method == 'POST':
    form = request.form 
    username = form.get('username')
    password = form.get('password')
    if not username or not password:
      return 'Invalid password or account'.encode('utf-8')
    with open('user.txt', 'r+') as file:
      user_txt = file.read()
      for user_line in user_txt.split('\n'):
        sname = user_line.split(' ')[0]
        spw = user_line.split(' ')[-1] # 1會out of range??
        user_store[sname] = spw  
      file.close()  
      if username in user_store: #帳號存在
        if user_store[username] != password: #但是密碼不符
           return 'user not exist or password not corrent'.encode('utf-8')       
      else:  #但是帳號不存在
         return 'user not exist or password not corrent'.encode('utf-8')
    with open('cookie.txt', 'r+') as file: #寫入name和cookie
      cookie_data = file.read()
      for cookie_line in cookie_data.split('\n'):
        user = cookie_line.split(' ')[0]
        user_cookie = cookie_line.split(' ')[-1] # 1會out of range??
        if( user == '' or user_cookie == ''):
          continue
        cookie_store[user] = user_cookie  
      if username in cookie_store: # 已有cookie了不用再生成新的
        return redirect('/index',cookies=cookie_store[username])
      session_id = generate_session_id()
      file.write(str(username)+' '+str(session_id)+'\n')
      file.close()
    return redirect('/index',cookies=session_id)
  return render_template('/login.html')

def download(request):
  print(request.headers)
  if check_user(request) != True:
    return Response(body="authentication failed",status=401)     
  headers = {
    "Content-Disposition":' attachment; filename="image.png"',
  }
  a = b''
  try:
    with open("image.png", 'rb') as file:
      a = file.read() 
  except FileNotFoundError:
    a = b'File not found.'
  return Response(a, headers=headers,status=200)    

def upload(request):
  headerindex = request.body.index(b'\r\n\r\n')
  filebody = request.body[headerindex:]
  headerbody = request.body[0:headerindex]
  f_start_pos = headerbody.index(b"filename=")
  f_end_pos = 0
  filename = ''
  clock = 0
  try:
    for i in range(f_start_pos,len(headerbody)):
      if chr(headerbody[i]) == "\"" and clock == 1:
        f_end_pos = i
        break
      if chr(headerbody[i]) == "\"":
        clock = clock + 1
        f_start_pos = i+1
      print(i,"->",chr(headerbody[i]))
    filename = headerbody[f_start_pos:f_end_pos]
    file_start_pos = filebody.index(b'\r\n\r\n')+4     
    file_end_pos = 0
    for i in range(file_start_pos,len(filebody)):
      if chr(filebody[i]) == "\r" and chr(filebody[i+1]) == "\n":
        file_end_pos = i
        break
    filedata = filebody[file_start_pos:file_end_pos]    
    with open(filename, 'wb+') as file:
      file.write(filedata)
    return Response(render_template('/index.html')+ " upload success",status=200)    
  except Exception:
    return Response(render_template('/index.html')+ " upload failed",status=200)  
def bad_request():
  body = render_template('/400.html')
  return Response(body, status=400) 

def Page_Not_Found():
  body = render_template('/404.html')
  return Response(body, status=404)   

def No_Content():
  return Response('', status=204)   
def HTTP_V_N_S():
  body = render_template('/505.html')
  return Response(body, status=505)

routes = {
    '/': (index, ['GET','POST','HEAD']),
    '/index': (index, ['GET','POST','HEAD']),
    '/index.html': (index, ['GET','POST','HEAD']),
    '/register.html': (register, ['GET','POST','HEAD']),
    '/register': (register, ['GET','POST','HEAD']),
    '/login.html': (login, ['GET','POST','HEAD']),
    '/login': (login, ['GET','POST','HEAD']),
    '/download': (download, ['GET']),
    '/upload':(upload, ['GET','POST','HEAD']),
}


def PutFuction(request):
   path = request.path[1:]
   if os.path.isfile(path) == False: # 沒有檔案
     header = {
        'Location': request.path,
     }
     with open(path, 'a+') as file: #建檔
       file.write(request.body)
       print("寫檔成功",request.body)
       print("分隔")
       file.close()
     return Response(body='',headers=header, status=201)
   else:
     with open(path, 'a+') as file: #續寫
       file.write(request.body)
       file.close()
     return Response(body=render_template(request.path), status=200)
    
def checkNotHtml(request):
  p = request.path
  if( p == '/' or p == '/index.html' or p == '/register.html', p == '/login.html' or p == '/download' or
      p == '/index' or p == '/register' or  p == '/login' or p == '/204.html' or p == '/400.html' or 
      p == '404.html' or p == '505.html' or p == '/image.png' or p == 'user.txt' or p == '/cookie.txt' or
      p == '/tools.py' or p == 'version2.py' ):
    return False
  return True

def checkHaveHtml(request):
  p = request.path
  if( p == '/' or p == '/index' or p == '/register' or  p == '/login' ):
    return True
  return False

def checkConditionalHeaders(request):
  if_modified_since = request.headers.get('If-Modified-Since')
  if_unmodified_since = request.headers.get('If-Unmodified-Since')
  if_match = request.headers.get('If-Match')
  if_none_match = request.headers.get('If-None-Match')
  if_range = request.headers.get('If-Range')
  if if_modified_since or if_unmodified_since or if_match or if_none_match or if_range:
    return True
  else:
    return False

def deleteData(request):
  filepath = request.path[1:]
  try:
    if os.path.isdir(filepath):
      os.rmkdir(filepath)     
      print("刪資料夾")
    else:
      os.remove(filepath)  
      print("刪檔案")
    return Response('file delete successed', status=200)
  except OSError as e:
    print("Get Error: %s : %s" % (filepath, e.strerror))
    raise OSError
  

def generate_etag(file_path):
    path = file_path[1:]
    statinfo = os.stat(path)
    mtime = str(int(statinfo.st_mtime))  # 最後一次修改時間
    size = str(statinfo.st_size)  # 文件大小
    etag = '"' + mtime + '-' + size + '"'
    return etag


def ConditionalGet(request):
    # If-Modified-Since
    if checkHaveHtml(request) == True:
      if request.path == '/':
        request.path += 'index.html'
      else:
        request.path += '.html'
    etag = generate_etag(request.path)
    print(etag)
    last_modified = timereply(request)

    header = {
      'Last-Modified': last_modified,
      'ETag': etag,
      'Cache-Control': "max-age=86400, no-cache", 
    }
    
    if_modified_since = request.headers.get('If-Modified-Since')
    if if_modified_since:
        try:
          modified_since_time = datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S')
          last_modified_time  = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S')
          if modified_since_time >= last_modified_time:
            return Response(body='', headers=header, status=304)  # 資源未修改
        except ValueError:
          return Response(body='',headers=header, status=400) #不是給時間就出錯
    # If-Unmodified-Since
    if_unmodified_since = request.headers.get('If-Unmodified-Since')
    if if_unmodified_since:
      try:
        unmodified_since_time = datetime.strptime(if_unmodified_since, '%a, %d %b %Y %H:%M:%S')
        last_modified_time  = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S')
        if unmodified_since_time < last_modified_time:
            return Response(body=render_template(request.path), headers=header, status=412) # 前置條件失敗
      except ValueError:
        return Response(body='',headers=header, status=400)  #不是給時間就出錯
    # If-Match
    if_match = request.headers.get('If-Match')
    if if_match:
        if if_match != etag:
            return Response(body="Precondition Failed => etag not same", headers=header,  status=412)  # 前置條件失敗

    # If-None-Match
    if_none_match = request.headers.get('If-None-Match')
    if if_none_match:
        if if_none_match == etag:
            return Response(body='', headers=header ,status=304)  # 資源未修改

    # If-Range
    if_range = request.headers.get('If-Range')
    if if_range:
      range_header = request.headers.get('Range')
      if range_header: # 沒有的話就直接200
        if if_range == etag: # 相同就範圍range請求
          ranges = parse_range(range_header)
          if ranges == 'bad request':
            return Response(body='bad request', headers=header, status=400)
          file_content = render_template(request.path)
          response_content = b''
          for start, end in ranges:  # 把range做拆分
            if end is not None and (end > len(file_content) or end < 0 or start < 0 or start > len(file_content) or start > end):
              header["Content-Range"] = "*/" + len(file_content)
              return Response(body="Range Not Satisfiable",headers=header,status=416)  # 範圍不合法，返回 416
            elif end is None:
              response_content += file_content[start-1:len(file_content)]    
            else: #正常請求
              response_content += file_content[start-1:end]
          header["Content-Range"] = range_header + "/" + len(file_content)
          header["Content-Type"] = 'multipart/byteranges'    
          return Response(body=response_content, status=206, headers=header)
        else: # 有可能是if_range是時間的樣式 或是 他跟etag不符合
          try:
            if_range_date = datetime.strptime(if_range, '%a, %d %b %Y %H:%M:%S')
            last_modified_time = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S')
            if if_range_date < last_modified_time:
              return Response(body=render_template(request.path), headers=header,  status=200)  # 返回資源
            else:
               ranges = parse_range(range_header)
               if ranges == 'bad request':
                 return Response(body='bad request', headers=header, status=400)
               file_content = render_template(request.path)
               response_content = ''
               for start, end in ranges:
                 if end is not None and (end >= len(file_content) or end < 0 or start < 0 or start >= len(file_content) or start > end):
                   header["Content-Range"] = "*/" + str(len(file_content))
                   return Response(body="Range Not Satisfiable",headers=header,status=416)  # 範圍不合法，返回 416
                 elif end is None:
                   response_content += file_content[start-1:len(file_content)]    
                 else: #正常請求
                   response_content += file_content[start-1:end]
               header["Content-Range"] = range_header + "/" + str(len(file_content))
               header["Content-Type"] = 'multipart/byteranges'    
               return Response(body=response_content, status=206, headers=header)
          except ValueError: #變成比etag 或是 錯誤的話都直接返回
            return Response(body=render_template(request.path), headers=header, status=200)
    return Response(body=render_template(request.path), headers=header,  status=200)  # 返回資源


def parse_range(range_header):
    ranges = []
    try:
      for r in range_header.replace('bytes=', '').split(','):
        start, end = r.split('-')
        start = int(start)
        end = int(end) if end else None
        ranges.append((start, end))
    except ValueError :
      return "bad request"      
    return ranges

  