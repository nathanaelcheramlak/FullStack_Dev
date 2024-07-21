import uuid
from datetime import datetime

t_format = "%Y-%m-%dT%H:%M:%S"

class BaseModel:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().strftime(t_format)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        class_info = ""

        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                class_info += "{}: {}\n".format(key, value)
        return class_info
    
    def to_dict(self):
        class_dict = {}
        for key, value in self.__dict__.items():
            if key != "_sa_instance_state":
                class_dict[key] = value
        return class_dict
    
    def save_to_db(self):
        from models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        from models import storage
        storage.delete(self)
        storage.save()
