"""
Module which defines application routes.
"""
import os

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

from .db import (
    list_tasks,
    save_task,
    edit_task,
    delete_task,
    get_task
)
from .forms import TaskForm


app = Flask(__name__)
app.secret_key = b'\x04\x8dMM\x1b\x01h[-\xd25.$\xe7\x99\x0f'
app.config['MONGO_URI'] = f'mongodb://{os.environ["MONGODB_HOSTNAME"]}/{os.environ["MONGODB_DATABASE"]}'
db = PyMongo(app).db


@app.route('/')
def index():
    """
    Renders index page with initial list of tasks.
    :return: rendered index page.
    """
    return render_template(
        'index.html', tasks=list_tasks(db), form=TaskForm()
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
            save_task(db, form)
            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html', tasks=list_tasks(db)
                )
            }
        else:
            data = {
                'form_is_valid': False,
                'form_html': render_template(
                    'create_task_form.html', form=form
                )
            }
    else:
        data = {
            'form_html': render_template(
                'create_task_form.html', form=TaskForm()
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
    task = get_task(db, task_id)
    if request.method == 'PUT':
        form = TaskForm(request.form)
        if form.validate_on_submit():
            edit_task(db, task_id, form)
            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html', tasks=list_tasks(db)
                )
            }
        else:
            data = {
                'form_is_valid': False,
                'form_html': render_template(
                    'update_task_form.html', form=form
                )
            }
    else:
        data = {
            'form_html': render_template(
                'update_task_form.html', form=TaskForm(
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
    delete_task(db, request.args.get('task'))
    data = {
        'tasks_html': render_template(
            'tasks_list.html', tasks=list_tasks(db)
        )
    }
    return jsonify(data)
