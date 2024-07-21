from models.base_model import BaseModel
from config import db

class User(BaseModel, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.String(60), primary_key=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Integer)
    transactions = db.relationship("Transaction", backref="user", cascade="all, delete")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
