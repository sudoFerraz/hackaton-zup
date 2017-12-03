import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
import json
from model import Sinais_Vitais, Ocorrencia, Recurso, Media
import model

class ostools(object):
	def __init__(self):
		pass

	def db_connection(self):
		engine = create_engine('postgresql://postgres:postgres@localhost/postgres')
		Session = scoped_session(sessionmaker())
		Session.configure(bind=engine)
		session = Session
		return session

class sinal_handler(object):

	def create_sinal(self, session, nid_ocorrencia, npressao, nfrequencia, nsaturacao, \
		ntemperatura):
		new_sinal = model.Sinais_Vitais(id_ocorrencia=nid_ocorrencia, pressao=npressao, \
			frequencia_cardiaca=nfrequencia, saturacao_oxigenio=nsaturacao, temperatura=ntemperatura)
		session.add(new_sinal)
		session.commit()
		session.flush()
		return "ok"

	def get_sinal(self, session, id_sinal):
		found_sinal = session.query(Sinais_Vitais).filter_by(id=id_sinal).first()
		if not found_sinal:
			return "erro"
		else:
			req = {}
			req['id_ocorrencia'] = found_sinal.id_ocorrencia
			req['pressao'] = found_sinal.pressao
			req['frequencia_cardiaca'] = found_sinal.frequencia_cardiaca
			req['saturacao_oxigenio'] = found_sinal.saturacao_oxigenio
			req['temperatura'] = found_sinal.temperatura
			return json.dumps(req)

	def get_sinal_by_ocorrencia(self, session, ocorrencia_id):
		found_sinal = session.query(Sinais_Vitais).filter_by(id_ocorrencia=ocorrencia_id).first()
		if not found_sinal:
			return "erro"
		else:
			req = {}
			req['id_ocorrencia'] = found_sinal.id_ocorrencia
			req['pressao'] = found_sinal.pressao
			req['frequencia_cardiaca'] = found_sinal.frequencia_cardiaca
			req['saturacao_oxigenio'] = found_sinal.saturacao_oxigenio
			req['temperatura'] = found_sinal.temperatura
			return json.dumps(req)

	def get_all_sinal(self, session):
		sinais = session.query(Sinais_Vitais).all()
		if not found_sinal:
			return "erro"
		else:
			sinal_list = []
			for sinal in sinais:
				req = {}
				req['id_ocorrencia'] = sinal.id_ocorrencia
				req['pressao'] = sinal.pressao
				req['frequencia_cardiaca'] = sinal.frequencia_cardiaca
				req['saturacao_oxigenio'] = sinal.saturacao_oxigenio
				req['temperatura'] = sinal.temperatura
				sinal_list.append(json.dumps(req))
			return sinal_list

class user_handler(object):

	def create_user(self, session, nname, ntipo):
		new_user = model.User(name=nname, tipo=ntipo)
		session.add(new_user)
		session.commit()
		session.flush()
		return 'ok'

	def delete_user(self, session, user_id):
		deleted_user = session.query(User).filter_by(id=user_id).delete()
		session.commit()
		session.flush()
		return "ok"

	def update_user(self, session, user_id, nname, ntipo):
		updated_user = session.qwuery(User).filter_by(id=user_id).first()
		updated_user.name = nname
		updated_user.tipo = ntipo
		session.commit()
		session.flush()
		return "ok"

	def get_all(self, session):
		users = session.query(User).all()
		if not users:
			return "erro"
		else:
			user_list = []
			for user in users:
				newuser = {}
				newuser['name'] = user.name
				newuser['tipo'] = user.tipo
				newuser['id'] = user.id
				user_list.append(json.dumps(newuser))
			return user_list


