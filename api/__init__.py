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
@app.route('/', methods=['GET']) # sem funcionar
def root():
    try:
        user_id = request.args.get('id')    
        if user_id:
            todo = user_ref.document(user_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in user_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"



@app.route('/', methods=['POST']) #funcionando
def create():
    try:
        user_ref.document(str(id)).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    


@app.route('/', methods=['GET', 'DELETE']) # sem funcionar
def delete():
    try:
        user_id = request.args.get(id)
        user_ref.document(user_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    





@app.route('/', methods=['POST', 'PUT']) # sem funcionar
def update():
    try:
        id = request.json['id']
        user_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


app.run()