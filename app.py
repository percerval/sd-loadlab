"""API simples para a Prática de Sistemas Distribuídos.
Endpoints:
  /         -> health check (leve)
  /items    -> simula leitura de dados (I/O leve)
  /cpu      -> carga de CPU (mostra o limite físico da máquina)
"""
import os, time, hashlib, socket
from flask import Flask, jsonify, request

app = Flask(__name__)
ITEMS = [{"id": i, "nome": f"Produto {i}", "preco": round(i * 1.5, 2)} for i in range(1, 51)]


@app.get("/")
def health():
    return jsonify(status="ok", host=socket.gethostname(), ts=time.time())


@app.get("/items")
def items():
    time.sleep(0.02)  # simula latência de banco (20 ms)
    return jsonify(ITEMS)


@app.get("/items/<int:item_id>")
def item(item_id):
    for it in ITEMS:
        if it["id"] == item_id:
            return jsonify(it)
    return jsonify(erro="não encontrado"), 404


@app.get("/cpu")
def cpu():
    try:
        n = int(request.args.get("n", "20000"))
    except ValueError:
        return jsonify(erro="n deve ser um inteiro entre 1 e 1000000"), 400
    if not 1 <= n <= 1_000_000:
        return jsonify(erro="n deve ser um inteiro entre 1 e 1000000"), 400
    h = b"sd"
    for _ in range(n):
        h = hashlib.sha256(h).digest()
    return jsonify(iteracoes=n, hash=h.hex()[:16])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
