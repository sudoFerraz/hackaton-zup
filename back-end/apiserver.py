from flask import Flask, render_template
from flask import jsonify
from flask import request
import auxiliary
import json
import pandas as pd
import model
from model import Ocorrencia, Media, Sinais_Vitais, Recurso
import flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_admin import Admin
import pandas_datareader as web

app = Flask(__name__, template_folder='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)
admin = Admin(app)

session = auxiliary.ostools().db_connection()

recurso_handler = auxiliary.recurso_handler()
ocorrencia_handler = auxiliary.ocorrencia_handler()

@app.teardown_request
def app_teardown(response_or_exc):
	session.remove()
	return response_or_exc

#@app.route('/')
#def index():
#	return "https://www.youtube.com/watch?v=hC8CH0Z3L54"

@app.route('/recurso/status/<int:recurso_id>', methods=['GET', 'POST'])
def update_status_recurso(recurso_id):
	if request.method == 'GET':
		recurso_handler.update_status(session, recurso_id)
		return "ok"
	elif request.method == 'POST':
		recurso_id = request.form['id']
		recurso_handler.update_status(session, recurso_id)
		return "ok"

@app.route('/recurso/delete/<int:recurso_id>', methods=['GET', 'POST'])
def delete_recurso(recurso_id):
	if request.method == 'GET':
		recurso_handler.delete_recurso(session, recurso_id)
		return "ok"
	if request.method == 'POST':
		recurso_id = request.form['id']
		recurso_handler.delete_recurso(session, recurso_id)
		return "ok"

@app.route('/recurso/getdata/<int:recurso_id>', methods=['GET', 'POST'])
def get_recurso(recurso_id):
	if request.method == 'GET':
		reurso = recurso_handler.get_recurso(session, recurso_id)
		return str(recurso)
	if request.method == 'POST':
		recurso_id = request.form['id']
		recurso = recurso_handler.get_recurso(session, recurso_id)
		return str(recurso)

@app.route('/recurso/register', methods=['GET', 'POST'])
def register_recurso():
	if request.method == 'GET':
		return "get"
	elif request.method == 'POST':
		status = request.form['status']
		localizacao = request.form['localizacao']
		tipo = request.form['tipo']
		recurso_handler.create_recurso(session, status, localizacao, tipo)
		return "ok"

@app.route('/recurso/getall', methods=['GET'])
def get_all_recurso():
	if requset.method == 'GET':
		recursos = recurso_handler.get_all_recurso(session)
		return str(recursos).replace("'", "")


@app.route('/recurso/getopen', methods=['GET'])
def get_recurso_open():
	if request.method == 'GET':
		open_recursos = recurso_handler.get_all_open(session)
		return str(open_recursos).replace("'", "")

@app.route('/recurso/getclosed', methods=['GET'])
def get_recurso_closed():
	if request.method == 'GET':
		closed_recurso = recurso_handler.get_all_closed(session)
		return str(closed_recurso).replace("'", "")

@app.route('/ocorrencia/register', methods=['POST'])
def ocorrencia_register():
	if request.method == 'POST':
		telefone = request.form['telefone']
		solicitante = request.form['solicitante']
		municipio = request.form['municipio']
		endereco = request.form['endereco']
		numero = request.form['numero']
		bairro = request.form['bairro']
		referencia = request.form['referencia']
		paciente = request.form['paciente']
		sexo = request.form['sexo']
		idade = request.form['idade']
		queixa = request.form['queixa']
		observacoes = request.form['observacoes']
		emergencia = request.form['emergencia']
		status = "aberta"
		id_atendente = request.form['id_atendente']
		ocorrencia_handler.create_ocorrencia(session, telefone, solicitante, \
			municipio, endereco, numero, bairro, referencia, paciente, \
			sexo, idade, queixa, observacoes, emergencia, status, id_atendente)
		return "ok"

@app.route('/ocorrencia/delete/<int:ocorrencia_id>', methods=['GET', 'POST'])
def delete_ocorrencia(ocorrencia_id):
	if request.method == 'GET':
		ocorrencia_handler.delete_ocorrencia(session, ocorrencia_id)
		return "ok"
	if request.method == 'POST':
		id_ocorrencia = request.form['id']
		ocorrencia_handler.delete_ocorrencia(session, id_ocorrencia)
		return "ok"

@app.route('/ocorrencia/update_status/<int:id_ocorrencia>', methods=['GET', 'POST'])
def update_status(id_ocorrencia):
	if request.method == 'GET':
		ocorrencia_handler.update_status(session, id_ocorrencia)
		return "ok"
	if request.method == 'POST':
		id_ocorrencia = request.form['id']
		ocorrencia_handler.update_status(session, id_ocorrencia)
		return "ok"

@app.route('/ocorrencia/getdata/<int:id_ocorrencia>', methods=['GET', 'POST'])
def get_ocorrencia(id_ocorrencia):
	if request.method == 'GET':
		found_ocorrencia. = ocorrencia_handler.get_ocorrencia(session, id_ocorrencia)
		return str(found_ocorrencia).replace("'", "")
	if request.method == 'POST':
		id_ocorrencia = request.form['id']
		found_ocorrencia = ocorrencia_handler.get_ocorrencia(session, id_ocorrencia)
		return str(found_ocorrencia).replace("'", "")

@app.route('/ocorrencia/update', methods=['POST'])
def update_ocorrencia():
	if request.method == 'POST':
		id_ocorrencia = request.form['id']
		telefone = request.form['telefone']
		solicitante = request.form['solicitante']
		municipio = request.form['municipio']
		endereco = request.form['endereco']
		numero = request.form['numero']
		bairro = request.form['bairro']
		referencia = request.form['referencia']
		paciente = request.form['paciente']
		sexo = request.form['sexo']
		idade = request.form['idade']
		queixa = request.form['queixa']
		observacoes = request.form['observacoes']
		emergencia = request.form['emergencia']
		status = request.form['status']
		id_atendente = request.form['id_atendente']
		updated_ocorrencia = ocorrencia_handler.update_ocorrencia(sesion, id_ocorrencia, telefone, \
			solicitante, municipio, enereco, numero, bairro, referencia, \
			paciente, sexo, idade, queixa, observacoes, emergencia, status, \
			id_atendente)
		return str(updated_ocorrencia)


@app.route('/ocorrencia/getall', methods=['GET'])
def get_all_ocorrencias():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_ocorrencias(session)
		return str(ocorrencias).replace("'", "")

@app.route('/ocorrencia/getopen', methods=['GET'])
def get_all_open():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_open(session)
		return str(ocorrencias).replace("'", "")

@app.route('/ocorrencia/getclosed', methods=['GET'])
def get_all_closed():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_closed(session)
		return str(ocorrencias).replace("'", "")





app.run(host='0.0.0.0')