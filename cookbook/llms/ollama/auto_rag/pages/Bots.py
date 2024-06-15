import streamlit as st
from lib.common import get_username


def main() -> None:
    get_username(st)
    # Get username
    # username = get_username_sidebar()
    # if username:
    #     st.sidebar.info(f":technologist: User: {username}")
    # else:
    #     st.markdown("---")
    #     st.markdown("#### :technologist: Enter a username, load a website and start chatting")
    #     return
    
# st.title("Local Auto RAG")
# st.markdown("##### :orange_heart: built using [phidata](https://github.com/phidatahq/phidata)")

main()