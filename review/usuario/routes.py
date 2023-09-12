from flask import redirect, render_template, url_for, flash, request, current_app, session
from flask_login import login_required, login_user, current_user, logout_user
from flask_bcrypt import check_password_hash

from .forms import FormularioRegistro, FormularioLogin
from .models import UsuarioDb
from .helpers import analises_geral, analises_filmes, analises_jogos

from review.material.models import Filme,Jogos,Generos,Categoria

from review.analise.models import Analise

from review.admin.routes import load_user
from review.admin.helpers import filtrar_material,comparar_por_data_recente

from review import app,db,photos, bcrypt, login_manager

from functools import cmp_to_key
from datetime import datetime
import secrets
import os


@app.route('/', methods= ['GET','POST'])
def home():
    
    title = 'Site Review'

    filmes = Filme.query.all()
    jogos = Jogos.query.all()
            
    material_combinado = filmes + jogos

    lista_ordenada = sorted(material_combinado, key=cmp_to_key(comparar_por_data_recente))
            
    generos = Generos.query.all()
    categorias = Categoria.query.all()

    dados_pesquisa = []

    if request.method == 'POST' and not request.form.get('limpar'):

        lista_ordenada, dados_pesquisa = filtrar_material()

    return render_template('usuario/home.html',title = title, filmes= filmes, jogos = jogos,dados_pesquisa = dados_pesquisa,
                            lista_ordenada = lista_ordenada, generos = generos, categorias = categorias)

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro_usuario():
    
    title = 'Cadastro de Usuário'
    form = FormularioRegistro(request.form)

    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            usuario = request.form.get('usuario')
            email = request.form.get('email')
            data_aniversario = datetime.strptime(request.form.get('data_aniversario'),'%Y-%m-%d').date()

            senha = request.form.get('senha')
            hash_senha = bcrypt.generate_password_hash(senha)

            file_foto_perfil = request.files.get('foto_perfil')   
            foto_perfil = photos.save(file_foto_perfil, name = secrets.token_hex(10) + '.' )

            usuario_db = UsuarioDb(nome = nome, nome_usuario = usuario, email = email, 
                                    data_aniversario = data_aniversario, 
                                    senha = hash_senha,foto_perfil = foto_perfil)

            db.session.add(usuario_db)
            db.session.commit()

            flash('Sucesso ao cadastrar','success')
            return redirect(url_for('login'))
        
        except:
            db.session.rollback()
            flash('Erro ao cadastrar','danger')
            raise

    return render_template('usuario/cadastro.html', form = form, title = title)


@app.route('/login', methods = ['GET','POST'])
def login():
    forms = FormularioLogin(request.form)

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = UsuarioDb.query.filter_by(email = email).first()

        if not usuario:
            
            flash('Erro email, email ou senha inválidos!','danger')
            return redirect(url_for('login'))
    
        if not check_password_hash(usuario.senha, senha):
            flash('Erro senha, email ou senha inválidos!','danger')
            return redirect(url_for('login'))

        login_user(usuario)
        return redirect(url_for('home'))
    
    return render_template('usuario/login.html', forms = forms)

@app.route('/lista/usuarios',methods = ['GET'])
@login_required
def lista_usuarios():
    title = 'Lista Usuários'
    usuarios = UsuarioDb.query.all()
    
    return render_template('usuario/usuarios_lista.html', title = title, usuarios = usuarios)

@app.route('/conta/<int:id>', methods = ['GET','POST'])
def conta(id):
    usuario = UsuarioDb.query.filter_by(id = id).first()

    analises = Analise.query.filter_by(
        id_autor_analise =usuario.id
    ).all()

    quantidade_analises = len(analises)

    if not usuario:
        flash('Usuário não encontrado!','danger')
        return redirect(url_for('home'))
    
    return render_template('usuario/conta.html', usuario = usuario, analises = analises, quantidade_analises = quantidade_analises)


