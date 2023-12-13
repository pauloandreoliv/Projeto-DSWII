from flask import Flask, jsonify
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from servico_autenticacao import gerar_token
from servico_validador import validar_token
import logging 
import uuid

logger = logging.getLogger()
logFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
consoleHanlder = logging.StreamHandler() 
consoleHanlder.setFormatter(logFormatter)
logger.addHandler(consoleHanlder)
fileHandler = logging.FileHandler("logs/log_api.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

app = Flask(__name__)
app.config.from_object('config')

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "app-mercado-4bae7",
  "private_key_id": "da5dc5afdf92b6008fdfec25c37c094c7e2a95db",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDJKWL2nLXUvOLz\nn2AaMI6IAEyB+CZD1YNV0QyovDRFH9VYgXFbDkOH7x844i/1H762skkvk7PrKmvF\nwWqK/FBKgbIDbqVxBU6L8bII/ybkz9zXCtawsWXMETyoQqYyEyxRh+iqCLzeIXeO\njLrXoA5d+FpVsThx8uhdE1czrTW6bjhK1hBgvL7ELFkoZ7TowbQnW9wLDK8WG6/Z\nngIa04uDw1/rRQ20J+FmXTA+0TtzjGIhGFAMP4X8ebFqdfVYIYbOM3u+/+n2/hVy\n4Qxw6mcs5uhvBMo8/kANv5lfc64ovknIiWI938SDDXKJoCZT4IyxAZ1fyPz3x9vA\nX7Qdrt5RAgMBAAECggEAFsWroVVOND4JxyCEpZJXoEfAYXoxAr7Z9k4LC9L6a9TV\ntwY4SeGMfYfxVeQtH6evVElMhalH1dhgiOuDXyZ/BGA4QbE141yBbtA2olQYGBD7\n5BAjC6+ZYYeWAUpCPCr1emlTSmRg1RieyzFdOWmyFqs1truwMx4Xdenplj0Gdwst\neBcPlWIbgfk3P8+mczbKY9YOFpnGwFWonLwA2SnWzoEO9r9csO/lW+gIk5ZKcI7j\nRRDjmW2/OH09CfdORH1xKEt5uRbjpPun4fdi3Ijh0/j2bM9CtiL0T5+NoztunXEW\nzDJD31cMbgcKwhGU/AYYA6izwBzgtahrl85zvvzY0QKBgQD+PWviKKlOrhxnZWzX\nAdJh2Jn45n6E+CeZxc20vfsoAi1njalWoxly61R1qs3bkWSMXKMK3Xb+7Oaw6WA5\nC2wDmBTN7atAxQnK5N6mdmrJCE0Wi/KgPA3QoB8hisTdjO5K7t4NyolxzQpVVexg\n0sUWmrR7ddZjwoX8euxKWGs1RQKBgQDKjeWV00KTqLjpngcJ1TmXkvXbHWH8FQlp\nq/+W/iMYX/J28LsICri1XNzAY2YYZGeJ/mw062GS42QFZaQHvJ873LFl2mtOWGIy\njTTaIODGLMk3py3sZZH6FoD9V4b3Oaczfx+UBjKMXi2ZLZ4QvbJ1TVBK+31RlvB2\nvqs5jO4XnQKBgAMzUL1bF66G4JKoozMdscFLkbyhYixYV19HLyy8S4IYbOvly6Ds\nkrBwp/KHQOonrWVa8S581TemUc0eUvjE3Qo6iuCAwmwhTttAAFGGIhf/w8Cp6Fb+\nCop6yYmJjqrfUEyfLyprR0modB3Y5A3f+V0se2Mme5lr5HXmMj1JWaglAoGAOikY\nXTb2DPQLdHk9yCMDkHRQSARd2EYqF7+dejuq1BrowiJJcfuyIdFySYPBEwvxdvwp\nEeDseYL1e18+BEKy7jtmbLqUyUAzohRNsrxyDjVZ6bMFSrW3frnre9MgG+jgC7da\n1+QXq5p3OV6R3ni5v1jdz0n7J+xRS6df/vxqeTkCgYBVUwRvR1RJGa9gPwx7W3ti\nF8AY5Nd3fDKjG9U0VutIYjESLqMoQUMqZixbWgcVgRC6g4Yd+Q/jaBLAYGTl/3al\npTwGfGp7iUSR4oOkJ/8FmX+iJkOJf3R6QKYVgUxe1RUAhR9u0FHA7NN1DP2i4Xg4\nOeIqxYHMlCZg3wNsypcsPw==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-xi17o@app-mercado-4bae7.iam.gserviceaccount.com",
  "client_id": "100181592438930488100",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xi17o%40app-mercado-4bae7.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}) 
