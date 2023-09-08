from review.material.models import Jogos, Filme

def redirecionar_material_unico(analise):
    if analise.categoria.nome == 'Filmes':
        return 'filme_unico'
    elif analise.categoria.nome == 'Jogos':
        return 'jogo_unico'


def verificar_material(categoria, id):
    if categoria.nome == 'Filmes':
        material = Filme.query.filter_by(id = id).first()
        tipo = 'Filme'
    elif categoria.nome == 'Jogos':
        tipo = 'Jogo'
        material = Jogos.query.filter_by(id = id).first()

    return material,tipo 