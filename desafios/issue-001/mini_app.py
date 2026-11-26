"""Mini-aplicação do microdesafio da Issue #1 (independente do GERLab)."""
from flask import Flask, jsonify

app = Flask(__name__)


# Rota de exemplo: responde um texto simples.
@app.get("/ola")
def ola():
    return "Olá!"


# TODO: crie aqui a rota /ping (somente GET) que responde
#       o JSON {"resposta": "pong"} com status 200.
@app.get("/ping")
def ping():
    return jsonify({"resposta": "pong"}), 200