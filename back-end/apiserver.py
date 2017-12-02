from flask import Flask, render_template
from flask import jsonify
from flask import request
import json
import pandas as pd
import model
from model import Ocorrencia, Media, Sinais_Vitais, Recurso
import flask
from flask_sqlalchemy import flask_sqlalchemy
import sqlalchemy
from flask_admin import Admin
import pandas_datareader as web

app = Flask(__name__, template_folder='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)
admin = Admin(app)



app.run(host='0.0.0.0')