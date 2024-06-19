import nest_asyncio
from typing import List
from lib.common import get_username, load_assistant, restart_assistant

import streamlit as st
from phi.assistant import Assistant
# from phi.document import Document
# from phi.document.reader.pdf import PDFReader
# from phi.document.reader.website import WebsiteReader
from phi.utils.log import logger
from phi.assistant.run import AssistantRun

from assistant import get_auto_rag_assistant  # type: ignore

nest_asyncio.apply()
st.set_page_config(
    page_title="Intelligent Enterprise Knowledge Navigator",
    page_icon=":robot_face:",
)
st.title("Intelligent Enterprise Knowledge Navigator")
# st.markdown("##### :orange_heart: built using [phidata](https://github.com/phidatahq/phidata)")

# ## load or create new gpt
# def load_assistant():
#     auto_rag_assistant: Assistant
#     if "auto_rag_assistant" not in st.session_state or st.session_state["auto_rag_assistant"] is None:
#         logger.info("---*--- Creating Assistant ---*---")
#         auto_rag_assistant = get_auto_rag_assistant()
#         auto_rag_assistant.rename_run("New convo..")
#         st.session_state["auto_rag_assistant"] = auto_rag_assistant
#     else:
#         auto_rag_assistant = st.session_state["auto_rag_assistant"]

#     # Create assistant run (i.e. log to database) and save run_id in session state
#     try:
#         st.session_state["auto_rag_assistant_run_id"] = auto_rag_assistant.create_run()
#     except Exception:
#         st.warning("Could not create assistant, is the database running?")
#         return
    
#     return auto_rag_assistant

# ## restart streamlit session (new gpt created)
# def restart_assistant():
#     logger.debug("---*--- Restarting Assistant ---*---")
#     st.session_state["auto_rag_assistant"] = None
#     st.session_state["auto_rag_assistant_run_id"] = None
#     if "url_scrape_key" in st.session_state:
#         st.session_state["url_scrape_key"] += 1
#     if "file_uploader_key" in st.session_state:
#         st.session_state["file_uploader_key"] += 1
#     st.rerun()

## load past chats
def load_history(new_auto_rag_assistant_run_id):
    if st.session_state["auto_rag_assistant_run_id"] != new_auto_rag_assistant_run_id:
        logger.info(f"---*--- Loading Assistant run: {new_auto_rag_assistant_run_id} ---*---")
        st.session_state["auto_rag_assistant"] = get_auto_rag_assistant(run_id=new_auto_rag_assistant_run_id)
        # st.rerun()

## sidebar UI
def sidebar(rag):
    # Get username
    get_username(st)

    #new chat
    if st.sidebar.button("New Chat", use_container_width=True):
        restart_assistant()

    #existing chat
    if rag.storage:
        rag_runs: List[AssistantRun] = rag.storage.get_all_runs()
        for r in rag_runs:
            st.sidebar.button(str(r.run_id if r.run_name is None else r.run_name), r.run_id, type="primary" if r.run_id == st.session_state["auto_rag_assistant_run_id"] else "secondary", on_click=load_history, args=[r.run_id], use_container_width=True)
    # if st.sidebar.button("Auto Rename"):
    #     rag.auto_rename_run()

## chat UI
def chat(auto_rag_assistant):
    # Load existing messages
    assistant_chat_history = auto_rag_assistant.memory.get_chat_history()
    if len(assistant_chat_history) > 0:
        logger.debug("Loading chat history")
        st.session_state["messages"] = assistant_chat_history
    else:
        logger.debug("No chat history found")
        st.session_state["messages"] = [{"role": "assistant", "content": "Upload a doc and ask me questions..."}]

    # Prompt for user input
    if prompt := st.chat_input():
        st.session_state["messages"].append({"role": "user", "content": prompt})
        
    # Display existing chat messages
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is from a user, generate a new response
    last_message = st.session_state["messages"][-1]
    if last_message.get("role") == "user":
        question = last_message["content"]
        with st.chat_message("assistant"):
            resp_container = st.empty()
            response = ""
            for delta in auto_rag_assistant.run(question):
                response += delta  # type: ignore
                resp_container.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})

    #rename the chat after 6 messages
    if len(st.session_state["messages"]) == 6:
        auto_rag_assistant.auto_rename_run()

## main 
def main() -> None:    
    # Get the assistant
    auto_rag_assistant: Assistant = load_assistant()
    chat(auto_rag_assistant)
    
    # Load knowledge base
    # if auto_rag_assistant.knowledge_base:
    #     # -*- Add websites to knowledge base
    #     if "url_scrape_key" not in st.session_state:
    #         st.session_state["url_scrape_key"] = 0

    #     input_url = st.sidebar.text_input(
    #         "Add URL to Knowledge Base", type="default", key=st.session_state["url_scrape_key"]
    #     )
    #     add_url_button = st.sidebar.button("Add URL")
    #     if add_url_button:
    #         if input_url is not None:
    #             alert = st.sidebar.info("Processing URLs...", icon="ℹ️")
    #             if f"{input_url}_scraped" not in st.session_state:
    #                 scraper = WebsiteReader(max_links=2, max_depth=1, chunk_size=2000)
    #                 web_documents: List[Document] = scraper.read(input_url)
    #                 if web_documents:
    #                     auto_rag_assistant.knowledge_base.load_documents(web_documents, upsert=True)
    #                 else:
    #                     st.sidebar.error("Could not read website")
    #                 st.session_state[f"{input_url}_uploaded"] = True
    #             alert.empty()
    #             restart_assistant()

    #     # Add PDFs to knowledge base
    #     if "file_uploader_key" not in st.session_state:
    #         st.session_state["file_uploader_key"] = 100

    #     uploaded_file = st.sidebar.file_uploader(
    #         "Add a PDF :page_facing_up:", type="pdf", key=st.session_state["file_uploader_key"]
    #     )
    #     if uploaded_file is not None:
    #         alert = st.sidebar.info("Processing PDF...", icon="🧠")
    #         rag_name = uploaded_file.name.split(".")[0]
    #         if f"{rag_name}_uploaded" not in st.session_state:
    #             reader = PDFReader(chunk_size=2000)
    #             rag_documents: List[Document] = reader.read(uploaded_file)
    #             if rag_documents:
    #                 auto_rag_assistant.knowledge_base.load_documents(rag_documents, upsert=True)
    #             else:
    #                 st.sidebar.error("Could not read PDF")
    #             st.session_state[f"{rag_name}_uploaded"] = True
    #         alert.empty()
    #         restart_assistant()

    #clear knowledge base
    # if auto_rag_assistant.knowledge_base and auto_rag_assistant.knowledge_base.vector_db:
    #     if st.sidebar.button("Clear Knowledge Base"):
    #         auto_rag_assistant.knowledge_base.vector_db.clear()
    #         st.sidebar.success("Knowledge base cleared")
    #         restart_assistant()

    sidebar(auto_rag_assistant)

main()
