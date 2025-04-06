from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os
import logging

app = Flask(__name__)

# Configuração do logging para capturar e registrar erros
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_email(data):
    """
    Tenta extrair o email a partir de diferentes campos do JSON.
    Prioridade:
      1. data['email']
      2. data['customer']['email']
      3. data['contactEmail']
    """
    return data.get('email') or (data.get('customer') or {}).get('email') or data.get('contactEmail')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Tenta converter o corpo da requisição para JSON.
        data = request.get_json(force=True)
    except Exception as ex:
        logging.exception("Erro ao ler o JSON:")
        return jsonify({"error": "Formato de JSON inválido"}), 400

    try:
        # Extrai o email utilizando a função get_email
        email = get_email(data)
        # Extrai o nome do produto (caso não exista, usa 'Produto' como padrão)
        produto = data.get('products', [{}])[0].get('name', 'Produto')

        if not email:
            logging.error("Email não encontrado no payload: %s", data)
            return jsonify({"error": "Email não encontrado"}), 400

        # Monta o corpo e a mensagem do e-mail
        corpo = f"Obrigado pela sua compra do produto: {produto}!"
        msg = MIMEText(corpo)
        msg['Subject'] = 'Confirmação de Compra'
        msg['From'] = 'ferreiramateuss000@gmail.com'
        msg['To'] = email

        # Envia o e-mail via SMTP usando uma conexão segura
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('ferreiramateuss000@gmail.com', 'ixam jqaf ljsd iwjv')  # Use a senha de app gerada no Gmail
            smtp.send_message(msg)

        logging.info("Email enviado com sucesso para %s", email)
        return jsonify({"status": "Email enviado"}), 200

    except Exception as e:
        logging.exception("Erro ao enviar o email:")
        # Retorna uma mensagem genérica sem expor detalhes sensíveis
        return jsonify({"error": "Falha no envio do email"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # O servidor será executado no host '0.0.0.0' para ser acessível externamente
    app.run(host='0.0.0.0', port=port)
