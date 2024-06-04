from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class GroupDTO(BaseModel):
    username: str
    groupname: str

# 웹 소켓 클라이언트 및 그룹 관리를 위한 딕셔너리
websocket_clients = {}
websocket_group = {}

@app.get("/client", response_class=HTMLResponse)
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request": request})

@app.post("/createGroup")
async def create_group(payload: GroupDTO):
    if payload.groupname not in websocket_group:
        websocket_group[payload.groupname] = []
    websocket_group[payload.groupname].append(payload.username)
    return {"groupname": payload.groupname}

@app.post("/joinGroup")
async def join_group(payload: GroupDTO):
    if payload.groupname in websocket_group:
        websocket_group[payload.groupname].append(payload.username)
    return {"groupname": payload.groupname}

@app.websocket("/ws/{username}/{groupname}")
async def websocket_endpoint(websocket: WebSocket, username: str, groupname: str):
    await websocket.accept()
    print(f"Client connected: {username}")
    
    if groupname not in websocket_group:
        websocket_group[groupname] = []
    websocket_group[groupname].append(username)
    
    websocket_clients[username] = websocket
    
    try:
        await websocket.send_text(f"Welcome to the group {groupname}, {username}")
        while True:
            data = await websocket.receive_text()
            print(f"Message received: {data} from {username}")
            
            # 같은 그룹의 유저에게만 메시지 전송
            for member in websocket_group[groupname]:
                if member != username and member in websocket_clients:
                    await websocket_clients[member].send_text(f"{username}: {data}")
    except Exception as e:
        print(f"Connection closed for {username}: {e}")
    finally:
        # 클라이언트 연결이 종료되면 리스트에서 제거
        websocket_group[groupname].remove(username)
        del websocket_clients[username]
        print(f"Client {username} disconnected")

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()
