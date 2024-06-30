from lib.common import get_auto_rag_assistant
# import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse, StreamingResponse
from phi.assistant import Assistant
from phi.assistant.run import AssistantRun
from typing import Generator, List, Annotated
from pydantic import BaseModel

# from assistant import get_auto_rag_assistant  # type: ignore

app = FastAPI(redoc_url=None)
class User(BaseModel):
    user_id: str


@app.get("/")
def get_root():
    return {"health":"online"}

'''
retrieve all sessions with run id and name
'''
@app.get("/sessions")
def get_sessions(user_id: Annotated[str | None, Header()] = None):
    """
    Get all sessions by user id. Returns everything if no user id
    """
    auto_rag_assistant: Assistant = get_auto_rag_assistant(user_id=user_id)
    sessions = []

    if auto_rag_assistant.storage:
        rag_runs: List[AssistantRun] = auto_rag_assistant.storage.get_all_runs(user_id=user_id)

        for r in rag_runs:
            sessions.append({"run_id":r.run_id,"run_name":r.run_name,"user_id":r.user_id})
    return JSONResponse(sessions)

'''
create new session
'''
@app.post("/sessions")
def post_sessions(user_id: Annotated[str | None, Header()] = None):
    auto_rag_assistant: Assistant = get_auto_rag_assistant(user_id=user_id)
    run_id: Optional[str] = auto_rag_assistant.create_run()
    auto_rag_assistant.rename_run("New convo..")
    if run_id is None:
        raise HTTPException(status_code=500, detail="Failed to create assistant run")
    print(f"Created Assistant Run: {run_id}")
    return {"run_id":run_id, "run_name":auto_rag_assistant.run_name}

'''
retrieve chat history of a session {run_id}
'''
@app.get("/sessions/{run_id}/history")
def get_sessions_history(run_id):
    auto_rag_assistant = get_auto_rag_assistant(run_id=run_id)
    auto_rag_assistant.read_from_storage()

    assistant_chat_history = auto_rag_assistant.memory.get_chat_history()
    print(auto_rag_assistant.run_id)
    print("hist len:",len(assistant_chat_history))
    return JSONResponse(assistant_chat_history) 

'''
post query to rag
'''
class ChatRequest(BaseModel):
    message: str
    user_id: str

@app.post("/sessions/{run_id}/chat")
def post_chat(run_id, body: ChatRequest):
    auto_rag_assistant = get_auto_rag_assistant(run_id=run_id)
    auto_rag_assistant.read_from_storage()
    
    return StreamingResponse(
        chat_response_streamer(auto_rag_assistant, body.message),
        media_type="text/event-stream",
    )   

def chat_response_streamer(assistant: Assistant, message: str) -> Generator:
    yield "{\"run_name\":\"" + str(assistant.run_name) + "\"}"
    for chunk in assistant.run(message):
        yield chunk


@app.get("/kb")
def get_kb():
    return "hello"