import uuid
from flask import request, current_app
from flask_sock import Sock, ConnectionClosed
from markupsafe import Markup


_CDN = 'https://cdn.jsdelivr.net'
_PKG = '@hotwired/turbo'
_VER = '8.0.5'


class Turbo:
    def __init__(self, app=None):
        self.user_id_callback = self.default_user_id
        self.sock = None
        self.clients = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        ws_route = app.config.setdefault('TURBO_WEBSOCKET_ROUTE',
                                         '/turbo-stream')
        if ws_route:
            self.sock = Sock()

            @self.sock.route(ws_route)
            def turbo_stream(ws):
                user_id = self.user_id_callback()
                if user_id not in self.clients:
                    self.clients[user_id] = []
                self.clients[user_id].append(ws)
                try:
                    while True:
                        ws.receive(timeout=10)
                except (BrokenPipeError, ConnectionClosed):
                    self.clients[user_id].remove(ws)
                    if not self.clients[user_id]:
                        del self.clients[user_id]

            self.sock.init_app(app)
        app.context_processor(self.context_processor)

    def turbo(self, version=_VER, url=None):
        """Add turbo.js to the page.

        This method is accessible in template files as ``turbo``. You must add
        ``{{ turbo() }}`` in the ``<head>`` section of your main template to
        activate turbo.js.

        :param version: the version of turbo.js to load.
        :param url: The URL for the turbo.js library, or ``None`` to use the
                    default version and CDN.
        """
        if url is None:
            v = ''
            if version is not None:
                v = f'@{version}'
            url = f'{_CDN}/npm/{_PKG}{v}/dist/turbo.es2017-umd.js'
        ws_route = current_app.config.get('TURBO_WEBSOCKET_ROUTE',
                                          '/turbo-stream')
        if ws_route:
            return Markup(f'''<script src="{url}"></script>
<script>Turbo.connectStreamSource(new WebSocket(`ws${{location.protocol.substring(4)}}//${{location.host}}{ws_route}`));</script>
''')  # noqa: E501
        else:
            return Markup(f'<script type="module" src="{url}"></script>')

    def user_id(self, f):
        """Configure an application-specific user id generator, to allow the
        application to push updates over WebSocket to individual clients.

        Example::

            @turbo.user_id
            def get_user_id():
                return current_user.id
        """
        self.user_id_callback = f
        return f

    def default_user_id(self):
        """Default user id generator. An application-specific function can be
        configured with the ``@user_id`` decorator."""
        return uuid.uuid4().hex

    def context_processor(self):
        return {'turbo': self.turbo}

    def requested_frame(self):
        """Returns the target frame the client expects, or ``None``."""
        return request.headers.get('Turbo-Frame')

    def can_stream(self):
        """Returns ``True`` if the client accepts turbo stream reponses."""
        stream_mimetype = 'text/vnd.turbo-stream.html'
        best = request.accept_mimetypes.best_match([
            stream_mimetype, 'text/html'])
        return best == stream_mimetype

    def can_push(self, to=None):
        """Returns ``True`` if the client accepts turbo stream updates over
        WebSocket.

        :param to: the id of the client. If not given then the answer
                   is ``True`` if there is at least one client listening to
                   updates over WebSocket.
        """
        if to is None:
            return self.clients != {}
        return to in self.clients

    def _make_stream(self, action, content, target):
        return (f'<turbo-stream action="{action}" target="{target}">'
                f'<template>{content}</template></turbo-stream>')

    def append(self, content, target):
        """Create an append stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('append', content, target)

    def prepend(self, content, target):
        """Create a prepend stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('prepend', content, target)

    def replace(self, content, target):
        """Create a replace stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('replace', content, target)

    def update(self, content, target):
        """Create an update stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('update', content, target)

    def remove(self, target):
        """Create a remove stream.

        :param target: the target ID for this change.
        """
        return self._make_stream('remove', '', target)

    def after(self, content, target):
        """Create an after stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('after', content, target)

    def before(self, content, target):
        """Create an before stream.

        :param content: the HTML content to include in the stream.
        :param target: the target ID for this change.
        """
        return self._make_stream('before', content, target)

    def stream(self, stream):
        """Create a turbo stream response.

        :param stream: one or a list of streamed responses generated by the
                       ``append()``, ``prepend()``, ``replace()``, ``update()``
                       and ``remove()`` methods.
        """
        return current_app.response_class(
            stream, mimetype='text/vnd.turbo-stream.html')

    def push(self, stream, to=None):
        """Push a turbo stream update over WebSocket to one or more clients.

        :param stream: one or a list of stream updates generated by the
                       ``append()``, ``prepend()``, ``replace()``, ``update()``
                       and ``remove()`` methods.
        :param to: the id of the target client. Set to ``None`` to send to all
                   connected clients, or to a list of ids to target multiple
                   clients.
        """
        if to is None:
            to = self.clients.keys()
        elif not hasattr(to, '__len__') or isinstance(to, str):
            to = [to]
        if hasattr(stream, '__len__') and not isinstance(stream, str):
            stream = ''.join(stream)
        for recipient in to:
            for ws in self.clients[recipient]:
                try:
                    ws.send(stream)
                except (BrokenPipeError, ConnectionClosed):  # pragma: no cover
                    pass
