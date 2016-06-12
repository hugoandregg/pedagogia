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
		query = """INSERT INTO usuario(papel_id, email, senha, nome, sobrenome, telefone) VALUES (%s,%s,%s,%s,%s,%s)""",(papel_id, email, senha, nome, sobrenome, telefone)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute(query)
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
		query = "SELECT * FROM usuario WHERE id=" + id
		cursor = mysql.connect().cursor()
		cursor.execute(query)
		data = cursor.fetchone()

		usuario = Usuario(data)
		return usuario

	def find_by_email(self, email):
		query = "SELECT * FROM usuario WHERE email='" + email + "'"
		cursor = mysql.connect().cursor()
		cursor.execute(query)
		data = cursor.fetchone()

		usuario = Usuario(data)
		return usuario

	def find_all(self):
		query = "SELECT * FROM usuario"
		cursor = mysql.connect().cursor()
		cursor.execute(query)
		data = cursor.fetchall()

		usuario = None
		usuarios = []
		for row in data:
			usuario = Usuario(row)
			usuarios.append(usuario)

	def update(self, id, papel_id, email, senha, nome, sobrenome, telefone):
		id = str(id)
		query = "UPDATE usuario SET papel_id=%s, email='%s', senha='%s', nome='%s', sobrenome='%s', telefone='%s' WHERE id=%s", (papel_id, email, senha, nome, sobrenome, telefone, id)
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute(query)
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
		query = "DELETE FROM usuario WHERE id=" + id
		db = mysql.connect()
		cursor = db.cursor()
		
		try:
			cursor.execute(query)
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
		query = "SELECT permissao FROM papel WHERE id=" + papel_id
		cursor = mysql.connect().cursor()
		cursor.execute(query)
		data = cursor.fetchone()[0]
		print data

		return str(data)