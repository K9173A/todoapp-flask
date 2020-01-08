"""
Module which implements database-related actions.
"""
from bson.objectid import ObjectId

from .forms import TaskForm


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


def get_task(db, task_id):
    """
    Gets task by id.
    :param db: database instance.
    :param task_id: task id (ObjectId).
    :return: task object.
    """
    return db.task.find_one({'_id': ObjectId(task_id)})


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


def edit_task(db, task_id, form):
    """
    Updates data of task.
    :param db: database instance.
    :param task_id: task id (ObjectId).
    :param form: form with data.
    :return: None.
    """
    db.task.replace_one(
        {
            '_id': ObjectId(task_id)
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
