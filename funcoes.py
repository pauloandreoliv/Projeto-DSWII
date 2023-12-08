from email.mime.multipart import MIMEMultipart as formatodoemail
from email.mime.text import MIMEText as textodoemail
import smtplib  
import logging

logging.basicConfig(filename='logs/debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def obtersuporte_email(email_cliente, texto_cliente):
    try:
        conectar = smtplib.SMTP("smtp.office365.com",587)
        conectar.starttls()
        conectar.login("enviarcompython@outlook.com", "Python@123456")

        mensagem = formatodoemail()
        HTML = f"<b>E-mail</b>: {email_cliente} </br> <b>Texto</b>: {texto_cliente}" 
        mensagem['Subject'] = f"NOVO PEDIDO DE SUPORTE: {email_cliente}"
        mensagem.attach(textodoemail(HTML,'html'))
        texto = mensagem.as_string()

        conectar.sendmail("enviarcompython@outlook.com","recebercompython@outlook.com",texto)
        conectar.close()

        logging.info(f'SUCESSO no envio de suporte por e-mail: {email_cliente} ')

        return "Pedido de suporte enviado com sucesso! Você receberá uma resposta no e-mail enviado."
    except Exception as e:
        logging.error(f"ERRO ao tentar enviar e-mail para {email_cliente} -> Ocorreu uma exceção:" + str(e))
        return "Ocorreu uma exceção:" + str(e)

def recuperarsenha_email(email_cliente, senha):
    try:
        conectar = smtplib.SMTP("smtp.office365.com",587)
        conectar.starttls()
        conectar.login("enviarcompython@outlook.com", "Python@123456")

        mensagem = formatodoemail()
        HTML = f"<b>E-mail</b>: {email_cliente} </br> <b>Senha</b>: {senha}" 
        mensagem['Subject'] = f"RECUPERAÇÃO DE SENHA: {email_cliente}"
        mensagem.attach(textodoemail(HTML,'html'))
        texto = mensagem.as_string()

        conectar.sendmail("enviarcompython@outlook.com",f"{email_cliente}",texto)
        conectar.close()

        logging.info(f'SUCESSO no envio de recuperação de senha por e-mail: {email_cliente} ')

        return "Pedido de redefinição enviado com sucesso! Você receberá um e-mail."
    except Exception as e:
        logging.error(f"ERRO ao tentar enviar e-mail para {email_cliente} -> Ocorreu uma exceção:" + str(e))
        return "Ocorreu uma exceção:" + str(e)
