# RELATÓRIO — PRÁTICA 2: TESTES DE CARGA COM LOCUST (máx. 3 páginas)

**Disciplina:** Sistemas Distribuídos — IFPA Campus Ananindeua
**Equipe:** [Nome 1], [Nome 2], [Nome 3]
**Alvo:** https://[servico].onrender.com (Render; registrar plano e recursos disponíveis no momento do teste)
**Versão do Locust:** [preencher]
**Data e ambiente do gerador de carga:** [preencher]

## 1. Objetivo
Avaliar o comportamento da API publicada sob concorrência crescente, medindo vazão (RPS), latência (mediana, p95, p99) e taxa de falhas, e identificar o limite físico da máquina.

## 2. Metodologia
- **Ferramenta:** Locust, executado a partir da máquina de um integrante da equipe.
- **Perfil de usuário simulado** (`locustfile.py`), com espera de 0,5 a 2 s entre ações:

| Tarefa | Peso | Descrição |
|---|---|---|
| `GET /items` | 5 | listagem (I/O simulado) |
| `GET /items/[id]` | 3 | consulta individual |
| `GET /` | 1 | health check |
| `GET /cpu` | 1 | carga de CPU |

- **Cenários:** metas de 10, 50 e 150 usuários, com spawn rates de 2, 5 e 10 usuários/s, respectivamente. Cada execução dura 2 minutos totais, incluindo a rampa de aproximadamente 5, 10 e 15 segundos. As estatísticas agregadas incluem essa rampa.

## 3. Resultados
*(Preencher com a linha "Aggregated" de cada `r_XXu_stats.csv`)*

Calcular **Falhas (%) = 100 × Failure Count / Request Count** quando `Request Count > 0`. Se não houver requisições, registrar N/A. `Failure Count` é uma contagem e `Failures/s` é uma taxa por segundo, não um percentual.

| Usuários | Requisições | Falhas (%) | RPS | Mediana (ms) | p95 (ms) | p99 (ms) |
|---|---|---|---|---|---|---|
| 10  | | | | | | |
| 50  | | | | | | |
| 150 | | | | | | |

[INSERIR PRINT: gráfico "Total Requests per Second"]
[INSERIR PRINT: gráfico "Response Times (ms)" com p50 e p95]
[INSERIR PRINT: gráfico "Number of Users"]

## 4. Análise
**Percentis de latência.** O p95 indica que 95% das requisições foram respondidas em até X ms; o p99, que 99% foram respondidas em até Y ms. Percentis complementam a média ao revelar a cauda da distribuição. A média sozinha não descreve a distribuição e pode ser bastante afetada por valores extremos. [Preencher X e Y com medições.]

**Limite físico.** [Comparar RPS, p95, p99 e falhas entre os cenários sem pressupor saturação.] RPS estabilizado e latências crescentes sugerem um limite de capacidade, mas não identificam sozinhos o gargalo. Correlacionar com métricas de CPU/memória disponíveis, logs, rede e capacidade do gerador de carga. [Registrar qual endpoint foi mais afetado e possíveis causas; não atribuir erros 502/503/timeouts automaticamente à CPU.]

**Cold start.** [Se aplicável] As primeiras requisições apresentaram latência elevada porque o serviço gratuito estava hibernado e precisou subir o container.

## 5. Possíveis melhorias
- **Escala vertical:** instância com mais CPU/RAM.
- **Escala horizontal:** múltiplas réplicas atrás de um balanceador de carga — viável porque a API é stateless.
- **Cache** (ex.: Redis) para `/items`, eliminando o custo repetido de I/O.
- Ajuste do número de workers/threads do Gunicorn conforme os núcleos disponíveis.

## 6. Conclusão
[Preencher após os testes: resumir o comportamento efetivamente medido, indicar se houve saturação e registrar limitações da análise. Sem evidências suficientes, não afirmar que o limite físico foi atingido nem que escalar a infraestrutura é a única solução.]
