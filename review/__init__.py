from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, patch_request_class, IMAGES
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

base_diretorio = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projetoreviews.db'
app.config['SECRET_KEY'] = 'projetoreview12345'

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(base_diretorio, 'static/images')
photos = UploadSet('photos',IMAGES)

configure_uploads(app, photos)
patch_request_class(app)

from review.usuario import routes
from review.admin import routes
from review.material import routes
from review.analise import routes