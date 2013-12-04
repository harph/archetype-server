from conf import template_environment


class HttpReponse(object):
    code = None
    headers = None
    content = None

    def __init__(self, code, content_type, content):
        self.code = code
        self.header = {'Content-type': content_type}
        self.content = content

    def _add_header(self, key, value):
        self.header[key] = value


def render(request, template_name, template_vars={}, code=200, content_type='text/html'):
    template_vars['request'] = request
    template = template_environment.get_template(template_name)
    rendered_template = template.render(template_vars)
    http_response = HttpReponse(code, content_type, rendered_template)
    return http_response
