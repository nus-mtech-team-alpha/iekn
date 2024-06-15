import streamlit as st

from phi.tools.streamlit.components import (
    get_openai_key_sidebar,
    check_password,
    reload_button_sidebar,
    get_username_sidebar,
)
from phi.utils.log import logger
from phi.assistant import Assistant
from assistant import get_auto_rag_assistant  # type: ignore


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