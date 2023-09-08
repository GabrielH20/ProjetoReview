from datetime import datetime
from review import app,db 

class Analise(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nota = db.Column(db.Integer, nullable = False)
    analise = db.Column(db.String(1500), nullable = False)

    likes = db.Column(db.Integer, default = 0)
    deslikes = db.Column(db.Integer, default = 0)

    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    categoria = db.relationship('Categoria', backref=db.backref('analises', lazy=True))

    id_autor_analise = db.Column(db.Integer, db.ForeignKey('usuario_db.id'))
    autor_analise = db.relationship('UsuarioDb', backref=db.backref('analises', lazy=True))

    id_material = db.Column(db.Integer)

    data_publi = db.Column(db.Date, default = datetime.utcnow())

with app.app_context():
    db.create_all()