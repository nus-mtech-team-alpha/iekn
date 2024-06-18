from typing import List

import streamlit as st
from lib.common import get_username, load_assistant, restart_assistant
from phi.document.reader.website import WebsiteReader
from phi.document.reader.pdf import PDFReader
from phi.document import Document

st.set_page_config(
    page_title="Intelligent Enterprise Knowledge Navigator - Bots Management",
    page_icon=":robot_face:",
)

def main() -> None:
    get_username(st)
    auto_rag_assistant = load_assistant()

    try:
        st.write(f"{auto_rag_assistant.knowledge_base.vector_db.get_count()} collections")
    except:
        st.write("0 collections")

    # Load knowledge base
    if auto_rag_assistant.knowledge_base:
        # -*- Add websites to knowledge base
        if "url_scrape_key" not in st.session_state:
            st.session_state["url_scrape_key"] = 0

        input_url = st.text_input(
            "Add URL to Knowledge Base", type="default", key=st.session_state["url_scrape_key"]
        )
        add_url_button = st.button("Add URL")
        if add_url_button:
            if input_url is not None:
                alert = st.info("Processing URLs...", icon="ℹ️")
                if f"{input_url}_scraped" not in st.session_state:
                    scraper = WebsiteReader(max_links=2, max_depth=1, chunk_size=2000)
                    web_documents: List[Document] = scraper.read(input_url)
                    if web_documents:
                        auto_rag_assistant.knowledge_base.load_documents(web_documents, upsert=True)
                    else:
                        st.error("Could not read website")
                    st.session_state[f"{input_url}_uploaded"] = True
                alert.empty()
                restart_assistant()

        # Add PDFs to knowledge base
        if "file_uploader_key" not in st.session_state:
            st.session_state["file_uploader_key"] = 100

        uploaded_file = st.file_uploader(
            "Add a PDF :page_facing_up:", type="pdf", key=st.session_state["file_uploader_key"]
        )
        if uploaded_file is not None:
            alert = st.info("Processing PDF...", icon="🧠")
            rag_name = uploaded_file.name.split(".")[0]
            if f"{rag_name}_uploaded" not in st.session_state:
                reader = PDFReader(chunk_size=2000)
                rag_documents: List[Document] = reader.read(uploaded_file)
                if rag_documents:
                    auto_rag_assistant.knowledge_base.load_documents(rag_documents, upsert=True)
                else:
                    st.error("Could not read PDF")
                st.session_state[f"{rag_name}_uploaded"] = True
            alert.empty()
            restart_assistant()

    #clear knowledge base
    if auto_rag_assistant.knowledge_base and auto_rag_assistant.knowledge_base.vector_db:
        if st.button("Clear Knowledge Base"):
            auto_rag_assistant.knowledge_base.vector_db.clear()
            st.success("Knowledge base cleared")
            restart_assistant()


st.title("Knowledge Base Management")

# st.markdown("##### :orange_heart: built using [phidata](https://github.com/phidatahq/phidata)")

main()