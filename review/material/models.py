from datetime import datetime
from review import app,db 

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True)
    descricao = db.Column(db.String(1500))

class Generos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('Generos', lazy=True))
 
class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150), unique = True)
    desenvolvedora = db.Column(db.String(200))
    descricao = db.Column(db.String(1000))
    data_lancamento = db.Column(db.Date)
    tempo_de_jogo = db.Column(db.Float)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('jogos', lazy=True))

    id_genero = db.Column(db.Integer, db.ForeignKey('generos.id'))
    generos = db.relationship('Generos', backref=db.backref('jogos', lazy=True))  

    foto_poster = db.Column(db.String(255), default='image.jpg')
    
    data_publicacao = db.Column(db.Date, default=datetime.utcnow())

class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True)
    diretor = db.Column(db.String(150))
    sinopse = db.Column(db.String(1000))
    data_lancamento = db.Column(db.Date)
    duracao = db.Column(db.Integer)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('filmes', lazy=True))

    id_genero = db.Column(db.Integer, db.ForeignKey('generos.id'))
    generos = db.relationship('Generos', backref=db.backref('filmes', lazy=True))  
    
    foto_poster = db.Column(db.String(255), default='image.jpg')
    
    data_publicacao = db.Column(db.Date, default=datetime.utcnow())

with app.app_context():
    db.create_all()