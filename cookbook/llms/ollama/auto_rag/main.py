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
    auto_rag_assistant: Assistant = get_auto_rag_assistant()
    sessions = []

    if auto_rag_assistant.storage:
        rag_runs: List[AssistantRun] = auto_rag_assistant.storage.get_all_runs()

        for r in rag_runs:
            sessions.append({"run_id":r.run_id,"run_name":r.run_name})
    return JSONResponse(sessions)

@app.get("/sessions/{run_id}/history")
def get_sessions_history(run_id):
    auto_rag_assistant = get_auto_rag_assistant(run_id=run_id)
    auto_rag_assistant.read_from_storage()

    assistant_chat_history = auto_rag_assistant.memory.get_chat_history()
    print(auto_rag_assistant.run_id)
    print("hist len:",len(assistant_chat_history))
    return JSONResponse(assistant_chat_history) 