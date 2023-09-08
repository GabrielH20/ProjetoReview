from wtforms import  validators, Form, TextAreaField, IntegerField

class FormAnalise(Form):
    nota = IntegerField('Nota', validators=[validators.DataRequired(),validators.NumberRange(min=0,max=100)])
    analise = TextAreaField('Analise', validators =[validators.DataRequired(),validators.Length(min=0,max=2500)])
