# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, redirect, request, session, flash
from functools import wraps
from modelo.dao import *
import os

app = Flask(__name__)
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
	dao = UsuarioDAO()
	usuario = dao.find_by_id(1)
	print usuario
	if usuario is None:
		return "deu merda"
	else:
		return "deu certo"


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

		papelDao = PapelDAO()
		papel = papelDao.find_by_permissao("aluno")
		alunoDao = AlunoDAO()
		
		if alunoDao.insert(papel.id, email, senha, nome, sobrenome, telefone, matricula, polo):
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

		dao = UsuarioDAO()
		usuario = dao.find_by_email(email)

		if senha == usuario.senha:
			print usuario.id
			print usuario.papel_id
			permissao = dao.papel(usuario.papel_id)
			print permissao

			if permissao == "administrador":
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("admin"))
			elif permissao == "pedagogo" or permissao == "psicologo" or permissao == "assistente social":
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("funcionario"))
			else:
				session['logged_in'] = True
				flash("Seja bem vindo!")
				return redirect(url_for("aluno"))
		else:
			flash('email e/ou senha incorreto(s)')
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