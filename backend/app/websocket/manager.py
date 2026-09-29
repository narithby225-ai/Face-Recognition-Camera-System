"""
WebSocket Manager
Real-time communication using Socket.IO
"""

import socketio
from typing import Dict, Any

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',  # Configure this properly in production
    logger=True,
    engineio_logger=True
)


# Connected clients
active_connections: Dict[str, Any] = {}


@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    active_connections[sid] = {
        "connected_at": None,
        "user_id": None
    }
    await sio.emit('connection_established', {'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")
    if sid in active_connections:
        del active_connections[sid]


@sio.event
async def start_recognition(sid, data):
    """Start face recognition"""
    print(f"Start recognition request from {sid}: {data}")
    # TODO: Implement face recognition start
    await sio.emit('recognition_started', {'camera_id': data.get('camera_id', 0)}, room=sid)


@sio.event
async def stop_recognition(sid):
    """Stop face recognition"""
    print(f"Stop recognition request from {sid}")
    # TODO: Implement face recognition stop
    await sio.emit('recognition_stopped', {}, room=sid)


@sio.event
async def update_settings(sid, data):
    """Update recognition settings"""
    print(f"Update settings from {sid}: {data}")
    await sio.emit('settings_updated', data, room=sid)


# Helper functions to emit events to clients

async def emit_face_detected(faces: list):
    """Emit face detection event to all clients"""
    await sio.emit('face_detected', {'faces': faces})


async def emit_person_recognized(student_id: int, name: str, confidence: float):
    """Emit person recognition event"""
    await sio.emit('person_recognized', {
        'student_id': student_id,
        'name': name,
        'confidence': confidence
    })


async def emit_attendance_marked(student_id: int, name: str, timestamp: str):
    """Emit attendance marked event"""
    await sio.emit('attendance_marked', {
        'student_id': student_id,
        'name': name,
        'timestamp': timestamp,
        'status': 'present'
    })


async def emit_camera_frame(frame_data: str):
    """Emit camera frame to all clients"""
    await sio.emit('camera_frame', {'frame': frame_data})


async def emit_camera_error(error: str):
    """Emit camera error to all clients"""
    await sio.emit('camera_error', {'error': error})