default_app = initialize_app(cred) 
db = firestore.client() 
user_ref = db.collection('user')
lista_ref = db.collection('lista')
produto_ref = db.collection('produto')
promocao_ref = db.collection('promocao')
dica_ref = db.collection('dica')

@app.route('/user', methods=['POST'])
def create_user():
    try:
        id = request.json['id']
        userid_ref = user_ref.document(id)
        dados = userid_ref.get().to_dict()
        if dados and dados.get('id') == id:
            logger.info(f"{id} já cadastrado")
            return jsonify({"error": "CPF já cadastrado"}), 401
        else:
            user_ref.document(str(id)).set(request.json)
            logger.info(f'Usuário criado com id={id}')
            return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/user', methods=['PUT'])
def update_user():
    try:
        id = request.json['id']
        senha = str(uuid.uuid4())
        doc = user_ref.document(id).get().to_dict()
        if doc:
            doc["senha"] = senha
            user_ref.document(id).set(doc)
            logger.info(f'Senha de {id} alterada')
            return jsonify({"senha": senha}), 200
        else:
            return jsonify({"erro": f"Não foi possível encontrar o usuário {id}"}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/login', methods=['GET'])
def login():
    try:
        id = request.json['id']
        senha = request.json['senha']
        userid_ref = user_ref.document(id)
        dados = userid_ref.get().to_dict()
        
        if dados and dados.get('senha') == senha:
            logger.info(f'Logado com sucesso')
            token = gerar_token(id)
            return jsonify({"id": id, "token": token}), 200
        else:
            return jsonify({"error": "Acesso negado. Dados inválidos."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/lista', methods=['GET'])
def get_lista():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            id = request.json['id']
            listaporid_ref = lista_ref.document(id)
            dados = listaporid_ref.get().to_dict()
            if dados:
                logger.info(f'Lista retornada com sucesso')
                return jsonify({"lista": dados}), 200
            else:
                return jsonify({"error": "Lista indisponível"}), 401
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/listas_por_creator', methods=['GET'])
def get_listas_por_creator():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            id_creator = request.json['id_creator']
            todas_listas = lista_ref.stream()
            listas_por_creator = []
            for lista in todas_listas:
                dados = lista.to_dict()
                if 'id_creator' in dados and dados['id_creator'] == id_creator:
                    listas_por_creator.append({"id": dados['id'], "nome": dados['nome']})
            if listas_por_creator:
                logger.info(f'Listas retornadas com sucesso para o ID creator {id_creator}')
                return jsonify({"listas": listas_por_creator}), 200
            else:
                return jsonify({"error": f"Nenhuma lista disponível para o ID creator {id_creator}"}), 401
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/lista', methods=['POST'])
def create_lista():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            id = str(uuid.uuid4())
            request_completa = request.json
            request_completa["id"] = id
            lista_ref.document(str(id)).set(request_completa)
            logger.info(f'Lista criada com id={id}')
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/lista', methods=['DELETE'])
def delete_lista():
    try:
        id = request.json['id']
        lista_ref.document(id).delete()
        logger.info(f'Lista com id={id} deletada')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/produto', methods=['GET'])
def get_produtos():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            all_id = [doc.to_dict() for doc in produto_ref.stream()]
            logger.warning('all firebase data returned')
            return jsonify(all_id), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/produto', methods=['POST'])
def create_produto():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            id = str(uuid.uuid4())
            request_completa = request.json
            request_completa["id"] = id
            produto_ref.document(str(id)).set(request_completa)
            logger.info(f'Produto criado com id={id}')
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/produto', methods=['DELETE'])
def delete_produto():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            id = request.json['id']
            lista_ref.document(id).delete()
            logger.info(f'Produto com id={id} deletado')
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/promocoes', methods=['GET'])
def get_promocoes():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            all_id = [doc.to_dict() for doc in promocao_ref.stream()]
            logger.warning('all firebase data returned')
            return jsonify(all_id), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/dicas', methods=['GET'])
def get_dicas():
    try:
        authorization_header = request.headers.get('Authorization')
        token = validar_token(authorization_header)
        if token:
            all_id = [doc.to_dict() for doc in dica_ref.stream()]
            logger.warning('all firebase data returned')
            return jsonify(all_id), 200
        else:
            return jsonify({"error": "Acesso negado. Token inválido ou expirado."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

if __name__ == '__main__':
    app.run()