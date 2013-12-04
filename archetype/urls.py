from views import StaticView, HomeView

URLS = (
    (r'^/static/(?P<static_path>.*)$', StaticView),
    (r'^/$', HomeView),
)
