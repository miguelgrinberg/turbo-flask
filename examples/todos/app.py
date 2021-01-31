from flask import Flask, render_template, request, redirect, url_for, abort
from turbo_flask import Turbo
from models import Todo

app = Flask(__name__)
turbo = Turbo(app)

todos = [Todo('buy eggs'), Todo('walk the dog')]


def get_todo_by_id(id):
    todo = [todo for todo in todos if todo.id == id]
    if len(todo) == 0:
        abort(404)
    return todo[0]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo = Todo(request.form['task'])
        todos.append(todo)
        if turbo.can_stream():
            return turbo.stream([
                turbo.append(
                    render_template('_todo.html', todo=todo), target='todos'),
                turbo.update(
                    render_template('_todo_input.html'), target='form')])
    return render_template('index.html', todos=todos)


@app.route('/toggle/<id>', methods=['POST'])
def toggle(id):
    todo = get_todo_by_id(id)
    todo.completed = not todo.completed
    if turbo.can_stream():
        return turbo.stream(
            turbo.replace(render_template('_todo.html', todo=todo),
                          target=f'todo-{todo.id}'))
    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    todo = get_todo_by_id(id)
    if request.method == 'POST':
        todo.task = request.form['task']
        return redirect(url_for('index'))
    return render_template('index.html', todos=todos, edit_id=todo.id)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    todo = get_todo_by_id(id)
    todos.remove(todo)
    if turbo.can_stream():
        return turbo.stream(turbo.remove(target=f'todo-{todo.id}'))
    return redirect(url_for('index'))
