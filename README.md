turbo-flask
===========

Integration of Hotwire's Turbo library with Flask, to allow you to create
applications that look and feel like single-page apps without using
JavaScript.

![Todo App Demo](todo-demo.gif)

How to Install
--------------

```bash
pip install turbo-flask
```

How to Add to your Project
--------------------------

Direct initialization:

```python
from flask import Flask
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
```

Factory function initialization:

```python
from flask import Flask
from turbo_flask import Turbo

turbo = Turbo()

def create_app():
    app = Flask(__name__)
    turbo.init_app(app)

    return app
```

To add Turbo-Flask to your pages, include `{{ turbo() }}` in the `<head>`
element of your main Jinja template:

```html
<!doctype html>
<html>
  <head>
    {{ turbo() }}
  </head>
  <body>
    ...
  </body>
</html>
```

How to Use
----------

See the [turbo.js documentation](https://turbo.hotwire.dev/) to learn how to
take advantage of this library.

If you decide to use the Turbo Streams feature, this extension has helper
functions to generate the correct Flask responses. Here is an example with a
single streamed response:

```python
    if turbo.can_stream():
        return turbo.stream(
            turbo.append(render_template('_todo.html', todo=todo), target='todos'),
        )
    else:
        return render_template('index.html', todos=todos)
```

And here is another with a list of them:

```python
    if turbo.can_stream():
        return turbo.stream([
            turbo.append(render_template('_todo.html', todo=todo), target='todos'),
            turbo.update(render_template('_todo_input.html'), target='form')
        ])
    else:
        return render_template('index.html', todos=todos)
```

WebSocket Streaming
-------------------

This feature of turbo.js has not been implemented at this time.
