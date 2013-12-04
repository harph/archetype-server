import re
import socket as _socket
import urllib2
import BaseHTTPServer
import threading
from http import render


class View(object):

    server = None

    def __init__(self, server):
        self.server = server

    def render(self, request, data=None, *args, **kwargs):
        template_vars = {
            'data': data,
        }


class HomeView(View):
    def render(self, request, data):
        template_vars= {
            'data': data,
        }
        self.server.send_to_socket('Vex')
        return render(request, "home.html", template_vars)


URLS = (
    (r'^/$', HomeView),
)


class ArchetypeHTTPServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    _data = None
    _listener = None
    _urls = URLS

    def set_data(self, data):
        self._data = data

    def _throw_reponse_error(self, error_code, msg):
        self.send_response(error_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(msg)

    def _thow_500(self):
        self._throw_reponse_error(500, '500 Error')

    def _throw_404(self):
        self._throw_reponse_error(404, '404, Page not fount')

    def _process_http_response(self, http_response):
        self.send_response(http_response.code)
        for k, v in http_response.header.iteritems():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(http_response.content)

    def do_GET(self):
        http_response = None
        for url in self._urls:
            regex, view = url
            if re.search(regex, self.path):
                http_response = view(self.server).render(self.request, self._data)
                self._process_http_response(http_response)
                break
        if not http_response:
            self._throw_404()




class ArchetypeHTTPServer(BaseHTTPServer.HTTPServer, threading.Thread):

    # Server host
    host = None

    # Server port
    port = None

    # Serve flag (use this to stop the server)
    serve = False

    def __init__(self, host, port):
        while True:
            try:
                super(ArchetypeHTTPServer, self).__init__(
                    (host, port), ArchetypeHTTPServerHandler)
                break
            except _socket.error:
                port += 1
        self.host = host
        self.port = port
        print 'running in port:', port
        threading.Thread.__init__(self)
        self.serve = True

    def _get_server_url(self):
        return 'http://%s:%d' % (self.host, self.port)

    def _execute_fake_request(self):
        # Use this function to execute a fake request and for a loop.
        url = self._get_server_url()
        print 'fake request to', url
        fake_request = urllib2.urlopen(url)
        #fake_request.close()

    def serve_forever(self):
        while self.serve:
            print "Serving"
            self.handle_request()
        print 'end of serve forever'

    def shutdown(self):
        self.serve = False
        print "shutting down"
        self._execute_fake_request()

    def send_to_socket(self, msg):
        pass

    def run(self):
        self.serve_forever()


def start_threaded_http_server(host, port):
    httpd = ArchetypeHTTPServer(host, port)
    return httpd
