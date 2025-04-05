from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Captura o e-mail do cliente corretamente
    email = data.get('customer', {}).get('email')
    produto = data.get('products', [{}])[0].get('name', 'Produto')

    if not email:
        return {'error': 'Email não encontrado'}, 400

    # Monta o e-mail
    msg = MIMEText(f"Olá! Obrigado pela sua compra do produto: {produto}! Em breve você receberá mais informações.")
    msg['Subject'] = 'Confirmação de Compra'
    msg['From'] = 'ferreiramateuss000@gmail.com'
    msg['To'] = email  # agora vai pro cliente certo!

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('ferreiramateuss000@gmail.com', 'ixam jqaf ljsd iwjv')  # senha de app
            smtp.send_message(msg)
        return {'status': 'Email enviado com sucesso!'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # usa a porta da Render se existir
    app.run(host='0.0.0.0', port=port)
