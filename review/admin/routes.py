from flask import redirect, request, flash, render_template, session, url_for
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy.sql.expression import union_all

from review import app,db, login_manager

from review.usuario.models import UsuarioDb

from review.material.routes import verificar_permissao_admin
from review.material.forms import FormCategoria
from review.material.models import Categoria, Filme, Jogos, Generos

from .helpers import comparar_por_data_recente,comparar_por_data_antiga, filtrar_material
from .models import Admin
from .forms import AdminLoginFormulario

from functools import cmp_to_key

# @app.route('/admin/criar',methods = ['GET','POST'])
# def admin_criar():
#     admin_add = Admin(nome = 'gabriel',senha = '123')
#     db.session.add(admin_add)
#     db.session.commit()
#     return 'admin criado com sucesso'


@app.route('/admin/home', methods=['GET','POST'])
@login_required
def admin_home():

    if verificar_permissao_admin()==False:
        return redirect(url_for('home'))
    
    title = 'Admin Home'

    filmes = Filme.query.all()
    jogos = Jogos.query.all()
            
    material_combinado = filmes + jogos

    lista_ordenada = sorted(material_combinado, key=cmp_to_key(comparar_por_data_recente))
            
    generos = Generos.query.all()
    categorias = Categoria.query.all()

    dados_pesquisa = []

    if request.method == 'POST' and not request.form.get('limpar'):

        lista_ordenada, dados_pesquisa = filtrar_material()

    return render_template('admin/home.html',title = title, filmes= filmes, jogos = jogos,dados_pesquisa = dados_pesquisa,
                            lista_ordenada = lista_ordenada, generos = generos, categorias = categorias)


@app.route('/admin/login', methods = ['GET','POST'])
def admin_login():
    title = 'Admin Login'
    forms = AdminLoginFormulario(request.form)
    
    if request.method == 'POST':
        nome = forms.nome.data
        senha = forms.senha.data

        admin = Admin.query.filter_by(nome = nome).first()  
    
        if admin and senha == admin.senha:

            login_user(admin)

            return redirect(url_for('admin_home'))
         
    return render_template('admin/login.html', forms = forms, title = title)

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    else:
        return UsuarioDb.query.get(int(user_id))
    

    

