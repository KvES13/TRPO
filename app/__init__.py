import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(Config)

# инициализирует расширения
db = SQLAlchemy(app)

from app import views, models

