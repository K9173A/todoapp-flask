"""
Module which defines application routes.
"""
import os
import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
from flask_pymongo import PyMongo


from . import database
from .forms import TaskForm
from .url_handler import URLHandler


app = Flask(__name__)
app.secret_key = b'\x04\x8dMM\x1b\x01h[-\xd25.$\xe7\x99\x0f'
app.config['MONGO_URI'] = f'mongodb://{os.environ["MONGODB_HOSTNAME"]}/{os.environ["MONGODB_DATABASE"]}'
database.db = PyMongo(app).db

url_handler = URLHandler()


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
            'date_added': datetime.datetime.fromtimestamp(task['date_added']).strftime('%H:%M:%S %d-%m-%Y'),
            'status': get_choice(TaskForm.STATUS_CHOICES, task['status']),
            'priority': get_choice(TaskForm.PRIORITY_CHOICES, task['priority']),
        })
    return data


def get_tasks(sorting_condition, **filters):
    """
    Gets tasks with applied offset and limit, and set paginator values.
    :param sorting_condition: sorting criteria.
    :param filters: filter documents in a way: { 'attr1': '42', ... }
    :return: tasks list.
    """
    if filters:
        tasks = database.get_tasks(**filters)
    else:
        tasks = database.get_tasks()

    url_handler.total = tasks.count()

    tasks = database.apply_sorting(tasks, sorting_condition)
    tasks = database.apply_offset(tasks, url_handler.offset)
    tasks = database.apply_limit(tasks, url_handler.PER_PAGE)

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
def index():
    """
    Renders index page with initial list of tasks.
    :return: rendered index page.
    """
    url_handler.handle_request()
    return render_template(
        'index.html',
        tasks=get_tasks(url_handler.get_sorting_condition()),
        form=TaskForm(),
        pagination=url_handler.get_pagination_data()
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

            tasks = get_tasks(url_handler.get_sorting_condition())

            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html',
                    tasks=tasks
                ),
                'pagination_html': render_template(
                    'pagination.html',
                    tasks=tasks,
                    pagination=url_handler.get_pagination_data()
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

            tasks = get_tasks(url_handler.get_sorting_condition())

            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html',
                    tasks=tasks
                ),
                'pagination_html': render_template(
                    'pagination.html',
                    tasks=tasks,
                    pagination=url_handler.get_pagination_data()
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

    url_handler.page = 1

    tasks = get_tasks(url_handler.get_sorting_condition())

    data = {
        'tasks_html': render_template(
            'tasks_list.html',
            tasks=tasks
        ),
        'pagination_html': render_template(
            'pagination.html',
            tasks=tasks,
            pagination=url_handler.get_pagination_data()
        )
    }
    return jsonify(data)
