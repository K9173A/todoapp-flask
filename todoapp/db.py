"""
Module which implements database-related actions.
"""
from bson.objectid import ObjectId

from .forms import TaskCreateForm


def get_choice(choices, choice_key):
    for k, v in choices:
        if k == choice_key:
            return v
    return None


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
            'status': get_choice(TaskCreateForm.STATUS_CHOICES, task['status']),
            'priority': get_choice(TaskCreateForm.PRIORITY_CHOICES, task['priority']),
        })
    return data


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



