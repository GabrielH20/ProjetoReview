from review import app, db
from datetime import datetime
from flask_login import UserMixin

class UsuarioDb(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)

    nome = db.Column(db.String(80), unique = False, nullable=False)

    nome_usuario = db.Column(db.String(80),unique = True, nullable = False)

    email = db.Column(db.String(80),unique = True, nullable=False)

    data_aniversario = db.Column(db.Date, nullable=False)

    senha = db.Column(db.String(80), unique= False, nullable=False)

    foto_perfil = db.Column(db.String(200),unique=False,nullable=False)

    data_cadastro = db.Column(db.Date,default=datetime.utcnow())
    
with app.app_context():

    db.create_all()