from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, PasswordField, DateField, validators, Form

class FormularioRegistro(Form):
    nome = StringField('Nome', validators=[validators.DataRequired(), validators.Length(min=3,max=40)])

    usuario = StringField('Nome Usuário',validators=[validators.DataRequired(),validators.Length(min=3,max=40)])

    email = StringField('Email',validators=[validators.DataRequired(), validators.Email(), validators.Length(min=3,max=35)])

    data_aniversario = DateField('Data de Nascimento', validators=[validators.DataRequired()], format='%d%m%Y')

    senha = PasswordField('Senha',
    validators=[validators.DataRequired(),
     validators.EqualTo('confirmar_senha')])
    
    confirmar_senha = PasswordField('Confirmar Senha')

    foto_perfil = FileField('Foto Perfil', validators = [FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], message='Somente Foto')])

class FormularioLogin(Form):
    email = StringField('Email', validators = [ validators.DataRequired(), validators.Length(min=3,max=35)])

    senha = PasswordField('Senha', validators= [ validators.DataRequired()])