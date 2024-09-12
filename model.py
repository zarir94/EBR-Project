from flask_sqlalchemy import SQLAlchemy
from common import all_boards
import sqlalchemy as sq

db = SQLAlchemy()

class SSCResult(db.Model):
    __tablename__ = 'ssc_result'
    id = db.Column(db.BigInteger, primary_key=True)
    to_update = db.Column(db.Boolean, default=True)
    reg = db.Column(db.BigInteger)
    roll = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    eiin = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    board = db.Column(db.Enum(*all_boards, name='board'), nullable=False)
    name = db.Column(db.String(120))
    father = db.Column(db.String(120))
    mother = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    dob = db.Column(db.String(120))


