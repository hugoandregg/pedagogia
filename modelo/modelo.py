# -*- coding: utf-8 
import datetime

class Papel(object):
	id = None
	permissao = None

	def __init__(self, tupla):
		self.id, self.permissao = tupla
		self.id = int(self.id)

class Aluno(object):
	matricula = None
	usuario_id = None
	polo = None

	def __init__(self, tupla):
		self.matricula, self.usuario_id, self.polo = tupla
		self.usuario_id = int(usuario_id)

class Usuario(object):
	id = None
	papel_id = None
	email = None
	senha = None
	nome = None
	sobrenome = None
	telefone = None

	def __init__(self, tupla):
		self.id, self.papel_id, self.email, self.senha, self.nome, self.sobrenome, self.telefone = tupla
		self.id = int(self.id)
		self.papel_id = int(self.papel_id)

class Funcionario(object):
	usuario_id = None
	sala = None
	ramal = None

	def __init__(self, tupla):
		self.usuario_id, self.sala, self.ramal = tupla
		self.usuario_id = int(self.usuario_id)

class Consulta(object):
	id = None
	aluno_id = None
	funcionario_id = None
	status = None
	hora_inicio = None
	comentario = None

	def __init__(self, tupla):
		self.id, self.aluno_id, self.funcionario_id, self.status, self.hora_inicio, self.comentario = tupla
		self.id = int(self.id)
		self.aluno_id = int(self.aluno_id)
		self.funcionario_id = int(self.funcionario_id)
		self.hora_inicio = datetime.datetime.fromtimestamp(int(self.hora_inicio)).strftime('%Y-%m-%d %H:%M:%S')

class Expediente(object):
	id = None
	funcionario_id = None
	hora_inicio = None

	def __init__(self, tupla):
		self.id, self.funcionario_id, self.hora_inicio= tupla
		self.id = int(self.id)
		self.funcionario_id = int(self.funcionario_id)

class Avaliacao(object):
	id = None
	aluno_id = None
	consulta_id = None
	avaliacao = None

	def __init__(self, tupla):
		self.id, self.aluno_id, self.consulta_id, self.avaliacao = tupla
		self.id = int(self.id)
		self.aluno_id = int(self.aluno_id)
		self.consulta_id = int(self.consulta_id)

class Encaminha_para(object):
	id = None
	aluno_id = None
	funcionario_origem = None
	funcionario_destino = None

	def __init__(self, tupla):
		self.id, self.aluno_id, self.funcionario_origem, self.funcionario_destino = tupla
		self.id = int(self.id)
		self.aluno_id = int(self.aluno_id)
		self.funcionario_origem = int(self.funcionario_origem)
		self.funcionario_destino = int(self.funcionario_destino)