from flask import Flask 
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# creating instances 

# name sets object's name the same as the folder's
app = Flask(__name__) 
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models #placed at bottom to avoid circular dependencies 