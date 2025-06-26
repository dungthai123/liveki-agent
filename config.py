"""Configuration settings for the Chinese tutor agent."""

import os
from dotenv import load_dotenv

load_dotenv()

# File paths
TOPICS_FILE = 'TrumChinese.conversation_topics.json'
RECORDINGS_DIR = "conversation_audio"

# LiveKit settings
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Azure settings
AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")

# Audio settings
BACKGROUND_AUDIO_VOLUME = 0.8
THINKING_AUDIO_VOLUME_1 = 0.8
THINKING_AUDIO_VOLUME_2 = 0.7
AUDIO_FILE_TYPE = "OGG"
RECORDING_PATH_PREFIX = "livekit-recordings"

# STT/TTS/LLM settings
STT_MODEL = "gpt-4o-mini-transcribe"
STT_LANGUAGE = "zh"
LLM_MODEL = "gpt-4o-mini-realtime-preview"
TTS_MODEL = "coral"

# VAD settings
VAD_THRESHOLD = 0.65
VAD_SILENCE_DURATION = 600
VAD_PREFIX_PADDING = 300
VAD_MIN_SPEECH_DURATION = 0.1
VAD_MIN_SILENCE_DURATION = 0.7
VAD_ACTIVATION_THRESHOLD = 0.65
VAD_SAMPLE_RATE = 16000

# Default messages
DEFAULT_WELCOME_MESSAGE = "你好！欢迎来练习中文对话！我们开始吧。" 