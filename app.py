from flask import Flask, render_template, request
from funcoes import obtersuporte_email

app = Flask(__name__)

@app.route('/obtersuporte', methods=['GET', 'POST'])
def obter_suporte():
    if request.method == 'POST':
        email = request.form['email']
        texto = request.form['texto']

        aviso= obtersuporte_email(email, texto) if email != '' and texto != '' else 'Preencha os campos'
        return render_template('obtersuporte.html', aviso=aviso)

    return render_template('obtersuporte.html', aviso='')

if __name__ == '__main__':
    app.run(debug=True)
