"""Audio handling functionality for recording and background audio."""

import os
from datetime import datetime
from typing import Dict, Optional, Callable

from livekit.agents import (
    BackgroundAudioPlayer, AudioConfig, BuiltinAudioClip, AgentSession
)

from config import (
    RECORDINGS_DIR, BACKGROUND_AUDIO_VOLUME, THINKING_AUDIO_VOLUME_1, 
    THINKING_AUDIO_VOLUME_2
)
from chinese_tutor import ChineseTutor


def create_transcript_saver(
    ctx, 
    category_id: Optional[str], 
    topic_id: Optional[str], 
    topic_data: Optional[Dict], 
    tutor: ChineseTutor, 
    session: AgentSession
) -> Callable:
    """Create a transcript saving callback function."""
    
    async def save_transcript():
        try:
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            transcript_filename = f"{RECORDINGS_DIR}/transcript_{ctx.room.name}_{current_date}.json"
            
            transcript_data = {
                "room_name": ctx.room.name,
                "category_id": category_id,
                "topic_id": topic_id,
                "topic_name": topic_data['topic_name'] if topic_data else "General Chinese",
                "category_name": topic_data['category_name'] if topic_data else "General",
                "timestamp": current_date,
                "student_details": tutor._student_details if tutor.has_student() else None,
                "conversation_history": session.history.to_dict() if hasattr(session, 'history') else []
            }
            
            import json
            with open(transcript_filename, 'w', encoding='utf-8') as f:
                json.dump(transcript_data, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Transcript saved: {transcript_filename}")
            
        except Exception as e:
            print(f"❌ Failed to save transcript: {e}")
    
    return save_transcript


def create_background_audio() -> BackgroundAudioPlayer:
    """Create and configure background audio player."""
    return BackgroundAudioPlayer(
        ambient_sound=AudioConfig(BuiltinAudioClip.OFFICE_AMBIENCE, volume=BACKGROUND_AUDIO_VOLUME),
        thinking_sound=[
            AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING, volume=THINKING_AUDIO_VOLUME_1),
            AudioConfig(BuiltinAudioClip.KEYBOARD_TYPING2, volume=THINKING_AUDIO_VOLUME_2),
        ],
    ) 