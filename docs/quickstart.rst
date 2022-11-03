Quick Start
-----------

How to Install
~~~~~~~~~~~~~~

::

    pip install turbo-flask


How to Add to your Project
~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct initialization::

    from flask import Flask
    from turbo_flask import Turbo

    app = Flask(__name__)
    turbo = Turbo(app)

Factory function initialization::

    from flask import Flask
    from turbo_flask import Turbo

    turbo = Turbo()

    def create_app():
        app = Flask(__name__)
        turbo.init_app(app)

        return app

To add Turbo-Flask to your pages, include ``{{ turbo() }}`` in the ``<head>``
element of your main Jinja template::

    <!doctype html>
    <html>
      <head>
        {{ turbo() }}
      </head>
      <body>
        ...
      </body>
    </html>

Configuration
~~~~~~~~~~~~~

Configuration for this extension is given through the Flask configuration
object. There is only one configuration variable supported by this extension:

- ``TURBO_WEBSOCKET_ROUTE``: The route URL on which the client can connect
  using WebSocket to receive Turbo Stream updates. By default, the
  ``/turbo-stream`` URL is used. If this variable is set to ``None``, the
  WebSocket endpoint is disabled.

How to Use
~~~~~~~~~~

The Turbo Drive and Turbo Frames features provided by turbo.js do not require
server side support, so access to these features in your templates is enabled
just by adding the library as indicated above. Consult the
`turbo.js documentation <https://turbo.hotwire.dev/>`_ to learn how to take
advantage of these features.

However, if you decide to use the Turbo Streams feature of turbo.js, this
extension has helpers to generate correctly formatted streams.

The ``turbo`` object has five helper methods that generate the different types
of Turbo Stream operations:

- ``turbo.append(content, target)``: add ``content`` at the end of ``target``
- ``turbo.prepend(content, target)``: add ``content`` at the start of ``target``
- ``turbo.replace(content, target)``: replace ``target`` with ``content``
- ``turbo.update(content, target)``: replace the contents of ``target`` with ``content``
- ``turbo.remove(target)``: remove ``target``

In all these methods, ``content`` is a string with HTML content, usually the
result of invoking Flask's ``render_template()`` function. The ``target``
argument is the id of the element in the page that will be modified.

There are two supported use cases for the Turbo Streams feature: a response to
a POST request, and a server-push update over WebSocket. The following sections
describe how to deliver streams for both.

Responding to a POST Request with a Turbo Stream
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows how to deliver a Turbo Stream as a response to a
POST request::


        if turbo.can_stream():
            return turbo.stream(
                turbo.append(render_template('_todo.html', todo=todo), target='todos'),
            )
        else:
            return render_template('index.html', todos=todos)

Here is another example using a list of updates::

        if turbo.can_stream():
            return turbo.stream([
                turbo.append(render_template('_todo.html', todo=todo), target='todos'),
                turbo.update(render_template('_todo_input.html'), target='form')
            ])
        else:
            return render_template('index.html', todos=todos)

The ``turbo.stream()`` method takes one or a list of Turbo Stream updates and
generates a Turbo Stream response that can be returned directly from the Flask
view function.

The ``turbo.can_stream()`` method is a helper methods that returns ``True`` if
the client indicated that it supports Turbo Stream responses. It is a good idea
to fall back to a standard Flask response when Turbo Streams aren't accepted by
the client, as shown in the above examples.

Pushing Updates via WebSocket Streaming
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The application can, at any time, push updates to parts of the page using the
``turbo.push()`` helper method. Below you can see a simple example::

    def update_load():
        with app.app_context():
            while True:
                time.sleep(5)
                turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))

In the above example the ``turbo.push()`` method will send the update to all
connected clients.

The ``turbo.push()`` method supports an optional ``to`` argument that can be
used to select one or more specific clients to receive the update. To take
advantage of this, the application first needs to provide a function that
assigns an id to each connected client, and decorate it with the
``turbo.user_id`` decorator. In the following example, the id for each client
is obtained from Flask-Login's ``current_user``::

    @turbo.user_id
    def get_user_id():
        return current_user.id

To push an update to a given client, the ``to`` argument can be added to the
``turbo.push()`` method::

    turbo.push(turbo.replace(render_template('loadavg.html'), 'load'),
               to=admin_user_id)

It is also possible to send the update to multiple clients by passing a list
in the ``to`` argument::

    turbo.push(turbo.replace(render_template('loadavg.html'), 'load'),
               to=[admin_user_id, moderator_user_id])

Deployment
~~~~~~~~~~

This extension implementes a WebSocket endpoint. The default location for this
endpoint is ``/turbo-stream``, but this can be changed by setting the
``TURBO_WEBSOCKET_ROUTE`` configuration variable.

When using a reverse proxy in front of the Flask application, the WebSocket
endpoint may need a special configuration to work correctly. For example, in
Nginx, the endpoint must be configured to explicitly forward the ``Upgrade``
and ``Connection`` headers, which are not proxied by default. While the actual
configuration may vary according to the needs of each application, the
following example can be used as a starting point::

    location /turbo-stream {
        include proxy_params;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_pass http://localhost:5000;
    }

The WebSocket support in this extension is provided by the
`Flask-Sock <https://github.com/miguelgrinberg/flask-sock>`_ package, which
supports WebSocket servers based on Gunicorn, Eventlet, Gevent and the Flask
development web server. Refer to the Flask-Sock documentation for additional
deployment details.
