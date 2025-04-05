from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

EMAIL = "ferreiramateuss000@gmail.com"
SENHA = "ixam jqaf ljsd iwjv"  # Senha de app do Gmail

@app.route('/')
def home():
    return "Servidor online! 🟢"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    produto = data.get('produto', 'Produto não identificado')
    cliente = data.get('cliente', 'Cliente anônimo')

    # Criação do e-mail
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = 'ferreiramateuss000@gmail.com'
    msg['Subject'] = "Compra Confirmada na Kirvano"
    corpo = f"Compra confirmada!\n\nCliente: {cliente}\nProduto: {produto}"
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, SENHA)
        server.sendmail(EMAIL, msg['To'], msg.as_string())
        server.quit()
        return jsonify({"status": "sucesso", "mensagem": "E-mail enviado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
