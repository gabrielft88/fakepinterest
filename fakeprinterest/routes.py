# criar as rotas do site (links)
from flask import render_template, url_for, redirect
from fakeprinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakeprinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakeprinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


# url_for -> permite pegar a URL de acordo com o nome da função
# render_template -> permite passar variáveis Python para o arquivo HTML pela pasta templates

@app.route("/", methods=['POST', 'GET'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/criarconta", methods=['POST', 'GET'])
def criarconta():
    formcrianconta = FormCriarConta()
    if formcrianconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcrianconta.senha.data)
        usuario = Usuario(username=formcrianconta.username.data,
                          email=formcrianconta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("criarconta.html", form = formcrianconta)

@app.route("/perfil/<id_usuario>", methods=['POST', 'GET'])  # o usuário é uma variável e é passado para função
@login_required
def perfil(id_usuario):
    if int(id_usuario)  == int(current_user.id):
        #o usuario está vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():  # se validou todas as informações do formulário
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo na foto pasta fotos_post
            caminho = os.path.  join(os.path.abspath(os.path.dirname(__file__)),
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # registrar esse arquivo no banco de dados
            foto = Foto(imagem = nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form = form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form = None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)