class recurso_handler(object):

	def create_recurso(self, session, nlongitude, nlatitude, ntipo):
		new_recurso = model.Recurso(status="disponivel", longitude=nlongitude, latitude=nlatitude, tipo=ntipo)
		session.add(new_recurso)
		session.commit()
		session.flush()
		return 'ok'


	def update_status(self, session, id_recurso, id_ocorrencia):
		found_recurso = session.query(Recurso).filter_by(id=id_recurso).first()
		if not found_recurso:
			return "erro"
		if found_recurso.status == "disponivel":
			found_recurso.status = "ocupado"
			found_recurso.atendendo = id_ocorrencia
		elif found_recurso.status == "ocupado":
			found_recurso.status = "disponivel"
		session.commit()
		session.flush()
		return "ok"


	def delete_recurso(self, session, id_recurso):
		try:
			deleted_recurso = session.query(Recurso).filter_by(id=id_recurso).delete()
			session.commit()
			session.flush()
			return "ok"
		except:
			return "erro"

	def get_recurso(self, session, id_recurso):
		found_recurso = session.query(Recurso).filter_by(id=id_recurso).first()
		if not found_recurso:
			return "erro"
		req = {}
		req['id'] = recurso.id
		req['status'] = recurso.status
		req['longitude'] = recurso.longitude
		req['latitude'] = recurso.latitude
		req['tipo'] = recurso.tipo
		req['atendendo'] = recurso.atendendo
		return json.dumps(req)

	def get_all_recurso(self, session):
		recursos = session.query(Recurso).all()
		if not recursos:
			return "erro"
		else:
			recurso_list = []
			for recurso in recursos:
				req = {}
				req['id'] = recurso.id
				req['status'] = recurso.status
				req['longitude'] = recurso.longitude
				req['latitude'] = recurso.latitude
				req['tipo'] = recurso.tipo
				req['atendendo'] = recurso.atendendo
				recurso_list.append(json.dumps(req))
			return recurso_list

	def get_all_open(self, session):
		recursos = session.query(Recurso).all()
		if not recursos:
			return "erro"
		else:
			recurso_list = []
			for recurso in recursos:
				if recurso.status == "disponivel":
					req = {}
					req['id'] = recurso.id
					req['status'] = recurso.status
					req['longitude'] = recurso.longitude
					req['latitude'] = recurso.latitude
					req['tipo'] = recurso.tipo
					req['atendendo'] = recurso.atendendo
					recurso_list.append(json.dumps(req))
			return recurso_list

	def get_all_closed(self, session):
		recursos = session.query(Recurso).all()
		if not recursos:
			return "erro"
		else:
			recurso_list = []
			for recurso in recursos:
				if recurso.status == "ocupado":
					req = {}
					req['id'] = recurso.id
					req['status'] = recurso.status
					req['longitude'] = recurso.longitude
					req['latitude'] = recurso.latitude
					req['tipo'] = recurso.tipo
					req['atendendo'] = recurso.atendendo
					recurso_list.append(json.dumps(req))
			return recurso_list



class media_handler(object):

	def create_media(self, session, id_ocorrencia, new_binary):
		new_media = model.Media(ocorrencia_id=id_ocorrencia, binary=new_binary)
		session.add(new_media)
		session.commit()
		session.flush()
		return "ok"

	def delete_media(self, session, id_ocorrencia):
		deleted_media = session.query(Media).filter_by(ocorrencia_id=id_ocorrencia).delete()
		session.commit()
		session.flush()
		return "ok"

	def update_media(self, session, id_ocorrencia, binary):
		return "ok"

