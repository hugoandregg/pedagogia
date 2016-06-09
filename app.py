# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request, session, flash
from functools import wraps
from flaskext.mysql import MySQL
import os

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123321'
app.config['MYSQL_DATABASE_DB'] = 'pedagogia'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key = os.urandom(24)

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Você precisa logar primeiro')
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def main():
	return "tela de inicio"

@app.route("/registrar_aluno", methods=['GET', 'POST'])
def registrar_aluno():
	if request.method == 'POST':
		nome = request.form['nome']
		sobrenome = request.form['sobrenome']
		email = request.form['email']
		matricula = request.form['matricula']
		polo = request.form['polo']
		telefone = request.form['telefone']
		senha = request.form['senha']

		db = mysql.connect()
		cursor = db.cursor()
		print cursor
		cursor.execute("SELECT id FROM papel WHERE permissao='aluno'")
		papel_id = cursor.fetchone()[0]
		papel_id = int(papel_id)
		print papel_id

		error = True
		try:
			cursor.execute("""INSERT INTO usuario(papel_id, email, senha, nome, sobrenome, telefone) VALUES (%s,%s,%s,%s,%s,%s)""",(papel_id, email, senha, nome, sobrenome, telefone))
			db.commit()
			print "chegou aqui"
			cursor.execute("SELECT id FROM usuario WHERE email='" + email + "' AND senha='" + senha + "'")
			usuario_id = cursor.fetchone()[0]
			usuario_id = int(usuario_id)
			print usuario_id
			cursor.execute("""INSERT INTO aluno(matricula, usuario_id, polo) VALUES (%s,%s,%s)""",(matricula, usuario_id, polo))
			db.commit()
			print "chegou aqui"
			error = False
		except db.Error, e:
			try:
				db.rollback()
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)

		if error == False:
			session['logged_in'] = True
			flash("Seja bem vindo!")
			return redirect(url_for("aluno"))
		else:
			flash('Problema para inserir os dados')
		
	return render_template('registrar_aluno.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		senha = request.form['senha']
		cursor = mysql.connect().cursor()
		cursor.execute("SELECT * FROM usuario WHERE email='" + email + "' AND senha='" + senha + "'")
		data = cursor.fetchone()
		
		if data is None:
			flash('email e/ou senha incorreto(s)')
		else:
			cursor.execute("SELECT papel_id FROM usuario WHERE email='" + email + "' AND senha='" + senha + "'")
			papel_id = cursor.fetchone()[0]
			papel_id = int(papel_id)

			cursor.execute("SELECT permissao FROM papel WHERE id =" + str(papel_id))
			data = cursor.fetchone()[0]

			if data == "administrador":
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("admin"))
			elif data == "pedagogo" or data == "psicologo" or data == "assistente social":
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("funcionario"))
			else:
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("aluno"))
	return render_template('login.html')

@app.route("/admin")
@login_required
def admin():
	return render_template('admin.html')

@app.route("/funcionario")
@login_required
def funcionario():
	return "welcome funcionario"

@app.route("/aluno")
@login_required
def aluno():
	return "welcome aluno"

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Deslogado com sucesso!')
    return redirect(url_for('main'))

if __name__ == '__main__':
	app.run()