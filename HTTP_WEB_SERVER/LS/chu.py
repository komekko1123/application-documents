#!/usr/bin/env python
# Reflects the requests from HTTP methods GET, POST, PUT, and DELETE
# Written by Nathan Hamiel (2010)

# Cloned & Updated from: https://gist.github.com/1kastner/e083f9e813c0464e6a2ec8910553e632
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

allow = False
port = 8080


class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def process_request(self):
        request_path = self.path
        method = self.command.upper()

        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0

        data = {
            'path': request_path,
            'method': method,
            'content-length': content_length,
            'headers': dict(request_headers),
            'data': json.loads(str(self.rfile.read(length).decode('ascii')) or '{}')
        }
        print(json.dumps(data, indent=2))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")

        if allow:
            self.send_header('ACCESS-CONTROL-ALLOW-CREDENTIALS', True)  # Boolean
            self.send_header('ACCESS-CONTROL-ALLOW-HEADERS',
                             'X-ALLOWED-1, X-ALLOWED-2, X-ALLOWED-3')  # * or Comma separated values
            self.send_header('ACCESS-CONTROL-ALLOW-METHODS', 'OPTIONS, PATCH, POST, GET')  # * or Comma separated values
            self.send_header('ACCESS-CONTROL-ALLOW-ORIGIN', '*')  # * or Comma separated values
            self.send_header('ACCESS-CONTROL-EXPOSE-HEADERS', '*')  # * or Comma separated values
            self.send_header('ACCESS-CONTROL-MAX-AGE', 600)  # seconds
            # self.send_header('ACCESS-CONTROL-REQUEST-HEADERS', 'content-type') #Comma separated values sent by client
            # self.send_header('ACCESS-CONTROL-REQUEST-METHOD', 'GET')  # Specific value sent by Client

        self.end_headers()
        self.wfile.write(bytes(json.dumps({
            'error': False,
            'message': 'Handled ' + method + ' request',
        }), 'utf-8'))

    def serve_get(self):
        request_path = self.path

        if request_path == '/favicon.ico':
            # Don't serve favicon
            self.send_response(200)
            self.end_headers()
            return

        self.process_request()

    def serve_post(self):
        self.process_request()

    def serve_options(self):
        self.process_request()

    do_GET = serve_get
    do_HEAD = serve_get
    do_DELETE = serve_post
    do_POST = serve_post
    do_PUT = serve_post
    do_PATCH = serve_post
    do_OPTIONS = serve_options


def main():
    print('Listening on 0.0.0.0:%s - %s CORS' % (port, 'ALLOWS' if allow else 'DISALLOWS'))
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = OptionParser()
    parser.usage = "Creates an http-server that will echo out HEAD, GET, POST, PUT, PATCH, DELETE in JSON format"
    parser.add_option('-a', '--allow', default='no')
    parser.add_option('-p', '--port', default=8080)
    (options, args) = parser.parse_args()

    if options.allow.lower()[0] == 'y':
        allow = True

    port = int(options.port)

    main()

# Commands to run
# python server.py --port 8090
# python server.py --allow y
# python server.py --allow y --port 8080