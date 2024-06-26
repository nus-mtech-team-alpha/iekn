from lib.common import get_auto_rag_assistant
# import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from phi.assistant import Assistant
from phi.assistant.run import AssistantRun
from typing import List

# from assistant import get_auto_rag_assistant  # type: ignore

app = FastAPI()


@app.get("/")
def get_root():
    return {"hello":"world"}

@app.get("/sessions")
def get_sessions():
    # return {"sessions":"ses"}
    auto_rag_assistant: Assistant = get_auto_rag_assistant()
    sessions = []
    if auto_rag_assistant.storage:
        rag_runs: List[AssistantRun] = auto_rag_assistant.storage.get_all_runs()

        for r in rag_runs:
            sessions.append({"run_id":r.run_id,"run_name":r.run_name})
    #         # st.sidebar.button(str(r.run_id if r.run_name is None else r.run_name), r.run_id, type="primary" if r.run_id == st.session_state["auto_rag_assistant_run_id"] else "secondary", on_click=load_history, args=[r.run_id], use_container_width=True)
    return JSONResponse(sessions)

@app.get("/sessions/{run_id}/history")
def get_sessions_history(run_id):
    auto_rag_assistant = get_auto_rag_assistant(run_id=run_id)
    print(len(auto_rag_assistant.storage.get_all_runs()))
    assistant_chat_history = auto_rag_assistant.memory.get_chat_history()
    print(auto_rag_assistant.run_id)
    print(assistant_chat_history)
    return JSONResponse(assistant_chat_history) 