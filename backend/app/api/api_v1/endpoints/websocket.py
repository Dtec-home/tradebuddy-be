from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from jose import jwt, JWTError
from app.core.config import settings
from app.core.websocket import websocket_manager
import asyncio

router = APIRouter()


async def get_current_user_from_websocket(websocket: WebSocket):
    """Extract and validate user from WebSocket connection"""
    try:
        # Get token from query params or headers
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
            
        # Decode token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
            
        return str(user_id)
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None


@router.websocket("/connect")
async def websocket_endpoint(websocket: WebSocket):
    user_id = await get_current_user_from_websocket(websocket)
    if not user_id:
        return
        
    await websocket_manager.connect(websocket, user_id)
    
    try:
        # Send initial connection message
        await websocket_manager.send_personal_message(
            {"type": "connection", "status": "connected"},
            user_id
        )
        
        # Keep connection alive
        while True:
            # Wait for any message from client (ping/pong)
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, user_id)