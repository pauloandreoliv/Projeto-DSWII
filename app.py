from flask import Flask, session, render_template, request
from funcoes import obtersuporte_email, recuperarsenha_email
import requests
import json
import logging

logging.basicConfig(filename='logs/debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'aplicacaoWeb2023.2'

url_api = "https://api-dswii.onrender.com"

#Renderização das páginas HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/principal')
def principal():
    if session.get('logado') != None:
        return render_template('principal.html')
    else:
        return render_template('erro.html')

@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/esqueceu')
def esqueceu():
    return render_template('esqueceu.html')

@app.route('/criarproduto')
def criarproduto():
    if session.get('logado') != None:
        return render_template('criarproduto.html')
    else:
        return render_template('erro.html')

#GET
@app.route('/minhaslistas')
def minhaslistas():
    if session.get('logado') != None:
        id_creator = session.get('logado')['id']
        data = {"id_creator": id_creator}
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/listas_por_creator", json=data, headers=headers)
        if return_request.status_code == 200:
            itens = json.loads(return_request.text)
            return render_template("minhaslistas.html", itens=itens['listas'])
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/minhaslistas'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

@app.route('/criarlista')
def criarlista():
    if session.get('logado') != None:
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/produto", headers=headers)
        if return_request.status_code == 200:
            itens = json.loads(return_request.text)
            total = len(itens)
            return render_template("criarlista.html", itens=itens, total=total)
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/criarlista'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

@app.route('/verlista', methods=['GET'])
def verlista():
    if session.get('logado') != None:
        id = request.args.get('id')
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/lista", json={"id": id}, headers=headers)
        if return_request.status_code == 200:
            lista = json.loads(return_request.text)
            itens_lista = eval(lista['lista']['itens'])
            return render_template('verlista.html', lista=lista['lista'], itens_lista=itens_lista)
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/verlista'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

@app.route('/verprodutos')
def verprodutos():
    if session.get('logado') != None:
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/produto", headers=headers)
        if return_request.status_code == 200:
            itens = json.loads(return_request.text)
            return render_template("verprodutos.html", itens=itens)
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/verprodutos'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

@app.route('/verpromocoes')
def verpromocoes():
    if session.get('logado') != None:
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/promocoes", headers=headers)
        if return_request.status_code == 200:
            itens = json.loads(return_request.text)
            return render_template("verpromocoes.html", itens=itens)
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/verpromocoes'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

@app.route('/verdicas')
def verdicas():
    if session.get('logado') != None:
        headers = {"Authorization": session.get('logado')['token']}
        return_request = requests.get(f"{url_api}/dicas", headers=headers)
        if return_request.status_code == 200:
            itens = json.loads(return_request.text)
            return render_template("verdicas.html", itens=itens)
        else:
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/verdicas'>Tentar novamente</a> <br> <a href='/'>Fazer login</a>"
    else:
        return render_template('erro.html')

#POST
@app.route('/obtersuporte', methods=['GET','POST'])
def obtersuporte():
    if request.method == 'POST':
        email = request.form['email']
        texto = request.form['texto']

        aviso= obtersuporte_email(email, texto) if email != '' and texto != '' else 'Preencha os campos'
        return render_template('obtersuporte.html', aviso=aviso)

    return render_template('obtersuporte.html', aviso='')

@app.route('/login', methods=['POST'])
def login():
    session.pop('logado', None)
    data = {
        "id" : str(request.form["cpf"]),
        "senha" : str(request.form["senha"])
    }
    return_request = requests.get(f"{url_api}/login", json=data)
    if return_request.status_code == 200:
        id = return_request.json()
        session['logado'] = id
        logging.info(f'Sessão de usuário {id} iniciada')
        return 'Login realizado com sucesso. <a href="/principal">Página Inicial</a>'
    else:
        logging.info(f'Sessão de usuário não permitida')
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/'>Tentar novamente</a>"

@app.route('/cadastrarusuario', methods=["POST"])
def cadastrarusuario():
    data = {
        "id" : str(request.form["cpf"]),
        "senha" : str(request.form["senha"])
    }
    return_request = requests.post(f"{url_api}/user", json=data)

    if return_request.status_code == 200:
        logging.info(f'Cadastro realizado com sucesso: {id}')
        return 'Cadastro realizado com sucesso. <a href="/">Página Inicial</a>'
    else:
        logging.info(f'Não foi possível cadastrar id: {id} -> {return_request.text}')
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/cadastrar'>Tentar novamente</a>"
        
@app.route('/cadastrarproduto', methods=["POST"])
def cadastrarproduto():
    data = {
        "nome" : str(request.form["nomedoproduto"]),
        "preco" : str(request.form["precodoproduto"])
    }
    headers = {"Authorization": session.get('logado')['token']}
    return_request = requests.post(f"{url_api}/produto", json=data, headers=headers)

    if return_request.status_code == 200:
        logging.info(f'Cadastro realizado com sucesso: {id}')
        return 'Cadastro realizado com sucesso. <a href="/principal">Página Inicial</a>'
    else:
        logging.info(f'Não foi possível cadastrar id: {id} -> {return_request.text}')
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/criarproduto'>Tentar novamente</a>"
        
@app.route('/cadastrarlista', methods=["POST"])
def cadastrarlista():
    id_creator = session.get('logado')['id']
    total = int(request.form['total'])
    nome_lista = request.form['nomedalista']
    lista = []
    for k in range(1, total + 1):
        nome = request.form.get(f'nome{k}')
        qtd = request.form.get(f'qtd{k}')
        preco = request.form.get(f'preco{k}')

        if nome != None and preco != None and qtd != None and qtd != '':
            if int(qtd) > 0:
                lista.append([nome,qtd,preco])
        else:
            logging.info(f"Campo {nome} não encontrado nos dados do formulário.")
    data = {
        "nome" : nome_lista,
        "itens" : str(lista),
        "id_creator": id_creator
    }

    headers = {"Authorization": session.get('logado')['token']}
    return_request = requests.post(f"{url_api}/lista", json=data, headers=headers)
    if return_request.status_code == 200:
        logging.info(f'Cadastro de lista realizado com sucesso')
        return 'Cadastro realizado com sucesso. <a href="/principal">Página Inicial</a>'
    else:
        logging.info(f'Não foi possível cadastrar lista -> {return_request.text}')
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/criarlista'>Tentar novamente</a>"
        
@app.route('/deletarlista', methods=["POST"])
def deletarlista():
    id_lista = request.form['id_lista']
    data = {
        "id" : id_lista
    }
    headers = {"Authorization": session.get('logado')['token']}
    return_request = requests.delete(f"{url_api}/lista", json=data, headers=headers)

    if return_request.status_code == 200:
        logging.info(f'Lista apagada com sucesso: {id_lista}')
        return 'Lista apagada com sucesso. <a href="/minhaslistas">Página Inicial</a>'
    else:
        logging.info(f'Não foi possível remover lista: {id_lista} -> {return_request.text}')
        return f"{return_request.status_code} : {return_request.text}  <br> <a href='/minhaslistas'>Tentar novamente</a>"

@app.route('/recuperarsenha', methods=["POST"])
def recuperarsenha():
    id = request.form['cpf']
    email = request.form['email']
    if id != '' and email != '' and id != None and email != None:
        data = {
            "id" : id
        }
        return_request = requests.put(f"{url_api}/user", json=data)
        if return_request.status_code == 200:
            json_return = json.loads(return_request.text)
            senha = json_return['senha']
            logging.info(f'Email de recuparação enviado para {email}')
            return recuperarsenha_email(email, senha) + '<a href="/">Página Inicial</a>'
        else:
            logging.info(f'Não foi possível enviar email {email} -> {return_request.text}')
            return f"{return_request.status_code} : {return_request.text}  <br> <a href='/esqueceu'>Tentar novamente</a>"          
    else:
        return 'Campos inválidos. Verifique os dados informados'

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return 'Logout realizado com sucesso. <a href="/">Página Inicial</a>'

if __name__ == '__main__':
    app.run(debug=True)
