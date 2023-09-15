from flask import redirect, request, flash, render_template, session, url_for, current_app
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError

from review import app,db, login_manager,photos

from review.material.forms import FormCategoria, FormGeneros, FormFilme, FormJogos, FormFiltro
from review.material.models import Categoria, Generos, Filme, Jogos

from review.analise.models import Analise, Comentario, ComentarioFilho

from datetime import datetime
import secrets
import os

@app.route('/jogo/<int:id>', methods = ['GET'])
def jogo_unico(id):
    jogo = Jogos.query.filter_by(id = id).first()

    title = f'Jogo {jogo.nome}'

    categoria = Categoria.query.filter_by(nome = 'Jogos').first()

    analises = Analise.query.filter_by(
        id_categoria = categoria.id, id_material = id
    ).all()

    quantidade_analises = len(analises)
    if quantidade_analises:
        nota_total = sum([analise.nota for analise in analises])/ quantidade_analises
    else:
        nota_total = 0
        
    return render_template('material/jogo_unico.html', jogo = jogo, title = title, analises = analises, quantidade_analises = quantidade_analises, nota_total = nota_total)

@app.route('/admin/jogos', methods = ['GET','POST'])
@login_required
def jogos():
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Jogos'

    jogos = Jogos.query.all()

    return render_template('material/jogos.html', title = title, jogos = jogos)

@app.route('/admin/jogos/criar', methods = ['GET','POST'])
@login_required
def jogos_criar():
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Jogos Cadastrar'

    form = FormJogos(request.form)

    categoria = Categoria.query.filter_by(nome='Jogos').first()

    generos = Generos.query.filter_by(id_categoria = categoria.id).all()

    if request.method == 'POST':
        try:
            nome = form.nome.data
            desenvolvedora = form.desenvolvedora.data
            descricao = form.descricao.data
            tempo_de_jogo = form.tempo_de_jogo.data
            data_lancamento_str = request.form.get('data_lancamento')
            data_lancamento = datetime.strptime(data_lancamento_str, '%Y-%m-%d').date()

            genero = request.form.get('genero')
            file_poster = request.files.get('poster')

            poster = photos.save(file_poster, name = secrets.token_hex(10) + '.')

            jogo = Jogos(nome = nome, desenvolvedora = desenvolvedora, 
                         descricao = descricao,data_lancamento = data_lancamento, 
                         tempo_de_jogo = tempo_de_jogo,
                        id_genero = genero,
                        id_categoria = categoria.id, foto_poster= poster)
            
            db.session.add(jogo)
            db.session.commit()

            flash(f'O jogo {nome} foi cadastrado com sucesso!','success')
        except:
            flash(f'Houve um erro ao cadastrar o jogo {nome}','danger')
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + poster))
            except:
                pass
                
            db.session.rollback()

        return redirect(url_for('jogos'))
    return render_template('material/jogos_criar.html', title = title, form = form, generos = generos)

