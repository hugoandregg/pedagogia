# -*- coding: utf-8 

class Papel(object):
	id = None
	permissao = None

	def __init__(self):
		print('oi hugo')

class Aluno(object):
	matricula = None
	usuario_id = None
	polo = None

	def __init__(self):
		print('oi hugo')

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

class Consulta(object):
	id = None
	aluno_id = None
	funcionario_id = None
	status = None
	hora_inicio = None
	hora_fim = None
	comentario = None

class Expediente(object):
	id = None
	funcionario_id = None
	hora_inicio = None
	hora_fim = None

	def __init__(self):
		print('oi hugo')

class Avaliacao(object):
	id = None
	aluno_id = None
	consulta_id = None
	avaliacao = None

	def __init__(self):
		print('oi hugo') 

class Encaminha_para(object):
	id = None
	aluno_id = None
	funcionario_origem = None
	funcionario_destino = None

	def __init__(self):
		print('oi hugo')