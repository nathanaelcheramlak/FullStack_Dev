from models.base_model import BaseModel
from config import db

class Transaction(BaseModel, db.Model):
    __tablename__ = 'Transaction'
    id = db.Column(db.String(60), primary_key=True, nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('User.id'), nullable=False)
    name = db.Column(db.String(60), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(60), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
