import unittest
import pytest
from flask import Flask, render_template_string
from werkzeug.exceptions import NotFound
import turbo_flask


class TestTurbo(unittest.TestCase):
    def test_direct_create(self):
        app = Flask(__name__)
        turbo_flask.Turbo(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo() }}')

        url_adapter = app.url_map.bind('localhost', '/')
        assert url_adapter.match('/turbo-stream', websocket=True) == \
            ('__flask_sock.turbo_stream', {})

        rv = app.test_client().get('/test')
        assert b'@hotwired/turbo.js' in rv.data
        assert b'Turbo.connectStreamSource' in rv.data

    def test_indirect_create(self):
        app = Flask(__name__)
        turbo = turbo_flask.Turbo()
        turbo.init_app(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo() }}')

        url_adapter = app.url_map.bind('localhost', '/')
        assert url_adapter.match('/turbo-stream', websocket=True) == \
            ('__flask_sock.turbo_stream', {})

        rv = app.test_client().get('/test')
        assert b'@hotwired/turbo.js' in rv.data
        assert b'Turbo.connectStreamSource' in rv.data

    def test_create_custom_ws(self):
        app = Flask(__name__)
        app.config['TURBO_WEBSOCKET_ROUTE'] = '/ws'
        turbo_flask.Turbo(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo() }}')

        url_adapter = app.url_map.bind('localhost', '/')
        with pytest.raises(NotFound):
            url_adapter.match('/turbo-stream', websocket=True)
        assert url_adapter.match('/ws', websocket=True) == \
            ('__flask_sock.turbo_stream', {})

        rv = app.test_client().get('/test')
        assert b'@hotwired/turbo.js' in rv.data
        assert b'Turbo.connectStreamSource' in rv.data

    def test_create_no_ws(self):
        app = Flask(__name__)
        app.config['TURBO_WEBSOCKET_ROUTE'] = None
        turbo_flask.Turbo(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo() }}')

        url_adapter = app.url_map.bind('localhost', '/')
        with pytest.raises(NotFound):
            url_adapter.match('/turbo-stream', websocket=True)

        rv = app.test_client().get('/test')
        assert b'@hotwired/turbo.js' in rv.data
        assert b'Turbo.connectStreamSource' not in rv.data

    def test_create_custom_turbo_version(self):
        app = Flask(__name__)
        turbo_flask.Turbo(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo(version="v1.2.3") }}')

        url_adapter = app.url_map.bind('localhost', '/')
        assert url_adapter.match('/turbo-stream', websocket=True) == \
            ('__flask_sock.turbo_stream', {})

        rv = app.test_client().get('/test')
        assert b'@hotwired/turbo@v1.2.3' in rv.data
        assert b'Turbo.connectStreamSource' in rv.data

    def test_create_custom_turbo_url(self):
        app = Flask(__name__)
        turbo_flask.Turbo(app)

        @app.route('/test')
        def test():
            return render_template_string('{{ turbo(url="/js/turbo.js") }}')

        url_adapter = app.url_map.bind('localhost', '/')
        assert url_adapter.match('/turbo-stream', websocket=True) == \
            ('__flask_sock.turbo_stream', {})

        rv = app.test_client().get('/test')
        assert b'/js/turbo.js' in rv.data
        assert b'Turbo.connectStreamSource' in rv.data

    def test_requested_frame(self):
        app = Flask(__name__)
        turbo = turbo_flask.Turbo(app)

        with app.test_request_context('/', headers={'Turbo-Frame': 'foo'}):
            assert turbo.requested_frame() == 'foo'

    def test_can_stream(self):
        app = Flask(__name__)
        turbo = turbo_flask.Turbo(app)

        with app.test_request_context('/', headers={'Accept': 'text/html'}):
            assert not turbo.can_stream()
        with app.test_request_context(
                '/', headers={'Accept': 'text/vnd.turbo-stream.html'}):
            assert turbo.can_stream()

    def test_can_push(self):
        app = Flask(__name__)
        turbo = turbo_flask.Turbo(app)

        assert not turbo.can_push()
        turbo.clients = {'123': 'client'}
        assert turbo.can_push()
        assert turbo.can_push(to='123')
        assert not turbo.can_push(to='456')

    def test_streams(self):
        app = Flask(__name__)
        turbo = turbo_flask.Turbo(app)

        actions = ['append', 'prepend', 'replace', 'update']
        for action in actions:
            assert getattr(turbo, action)('foo', 'bar') == (
                f'<turbo-stream action="{action}" target="bar">'
                f'<template>foo</template></turbo-stream>'
            )
        assert turbo.remove('bar') == (
            '<turbo-stream action="remove" target="bar">'
            '<template></template></turbo-stream>'
        )