@app.route('/admin/jogos/atualizar/<int:id>', methods = ['GET','POST'])
@login_required
def jogos_atualizar(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Atualizar Jogo'

    jogo = Jogos.query.filter_by(id = id).first()
    
    categoria = Categoria.query.filter_by(nome = 'Jogos').first()

    generos = Generos.query.filter_by(id_categoria = categoria.id)

    if request.method == 'POST':
        try:
            jogo.nome = request.form.get('nome')
            jogo.descricao = request.form.get('descricao')
            jogo.desenvolvedora = request.form.get('desenvolvedora')
            jogo.tempo_de_jogo = request.form.get("tempo_de_jogo")
            jogo.duracao = request.form.get('tempo_de_jogo')

            data_lancamento_str = request.form.get('data_lancamento')    
            jogo.data_lancamento = datetime.strptime(data_lancamento_str, '%Y-%m-%d').date()

            genero = Generos.query.filter_by(id = int(request.form.get('genero'))).first()
            jogo.generos = genero

            foto_poster = request.files.get('foto_poster')
            if foto_poster:
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/images/' + jogo.foto_poster))
                except FileNotFoundError:
                    pass  

                jogo.foto_poster = photos.save(foto_poster, name=secrets.token_hex(10) + '.')
            
            flash(f'Jogo {jogo.nome} Atualizado com sucesso','success')
            db.session.commit()
            return redirect(url_for('jogos'))
        except:
            db.session.rollback()
            flash(f'Jogo {jogo.nome} houve erro em atualizar!','danger')

    return render_template('material/jogos_atualizar.html', generos = generos, jogo = jogo, title = title)

@app.route('/admin/jogos/excluir/<int:id>', methods = ['GET'])
@login_required
def jogos_excluir(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    jogo_excluir = Jogos.query.filter_by(id = id).first()

    analises = Analise.query.filter_by(id_material = id).all()

    for analise in analises:
        comentarios = Comentario.query.filter_by(id_analise_comentada = analise.id)

        for comentario in comentarios:

            comentarios_filhos = ComentarioFilho.query.filter_by(id_comentario_pai = comentario.id).all()

            for comentario_filho in comentarios_filhos:
                db.session.delete(comentario_filho)

            db.session.delete(comentario)

        db.session.delete(analise)

    db.session.delete(jogo_excluir)
    db.session.commit()

    flash('Jogo foi excluido com sucesso','success')

    return redirect(url_for('admin_home'))

@app.route('/admin/filmes', methods = ['GET','POST'])
@login_required
def filmes():
    title = 'Filmes'
    filmes = Filme.query.all()
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    return render_template('material/filmes.html', filmes = filmes, title = title)

@app.route('/filme/<int:id>', methods = ['GET'])
@login_required
def filme_unico(id):

    filme = Filme.query.filter_by(id = id).first()
    title = f'Filme {filme.nome}'

    categoria = Categoria.query.filter_by(nome = 'Filmes').first()
     
    analises = Analise.query.filter_by(
        id_categoria = categoria.id, id_material = id
    ).all()

    quantidade_analises = len(analises)

    if quantidade_analises:
        nota_total = sum([analise.nota for analise in analises])/ quantidade_analises
    else:
        nota_total = 0

    return render_template('material/filme_unico.html', filme = filme, title = title, analises = analises, quantidade_analises = quantidade_analises, nota_total = nota_total)

@app.route('/admin/filmes/criar',methods = ['GET','POST'])
@login_required
def filme_criar():
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    form = FormFilme(request.form)
    title = 'Filme Criar'

    categoria = Categoria.query.filter_by(nome = 'Filmes').first()

    generos = Generos.query.filter_by(id_categoria = categoria.id)

    if request.method == 'POST':
        try:
            nome = form.nome.data
            diretor = form.diretor.data
            sinopse = form.sinopse.data
            duracao = form.duracao.data

            data_lancamento_str = request.form.get('data_lancamento')
            data_lancamento = datetime.strptime(data_lancamento_str, '%Y-%m-%d').date()

            genero = request.form.get('genero')
            file_foto_poster = request.files.get('poster')
        
            foto_poster = photos.save(file_foto_poster, name = secrets.token_hex(10) + '.')

            filme = Filme(nome = nome, diretor = diretor, sinopse = sinopse,
                        id_genero = genero, id_categoria = categoria.id,
                        data_lancamento = data_lancamento, duracao = duracao, foto_poster = foto_poster)
            
            db.session.add(filme)
            db.session.commit()
            flash('Filme Adicionado com sucesso','success')
            return redirect(url_for('filmes'))
        except:
            flash('Falha em adicionar filme!','danger')
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + foto_poster))
            except:
                pass
            db.session.rollback()
    
    return render_template('material/filme_criar.html',form = form, title = title, generos = generos)

