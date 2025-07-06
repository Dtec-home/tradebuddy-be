from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, bots, trading, websocket, api_keys

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bots.router, prefix="/bots", tags=["bots"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])