@app.route('/conta/atualizar', methods = ['GET','POST'])
@login_required
def conta_atualizar():

    usuario_atualizar = UsuarioDb.query.get(current_user.id)
    
    if request.method == 'POST': 
        try:
            usuario_atualizar.nome = request.form.get('nome')
            usuario_atualizar.nome_usuario = request.form.get('nome_usuario')
            usuario_atualizar.email = request.form.get('email')
            usuario_atualizar.data_aniversario = datetime.strptime(request.form.get('data_aniversario'),'%Y-%m-%d').date()

            nova_foto_perfil = request.files.get('foto_perfil')
            if nova_foto_perfil:
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/images/' + current_user.foto_perfil))
                except FileNotFoundError:
                    pass  
                usuario_atualizar.foto_perfil = photos.save(nova_foto_perfil, name=secrets.token_hex(10) + '.')

            db.session.commit()
            flash(f'{usuario_atualizar.nome} foi atualizado com sucesso!','success')

        except:
            db.session.rollback()

            nome_usuario = request.form.get('nome_usuario')
            email = request.form.get('email')

            if UsuarioDb.query.filter_by(nome_usuario = nome_usuario ) and current_user.nome_usuario!=nome_usuario and nome_usuario:
                flash(f'{request.form.get("nome_usuario")} já está em uso!, tente outro!','danger')

            elif UsuarioDb.query.filter_by(email = email) and current_user.email!=email:
                flash(f'{request.form.get("email")}  já está em uso!, tente outro!','danger')

            else:
                raise

            return redirect(url_for('conta_atualizar'))

        return redirect(url_for('conta'))
    
    return render_template('usuario/usuario_atualizar.html')

@app.route('/conta/excluir', methods = ['GET','POST'])
def conta_excluir():
    try:
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + current_user.foto_perfil))
    except FileNotFoundError:
        pass  
    
    usuario = UsuarioDb.query.get(current_user.id)
    db.session.delete(usuario)
    db.session.commit()
    
    flash('A conta foi deletada com Sucesso','success')
    return redirect(url_for('login'))

@app.route('/conta/<int:id>/graficos', methods = ['GET','POST'])
def conta_graficos(id):
    title = "Gráficos da Conta"

    analises = Analise.query.filter_by(id_autor_analise = id).all()

    usuario = UsuarioDb.query.filter_by(id = id).first()

    if len(analises) != 0:
        nota_geral = round(sum([analise.nota for analise in analises])/len(analises))
    else:
        nota_geral = 0

    categoria_filme = Categoria.query.filter_by(nome = 'Filmes').first()
    categoria_jogos = Categoria.query.filter_by(nome = 'Jogos').first()

    filmes = Analise.query.filter_by(id_autor_analise = id, id_categoria = categoria_filme.id).all()

    if len(filmes) != 0:
        nota_filmes = round(sum([analise.nota for analise in filmes])/len(filmes))
    else:
        nota_filmes = 0
    
    jogos = Analise.query.filter_by(id_autor_analise = id, id_categoria = categoria_jogos.id).all()

    if len(jogos) != 0:
        nota_jogos = round(sum([analise.nota for analise in jogos])/ len(jogos))
    else:
        nota_jogos = 0

    analises_geral_img = analises_geral(jogos, filmes)

    img_generos_filmes = analises_filmes(filmes)

    img_generos_jogos = analises_jogos(jogos)

    return render_template('usuario/graficos.html', title = title, analises_geral_img = analises_geral_img, img_generos_filmes = img_generos_filmes, img_generos_jogos = img_generos_jogos,
                           quantidade_jogos = len(jogos), quantidade_filmes = len(filmes), quantidade_analises = len(analises),
                           nota_geral = nota_geral, nota_filmes = nota_filmes, nota_jogos = nota_jogos, usuario = usuario)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.unauthorized_handler
def unauthorized():
    flash('Você precisa estar logado para acessar esta página.', 'info')
    return redirect(url_for('login'))

