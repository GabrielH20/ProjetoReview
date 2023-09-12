import matplotlib.pyplot as plt
from io import BytesIO
import base64

from review.material.models import Filme,Jogos

nomes_cores = [
    'red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink',
    'brown', 'gray', 'black', 'white',
    'aliceblue', 'aqua', 'fuchsia', 'lime', 'navy', 'teal',
    'aquamarine', 'gold', 'olive', 'thistle'
]

def analises_geral(quantidade_jogos, quantidades_filmes):
    labels = ['Jogos', 'Filmes']
    quantidades = [len(quantidade_jogos),len(quantidades_filmes)]
    cores = ['red', 'yellow']
    
    plt.figure(figsize=(2,2))

    plt.pie(quantidades, labels=labels, colors=cores, autopct='%1.1f%%', startangle=3000)

    plt.title('Estatisticas Análises')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    analises_geral_img = base64.b64encode(img_buffer.read()).decode()

    return analises_geral_img

def analises_filmes(quantidade_filmes):
    generos_filmes = []

    for valor in quantidade_filmes:
        filme = Filme.query.filter_by(id = valor.id_material).first()
        generos_filmes.append(filme.generos.nome)

    generos_list = []

    for valor in generos_filmes:
        genero_e_quantidade = (generos_filmes.count(valor),valor)
        if genero_e_quantidade not in generos_list:
            generos_list.append(genero_e_quantidade)

    labels = [valor[1] for valor in generos_list]
    quantidades = [valor[0] for valor in generos_list]
    cores = [nomes_cores[i] for i in range(len(generos_list))]
    
    plt.figure(figsize=(2,2))

    plt.pie(quantidades, labels=labels, colors=cores, autopct='%1.1f%%', startangle=3000)

    plt.title('Gêneros Analisados')
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    img_generos_filmes = base64.b64encode(img_buffer.read()).decode()

    return img_generos_filmes

def analises_jogos(quantidade_jogos):
    generos_jogos = []

    for valor in quantidade_jogos:
        jogo = Jogos.query.filter_by(id = valor.id_material).first()
        generos_jogos.append(jogo.generos.nome)

    generos_list = []

    for valor in generos_jogos:
        genero_e_quantidade = (generos_jogos.count(valor),valor)
        if genero_e_quantidade not in generos_list:
            generos_list.append(genero_e_quantidade)

    labels = [valor[1] for valor in generos_list]
    quantidades = [valor[0] for valor in generos_list]
    cores = [nomes_cores[i] for i in range(len(generos_list))]

    img_generos_jogos = info_matlib(quantidades, labels, cores)
    return img_generos_jogos

def info_matlib(quantidades, labels, cores):
    plt.figure(figsize=(2,2))

    plt.pie(quantidades, labels=labels, colors=cores, autopct='%1.1f%%', startangle=3000)

    plt.title('Gêneros Analisados')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    img = base64.b64encode(img_buffer.read()).decode()

    return img