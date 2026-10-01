"""Teste de carga - Prática 2.
Uso (interface web, para os gráficos ao vivo):
    locust -f locustfile.py --host https://SUA-URL.onrender.com
    -> abrir http://localhost:8089
Uso headless (gera CSV para o relatório):
    locust -f locustfile.py --host https://SUA-URL.onrender.com \
        --headless -u 50 -r 5 -t 2m --csv resultados_50u --html resultados_50u.html
"""
import random
from locust import HttpUser, task, between


class UsuarioAPI(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def listar_itens(self):
        self.client.get("/items")

    @task(3)
    def ver_item(self):
        self.client.get(f"/items/{random.randint(1, 50)}", name="/items/[id]")

    @task(1)
    def health(self):
        self.client.get("/")

    @task(1)
    def cpu(self):
        self.client.get("/cpu?n=20000", name="/cpu")
