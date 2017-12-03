import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy import LargeBinary


Base = declarative_base()

class Ocorrencia(Base):
	__tablename__ = 'Ocorrencia'
	id = Column(Integer, primary_key=True)
	telefone = Column(String)
	solicitante = Column(String)
	municipio = Column(String)
	endereco = Column(String)
	numero = Column(Integer)
	bairro = Column(String)
	referencia = Column(String)
	paciente = Column(String)
	sexo = Column(String)
	idade = Column(Integer)
	queixa = Column(String)
	observacoes = Column(String)
	emergencia = Column(Boolean)
	status = Column(String)
	data = Column(DateTime, server_default=func.now())
	id_atendente = Column(Integer, ForeignKey('User.id'))


class User(Base):

    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tipo = Column(String)

class Media(Base):
	__tablename__ = 'Media'
	id = Column(Integer, primary_key=True)
	ocorrencia_id = Column(Integer, ForeignKey('Ocorrencia.id'))
	binary = Column(LargeBinary)


class Recurso(Base):

    __tablename__ = 'Recurso'
    id = Column(Integer, primary_key=True)
    status = Column(String)
    longitude = Column(String)
    latitude = Column(String)
    tipo = Column(String)
    atendendo = Column(Integer, ForeignKey('Ocorrencia.id'))

class Sinais_Vitais(Base):
	__tablename__ = 'Sinais_Vitais'
	id = Column(Integer, primary_key=True)
	id_ocorrencia = Column(Integer, ForeignKey('Ocorrencia.id'))
	pressao = Column(String)
	frequencia_cardiaca = Column(String)
	saturacao_oxigenio = Column(String)
	temperatura = Column(String)


engine = create_engine('postgresql://postgres:postgres@localhost/postgres')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