class ocorrencia_handler(object):

	def create_ocorrencia(self, session, ntelefone, nsolicitante, \
		nmunicipio, nendereco, nnumero, nbairro, nreferencia, \
		npaciente, nsexo, nidade, nqueixa, nobservacoes, \
		nemergencia, nstatus, nid_atendente):
		new_ocorrencia = model.Ocorrencia(telefone=ntelefone, \
			solicitante=nsolicitante, municipio=nmunicipio, \
			endereco=nendereco, numero=nnumero, bairro=nbairro, \
			referencia=nreferencia, paciente=npaciente, sexo=nsexo, \
			idade=nidade, queixa=nqueixa, observacoes=nobservacoes, \
			emergencia=nemergencia, status=nstatus, id_atendente=nid_atendente)
		session.add(new_ocorrencia)
		session.commit()
		session.flush()
		return "ok"

	def delete_ocorrencia(self, session, id_ocorrencia):
		try:
			deleted_ocorrencia = session.query(Ocorrencia).filter_by(id=id_ocorrencia).delete()
			session.commit()
			session.flush()
			return "ok"
		except:
			return "erro"

	def update_status(self, session, id_ocorrencia):
		found_ocorrencia = session.query(Ocorrencia).filter_by(id=id_ocorrencia).first()
		if not found_ocorrencia:
			return "erro"
		if found_ocorrencia.status == "aberta":
			found_ocorrencia.status = "encerrada"
		elif found_ocorrencia.status == "encerrada":
			found_ocorrencia.status = "aberta"
		session.commit()
		session.flush()
		return "ok"

	def get_ocorrencia(self, session, id_ocorrencia):
		found_ocorrencia = session.query(Ocorrencia).filter_by(id=id_ocorrencia).first()
		if not found_ocorrencia:
			return False
		else:
			if found_ocorrencia.id == id_ocorrencia:
				req = {}
				req['id'] = found_ocorrencia.id
				req['telefone'] = found_ocorrencia.telefone
				req['solicitante'] = found_ocorrencia.solicitante
				req['municipio'] = found_ocorrencia.municipio
				req['endereco'] = found_ocorrencia.endereco
				req['numero'] = found_ocorrencia.numero
				req['bairro'] = found_ocorrencia.bairro
				req['referencia'] = found_ocorrencia.referencia
				req['paciente'] = found_ocorrencia.paciente
				req['sexo'] = found_ocorrencia.sexo
				req['idade'] = found_ocorrencia.idade
				req['queixa'] = found_ocorrencia.queixa
				req['observacoes'] = found_ocorrencia.observacoes
				req['emergencia'] = found_ocorrencia.emergencia
				req['status'] = found_ocorrencia.status
				req['data'] = str(found_ocorrencia.data)[0:19]
				req['id_atendente'] = found_ocorrencia.id_atendente
				return json.dumps(req)
			else:
				return False

	def teste(self, session):
			return "ok"

	def get_all_ocorrencias(self, session):
		ocorrencias = session.query(Ocorrencia).all()
		ocorrencia_list = []
		if not ocorrencias:
			return False
		else:
			for found_ocorrencia in ocorrencias:
				req = {}
				req['id'] = found_ocorrencia.id
				req['telefone'] = found_ocorrencia.telefone
				req['solicitante'] = found_ocorrencia.solicitante
				req['municipio'] = found_ocorrencia.municipio
				req['endereco'] = found_ocorrencia.endereco
				req['numero'] = found_ocorrencia.numero
				req['bairro'] = found_ocorrencia.bairro
				req['referencia'] = found_ocorrencia.referencia
				req['paciente'] = found_ocorrencia.paciente
				req['sexo'] = found_ocorrencia.sexo
				req['idade'] = found_ocorrencia.idade
				req['queixa'] = found_ocorrencia.queixa
				req['observacoes'] = found_ocorrencia.observacoes
				req['emergencia'] = found_ocorrencia.emergencia
				req['status'] = found_ocorrencia.status
				req['data'] = str(found_ocorrencia.data)[0:19]
				req['id_atendente'] = found_ocorrencia.id_atendente
				ocorrencia_list.append(json.dumps(req))
			return ocorrencia_list

	def get_all_open(self, session):
		ocorrencias = session.query(Ocorrencia).all()
		ocorrencia_list = []
		if not ocorrencias:
			return False
		else:
			for found_ocorrencia in ocorrencias:
				if found_ocorrencia.status == 'aberta':
					req = {}
					req['id'] = found_ocorrencia.id
					req['telefone'] = found_ocorrencia.telefone
					req['solicitante'] = found_ocorrencia.solicitante
					req['municipio'] = found_ocorrencia.municipio
					req['endereco'] = found_ocorrencia.endereco
					req['numero'] = found_ocorrencia.numero
					req['bairro'] = found_ocorrencia.bairro
					req['referencia'] = found_ocorrencia.referencia
					req['paciente'] = found_ocorrencia.paciente
					req['sexo'] = found_ocorrencia.sexo
					req['idade'] = found_ocorrencia.idade
					req['queixa'] = found_ocorrencia.queixa
					req['observacoes'] = found_ocorrencia.observacoes
					req['emergencia'] = found_ocorrencia.emergencia
					req['status'] = found_ocorrencia.status
					req['data'] = str(found_ocorrencia.data)[0:19]
					req['id_atendente'] = found_ocorrencia.id_atendente
					ocorrencia_list.append(json.dumps(req))
			return ocorrencia_list

	def get_all_close(self, session):
		ocorrencias = session.query(Ocorrencia).all()
		ocorrencia_list = []
		if not ocorrencias:
			return False
		else:
			for found_ocorrencia in ocorrencias:
				if found_ocorrencia.status == 'encerrada':
					req = {}
					req['id'] = found_ocorrencia.id
					req['telefone'] = found_ocorrencia.telefone
					req['solicitante'] = found_ocorrencia.solicitante
					req['municipio'] = found_ocorrencia.municipio
					req['endereco'] = found_ocorrencia.endereco
					req['numero'] = found_ocorrencia.numero
					req['bairro'] = found_ocorrencia.bairro
					req['referencia'] = found_ocorrencia.referencia
					req['paciente'] = found_ocorrencia.paciente
					req['sexo'] = found_ocorrencia.sexo
					req['idade'] = found_ocorrencia.idade
					req['queixa'] = found_ocorrencia.queixa
					req['observacoes'] = found_ocorrencia.observacoes
					req['emergencia'] = found_ocorrencia.emergencia
					req['status'] = found_ocorrencia.status
					req['data'] = str(found_ocorrencia.data)[0:19]
					req['id_atendente'] = found_ocorrencia.id_atendente
					ocorrencia_list.append(json.dumps(req))
			return ocorrencia_list

	def update_ocorrencia(self, session, idocorrencia, ntelefone, nsolicitante, \
		nmunicipio, nendereco, nnumero, nbairro, nreferencia, \
		npaciente, nsexo, nidade, nqueixa, nobservacoes, nemergencia, \
		nstatus, nid_atendente):
		found_ocorrencia = session.query(Ocorrencia).filter_by(id=idocorrencia).first()
		if not found_ocorrencia:
			return False
		else:
			if found_ocorrencia.id == idocorrencia:
				found_ocorrencia.telefone = ntelefone
				found_ocorrencia.solicitante = nsolicitante
				found_ocorrencia.municipio = nmunicipio
				found_ocorrencia.endereco = nendereco
				found_ocorrencia.numero = nnumero
				found_ocorrencia.bairro = nbairro
				found_ocorrencia.referencia = nreferencia
				found_ocorrencia.paciente = npaciente
				found_ocorrencia.sexo = nsexo
				found_ocorrencia.idade = nidade
				found_ocorrencia.queixa = nqueixa
				found_ocorrencia.observacoes = nobservacoes
				found_ocorrencia.emergencia = nemergencia
				found_ocorrencia.status = nstatus
				found_ocorrencia.id_atendente = nid_atendente
				session.commit()
				session.flush()
				req = {}
				req['id'] = found_ocorrencia.id
				req['telefone'] = found_ocorrencia.telefone
				req['solicitante'] = found_ocorrencia.solicitante
				req['municipio'] = found_ocorrencia.municipio
				req['endereco'] = found_ocorrencia.endereco
				req['numero'] = found_ocorrencia.numero
				req['bairro'] = found_ocorrencia.bairro
				req['referencia'] = found_ocorrencia.referencia
				req['paciente'] = found_ocorrencia.paciente
				req['sexo'] = found_ocorrencia.sexo
				req['idade'] = found_ocorrencia.idade
				req['queixa'] = found_ocorrencia.queixa
				req['observacoes'] = found_ocorrencia.observacoes
				req['emergencia'] = found_ocorrencia.emergencia
				req['status'] = found_ocorrencia.status
				req['data'] = str(found_ocorrencia.data)[0:19]
				req['id_atendente'] = found_ocorrencia.id_atendente
				return json.dumps(req)
			return False








