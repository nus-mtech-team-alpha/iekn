# This code tests the app main_function and whether there os any exception raised

from streamlit.testing.v1 import AppTest

def test_main_function():
    at = AppTest.from_file("app.py")
    at.run()
    
    assert len(at.exception) == 0
    assert len(at.session_state["messages"]) != 0