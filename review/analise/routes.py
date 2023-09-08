from flask import redirect, render_template, url_for, flash, request, current_app, session
from flask_login import login_required, login_user, current_user, logout_user

from .forms import FormAnalise
from .models import Analise
from .helpers import redirecionar_material_unico, verificar_material

from review.material.models import Categoria, Filme, Jogos

#from review.usuario.models import UsuarioDb

from review import app,db,photos

@app.route('/analise/<int:id_categoria>/<int:id>', methods = ['GET','POST'])
@login_required
def analise(id_categoria,id):
    title = 'Análise'

    form = FormAnalise(request.form)

    categoria = Categoria.query.filter_by(id = id_categoria).first()

    analise = Analise.query.filter_by(
        id_categoria = id_categoria, id_material = id, id_autor_analise = current_user.id
    ).first()

    material, tipo = verificar_material(categoria, id)

    if analise and request.method != 'POST':
        flash('Você já tem uma análise publicada!','info')

        material_url = redirecionar_material_unico(analise)
        return redirect(url_for(material_url,id=id))
    
    if request.method == 'POST':
        try:
            nota = form.nota.data
            analise = form.analise.data

            analise_usuario = Analise(
                nota = nota,
                analise = analise,
                id_categoria =  categoria.id,
                id_autor_analise = current_user.id,
                id_material = id
            )

            db.session.add(analise_usuario)
            db.session.commit()

            flash('Análise publicada com sucesso','success')
        except:
            flash('Falha ao publicar a análise','danger')
            db.session.rollback()
  
        material_url = redirecionar_material_unico(analise_usuario)

        return redirect(url_for(material_url,id=id))
        
    return render_template('analise/analise.html', title = title, form = form, material = material, tipo = tipo)

@app.route('/analise/<int:id>' , methods = ['GET','POST'])
def analise_detalhar(id):
    analise = Analise.query.filter_by(id = id).first()

    title = 'Analise Detalhada'

    if not analise:
        flash('Análise não encontrda','danger')
        return redirect('home')
    
    return render_template('analise/analise_detalhada.html', analise = analise, title = title)

@app.route('/analise/excluir/<int:id>', methods = ['GET'])
@login_required
def analise_excluir(id):
    analise = Analise.query.filter_by(id = id).first()
    id_material = analise.id_material

    if analise.id_autor_analise != current_user.id:
        flash('Erro ao excluir análise!','danger')

        material = redirecionar_material_unico(analise)
        return redirect(url_for(material,id=id))

    material = redirecionar_material_unico(analise)
    
    db.session.delete(analise)
    db.session.commit()

    flash('Análise excluida com sucesso!','success')
    return redirect(url_for(material,id=id_material))

@app.route('/analise/editar/<int:id>', methods = ['GET','POST'])
@login_required
def analise_editar(id):

    analise = Analise.query.filter_by(id = id).first()
    
    categoria = Categoria.query.filter_by(id = analise.id_categoria).first()

    form = FormAnalise(request.form)

    material, tipo = verificar_material(categoria, analise.id_material)

    title = 'Editar Análise'

    if analise.id_autor_analise != current_user.id:
            flash('Erro ao editar análise!','danger')

            material = redirecionar_material_unico(analise)
            return redirect(url_for(material,id=id))
    
    if request.method == 'POST':

        nota = request.form.get('nota')
        analise_nova = request.form.get('analise')

        analise.nota = nota
        analise.analise = analise_nova
        
        db.session.commit()

        flash('Análise atualizada com sucesso!', 'success')

        material = redirecionar_material_unico(analise)
        return redirect(url_for(material,id = analise.id_material))
    
    return render_template('analise/analise_editar.html', title = title, analise = analise, material = material, tipo = tipo, form = form)

@app.route('/like/<int:id>', methods = ['GET','POST'])
@login_required
def like(id):
    like = Analise.query.filter_by(id = id).first()

    like.likes += 1

    db.session.commit()

    return redirect(url_for('home'))