from flask import Flask, render_template
from flask import redirect
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
from flask import Response

app = Flask(__name__, template_folder='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SECRET_KEY'] = 'postgres'

db = SQLAlchemy(app)
admin = Admin(app)

session = auxiliary.ostools().db_connection()

@app.route('/redirect')
def redirected():
    return redirect("http://www.google.com", code=302)

sinal_handler = auxiliary.sinal_handler()
recurso_handler = auxiliary.recurso_handler()
ocorrencia_handler = auxiliary.ocorrencia_handler()
user_handler = auxiliary.user_handler()


@app.teardown_request
def app_teardown(response_or_exc):
	session.remove()
	return response_or_exc

#@app.route('/')
#def index():
#	return "https://www.youtube.com/watch?v=hC8CH0Z3L54"

@app.route('/user/register', methods=['GET', 'POST'])
def create_user():
	if request.method == 'GET':
		return "get"
	if request.method == 'POST':
		name = request.form['name']
		tipo = request.form['tipo']
		user_handler.create_handler(session, name, tipo)
		return "ok"

@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
	if request.method == 'GET':
		return "get"
	if request.method == 'POST':
		user_id = request.form['id']
		name = request.form['name']
		tipo = request.form['tipo']
		user_handler.update_user(session, user_id, name, tipo)
		return "ok"

@app.route('/ocorrencia/sinais/<int:id_ocorrencia>')
def ocorrencia_sinais(id_ocorrencia):
    found_sinal = sinal_handler.get_sinal_by_ocorrencia(session, id_ocorrencia)
    found_ocorrencia = ocorrencia_handler.get_ocorrencia(session, id_ocorrencia)
    req = {}
    req['ocorrencia'] = found_ocorrencia
    req['sinais'] = found_sinal
    return Response(str(req).replace("'", ""))

@app.route('/sinal/register/<int:id_ocorrencia>/<string:pressao>/<string:frequencia_cardiaca>/<string:saturacao_oxigenio>/<string:temperatura>', methods=['GET'])
def create_sinal(id_ocorrencia, pressao, frequencia_cardiaca, saturacao_oxigenio, temperatura):
	if request.method == 'GET':
		sinal_handler.create_sinal(session, id_ocorrencia, pressao, frequencia_cardiaca, saturacao_oxigenio, temperatura)
		return "ok"
	# if request.method == 'POST':
	# 	id_ocorrencia = request.form['id_ocorrencia']
	# 	pressao = request.form['pressao']
	# 	frequencia_cardiaca = request.form['frequencia_cardiaca']
	# 	saturacao_oxigenio = request.form['saturacao_oxigenio']
	# 	temperatura = request.form['temperatura']
	# 	return "ok"


@app.route('/sinal/getdata/<int:id_sinal>', methods=['GET'])
def get_data_sinal(id_sinal):
	if request.method == 'GET':
		found_sinal = sinal_handler.get_sinal(session, id_sinal)
		return Response(str(found_sinal), mimetype='application/json')

@app.route('/sinal/get_by_ocorrencia/<int:ocorrencia_id>', methods=['GET'])
def get_sinal_by_ocorrencia(ocorrencia_id):
	if request.method == 'GET':
		found_sinal = sinal_handler.get_sinal_by_ocorrencia(session, ocorrencia_id)
		return Response(str(found_sinal), mimetype='application/json')

@app.route('/sinal/getall', methods=['GET'])
def get_all_sinal():
	if request.method == 'GET':
		sinais = sinal_handler.get_all_sinal(session)
		return Response(str(sinais), mimetype='application/json')

@app.route('/recurso/status/<int:recurso_id>/<int:ocorrencia_id>', methods=['GET', 'POST'])
def update_status_recurso(recurso_id, ocorrencia_id):
	if request.method == 'GET':
		recurso_handler.update_status(session, recurso_id, ocorrencia_id)
		#recurso_handler.update_status(session, recurso_id)
		return "get"
	elif request.method == 'POST':
		recursoid = request.form['recurso_id']
		ocorrenciaid = request.form['ocorrencia_id']
		for recurso in recurso_id:
			recurso_handler.update_status(session, recursoid, ocorrenciaid)
		return "ok"
		#recurso_handler.update_status(session, recurso_id, ocorrencia_id)
		#return "ok"

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
		return Response(str(recurso), mimetype='application/json')


@app.route('/recurso/register/<string:longitude>/<string:latitude>/<string:tipo>', methods=['GET', 'POST'])
def register_recurso(longitude, latitude, tipo):
	if request.method == 'GET':
		recurso_handler.create_recurso(session, longitude, latitude, tipo)
        return "get"
	if request.method == 'POST':
		status = request.form['status']
		localizacao = request.form['localizacao']
		tipo = request.form['tipo']
		recurso_handler.create_recurso(session, status, localizacao, tipo)
		return "ok"

@app.route('/recurso/getall', methods=['GET'])
def get_all_recurso():
	if request.method == 'GET':
		recursos = recurso_handler.get_all_recurso(session)
		return Response(str(recursos).replace("'", ""), mimetype='application/json')


@app.route('/recurso/getopen', methods=['GET'])
def get_recurso_open():
	if request.method == 'GET':
		open_recursos = recurso_handler.get_all_open(session)
		return Response(str(open_recursos).replace("'", ""), mimetype='application/json')

@app.route('/recurso/getclosed', methods=['GET'])
def get_recurso_closed():
	if request.method == 'GET':
		closed_recurso = recurso_handler.get_all_closed(session)
		return Response(str(closed_recurso).replace("'", ""), mimetype='application/json')

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
		found_ocorrencia = ocorrencia_handler.get_ocorrencia(session, id_ocorrencia)
		return Response(str(found_ocorrencia).replace("'", ""), mimetype='application/json')
	if request.method == 'POST':
		id_ocorrencia = request.form['id']
		found_ocorrencia = ocorrencia_handler.get_ocorrencia(session, id_ocorrencia)
		return Response(str(found_ocorrencia).replace("'", ""), mimetype='application/json')

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
		return Response(str(updated_ocorrencia), mimetype='application/json')


@app.route('/ocorrencia/getall', methods=['GET'])
def get_all_ocorrencias():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_ocorrencias(session)
		return Response(str(ocorrencias).replace("'", ""), mimetype='application/json')

@app.route('/ocorrencia/getopen', methods=['GET'])
def get_all_open():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_open(session)
		return Response(str(ocorrencias).replace("'", ""), mimetype='application/json')

@app.route('/ocorrencia/getclosed', methods=['GET'])
def get_all_closed():
	if request.method == 'GET':
		ocorrencias = ocorrencia_handler.get_all_closed(session)
		return Response(str(ocorrencias).replace("'", ""), mimetype='application/json')





app.run(host='0.0.0.0')
