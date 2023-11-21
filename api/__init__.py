from flask import Flask, jsonify
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


#inicializando o flask 

app = Flask(__name__)
app.config.from_object('config')

# Inicializar Firestore DB 

cred = credentials.Certificate('key.json') 
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
            return jsonify(user_id.to_dict()), 200
        else:
            all_id = [doc.to_dict() for doc in user_ref.stream()]
            return jsonify(all_id), 200
        
    except Exception as e:
        return f"An Error Occured: {e}"



@app.route('/user', methods=['POST']) #funcionando
def create():
    try:
        id = request.json['id']
        user_ref.document(str(id)).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    


@app.route('/user', methods=['GET', 'DELETE']) # funcionando 
def delete():
    try:
        id = request.args.get('id')
        user_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"



@app.route('/user', methods=['POST', 'PUT']) # funcionando mas obs**
def update():
    try:
        id = request.json['id']
        user_ref.document(str(id)).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


app.run()