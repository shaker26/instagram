from flask_migrate import MigrateCommand
from flask_script import Manager
from src import app

manager = Manager(app)

# Enable db migrations to be run via the command line
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
