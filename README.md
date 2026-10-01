# SD LoadLab — Docker, Deploy PaaS e Testes de Carga (Locust)

Laboratório de Sistemas Distribuídos: API Python (Flask + Gunicorn) empacotada em Docker, preparada para deploy no Render e testes de carga com Locust. Não requer banco de dados nem credenciais para executar.

## Endpoints
| Rota | O que faz |
|---|---|
| `GET /` | Health check (resposta leve) |
| `GET /items` | Lista 50 itens, simula 20 ms de latência de banco |
| `GET /items/<id>` | Busca um item |
| `GET /cpu?n=20000` | Carga de CPU (20 mil SHA-256) — evidencia o limite físico da máquina |

`n` aceita inteiros de **1 a 1.000.000**; entradas inválidas retornam HTTP 400 com erro JSON. O limite reduz o custo de uma requisição, mas não substitui rate limiting. Esta é uma API didática com uma rota intencionalmente custosa, não um serviço endurecido para produção.

---

## Executar, validar e publicar

### 1. Rodar localmente (5 min)
```bash
docker build -t sd-loadlab .
docker run --rm -p 8000:8000 sd-loadlab
# abrir http://localhost:8000
```
Sem Docker, use Python 3.12+ em um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Testes automatizados**, sem dependências extras de teste:
```bash
docker run --rm -v "$PWD/tests:/app/tests:ro" sd-loadlab python -m unittest discover -s tests -v
# Alternativa no ambiente virtual:
python -m unittest discover -s tests -v
```

### 2. Subir no GitHub (5 min)
```bash
git init
git branch -M main
git add .
git diff --cached
git commit -m "feat: add SD LoadLab API with Docker and load tests"
gh repo create sd-loadlab --public --source=. --remote=origin
git push -u origin main
```
Use `--private` no lugar de `--public` se necessário. Execute a criação somente se o repositório remoto ainda não existir. Revise os arquivos antes do commit; não publique credenciais nem chaves privadas.

### 3. Deploy no Render — Docker
1. Entre em https://render.com com a conta do GitHub.
2. **New → Web Service** → escolha o repositório `sd-loadlab`.
3. **Language/Runtime: Docker** (ele detecta o Dockerfile sozinho).
4. Instance Type: **Free**. Configure **Health Check Path: `/`**. Não defina Build Command ou Start Command: o Dockerfile contém ambos. Clique em **Deploy**.
5. Aguarde o build e copie a URL real do painel. O nome do serviço não garante um subdomínio específico.
6. Teste no navegador: `/`, `/items`, `/cpu`.

**Alternativa declarativa:** use **New → Blueprint**, selecione o repositório e revise o serviço Free definido em `render.yaml`. Escolha apenas um dos caminhos para não criar serviços duplicados.

O Gunicorn respeita `PORT`, escuta em `0.0.0.0` e envia logs para stdout/stderr. Não precisa de disco persistente.

> ⚠️ O plano grátis pode hibernar após inatividade. Confirme uma resposta saudável antes da apresentação e das medições. Confira limites e condições atuais na plataforma.

Valide a URL real após o deploy:
```bash
curl --fail https://SUA-URL.onrender.com/
curl --fail https://SUA-URL.onrender.com/items/1
curl -i 'https://SUA-URL.onrender.com/cpu?n=abc' # esperado: HTTP 400
```

### 4. Teste de carga com Locust (30 min)
Instale no ambiente virtual local, não no container de produção. Registre `locust --version` e os recursos do serviço no relatório. Execute carga somente contra seu próprio serviço e dentro das regras do provedor. Comece pelo cenário menor e interrompa se houver degradação intensa.

```bash
pip install locust
```
**Interface web (gráficos em tempo real — use na apresentação):**
```bash
locust -f locustfile.py --host https://SUA-URL.onrender.com
# abrir http://localhost:8089 → Users: 50, Spawn rate: 5 → Start
```
**Headless (gera CSV + HTML para o relatório) — rode 3 cenários:**
```bash
locust -f locustfile.py --host https://SUA-URL.onrender.com --headless -u 10  -r 2  -t 2m --csv r_10u  --html r_10u.html
locust -f locustfile.py --host https://SUA-URL.onrender.com --headless -u 50  -r 5  -t 2m --csv r_50u  --html r_50u.html
locust -f locustfile.py --host https://SUA-URL.onrender.com --headless -u 150 -r 10 -t 2m --csv r_150u --html r_150u.html
```
Os arquivos `r_XXu_stats.csv` têm a linha **Aggregated** com RPS, mediana, **95%** e **99%** — são os números da tabela do relatório.
Os dois minutos incluem a rampa de usuários. Calcule o percentual de falhas como `100 × Failure Count / Request Count` (ou N/A se não houver requisições); não confunda contagem ou falhas/s com percentual.
Os `.html` têm os gráficos prontos (tire print para o PDF).

---

## Explicações rápidas (para relatório e arguição)

- **p95 / p99:** 95% (ou 99%) das requisições responderam em até X ms. São melhores que a média porque mostram a "cauda": os usuários que tiveram a pior experiência. A média esconde picos.
- **Limite físico da máquina:** registre os recursos efetivamente disponíveis no plano usado. RPS estabilizado com latência crescente sugere saturação, mas não prova gargalo de CPU: correlacione com métricas de recursos, rede e erros. A rota `/cpu` permite exercitar processamento.
- **Por que Gunicorn e não `python app.py`?** O servidor de desenvolvimento do Flask normalmente usa threads, mas não é adequado para produção. O Gunicorn gerencia **workers (processos)** e **threads**. Threads ajudam na concorrência de I/O; não implicam paralelismo de CPU para código Python sujeito ao GIL.
- **Por que Docker?** Empacota código + dependências + runtime numa imagem imutável: roda igual na máquina do aluno e na nuvem ("na minha máquina funciona" resolvido). Reprodutibilidade e portabilidade.
- **PaaS vs IaaS:** no PaaS (Render) não gerenciamos servidor, SO nem rede — só entregamos o container. Em IaaS (EC2) teríamos que configurar tudo.
- **Escalabilidade:** vertical = máquina maior; horizontal = mais instâncias atrás de um balanceador de carga. A API é **stateless** (não guarda sessão), então escala horizontalmente fácil.
- **Erros sob carga:** status 502/503/timeouts podem indicar sobrecarga, indisponibilidade ou falhas de infraestrutura. Consulte os logs antes de atribuir uma causa.
- **Teorema CAP / consistência:** a API não tem banco distribuído; com várias réplicas e um banco, teríamos que escolher entre consistência e disponibilidade em caso de partição.
- **Cold start:** a primeira requisição após o serviço dormir é lenta (o container está subindo) — explica um p99 alto no começo do teste.

## Checklist da entrega

- [ ] Repositório publicado e acessível ao avaliador.
- [ ] Serviço no Render com status Live e endpoints validados.
- [ ] Integrantes e URLs reais preenchidos nos dois relatórios.
- [ ] Screenshots reais do build, deploy e testes anexados.
- [ ] Resultados medidos do Locust registrados, com análise baseada nas evidências.
