from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/code/ps-flask-rest-api/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
