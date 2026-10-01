# RELATÓRIO — PRÁTICA 1: DOCKER & DEPLOY PaaS (máx. 2 páginas)

**Disciplina:** Sistemas Distribuídos — IFPA Campus Ananindeua
**Equipe:** [Nome 1], [Nome 2], [Nome 3]
**Repositório:** https://github.com/[usuario]/sd-loadlab
**URL pública:** https://[servico].onrender.com

## 1. Objetivo
Conteinerizar uma API REST em Python e publicá-la em uma plataforma PaaS, tornando-a acessível por uma URL pública.

## 2. Aplicação
API SD LoadLab desenvolvida em Flask com quatro endpoints: `/` (health check), `/items` (listagem com latência simulada de 20 ms), `/items/<id>` (consulta individual) e `/cpu` (processamento com hashes SHA-256). A rota de CPU aceita de 1 a 1.000.000 de iterações e rejeita entradas inválidas com HTTP 400. O Gunicorn usa 2 workers e 4 threads por worker. O servidor de desenvolvimento do Flask também suporta threads, mas não é recomendado para produção. Threads favorecem concorrência de I/O; processos permitem explorar múltiplos núcleos quando disponíveis.

## 3. Conteinerização (Dockerfile)
- **Imagem base `python:3.12-slim`:** imagem enxuta, reduz tamanho e tempo de build.
- **Cópia do `requirements.txt` antes do código:** aproveita o cache de camadas do Docker — as dependências só são reinstaladas se mudarem.
- **`--no-cache-dir`:** não guarda cache do pip, imagem menor.
- **Porta via variável `PORT`:** o PaaS define a porta em tempo de execução; o container se adapta.
- **`.dockerignore`:** evita copiar arquivos desnecessários para a imagem.

[INSERIR PRINT: `docker build` / `docker run` local funcionando]

## 4. Deploy na plataforma PaaS (Render)
*Confirmar esta seção após executar o deploy; os passos abaixo descrevem o procedimento previsto.*

1. Código versionado e enviado ao GitHub.
2. Criação de um Web Service no Render conectado ao repositório, com runtime Docker.
3. O Render executa o build da imagem a partir do Dockerfile e publica o container com HTTPS automático.
4. A cada `git push`, um novo deploy é feito automaticamente (deploy contínuo).

[INSERIR PRINT: painel do Render com status "Live" + navegador acessando a URL]

## 5. Dificuldades e soluções
- [Ex.: porta fixa causava falha no health check do Render → passamos a usar `${PORT}`.]
- [Ex.: serviço do plano gratuito hiberna após inatividade → acesso prévio antes dos testes (cold start).]

## 6. Conclusão
[Após a execução, descrever as evidências de portabilidade da imagem e os resultados do deploy. Docker padroniza runtime e dependências, mas não torna hardware ou rede idênticos entre ambientes.]
