"""
Module which implements database-related actions.
"""
from bson.objectid import ObjectId


db = None


def get_task(task_id):
    """
    Gets task by id.
    :param task_id: task id (ObjectId).
    :return: task object.
    """
    return db.task.find_one({'_id': ObjectId(task_id)})


def get_tasks(**filters):
    """
    Gets list of tasks with searching filters.
    :param filters: filter documents in a way: { 'attr1': '42', ... }
    :return: list with tasks.
    """
    return db.task.find(filters) if filters else db.task.find()


def apply_offset(tasks, offset):
    """
    Applies offset to the list of tasks.
    :param tasks: tasks cursor.
    :param offset: skip `offset` documents from the current cursor position.
    :return: tasks shifted on the value of offset.
    """
    return tasks.skip(offset)


def apply_limit(tasks, limit):
    """
    Cuts the size of tasks list.
    :param tasks: tasks cursor.
    :param limit: limit returned number of documents.
    :return: tasks with set limit.
    """
    return tasks.limit(limit)


def edit_task(task_id, form):
    """
    Updates data of task.
    :param task_id: task id (ObjectId).
    :param form: form with data.
    :return: None.
    """
    db.task.replace_one(
        {
            '_id': ObjectId(task_id)
        },
        {
            'title': form.title.data,
            'description': form.description.data,
            'status': form.status.data,
            'priority': form.priority.data
        }
    )


def save_task(form):
    """
    Saves task to the mongodb.
    :param form: form with data.
    :return: None.
    """
    db.task.insert_one({
        'title': form.title.data,
        'description': form.description.data,
        'status': form.status.data,
        'priority': form.priority.data
    })


def delete_task(task_id):
    """
    Removes task from mongodb collection.
    :param task_id: task id (ObjectId).
    :return: None.
    """
    db.task.delete_many({'_id': ObjectId(task_id)})
