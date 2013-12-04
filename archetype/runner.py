from socketserver import ArchetypeSocketServer


def run():
    host = ''
    port = 9898
    socket_server = ArchetypeSocketServer(host, port)
    try:
        socket_server.serve_forever()
    except KeyboardInterrupt:
        socket_server.close()
