# app.py
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    email = data.get('email')
    produto = data.get('produto', 'Produto')

    if not email:
        return {'error': 'Email não encontrado'}, 400

    # Enviar e-mail
    msg = MIMEText(f"Obrigado pela sua compra do produto: {produto}!")
    msg['Subject'] = 'Confirmação de Compra'
    msg['From'] = 'poetese62@gmail.com'  # seu e-mail
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('poetese62@gmail.com', 'SUA_SENHA_DE_APP')
            smtp.send_message(msg)
        return {'status': 'Email enviado'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
