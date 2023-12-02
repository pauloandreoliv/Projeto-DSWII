from flask import Flask, jsonify
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import logging 



#logging

logger = logging.getLogger()

logFormatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")


consoleHanlder = logging.StreamHandler() 
consoleHanlder.setFormatter(logFormatter)
logger.addHandler(consoleHanlder)


fileHandler = logging.FileHandler("logs/log_api.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)


#inicializando o flask 

app = Flask(__name__)
app.config.from_object('config')

# Inicializar Firestore DB 

cred = credentials.Certificate('api/key.json') 
default_app = initialize_app(cred) 
db = firestore.client() 
user_ref = db.collection('user')



####### requisições ##################

## ex: http://127.0.0.1:5000/user?id="id"

@app.route('/user', methods=['GET']) # funcionando 
def root():
    try:
        id = request.args.get('id')    
        if id:
            user_id = user_ref.document(id).get()
            logger.warning(f'returned ID = {id} data')
            return jsonify(user_id.to_dict()), 200
        else:
            all_id = [doc.to_dict() for doc in user_ref.stream()]
            logger.warning('all firebase data returned')
            return jsonify(all_id), 200
        
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500



@app.route('/user', methods=['POST']) #funcionando
def create():
    try:
        id = request.json['id']
        user_ref.document(str(id)).set(request.json)
        logger.warning(f'ID data successfully created from firebase with id ={id}')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500
    


@app.route('/user', methods=['GET', 'DELETE']) # funcionando 
def delete():
    try:
        id = request.args.get('id')
        user_ref.document(id).delete()
        logger.warning(f'ID = {id} data successfully deleted')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500


@app.route('/user', methods=['POST', 'PUT']) # funcionando mas obs**
def update():
    try:
        id = request.json['id']
        user_ref.document(str(id)).update(request.json)
        logger.warning(f'ID = {id} data updated successfully')
        return jsonify({"success": True}), 200
    except Exception as e:
        logger.error(f"An Error Occurred: {e}")
        return f"An Error Occurred: {e}", 500

app.run()