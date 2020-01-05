"""

"""


def get_max_id(db):
    task = db.task.find_one(sort=[('id', -1)])
    if task:
        return task.get('id', 0)
    return 0


def list_tasks(db):
    tasks = db.task.find()
    data = []
    for task in tasks:
        data.append({
            'id': task['id'],
            'description': task['description'],
            'status': task['status']
        })
    return data


def save_task(db, form):
    db.task.insert_one({
        'id': get_max_id(db) + 1,
        'description': form.description.data,
        'status': form.status.data
    })


def delete_task(db, task_id):
    db.task.remove({'id': task_id})
