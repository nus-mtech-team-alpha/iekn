# This code tests the session state management and assistant creation

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

# Import the main function from app.py
from cookbook.llms.ollama.auto_rag.app import main

@patch('app.get_auto_rag_assistant')
@patch('app.st')
def test_main_function(mock_st, mock_get_auto_rag_assistant):
    mock_st.session_state = {}
    mock_st.chat_input.return_value = "What is the weather today?"
    # mock_st.sidebar.file_uploader.return_value = BytesIO(b"mock pdf content")
    mock_st.sidebar.button.return_value = False

    mock_assistant = MagicMock()
    mock_get_auto_rag_assistant.return_value = mock_assistant
    mock_assistant.memory.get_chat_history.return_value = []

    main()

    assert mock_get_auto_rag_assistant.called
    assert mock_assistant.create_run.called
    assert mock_assistant.memory.get_chat_history.called
    assert mock_st.session_state["auto_rag_assistant"] is not None
    assert len(mock_st.session_state["messages"]) == 2  # Expecting initial message + user message

# import pytest
# from unittest.mock import patch, MagicMock

# # Import the main function
# from app import main  # replace 'your_module' with the actual module name

# @pytest.mark.parametrize("user_input, expected_messages", [
#     ("Hello", [{"role": "assistant", "content": "Upload a doc and ask me questions..."}, {"role": "user", "content": "Hello"}]),
#     ("How are you?", [{"role": "assistant", "content": "Upload a doc and ask me questions..."}, {"role": "user", "content": "How are you?"}]),
# ])
# @patch('your_module.st.session_state', new_callable=dict)
# @patch('your_module.st.chat_input')
# @patch('your_module.st.chat_message')
# def test_main(mock_chat_message, mock_chat_input, mock_session_state, user_input, expected_messages):
#     # Mocking the Assistant
#     mock_assistant = MagicMock()
#     mock_assistant.memory.get_chat_history.return_value = []
#     mock_assistant.run.return_value = ["Response from assistant"]
#     mock_session_state["auto_rag_assistant"] = mock_assistant
#     mock_session_state["auto_rag_assistant_run_id"] = "test_run_id"
    
#     # Mocking the Streamlit chat_input
#     mock_chat_input.return_value = user_input
    
#     # Call main function
#     main()
    
#     # Assert the messages in session state
#     assert mock_session_state["messages"] == expected_messages
    
#     # Assert assistant run is called with user input
#     mock_assistant.run.assert_called_once_with(user_input)

#     # Assert chat message is called with assistant's response
#     mock_chat_message.assert_called_with("assistant")
#     mock_chat_message().markdown.assert_called_once_with("Response from assistant")


# # import pytest
# # from unittest.mock import MagicMock, patch
# # import streamlit as st

# # from assistant import get_auto_rag_assistant

# # # Test checks if the assistant is initialized correctly 
# # # and its state is stored in st.session_state
# # @patch('your_module.get_auto_rag_assistant')
# # def test_assistant_initialization(mock_get_auto_rag_assistant):
# #     mock_assistant = MagicMock()
# #     # mock_get_auto_rag_assistant.return_value = mock_assistant
# #     # st.session_state.clear()
    
# #     # from app import main
# #     # main()
    
# #     # assert "auto_rag_assistant" in st.session_state
# #     # assert st.session_state["auto_rag_assistant"] == mock_assistant
# #     # mock_assistant.create_run.assert_called_once()
# #     # assert "auto_rag_assistant_run_id" in st.session_state

# # # This test simulates a user input and checks if the chat messages 
# # # are updated correctly in the session state
# # # @patch('your_module.get_auto_rag_assistant')
# # # def test_chat_message_handling(mock_get_auto_rag_assistant):
# # #     mock_assistant = MagicMock()
# # #     mock_assistant.memory.get_chat_history.return_value = []
# # #     mock_assistant.run.return_value = ["response"]
# # #     mock_get_auto_rag_assistant.return_value = mock_assistant
# # #     st.session_state.clear()
    
# # #     from your_module import main
# # #     st.session_state["messages"] = [{"role": "user", "content": "question"}]
# # #     main()
    
# # #     assert len(st.session_state["messages"]) == 2
# # #     assert st.session_state["messages"][-1]["role"] == "assistant"
# # #     assert st.session_state["messages"][-1]["content"] == "response"

# # # # Test verifies if a URL is correctly processed and added to the knowledge base
# # # @patch('your_module.WebsiteReader')
# # # @patch('your_module.get_auto_rag_assistant')
# # # def test_add_url_to_knowledge_base(mock_get_auto_rag_assistant, mock_website_reader):
# # #     mock_assistant = MagicMock()
# # #     mock_get_auto_rag_assistant.return_value = mock_assistant
# # #     mock_scraper = mock_website_reader.return_value
# # #     mock_scraper.read.return_value = [MagicMock()]
    
# # #     st.session_state.clear()
# # #     from your_module import main
# # #     st.sidebar.text_input = MagicMock(return_value="http://example.com")
# # #     st.sidebar.button = MagicMock(side_effect=[True, False])
    
# # #     main()
    
# # #     assert "http://example.com_uploaded" in st.session_state
# # #     mock_scraper.read.assert_called_once_with("http://example.com")
# # #     mock_assistant.knowledge_base.load_documents.assert_called_once()
