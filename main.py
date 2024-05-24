from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.logger import logger

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/client")
async def client(request: Request):
    return templates.TemplateResponse("client.html", {"request":request})

# 웹 소켓 클라이언트 관리를 위한 리스트
websocket_clients = []

@app.websocket("/ws")
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


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

