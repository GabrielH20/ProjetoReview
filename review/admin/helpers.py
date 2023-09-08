from review.material.models import Filme,Jogos,Generos,Categoria
from flask import request
from functools import cmp_to_key

def comparar_por_data_recente(item1,item2):
    data1 = item1.data_lancamento
    data2 = item2.data_lancamento
    if data1<data2:
        return 1
    elif data1>data2:
        return -1
    else:
        return 0

def comparar_por_data_antiga(item1,item2):
    data1 = item1.data_lancamento
    data2 = item2.data_lancamento
    if data1<data2:
        return -1
    elif data1>data2:
        return 1
    else:
        return 0

def filtrar_material():
    
        filtro_categoria = request.form.get('filtro_categoria')
        filtro_genero = request.form.get('filtro_genero')
        filtro_nome = request.form.get('filtro_nome') if request.form.get('filtro_nome') else ''
        data_lancamento = request.form.get('filtro_data_lancamento')

        categoria_filtrada = Categoria.query.filter_by(id = filtro_categoria).first() if filtro_categoria else Categoria.query.all()

        genero_filtrado = Generos.query.filter_by(id = filtro_genero).first() if filtro_genero else Generos.query.all()

        if type(categoria_filtrada)==list:
            filmes = Filme.query.filter(Filme.nome.like(f'%{filtro_nome}%')).all()
            jogos = Jogos.query.filter(Jogos.nome.like(f'%{filtro_nome}%')).all()
            material_filtrado = filmes + jogos

        elif categoria_filtrada.nome == 'Filmes':
            material_filtrado = Filme.query.filter(Filme.nome.like(f'%{filtro_nome}%'))
        elif categoria_filtrada.nome == 'Jogos':
            material_filtrado = Jogos.query.filter(Jogos.nome.like(f'%{filtro_nome}%'))

        if filtro_genero:
            material_filtrado = [valor for valor in material_filtrado
                                if valor.id_genero == genero_filtrado.id]
            
        if data_lancamento == 'Recentes' or data_lancamento == 'Selecionar Data':
            material_ordenado = sorted(material_filtrado, key=cmp_to_key(comparar_por_data_recente))
        else:
            material_ordenado = sorted(material_filtrado, key=cmp_to_key(comparar_por_data_antiga))
        

        nome_categoria_filtrada = f'{categoria_filtrada.nome}' if filtro_categoria else 'Todas as Categorias'
        nome_genero_filtrado = f'{genero_filtrado.nome}' if filtro_genero else 'Todos os Gêneros'

        dados_pesquisa = [ (filtro_categoria,nome_categoria_filtrada), (filtro_genero,nome_genero_filtrado), filtro_nome, data_lancamento]

        lista_ordenada = material_ordenado

        return lista_ordenada,dados_pesquisa