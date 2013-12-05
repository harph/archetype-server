import os
from http import render, render_static
from settings import STATIC_FOLDER


class View(object):
    server = None

    def __init__(self, server, request, path, data):
        self.server = server
        self.request = request
        self.path = path
        self.data = data

    def render(self, *args, **kwargs):
        template_vars = {
            'data': self. data,
        }
        # render a default template


class StaticView(View):

    CONTENT_TYPES = {
        '.css': 'text/css',
        '.js': 'text/js',
    }

    @property
    def static_path(self):
        return self.path

    def _get_content_type(self, file_path):
        f, ext = os.path.splitext(file_path)
        return self.CONTENT_TYPES.get(ext.lower(), 'text/plain')

    def render(self, static_path):
        file_path = os.path.join(STATIC_FOLDER, static_path)
        if not os.path.isfile(file_path):
            return None
        static_file = file(file_path, 'r')
        print 'static_path', static_path
        static_content = static_file.read()
        static_file.close()
        content_type = self._get_content_type(file_path)
        return render_static(static_content, content_type=content_type)


class HomeView(View):
    def render(self):
        template_vars = {
            'data': self.data,
        }
        #self.server.send_to_socket('Vex')
        return render(self.request, "home.html", template_vars)
