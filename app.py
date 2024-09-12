from flask_migrate import Migrate
from flask import Flask, request, jsonify
from model import *
from common import all_boards
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

@app.route('/add-to-fetch', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        roll = request.form.get('roll', None, int)
        year = request.form.get('year', None, int)
        board = request.form.get('board', None, str)
        if not roll: return jsonify(dict(success=False, msg='Invalid roll.'))
        if len(str(year)) != 4: return jsonify(dict(success=False, msg='Invalid year.'))
        if board.upper() not in all_boards: return jsonify(dict(success=False, msg='Invalid board. Should be one of ' + ','.join(all_boards)))
        board = board.upper()
        if not SSCResult.query.filter_by(roll=roll, year=year, board=board).first():
            db.session.add(SSCResult(roll=roll, year=year, board=board))
            db.session.commit()
        return jsonify(success=True, msg='Record will be added.')
    return 'Send POST with roll, year, board'


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, False)
    # t = threading.Thread(target=lambda: app.run('0.0.0.0', 8000, False))
    # t.start()
    # import data_entry
    

# DB UPDATE
# flask db init    #creates the migration folder (one time only)
# flask db migrate && flask db upgrade
# python -m flask db migrate && python -m flask db upgrade
