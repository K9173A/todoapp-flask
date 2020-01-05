"""
Module which defines application routes.
"""
import os

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

from .db import list_tasks, save_task, delete_task
from .forms import TaskCreateForm


app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://{os.environ["MONGODB_HOSTNAME"]}/{os.environ["MONGODB_DATABASE"]}'
db = PyMongo(app).db

app.secret_key = b'\x04\x8dMM\x1b\x01h[-\xd25.$\xe7\x99\x0f'


@app.route('/')
def index():
    """
    Renders index page with initial list of tasks.
    :return: rendered index page.
    """
    return render_template(
        'index.html',
        tasks=list_tasks(db),
        form=TaskCreateForm()
    )


@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    """
    Depending on the choice of method:
    - GET - shows empty form.
    - POST - validates received data and sends appropriate response.
    :return: JSON data with rendered template.
    """
    if request.method == 'POST':
        form = TaskCreateForm(request.form)
        if form.validate_on_submit():
            save_task(db, form)
            data = {
                'form_is_valid': True,
                'tasks_html': render_template(
                    'tasks_list.html',
                    tasks=list_tasks(db)
                )
            }
            return data
        else:
            data = {
                'form_is_valid': False,
                'form_html': render_template(
                    'create_task_form.html',
                    form=form
                )
            }
        print(form.errors)
    else:
        data = {
            'form_html': render_template(
                'create_task_form.html',
                form=TaskCreateForm()
            )
        }
    return jsonify(data)


@app.route('/remove_task/<task_id>/', methods=['DELETE'])
def remove_task(task_id):
    delete_task(db, task_id)
    data = {
        'tasks_html': render_template(
            'tasks_list.html',
            tasks=list_tasks(db)
        )
    }
    return jsonify(data)
