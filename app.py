from flask_migrate import Migrate
from flask import Flask
from model import *
import os, threading

app = Flask(__name__)
app.config['SECRET_KEY'] = '09bfcb54-3fc0-4105-8904-4d64ecd0c318'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('RESULT_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context(): db.create_all()

@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    t = threading.Thread(target=lambda: app.run('0.0.0.0', 8000, False))
    t.start()
    import data_entry
    

# DB UPDATE
# flask db init    #creates the migration folder (one time only)
# flask db migrate && flask db upgrade
# python -m flask db migrate && python -m flask db upgrade
