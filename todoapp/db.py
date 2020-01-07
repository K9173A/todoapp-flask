"""
Module which implements database-related actions.
"""
from bson.objectid import ObjectId

from .forms import TaskForm


def get_choice(choices, choice_key):
    for k, v in choices:
        if k == choice_key:
            return v


def get_task(db, task_id):
    """
    Gets task by id.
    :param db: database instance.
    :param task_id: task id (ObjectId).
    :return: task object.
    """
    return db.task.find({'_id': ObjectId(task_id)})[0]


def list_tasks(db):
    """
    Takes all tasks and prepares them for rendering.
    :param db: database instance.
    :return: list with tasks.
    """
    tasks = db.task.find()
    data = []
    for task in tasks:
        data.append({
            'id': task['_id'],
            'description': task['description'],
            'status': get_choice(TaskForm.STATUS_CHOICES, task['status']),
            'priority': get_choice(TaskForm.PRIORITY_CHOICES, task['priority']),
        })
    return data


def update_task(db, form):
    """
    Updates data of task.
    :param db: database instance.
    :param form: form with data.
    :return: None.
    """
    db.task.replace_one(
        {
            '_id': ObjectId(form.id.data)
        },
        {
            'description': form.description.data,
            'status': form.status.data,
            'priority': form.priority.data
        }
    )


def save_task(db, form):
    """
    Saves task to the mongodb.
    :param db: database instance.
    :param form: form with data.
    :return: None.
    """
    db.task.insert_one({
        'description': form.description.data,
        'status': form.status.data,
        'priority': form.priority.data
    })


def delete_task(db, task_id):
    """
    Removes task from mongodb collection.
    :param db: database instance.
    :param task_id: task id (ObjectId).
    :return: None.
    """
    db.task.delete_many({'_id': ObjectId(task_id)})
