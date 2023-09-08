from wtforms import StringField, PasswordField, validators, Form

class AdminLoginFormulario(Form):
    nome = StringField('Nome:',validators=[validators.DataRequired()])
    senha = PasswordField('Senha:',validators=[validators.DataRequired()])
    