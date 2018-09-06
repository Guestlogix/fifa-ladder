import os
from flask_script import Manager, commands
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# Migrations
migrate = Migrate(app, db)

# Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command(
    "runserver",
    commands.Server(
        host=None, # use default [0.0.0.0]
        port=None, # use env port or default [5000]
        threaded=True # run as threaded
    ) 
)

if __name__ == '__main__':
    manager.run()