# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, jsonify, redirect, request, session, flash
from functools import wraps
from modelo.dao import *
import os, datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'current_user' in session:
			return f(*args, **kwargs)
		else:
			flash('Voce precisa logar primeiro')
			return redirect(url_for('login'))
	return wrap

@app.route("/")
def main():
	return render_template('home.html')


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
			usuarioDao = UsuarioDAO()
			usuario = usuarioDao.find_by_email(email)
			session['current_user'] = usuario.id
			flash("Seja bem vindo!")
			return redirect(url_for("aluno"))
		else:
			flash('Problema para inserir os dados')
		
	return render_template('registrar_aluno.html')

@app.route("/registrar_funcionario", methods=['GET', 'POST'])
def registrar_funcionario():
	if request.method == 'POST':
		nome = request.form['nome']
		sobrenome = request.form['sobrenome']
		papel = request.form['papel']
		email = request.form['email']
		sala = request.form['sala']
		ramal = request.form['ramal']
		telefone = request.form['telefone']
		senha = request.form['senha']

		papelDao = PapelDAO()
		papel = papelDao.find_by_permissao(papel)
		funcionarioDao = FuncionarioDAO()

		if funcionarioDao.insert(papel.id, email, senha, nome, sobrenome, telefone, sala, ramal):
			flash("Usuario cadastrado com sucesso!")
			return redirect(url_for("admin"))
		else:
			flash('Problema para cadastrar funcionario')
	return render_template('registrar_funcionario.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		senha = request.form['senha']

		dao = UsuarioDAO()
		usuario = dao.find_by_email(email)

		if senha == usuario.senha:
			permissao = dao.papel(usuario.papel_id)

			if permissao == "administrador":
				session['current_user'] = usuario.id
				flash("Seja bem vindo!")
				return redirect(url_for("admin"))
			elif permissao == "pedagogo" or permissao == "psicologo" or permissao == "assistente social":
				session['current_user'] = usuario.id
				flash("Seja bem vindo!")
				return redirect(url_for("funcionario"))
			else:
				session['current_user'] = usuario.id
				flash("Seja bem vindo!")
				return redirect(url_for("aluno"))
		else:
			flash('email e/ou senha incorreto(s)')
	return render_template('login.html')

@app.route("/admin")
@login_required
def admin():
	usuario = current_user()
	consultaDao = ConsultaDAO()
	consultas = consultaDao.find_all()
	return render_template('admin.html', consultas=consultas, usuario=usuario)

@app.route("/consultas_avaliadas")
@login_required
def consultas_avaliadas():
	usuario = current_user()
	avaliacaoDao = AvaliacaoDAO()
	avaliacoes = avaliacaoDao.find_consultas_avaliadas()
	print avaliacoes
	return render_template('consultas_avaliadas.html', avaliacoes=avaliacoes, usuario=usuario)

@app.route("/funcionario")
@login_required
def funcionario():
	usuario = current_user()
	consultaDao = ConsultaDAO()
	consultas = consultaDao.find_by_funcionario(usuario.id)
	return render_template('funcionario.html', consultas=consultas, usuario=usuario)

@app.route("/editar_consulta/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_consulta(id):
	consultaDao = ConsultaDAO()
	consulta = consultaDao.find_by_id(id)
	if request.method == 'POST':
		status = request.form['status']
		hora_inicio = request.form['hora_inicio']
		comentario = request.form['comentario']
		if consultaDao.update(id, consulta.aluno_id, consulta.funcionario_id, status, hora_inicio, comentario):
			flash("Consulta atualizada com sucesso!")
			return redirect(url_for("funcionario"))
		else:
			flash('Problema para atualizar a consulta')
	return render_template('editar_consulta.html', consulta=consulta)

@app.route("/realizar_consulta/<int:id>")
@login_required
def realizar_consulta(id):
	consultaDao = ConsultaDAO()
	consulta = consultaDao.find_by_id(id)
	if consultaDao.update(id, consulta.aluno_id, consulta.funcionario_id, 'Realizada', consulta.hora_inicio, consulta.comentario):
		flash("Consulta realizada com sucesso!")
		return redirect(url_for("funcionario"))
	else:
		flash('Problema para realizar a consulta')
		return redirect(url_for("funcionario"))

@app.route("/cancelar_consulta/<int:id>")
@login_required
def cancelar_consulta(id):
	consultaDao = ConsultaDAO()
	consulta = consultaDao.find_by_id(id)
	if consultaDao.update(id, consulta.aluno_id, consulta.funcionario_id, 'Cancelada', consulta.hora_inicio, consulta.comentario):
		flash("Consulta realizada com sucesso!")
		return redirect(url_for("funcionario"))
	else:
		flash('Problema para realizar a consulta')
		return redirect(url_for("funcionario"))

@app.route("/meus_expedientes")
@login_required
def meus_expedientes():
	usuario = current_user()
	expedienteDao = ExpedienteDAO()
	expedientes = expedienteDao.find_by_funcionario(usuario.id)
	return render_template('meus_expedientes.html', expedientes=expedientes, usuario=usuario)

@app.route("/marcar_expediente", methods=['GET', 'POST'])
@login_required
def marcar_expediente():
	if request.method == 'POST':
		hora_inicio = request.form['hora_inicio']
		#datetime.datetime.fromtimestamp(hora_inicio).strftime('%Y-%m-%d %H:%M:%S')
		usuario = current_user()
		expedienteDao = ExpedienteDAO()
		if expedienteDao.insert(usuario.id, hora_inicio):
			flash("Expediente cadastrado com sucesso!")
			return redirect(url_for("funcionario"))
		else:
			flash('Problema para cadastrar funcionario')
	return render_template('marcar_expediente.html')

@app.route("/aluno")
@login_required
def aluno():
	usuario = current_user()
	consultaDao = ConsultaDAO()
	consultas = consultaDao.find_by_aluno(usuario.id)
	return render_template('aluno.html', consultas=consultas, usuario=usuario)

@app.route("/marcar_consulta", methods=['GET', 'POST'])
@login_required
def marcar_consulta():
	if request.method == 'POST':
		funcionario_id = request.form['funcionario_id']
		hora_inicio = request.form['hora_inicio']
		#hora_inicio = datetime.datetime.strptime(hora_inicio, '%Y-%m-%d %H:%M:%S').date()
		aluno = current_user()
		status = 'Marcado'
		consultaDao = ConsultaDAO()
		if consultaDao.insert(aluno.id, funcionario_id, status, hora_inicio, None):
			flash("Consulta marcada com sucesso!")
			return redirect(url_for("aluno"))
		else:
			flash('Problema para marcar a consulta')
	return render_template('marcar_consulta.html')

@app.route("/avaliar_consulta/<int:id>", methods=['GET', 'POST'])
@login_required
def avaliar_consulta(id):
	consultaDao = ConsultaDAO()
	consulta = consultaDao.find_by_id(id)
	avaliacaoDao = AvaliacaoDAO()
	avaliacaoObj = avaliacaoDao.find_by_consulta(consulta.id)
	if request.method == 'POST':
		avaliacao = request.form['avaliacao']
		usuario = current_user()
		if avaliacaoObj is not None:
			if avaliacaoDao.update(avaliacaoObj.id, usuario.id, consulta.id, avaliacao):
				flash("Consulta avaliada com sucesso!")
				return redirect(url_for("aluno"))
			else:
				flash('Problema para avaliar a consulta')
		else:
			if avaliacaoDao.insert(usuario.id, consulta.id, avaliacao):
				flash("Consulta avaliada com sucesso!")
				return redirect(url_for("aluno"))
			else:
				flash('Problema para avaliar a consulta')
	return render_template('avaliar_consulta.html', avaliacao=avaliacaoObj)

@app.route("/_funcionarios")
@login_required
def funcionarios():
	papel_id = request.args.get('especialidade', 0, type=int)
	funcionarioDao = FuncionarioDAO()
	funcionarios = funcionarioDao.find_funcionarios(papel_id)
	return jsonify(funcionarios=funcionarios)

@app.route("/_expedientes")
@login_required
def expedientes():
	funcionario_id = request.args.get('profissional', 0, type=int)
	expedienteDao = ExpedienteDAO()
	expedientes = expedienteDao.find_all_funcionarios(funcionario_id)
	print expedientes
	return jsonify(expedientes=expedientes)

def current_user():
	usuarioDao = UsuarioDAO()
	usuario = usuarioDao.find_by_id(session['current_user'])
	return usuario

@app.route("/logout")
@login_required
def logout():
    session.pop('current_user', None)
    flash('Deslogado com sucesso!')
    return redirect(url_for('main'))

if __name__ == '__main__':
	app.run(debug=True)