@app.route('/admin/filme/atualizar/<int:id>', methods = ['GET','POST'])
@login_required
def filme_atualizar(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    filme = Filme.query.filter_by( id = id).first()
    title = 'Filme Atualizar'


    categoria = Categoria.query.filter_by(nome = 'Filmes').first()

    generos = Generos.query.filter_by(id_categoria = categoria.id).all()

    if request.method == 'POST':

        try:
            filme.nome = request.form.get('nome')
            filme.sinopse = request.form.get('sinopse')
            filme.diretor = request.form.get('diretor')
            filme.duracao = request.form.get('duracao')

            data_lancamento_str = request.form.get('data_lancamento')    
            filme.data_lancamento = datetime.strptime(data_lancamento_str, '%Y-%m-%d').date()

            genero = Generos.query.filter_by(id = int(request.form.get('genero'))).first()
            filme.generos = genero

            foto_poster = request.files.get('foto_poster')
            if foto_poster:
                try:
                    os.unlink(os.path.join(current_app.root_path, 'static/images/' + filme.foto_poster))
                except FileNotFoundError:
                    pass  

                filme.foto_poster = photos.save(foto_poster, name=secrets.token_hex(10) + '.')
            
            flash(f'Filme {filme.nome} Atualizado com sucesso','success')
            db.session.commit()
        except:
            db.session.rollback()
            flash(f'Filme {filme.nome} houve erro em atualizar!','danger')


        return redirect(url_for('filmes'))
    
    return render_template('material/filme_atualizar.html', filme = filme, title = title, generos = generos )

@app.route('/admin/filme/excluir/<int:id>', methods = ['GET'])
@login_required
def filme_excluir(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    filme_excluir = Filme.query.filter_by(id = id).first()
    try:
        os.unlink(os.path.join(current_app.root_path, 'static/images/' + filme_excluir.foto_poster))
    except:
        pass
    
    analises = Analise.query.filter_by(id_material = id).all()

    for analise in analises:
        comentarios = Comentario.query.filter_by(id_analise_comentada = analise.id)

        for comentario in comentarios:

            comentarios_filhos = ComentarioFilho.query.filter_by(id_comentario_pai = comentario.id).all()

            for comentario_filho in comentarios_filhos:
                db.session.delete(comentario_filho)

            db.session.delete(comentario)

        db.session.delete(analise)

    db.session.delete(filme_excluir)
    db.session.commit()

    flash('Filme excluido com sucesso!','success')

    return redirect(url_for('admin_home'))

@app.route('/admin/generos/filme',methods = ['GET','POST'])
@login_required
def generos():
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Genero Filme'
    form = FormGeneros(request.form)
    categorias = Categoria.query.all()
    generos_filme = Generos.query.all()

    generos_filtrados = None
    categoria_especifica = None
    filtro = None
    categoria = None

    if request.method == 'POST' and request.form.get('filtro_nome'):
        filtro = request.form.get('filtro_nome')

        if request.form.get('filtro_categoria'):

            categoria = Categoria.query.filter_by(id = request.form.get('filtro_categoria')).first()

            generos_filtrados = Generos.query.filter(
                (Generos.id_categoria == categoria.id) & (Generos.nome.like(f'%{filtro}%'))
            ).all()
            categoria_especifica = f'Categoria {categoria.nome}'

        else:
            
            categoria = Categoria.query.all()
            generos_filtrados = Generos.query.filter(Generos.nome.like(f'%{filtro}%')).all()
            categoria_especifica = 'Todas as Categorias'

    if request.method == 'POST' and form.nome.data:

        nome = form.nome.data
        categoria = request.form.get('categoria')
        try:
            genero = Generos(nome = nome, id_categoria = categoria)
            db.session.add(genero)
            db.session.commit()
            flash(f'Gênero {genero.nome} adicionado com sucesso!','success')
        except:
            flash(f'Gênero de filme {nome} já existente','danger')
            db.session.rollback()

        return redirect(url_for('generos'))
    
    return render_template('material/generos.html', form = form,generos_filtrados = generos_filtrados, categoria_especifica = categoria_especifica,
                            generos_filme = generos_filme, title = title, categorias = categorias, filtro = filtro, categoria = categoria)

@app.route('/admin/genero/atualizar/<int:id>', methods = ['GET','POST'])
@login_required
def generos_atualizar(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Atualizar Gênero Filme'

    genero_filme = Generos.query.filter_by(id = id).first()

    if request.method == 'POST':
        nome = request.form.get('nome')
        try:
            genero_filme.nome = nome
            db.session.commit()
            flash('O Gênero foi atualizado com sucesso','success')
        except:
            db.session.rollback()
            flash('Falha ao atualizar gênero, já existe!','danger')

        return redirect(url_for('generos'))
    
    return render_template("material/generos_atualizar.html", genero_filme = genero_filme, title = title)

@app.route('/admin/genero/excluir/<int:id>', methods = ['GET'])
@login_required
def generos_excluir(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    genero_filme = Generos.query.filter_by(id = id).first()

    db.session.delete(genero_filme)
    db.session.commit()

    flash('Gênero Deletado com sucesso!','success')

    return redirect(url_for('generos'))

@app.route('/admin/categorias', methods = ['GET','POST'])
@login_required
def categorias():
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))

    title = 'Criar Categoria'
    form = FormCategoria(request.form)
    form_filtro = FormFiltro(request.form)

    categorias_existentes = Categoria.query.all()
    categorias_filtradas = []
    filtro = request.form.get('filtro')


    if request.method == 'POST' and filtro:
        categorias_filtradas = Categoria.query.filter(Categoria.nome.like(f'%{filtro}%')).all()

    if request.method == 'POST' and form.nome.data:
        nome = form.nome.data
        descricao = form.descricao.data

        db_categoria = Categoria(nome = nome, descricao = descricao)

        db.session.add(db_categoria)

        db.session.commit()

        flash('A categoria foi criada com sucesso!','success')
        
        return redirect(url_for('categorias'))
    
    return render_template('material/categoria.html',title = title, form = form, form_filtro = form_filtro,
                           categorias_existentes = categorias_existentes,categorias_filtradas = categorias_filtradas, filtro = filtro )

@app.route('/admin/categorias/atualizar/<int:id>',methods=['GET','POST'])
@login_required
def categoria_atualizar(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    categoria = Categoria.query.filter_by(id = id).first()

    if request.method == 'POST':
        try:
            categoria.nome = request.form.get('nome')
            categoria.descricao = request.form.get('descricao')

            db.session.commit()

            flash('A categoria foi atualizada com sucesso!','success')
            
        except IntegrityError:
            db.session.rollback()
            flash('Categoria já existente!','danger')
        return redirect(url_for('categorias'))
    return render_template('material/categoria_atualizar.html', categoria = categoria)

@app.route('/admin/categorias/excluir/<int:id>', methods = ['GET','POST'])
@login_required
def categoria_excluir(id):
    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    categoria_excluir = Categoria.query.filter_by(id = id).first()

    db.session.delete(categoria_excluir)
    db.session.commit()

    flash("A categoria foi excluida com sucesso!",'success')

    return redirect(url_for('categorias'))

def verificar_permissao_admin():
    try:
        if current_user.role == 'admin':
            return True
    except:
        flash('Você não tem permissão de admin','danger')
        return False