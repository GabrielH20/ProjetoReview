from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, validators, Form, TextAreaField, FloatField, DateField, IntegerField

class FormCategoria(Form):
    nome = StringField('Nome Categoria', validators = [validators.DataRequired(),validators.Length(min = 3, max=150)])
    descricao = TextAreaField('Descrição Categoria',validators = [validators.DataRequired(),validators.Length(min = 3, max=1500)])

class FormGeneros(Form):
    nome = StringField('Nome do Gênero do Fime', validators = [validators.DataRequired(),validators.Length(min = 3, max=150)])

class FormFiltro(Form):
    nome_filtro = StringField('Pesquisa Filtro')

class FormFilme(Form):
    nome = StringField('Nome')
    diretor = StringField('Diretor')
    sinopse = TextAreaField('Sinopse')
    data_lancamento = DateField('Data de Lançamento', validators=[validators.DataRequired()], format='%d%m%Y')
    duracao = IntegerField('Duração do Filme')
    foto_poster = FileField('Poster Filme', validators = [FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], message='Somente Foto')])
 
class FormJogos(Form):
    nome = StringField('Nome')
    desenvolvedora = StringField('Desenvolvedora')
    descricao = TextAreaField('Sinopse')
    data_lancamento = DateField('Data de Lançamento', validators=[validators.DataRequired()], format='%d%m%Y')
    tempo_de_jogo = IntegerField('Tempo de jogo')
    foto_poster = FileField('Poster do Jogo', validators = [FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], message='Somente Foto')])
 
class LivroForm(Form):
    nome = StringField('Nome')
    autor = StringField('Diretor')
    sinopse = TextAreaField('Sinopse')
    data_lancamento = DateField('Data de Lançamento', validators=[validators.DataRequired()], format='%d%m%Y')
    quantidade_paginas = StringField('Quantidade de Páginas')
    foto_capa = FileField('Capa do Livro', validators = [FileRequired(), FileAllowed(['jpg','png','gif','jpeg'], message='Somente Foto')])


