# todoapp-flask
A simple todo app built using Flask and MongoDB.

## Components
* Flask (v1.1.1) - Python framework.
* Flask-PyMongo (v2.3.0) - adapter which allows to use PyMongo (adapter of MongoDB for Python) in Flask.
* Flask-WTF (v0.14.2) - separate module for forms creation in Flask.
* jQuery (v3.3.1) - library which was used for AJAX requests. Linked as CDN.
* Bootstrap (v4.0.0) - framework which was used for adaptive design. Linked as CDN.

## Getting started
* Install a relatively fresh version of Python. I used Python 3.6.8.
* Clone the repo or download the sources as ZIP.
* Create `venv` and install packages:
```
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* Set environment variables for MongoDB:
```
export MONGODB_HOSTNAME="127.0.0.1:27017"
export MONGODB_DATABASE="todoapp"
```
* Start development server:
```
env FLASK_APP=todoapp/app.py FLASK_ENV=development flask run
```

## License
todoapp-flask is released under the terms of the MIT license. See [MIT](https://opensource.org/licenses/MIT) and
[LICENSE](https://github.com/K9173A/todoapp-flask/blob/master/LICENSE) for more information.