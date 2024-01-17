# criar a estrutura do banco de dados
from fakeprinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  # retorno um usuario expecífico

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable = False, unique = True)
    senha = database.Column(database.String, nullable = False)
    fotos = database.relationship("Foto", backref="usuario", lazy=True) #fazer busca no bd de maneira eficiente com um ponteiro

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    imagem = database.Column(database.String, default = "default.png") # é string pq a informação armazenada no bd é o local onde a imagem está dentro do sistema (pasta static)
    data_criacao = database.Column(database.DateTime, nullable = False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)