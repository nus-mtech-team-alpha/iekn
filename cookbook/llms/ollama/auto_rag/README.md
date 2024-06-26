# Autonomous RAG with Local Models

This cookbook shows how to do Autonomous retrieval-augmented generation with Hermes 2 Pro Llama3 on Ollama.

> Note: Fork and clone this repository if needed

### 1. [Install](https://github.com/ollama/ollama?tab=readme-ov-file#macos) ollama and pull models

```shell
ollama pull adrienbrault/nous-hermes2pro-llama3-8b:q8_0

ollama pull nomic-embed-text
```

### 2. Create a virtual environment

```shell
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/bin/activate
```

### 3. Install libraries

```shell
pip install -r requirements.txt
```

### 4. Run PgVector

> Install [docker desktop](https://docs.docker.com/desktop/install/mac-install/) first.

- Run using a helper script

```shell
./cookbook/run_pgvector.sh
```

- OR run using the docker run command

```shell
docker run -d 
  -e POSTGRES_DB=ai 
  -e POSTGRES_USER=ai 
  -e POSTGRES_PASSWORD=ai 
  -e PGDATA=/var/lib/postgresql/data/pgdata 
  -v pgvolume:/var/lib/postgresql/data 
  -p 5532:5432 
  --name pgvector 
  phidata/pgvector:16
```

### 5. Run Autonomous RAG App

```shell
streamlit run app.py
```

- Open [localhost:8501](http://localhost:8501) to view your RAG app.
- Add websites or PDFs and ask question.

### 6. Run API
```shell
uvicorn main:app --reload --port 80
```

### 7. Star ⭐️ the project if you like it.

### 8. Share with your friends: https://git.new/ollama-autorag
