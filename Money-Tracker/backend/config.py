from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

load_dotenv()
DB_USER = getenv("DB_USER")
PASSWORD = getenv("PASSWORD")
HOST = getenv("HOST")
DATABASE = getenv("DATABASE")



