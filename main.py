from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger

app = FastAPI()

# 웹 소켓 클라이언트 관리를 위한 리스트
websocket_clients = []

@app.websocket("/ws") # 웹 소켓을 만드는 부분
async def websocket_endpoint(websocket: WebSocket):
    print(f"client connected : {websocket.client}")
    await websocket.accept()
    await websocket.send_text(f"Welcome client : {websocket.client}")
    
    # 새로운 클라이언트를 리스트에 추가
    websocket_clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"message received : {data} from : {websocket.client}")
            
            # 연결된 모든 클라이언트에게 메시지 전송
            for client in websocket_clients:
                await client.send_text(f"Message text was: {data}")
    except:
        # 클라이언트 연결이 종료되면 리스트에서 제거
        websocket_clients.remove(websocket)
