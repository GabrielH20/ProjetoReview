from datetime import datetime
from review import app,db
from flask_login import UserMixin

class Admin(db.Model,UserMixin):
    id =  db.Column( db.Integer, primary_key = True)
    nome = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(50))
    role = db.Column(db.String(50),default='admin')
    data_create = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"<AdminDb {self.nome}>"
with app.app_context():
    db.create_all()