from config import db
from models.user import User
from models.transaction import Transaction

classes = {'User': User, 'Transaction': Transaction}

class DBStorage:
    def __init__(self):
        self.__session = db.session

    def all(self, cls=None):
        key_obj = {}

        if cls in classes:
            objects = classes[cls].query.all()
            for obj in objects:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                key_obj[key] = obj
        
        return key_obj
    
    def new(self, data):
        self.__session.add(data)

    def save(self):
        self.__session.commit()

    def delete(self, data=None):
        if data:
            self.__session.delete(data)
        
    def close(self):
        self.__session.close()

    def get(self, cls, id=None, email=None):
        if cls in classes:
            if id:
                return classes[cls].query.get(id)
            elif email:
                return classes[cls].query.filter_by(email=email).first()
        return None