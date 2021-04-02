from HujiaServer import create_app
from  flask_script import Manager, Server

app = create_app('product')
manage = Manager(app)
manage.add_command('runserver', Server(host='0.0.0.0', port=5000))


if __name__ == '__main__':
    manage.run()
