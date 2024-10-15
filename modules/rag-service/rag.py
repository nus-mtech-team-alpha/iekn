import json

import requests
from phi.assistant import Assistant, AssistantKnowledge
from phi.embedder.ollama import OllamaEmbedder
from phi.knowledge.combined import CombinedKnowledgeBase
from phi.llm.ollama import Ollama
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.vectordb.pgvector import PgVector2

model_name = "adrienbrault/nous-hermes2pro-llama3-8b:q8_0"
name = {"name": model_name}
requests.post("http://localhost:11434/api/pull", json=name, stream=True)
db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

storage = PgAssistantStorage(
    # store runs in the ai.assistant_runs table
    table_name="assistant_runs",
    # db_url: Postgres database URL
    db_url=db_url,
)
knowledge_base_1 = AssistantKnowledge(
    vector_db=PgVector2(
        collection="test1",
        db_url=db_url,
        embedder=OllamaEmbedder(model="nomic-embed-text", dimensions=768),
    )
)
knowledge_base_1.load_text("Alice is a character in the book Alice in Wonderland.")
knowledge_base_2 = AssistantKnowledge(
    vector_db=PgVector2(
        collection="test2",
        db_url=db_url,
        embedder=OllamaEmbedder(model="nomic-embed-text", dimensions=768),
    )
)
knowledge_base_2.load_text("Alice is the cheerleader of Oak high school.")
knowledge_base = CombinedKnowledgeBase(
    sources=[knowledge_base_1, knowledge_base_2],
    vector_db=PgVector2(
        collection="test_combined",
        db_url=db_url,
        embedder=OllamaEmbedder(model="nomic-embed-text", dimensions=768),
    )
)
assistant = Assistant(
    user_id="1",
    llm=Ollama(host="localhost", port="11434", model=model_name),
    knowledge_base=knowledge_base,
    db_url=db_url,
    storage=storage,
    instructions=[
        "When a user asks a question, you will be provided with information about the question.",
        "Carefully read this information and provide a clear and concise answer to the user.",
        "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
    ],
    show_tool_calls=True,
    add_references_to_prompt=True,
    markdown=True
)
assistant.knowledge_base.load(recreate=False)
assistant.print_response("Who is Alice?")
