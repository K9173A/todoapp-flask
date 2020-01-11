"""
Module which defines application routes.
"""
import os

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
)
from flask_pymongo import PyMongo

from . import database
from .forms import TaskForm
from .pagination import Paginator


app = Flask(__name__)
app.secret_key = b'\x04\x8dMM\x1b\x01h[-\xd25.$\xe7\x99\x0f'
app.config['MONGO_URI'] = f'mongodb://{os.environ["MONGODB_HOSTNAME"]}/{os.environ["MONGODB_DATABASE"]}'
database.db = PyMongo(app).db

paginator = Paginator()


def prepare_tasks(tasks):
    """
    Converts tasks in "renderable" form.
    :param tasks: cursor with tasks.
    :return: tasks list.
    """
    data = []
    for task in tasks:
        data.append({
            'id': task['_id'],
            'title': task['title'],
            'description': task['description'],
            'status': get_choice(TaskForm.STATUS_CHOICES, task['status']),
            'priority': get_choice(TaskForm.PRIORITY_CHOICES, task['priority']),
        })
    return data


def get_tasks():
    """
    Gets tasks with applied offset and limit, and set paginator values.
    :return: tasks list.
    """
    tasks = database.get_tasks()

    paginator.total_items = tasks.count()

    tasks = database.apply_offset(tasks, paginator.offset)
    tasks = database.apply_limit(tasks, paginator.items_per_page)

    return prepare_tasks(tasks)


def get_choice(choices, choice_key):
    """
    Gets choice value by its key.
    :param choices: list of choices (list of tuples).
    :param choice_key: chosen item (key).
    :return: value of chosen item.
    """
    for key, value in choices:
        if key == choice_key:
            return value


@app.route('/')
def root():
    """
    Redirect to the index page.
    :return:
    """
    return redirect('/p/1')


@app.route('/p/<page>')
def index(page):
    """
    Renders index page with initial list of tasks.
    :return: rendered index page.
    """
    paginator.current_page = int(page)

    return render_template(
        'index.html',
        tasks=get_tasks(),
        form=TaskForm(),
        pagination=paginator.get_pagination()
    )


@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    """
    Depending on the choice of method:
    - GET - shows empty form.
    - POST - validates received data and sends appropriate response.
    :return: update list of tasks / form.
    """
    if request.method == 'POST':
        form = TaskForm(request.form)
        if form.validate_on_submit():
            database.save_task(form)

            tasks = get_tasks()

            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html',
                    tasks=tasks
                ),
                'pagination_html': render_template(
                    'pagination.html',
                    tasks=tasks,
                    pagination=paginator.get_pagination()
                )
            }
        else:
            data = {
                'form_is_valid': False,
                'form_html': render_template(
                    'create_task_form.html',
                    form=form
                )
            }
    else:
        data = {
            'form_html': render_template(
                'create_task_form.html',
                form=TaskForm()
            )
        }
    return jsonify(data)


@app.route('/update_task', methods=['GET', 'PUT'])
def update_task():
    """
    Depending on the choice of method:
    - GET - shows prepopulated form.
    - POST - validates data and updates task.
    :return: update list of tasks / form.
    """
    task_id = request.args.get('task')
    task = database.get_task(task_id)
    if request.method == 'PUT':
        form = TaskForm(request.form)
        if form.validate_on_submit():
            database.edit_task(task_id, form)

            tasks = get_tasks()

            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html',
                    tasks=tasks
                ),
                'pagination_html': render_template(
                    'pagination.html',
                    tasks=tasks,
                    pagination=paginator.get_pagination()
                )
            }
        else:
            data = {
                'form_is_valid': False,
                'form_html': render_template(
                    'update_task_form.html',
                    form=form
                )
            }
    else:
        data = {
            'form_html': render_template(
                'update_task_form.html',
                form=TaskForm(
                    id=task['_id'],
                    title=task['title'],
                    description=task['description'],
                    status=task['status'],
                    priority=task['priority']
                )
            )
        }
    return jsonify(data)


@app.route('/remove_task', methods=['DELETE'])
def remove_task():
    """
    Removes task by its id.
    :return: updates list of tasks.
    """
    database.delete_task(request.args.get('task'))

    paginator.current_page = 1

    tasks = get_tasks()

    data = {
        'tasks_html': render_template(
            'tasks_list.html',
            tasks=tasks
        ),
        'pagination_html': render_template(
            'pagination.html',
            tasks=tasks,
            pagination=paginator.get_pagination()
        )
    }

    return jsonify(data)
