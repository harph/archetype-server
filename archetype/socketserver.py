import socket as _socket
import asyncore
import threading
from webserver import start_threaded_http_server


class ArchetypeSocketConnectionHandler(threading.Thread):

    http_server = None
    _closed = False


    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        self._start_webserver()

    def _start_webserver(self):
        self.http_server = start_threaded_http_server('localhost', 9000)
        self.http_server.start()

    def _process_data(self, data):
        pass

    def send(self, msg):
        if self._closed:
            return
        print "sending message", msg
        self.connection.sendall(msg)

    def run(self):
        conn = self.connection
        while not self._closed:
            data = conn.recv(1024)
            print data
            if not data:
                print "NO DATA"
                break
            self._process_data(data)
        self.close()
        print 'closed'

    def close(self):
        if self._closed:
            return
        self._closed = True
        self.connection.close()
        self.http_server.shutdown()
        print 'joining'
        self.http_server.join()
        print 'socket closed'


class ArchetypeSocketServer(object):

    socket = None
    socket_clients = None

    def __init__(self, hostname, port):
        self.socket = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        self.socket.bind((hostname, port))
        self.socket.listen(1)
        self.socket_clients = []

    def serve_forever(self):
        while True:
            conn, addr = self.socket.accept()
            print 'After accept'
            client = ArchetypeSocketConnectionHandler(conn)
            self.socket_clients.append(client)
            client.start()
            print 'After start_new_thread'
        print 'exited loop'

    def close(self):
        for client in self.socket_clients:
            print "closing client"
            client.close()
        self.socket.close()
        print "all closed"
        

#class ArchetypeSocketServer(asyncore.dispatcher):
#
#    # active webservers
#    webservers = None
#
#    # messages that are going to be sent to the editor
#    outgoing_messages = None
#
#    def __init__(self, host, port):$
#        asyncore.dispatcher.__init__(self)$
#        self.create_socket(_socket.AF_INET, _socket.SOCK_STREAM)$
#        self.connect((host, port))$
#        self.webservers = []
#
#    def handle_connect(self):
#        print 'new connection'
#
#    def handle_close(self):
#        print 'close'
#        self.close()
#
#    def writable(self):
#        webservers = []
#        messages = self.outgoing_messages
#        for ws in self.webservers:
#            if not ws.running:
#                continue
#            webserversa.append(ws)
#            messages += webserver.messages
#        return len(messages) > 0
#
#    def handle_write(sel
