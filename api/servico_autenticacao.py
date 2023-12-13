import jwt
import datetime

def gerar_token(id):
    chave_secreta = 'aplicacaoWeb2023.2'
    timestamp_expiracao = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    json = {
        'id': id,
        'exp': timestamp_expiracao
    }
    token = jwt.encode(json, chave_secreta, algorithm='HS256')
    return token