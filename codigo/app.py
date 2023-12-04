from flask import Flask, render_template, request, jsonify
from funcoes import obtersuporte_email
from Lista import Listas

todas_listas=Listas()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/esqueceu')
def esqueceu():
    return render_template('esqueceu.html')

@app.route('/minhaslistas')
def minhaslistas():
    return render_template('minhaslistas.html')


@app.route('/criarlista', methods=['POST'])
def criarlista():
    dados = request.get_json()  
    nova_lista = {
            "nome": dados["nome"],
            "produtos": []
        }
    todas_listas.listas.append(nova_lista)
    return jsonify({"message": "Lista criada com sucesso!"})

#http://127.0.0.1:5000/lista/novalista/produto
@app.route('/lista/<string:nome_lista>/produto', methods=['POST'])
def adicionar_produto(nome_lista):  
    dados = request.get_json()
    for lista in todas_listas.listas:
        if lista["nome"] == nome_lista:
            lista["produtos"].append(dados)
            return jsonify({"message": f"Produto {dados['produto']} adicionado na lista {nome_lista}."})
    return jsonify({"error": "Lista não encontrada."}), 404


@app.route('/verlista')
def verlista():
    return render_template('verlista.html')

@app.route('/verprodutos')
def verprodutos():
    return render_template('verprodutos.html')

@app.route('/criarproduto')
def cadastrarproduto():
    return render_template('criarproduto.html')

@app.route('/verdicas')
def verdicas():
    return render_template('verdicas.html')

@app.route('/verpromocoes')
def verpromocoes():
    return render_template('verpromocoes.html')

@app.route('/obtersuporte', methods=['GET','POST'])
def obtersuporte():
    if request.method == 'POST':
        email = request.form['email']
        texto = request.form['texto']

        aviso= obtersuporte_email(email, texto) if email != '' and texto != '' else 'Preencha os campos'
        return render_template('obtersuporte.html', aviso=aviso)

    return render_template('obtersuporte.html', aviso='')

if __name__ == '__main__':
    app.run(debug=True)
