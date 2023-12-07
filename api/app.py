from flask import Flask, jsonify
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
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

cred = credentials.Certificate('api/key.json') 
default_app = initialize_app(cred) 
db = firestore.client() 
user_ref = db.collection('user')
lista_ref = db.collection('lista')
produto_ref = db.collection('produto')

@app.route('/user', methods=['POST'])
def create_user():
    try:
        id = request.json['id']
        user_ref.document(str(id)).set(request.json)
        logger.info(f'Usuário criado com id={id}')
        return jsonify({"success": True}), 200
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
            return jsonify({"id": id}), 200
        else:
            return jsonify({"error": "Acesso negado. Dados inválidos."}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/lista', methods=['GET'])
def get_lista():
    try:
        id = request.json['id']
        listaporid_ref = lista_ref.document(id)
        dados = listaporid_ref.get().to_dict()
        if dados:
            logger.info(f'Lista retornada com sucesso')
            return jsonify({"lista": dados}), 200
        else:
            return jsonify({"error": "Lista indisponível"}), 401
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/lista', methods=['POST'])
def create_lista():
    try:
        id = str(uuid.uuid4())
        request_completa = request.json
        request_completa["id"] = id
        lista_ref.document(str(id)).set(request_completa)
        logger.info(f'Lista criada com id={id}')
        return jsonify({"success": True}), 200
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
        all_id = [doc.to_dict() for doc in user_ref.stream()]
        logger.warning('all firebase data returned')
        return jsonify(all_id), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/produto', methods=['POST'])
def create_produto():
    try:
        id = str(uuid.uuid4())
        request_completa = request.json
        request_completa["id"] = id
        produto_ref.document(str(id)).set(request_completa)
        logger.info(f'Produto criado com id={id}')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

@app.route('/produto', methods=['DELETE'])
def delete_produto():
    try:
        id = request.json['id']
        lista_ref.document(id).delete()
        logger.info(f'Produto com id={id} deletado')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

if __name__ == '__main__':
    app.run()