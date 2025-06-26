"""Main entrypoint for the Chinese tutor agent."""

import asyncio
from typing import Optional, Dict

from livekit import agents
from livekit.agents import AutoSubscribe, RoomInputOptions, llm
from livekit.plugins import noise_cancellation

# Import from our modules
from topic_handler import extract_topic_from_participant, get_welcome_message
from chinese_tutor import ChineseTutor
from session_manager import create_agent_session
from audio_handler import  create_transcript_saver, create_background_audio


async def entrypoint(ctx: agents.JobContext):
    """Main entrypoint for the Chinese tutor agent."""
    category_id: Optional[str] = None
    topic_id: Optional[str] = None
    topic_data: Optional[Dict] = None
    
    # Connect to room and extract topic information
    try:
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        participant = await ctx.wait_for_participant()
        category_id, topic_id, topic_data = extract_topic_from_participant(participant)
        
    except Exception as e:
        print(f"⚠️ Failed to get topic from participant metadata: {e}")
        try:
            await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        except Exception as connect_error:
            print(f"❌ Failed to connect to room: {connect_error}")
    
    print(f"🎯 Using topic: {topic_data['topic_name'] if topic_data else 'General Chinese'}")
    
    # Create tutor and session
    tutor = ChineseTutor(topic_data=topic_data)
    session = create_agent_session()
    
    # Set up speech handling
    @session.on("user_speech_committed")
    def on_speech(msg: llm.ChatMessage):
        asyncio.create_task(tutor.handle_user_speech(session, msg))

    # Set up audio recording
    
    # Set up transcript saving
    save_transcript = create_transcript_saver(ctx, category_id, topic_id, topic_data, tutor, session)
    ctx.add_shutdown_callback(save_transcript)

    # Start session
    await session.start(
        room=ctx.room,
        agent=tutor,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    
    # Start background audio
    background_audio = create_background_audio()
    await background_audio.start(room=ctx.room, agent_session=session)

    # Send welcome message
    welcome_message = get_welcome_message(topic_data)
    await session.generate_reply(instructions=welcome_message)


if __name__ == "__main__":
    print("🤖 Running Chinese Tutor Agent with automatic dispatch")
    print("💡 Topic extracted from participant metadata")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))