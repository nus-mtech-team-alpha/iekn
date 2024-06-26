import streamlit as st
from typing import Optional

from phi.assistant import Assistant
from phi.knowledge import AssistantKnowledge
from phi.llm.ollama import Ollama
from phi.embedder.ollama import OllamaEmbedder
from phi.vectordb.pgvector import PgVector2
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.tools.streamlit.components import (
    get_username_sidebar,
)
from phi.utils.log import logger

db_url = "postgresql+psycopg://ai:ai@pgvector-db:5432/ai"

def get_username(st):
    username = get_username_sidebar()
    if username:
        st.sidebar.info(f":technologist: User: {username}")
    else:
        st.markdown("---")
        st.markdown("#### :technologist: Enter a username, load a website and start chatting")
         
## load or create new gpt
def load_assistant():
    auto_rag_assistant: Assistant
    if "auto_rag_assistant" not in st.session_state or st.session_state["auto_rag_assistant"] is None:
        logger.info("---*--- Creating Assistant ---*---")
        auto_rag_assistant = get_auto_rag_assistant()
        auto_rag_assistant.rename_run("New convo..")
        st.session_state["auto_rag_assistant"] = auto_rag_assistant
    else:
        auto_rag_assistant = st.session_state["auto_rag_assistant"]

    #TODO: Check for latest chat session, if no history, reuse 
    
    # Create assistant run (i.e. log to database) and save run_id in session state
    try:
        st.session_state["auto_rag_assistant_run_id"] = auto_rag_assistant.create_run()
    except Exception:
        st.warning("Could not create assistant, is the database running?")
        return
    
    return auto_rag_assistant

## restart streamlit session (new gpt created)
def restart_assistant():
    logger.debug("---*--- Restarting Assistant ---*---")
    st.session_state["auto_rag_assistant"] = None
    st.session_state["auto_rag_assistant_run_id"] = None
    if "url_scrape_key" in st.session_state:
        st.session_state["url_scrape_key"] += 1
    if "file_uploader_key" in st.session_state:
        st.session_state["file_uploader_key"] += 1
    st.rerun()

def get_auto_rag_assistant(
    user_id: Optional[str] = None,
    run_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Assistant:
    """Get a Local Auto RAG Assistant."""

    return Assistant(
        name="auto_rag_assistant_ollama",
        run_id=run_id,
        user_id=user_id,
        llm=Ollama(host="ollama", model="adrienbrault/nous-hermes2pro-llama3-8b:q8_0"),
        storage=PgAssistantStorage(table_name="auto_rag_assistant_ollama", db_url=db_url),
        knowledge_base=AssistantKnowledge(
            vector_db=PgVector2(
                db_url=db_url,
                collection="auto_rag_documents_groq_ollama",
                embedder=OllamaEmbedder(host="ollama", model="nomic-embed-text", dimensions=768),
            ),
            # 1 reference are added to the prompt
            num_documents=1,
        ),
        description="You are an Assistant called 'AutoRAG' that answers questions by calling functions.",
        instructions=[
            "First get additional information about the users question from your knowledge base or the internet.",
            "Use the `search_knowledge_base` tool to search your knowledge base or the `duckduckgo_search` tool to search the internet.",
            "If the user asks to summarize the conversation, use the `get_chat_history` tool to get your chat history with the user.",
            "Carefully process the information you have gathered and provide a clear and concise answer to the user.",
            "Respond directly to the user with your answer, do not say 'here is the answer' or 'this is the answer' or 'According to the information provided'",
            "NEVER mention your knowledge base or say 'According to the search_knowledge_base tool' or 'According to {some_tool} tool'.",
        ],
        # Show tool calls in the chat
        show_tool_calls=True,
        # This setting gives the LLM a tool to search for information
        search_knowledge=True,
        # This setting gives the LLM a tool to get chat history
        read_chat_history=True,
        # tools=[DuckDuckGo()],
        # This setting tells the LLM to format messages in markdown
        markdown=True,
        # Adds chat history to messages
        add_chat_history_to_messages=True,
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
    )
