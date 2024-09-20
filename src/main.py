from fastapi import FastAPI
from .api import market_data as market_data_router
from .websockets import websocket_data as websocket_router

app = FastAPI()

# Mount the API routes
app.include_router(market_data_router.router)

# Mount the WebSocket routes
app.include_router(websocket_router.router)
