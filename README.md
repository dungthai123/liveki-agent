# Chinese Tutor Agent - Backend

## 📁 Project Structure

```
backend/
├── agent.py                 # Main entrypoint - orchestrates all components
├── config.py               # Configuration settings and environment variables
├── topic_handler.py        # Topic management and extraction logic
├── chinese_tutor.py        # AI tutor agent class with student tracking
├── session_manager.py      # LiveKit session configuration
├── audio_handler.py        # Audio recording and background audio
├── db_driver.py           # Database operations
├── server.py              # Flask API server
└── TrumChinese.conversation_topics.json  # Topic data
```

## 🔧 Module Responsibilities

### `agent.py` - Main Orchestrator

- **Purpose**: Entry point that coordinates all other modules
- **Key Functions**:
  - `entrypoint()`: Main async function that sets up and runs the agent
- **Responsibilities**:
  - Connect to LiveKit room
  - Extract topic from participant metadata
  - Create tutor and session
  - Set up audio recording and transcript saving
  - Handle speech events
  - Send welcome message

### `config.py` - Configuration Management

- **Purpose**: Centralized configuration and environment variables
- **Contains**:
  - File paths and directories
  - LiveKit and Azure settings
  - Audio/STT/TTS/LLM configurations
  - VAD (Voice Activity Detection) parameters
  - Default messages

### `topic_handler.py` - Topic Management

- **Purpose**: Handle Chinese conversation topics and participant metadata
- **Key Functions**:
  - `get_topic_by_ids()`: Retrieve topic data from JSON
  - `extract_topic_from_participant()`: Parse participant metadata
  - `get_welcome_message()`: Generate topic-specific welcome messages
  - `create_instructions()`: Create AI instructions based on topic

### `chinese_tutor.py` - AI Agent Class

- **Purpose**: Main AI tutor agent with student tracking
- **Key Features**:
  - Topic-specific instructions
  - Student profile management
  - Function tools for database operations
- **Methods**:
  - `lookup_student()`: Find student by name
  - `get_student_str()`: Format student details
  - `has_student()`: Check if student is registered

### `session_manager.py` - LiveKit Session Setup

- **Purpose**: Configure LiveKit AgentSession with proper models
- **Key Functions**:
  - `create_agent_session()`: Set up STT, LLM, TTS, VAD
- **Features**:
  - OpenAI Realtime model configuration
  - Chinese language STT setup
  - Voice Activity Detection tuning
  - Turn detection settings

### `audio_handler.py` - Audio Processing

- **Purpose**: Handle audio recording and background audio
- **Key Functions**:
  - `setup_audio_recording()`: Start session recording to Azure
  - `create_transcript_saver()`: Save conversation transcripts
  - `create_background_audio()`: Set up ambient and thinking sounds
- **Features**:
  - Azure Blob Storage integration
  - Automatic transcript generation
  - Background audio management

## 🚀 How It Works

### 1. Initialization Flow

```python
# agent.py coordinates everything
participant = await ctx.wait_for_participant()
category_id, topic_id, topic_data = extract_topic_from_participant(participant)
tutor = ChineseTutor(topic_data=topic_data)
session = create_agent_session()
```

### 2. Topic Processing

```python
# topic_handler.py extracts and processes topics
topic_data = get_topic_by_ids(category_id, topic_id)
instructions = create_instructions(topic_data)
welcome_message = get_welcome_message(topic_data)
```

### 3. Session Setup

```python
# session_manager.py configures the AI models
session = AgentSession(
    llm=openai.realtime.RealtimeModel(...),
    vad=silero.VAD.load(...)
)
```

### 4. Audio & Recording

```python
# audio_handler.py manages audio features
await setup_audio_recording(ctx)
background_audio = create_background_audio()
save_transcript = create_transcript_saver(...)
```

## 🎯 Benefits of This Architecture

### **Modularity**

- Each module has a single responsibility
- Easy to test individual components
- Clear separation of concerns

### **Maintainability**

- Configuration centralized in one place
- Easy to modify specific features
- Reduced code duplication

### **Scalability**

- Easy to add new features to specific modules
- Can extend functionality without touching main logic
- Modular imports allow for lazy loading

### **Readability**

- Main `agent.py` is now clean and focused
- Each module is self-contained and documented
- Clear import structure shows dependencies

## 🔄 Development Workflow

### Adding New Features

1. **New topic types**: Modify `topic_handler.py`
2. **Audio features**: Extend `audio_handler.py`
3. **AI capabilities**: Update `chinese_tutor.py`
4. **Configuration**: Add to `config.py`

### Testing Individual Modules

```python
# Test topic handling
from topic_handler import get_topic_by_ids
topic = get_topic_by_ids(1, 36)

# Test session creation
from session_manager import create_agent_session
session = create_agent_session()
```

### Environment Setup

1. Copy configuration from `config.py`
2. Set environment variables in `.env`
3. Run `python agent.py dev` for development

This modular structure makes the codebase much more maintainable and easier to understand! 🎉
# liveki-agent
# liveki-agent
# liveki-agent
