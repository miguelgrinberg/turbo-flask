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
