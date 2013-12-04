import jinja2
import settings


def _get_template_environment():
    # Template loader
    template_loader = jinja2.FileSystemLoader(searchpath=settings.TEMPLATE_FOLDER)
    # Template Environment
    return jinja2.Environment(loader=template_loader)

# Jinga2 template environment
template_environment = _get_template_environment()
