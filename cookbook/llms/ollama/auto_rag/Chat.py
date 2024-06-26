import nest_asyncio
from typing import List
from lib.common import get_username, load_assistant, restart_assistant, get_auto_rag_assistant

import streamlit as st
from phi.assistant import Assistant
from phi.utils.log import logger
from phi.assistant.run import AssistantRun

nest_asyncio.apply()
st.set_page_config(
    page_title="Intelligent Enterprise Knowledge Navigator",
    page_icon=":robot_face:",
)
st.title("Intelligent Enterprise Knowledge Navigator")

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
    sidebar(auto_rag_assistant)

main()
