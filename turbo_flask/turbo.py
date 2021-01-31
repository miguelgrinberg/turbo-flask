from flask import request, current_app
from jinja2 import Markup


_CDN = 'https://cdn.skypack.dev'
_PKG = '@hotwired/turbo'
_VER = 'v7.0.0-beta.4-TQFv5Y2xd4hn2VnTxVul'


class Turbo:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.context_processor(self.context_processor)

    def turbo(self, version=_VER, url=None):
        """Add turbo.js to the template.

        Add `{{ turbo() }}` in the `<head>` section of your main template.
        """
        if url is None:
            url = f'{_CDN}/pin/{_PKG}@{version}/min/{_PKG}.js'
        return Markup(f'<script type="module" src="{url}"></script>')

    def context_processor(self):
        return {'turbo': self.turbo}

    def can_stream(self):
        """Returns `True` if the client accepts turbo streams."""
        stream_mimetype = 'text/vnd.turbo-stream.html'
        best = request.accept_mimetypes.best_match([
            stream_mimetype, 'text/html'])
        return best == stream_mimetype

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

    def stream(self, response_stream):
        """Create a turbo stream response.

        :param response_stream: one or a list of streamed responses generated
                                by the `append()`, `prepend()`, `replace()`,
                                `update()` and `remove()` methods.
        """
        return current_app.response_class(
            response_stream, mimetype='text/vnd.turbo-stream.html')
