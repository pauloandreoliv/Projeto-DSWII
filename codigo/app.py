from flask import Flask, render_template, request
from funcoes import obtersuporte_email

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

@app.route('/criarlista')
def criarlista():
    return render_template('criarlista.html')

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
