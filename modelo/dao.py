# -*- coding: utf-8 
from modelo import *
from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123321'
app.config['MYSQL_DATABASE_DB'] = 'pedagogia'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class UsuarioDAO(object):
	def insert(self, papel_id, email, senha, nome, sobrenome, telefone):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO usuario(papel_id, email, senha, nome, sobrenome, telefone) VALUES (%s,%s,%s,%s,%s,%s)""",(papel_id, email, senha, nome, sobrenome, telefone))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM usuario WHERE id=" + id)
		data = cursor.fetchone()

		usuario = Usuario(data)
		return usuario

	def find_by_email(self, email):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM usuario WHERE email='" + email + "'")
		data = cursor.fetchone()

		usuario = Usuario(data)
		return usuario

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM usuario")
		data = cursor.fetchall()

		usuario = None
		usuarios = []
		for row in data:
			usuario = Usuario(row)
			usuarios.append(usuario)

	def update(self, id, papel_id, email, senha, nome, sobrenome, telefone):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE usuario SET papel_id=%s, email='%s', senha='%s', nome='%s', sobrenome='%s', telefone='%s' WHERE id=%s", (papel_id, email, senha, nome, sobrenome, telefone, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM usuario WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def papel(self, papel_id):
		papel_id = str(papel_id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT permissao FROM papel WHERE id=" + papel_id)
		data = cursor.fetchone()[0]
		print data

		return str(data)


class AlunoDAO(object):
	def insert(self, papel_id, email, senha, nome, sobrenome, telefone, matricula, polo):
		usuarioDao = UsuarioDAO()
		usuarioDao.insert(papel_id, email, senha, nome, sobrenome, telefone)
		
		db = mysql.connect()
		cursor = db.cursor()

		cursor.execute("SELECT id FROM usuario WHERE email='" + email + "' AND senha='" + senha + "'")
		usuario_id = cursor.fetchone()[0]
		usuario_id = int(usuario_id)
		
		try:
			cursor.execute("""INSERT INTO aluno(matricula, usuario_id, polo) VALUES (%s,%s,%s)""",(matricula, usuario_id, polo))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_usuario(self, usuario_id):
		usuario_id = str(usuario_id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM aluno WHERE usuario_id=" + usuario_id)
		data = cursor.fetchone()

		aluno = Aluno(data)
		return aluno

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM aluno")
		data = cursor.fetchall()

		aluno = None
		alunos = []
		for row in data:
			aluno = Aluno(row)
			alunos.append(aluno)

	def update(self, id, papel_id, email, senha, nome, sobrenome, telefone, matricula, polo):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()

		usuarioDao = UsuarioDAO()
		dao.update(id, papel_id, email, senha, nome, sobrenome, telefone)
		
		try:
			cursor.execute("UPDATE aluno SET matricula='%s', polo='%s' WHERE usuario_id=%s", (matricula, polo, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		usuarioDao = UsuarioDAO()
		usuarioDao.delete(id)

		try:
			cursor.execute("DELETE FROM aluno WHERE usuario_id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class FuncionarioDAO(object):
	def insert(self, papel_id, email, senha, nome, sobrenome, telefone, sala, ramal):
		usuarioDao = UsuarioDAO()
		usuarioDao.insert(papel_id, email, senha, nome, sobrenome, telefone)
		
		db = mysql.connect()
		cursor = db.cursor()

		cursor.execute("SELECT id FROM usuario WHERE email='" + email + "' AND senha='" + senha + "'")
		usuario_id = cursor.fetchone()[0]
		
		try:
			cursor.execute("""INSERT INTO funcionario(usuario_id, sala, ramal) VALUES (%s,%s,%s)""",(usuario_id, sala, ramal))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_usuario(self, usuario_id):
		usuario_id = str(usuario_id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM funcionario WHERE usuario_id=" + usuario_id)
		data = cursor.fetchone()

		funcionario = Funcionario(data)
		return funcionario

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM funcionario")
		data = cursor.fetchall()

		funcionario = None
		funcionarios = []
		for row in data:
			funcionario = Funcionario(row)
			funcionarios.append(funcionario)

	def update(self, id, papel_id, email, senha, nome, sobrenome, telefone, sala, ramal):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()

		usuarioDao = UsuarioDAO()
		dao.update(id, papel_id, email, senha, nome, sobrenome, telefone)
		
		try:
			cursor.execute("UPDATE funcionario SET sala='%s', ramal='%s' WHERE usuario_id=%s", (sala, ramal, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		usuarioDao = UsuarioDAO()
		usuarioDao.delete(id)

		try:
			cursor.execute("DELETE FROM funcionario WHERE usuario_id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class PapelDAO(object):
	def insert(self, permissao):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO papel(permissao) VALUES (%s,%s,%s,%s,%s,%s)""",(permissao))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM papel WHERE id=" + id)
		data = cursor.fetchone()

		papel = Papel(data)
		return papel

	def find_by_permissao(self, permissao):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM papel WHERE permissao='" + permissao + "'")
		data = cursor.fetchone()

		papel = Papel(data)
		return papel

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM papel")
		data = cursor.fetchall()

		papel = None
		papeis = []
		for row in data:
			papel = papel(row)
			papeis.append(papel)

	def update(self, id, permissao):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE papel SET permissao='%s' WHERE id=%s", (permissao, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM papel WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class ConsultaDAO(object):
	def insert(self, aluno_id, funcionario_id, status, hora_inicio, hora_fim, comentario):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO consulta(aluno_id, funcionario_id, status, hora_inicio, hora_fim, comentario) VALUES (%s,%s,%s,%s,%s,%s)""",(aluno_id, funcionario_id, status, hora_inicio, hora_fim, comentario))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM consulta WHERE id=" + id)
		data = cursor.fetchone()

		consulta = Consulta(data)
		return consulta

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM consulta")
		data = cursor.fetchall()

		consulta = None
		consultas = []
		for row in data:
			consulta = Consulta(row)
			consultas.append(consulta)

	def update(self, id, aluno_id, funcionario_id, status, hora_inicio, hora_fim, comentario):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE consulta SET aluno_id=%s, funcionario_id=%s, status='%s', hora_inicio='%s', hora_fim='%s', comentario='%s' WHERE id=%s", (aluno_id, funcionario_id, status, hora_inicio, hora_fim, comentario, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM consulta WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class ExpedienteDAO(object):
	def insert(self, funcionario_id, hora_inicio, hora_fim):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO expediente(funcionario_id, hora_inicio, hora_fim) VALUES (%s,%s,%s)""",(funcionario_id, hora_inicio, hora_fim))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM expediente WHERE id=" + id)
		data = cursor.fetchone()

		expediente = Expediente(data)
		return expediente

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM expediente")
		data = cursor.fetchall()

		expediente = None
		expedientes = []
		for row in data:
			expediente = Expediente(row)
			expedientes.append(expediente)

	def update(self, id, funcionario_id, hora_inicio, hora_fim):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE expediente SET funcionario_id=%s, hora_inicio='%s', hora_fim='%s' WHERE id=%s", (funcionario_id, hora_inicio, hora_fim, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM expediente WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class AvaliacaoDAO(object):
	def insert(self, aluno_id, consulta_id, avaliacao):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO avaliacao(aluno_id, consulta_id, avaliacao) VALUES (%s,%s,%s)""",(aluno_id, consulta_id, avaliacao))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM avaliacao WHERE id=" + id)
		data = cursor.fetchone()

		avaliacao = Avaliacao(data)
		return avaliacao

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM avaliacao")
		data = cursor.fetchall()

		avaliacao = None
		avaliacoes = []
		for row in data:
			avaliacao = Avaliacao(row)
			avaliacoes.append(avaliacao)

	def update(self, id, aluno_id, consulta_id, avaliacao):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE avaliacao SET aluno_id=%s, consulta_id=%s, avaliacao='%s' WHERE id=%s", (aluno_id, consulta_id, avaliacao, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM avaliacao WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False


class Encaminha_paraDAO(object):
	def insert(self, aluno_id, funcionario_origem, funcionario_destino):
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("""INSERT INTO encaminha_para(aluno_id, funcionario_origem, funcionario_destino) VALUES (%s,%s,%s)""",(aluno_id, funcionario_origem, funcionario_destino))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def find_by_id(self, id):
		id = str(id)
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM encaminha_para WHERE id=" + id)
		data = cursor.fetchone()

		encaminha_para = Encaminha_para(data)
		return encaminha_para

	def find_all(self):
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM encaminha_para")
		data = cursor.fetchall()

		encaminha_para = None
		encaminham_para = []
		for row in data:
			encaminha_para = Encaminha_para(row)
			encaminham_para.append(encaminha_para)

	def update(self, id, aluno_id, funcionario_origem, funcionario_destino):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("UPDATE encaminha_para SET aluno_id=%s, funcionario_origem=%s, funcionario_destino=%s WHERE id=%s", (aluno_id, funcionario_origem, funcionario_destino, id))
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False

	def delete(self, id):
		id = str(id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute("DELETE FROM encaminha_para WHERE id=" + id)
			db.commit()
			return True
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				return False
			except IndexError:
				print "MySQL Error: %s" % str(e)
				return False