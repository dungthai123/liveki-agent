"""Topic handling functionality for Chinese conversation topics."""

import json
from typing import Dict, Optional, Tuple
from config import TOPICS_FILE, DEFAULT_WELCOME_MESSAGE

# Load Chinese conversation topics
with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
    CHINESE_TOPICS = json.load(f)


def get_topic_by_ids(category_id: str, topic_id: str) -> Optional[Dict]:
    """Get topic data by category_id and topic_id."""
    for category in CHINESE_TOPICS:
        if category['id'] == category_id:
            for topic_detail in category['topic_details']:
                if topic_detail['topic_id'] == topic_id:
                    return {
                        'category_name': category['regions']['en']['name'],
                        'topic_name': topic_detail['regions']['en']['title'],
                        'description': topic_detail['regions']['en']['description'],
                        'tasks': topic_detail['regions']['en']['tasks'],
                        'prompt': topic_detail['prompt'],
                        'first_message': topic_detail['first_message'],
                        'image_url': topic_detail['image_url']
                    }
    return None


def get_welcome_message(topic_data: Optional[Dict]) -> str:
    """Generate welcome message for Chinese conversation topic."""
    if not topic_data:
        return DEFAULT_WELCOME_MESSAGE
    
    return f""" your first message is {topic_data['first_message']}, speak shortly like in the real conversation, you are a real Chinese, not an AI"""


def create_instructions(topic_data: Optional[Dict]) -> str:
    """Create instructions for the Chinese tutor based on topic data."""
    if topic_data:
        tasks_list = "\n".join([f"- {task}" for task in topic_data['tasks']])
        
        return f"""You are a real Chinese language tutor, not an AI, helping students practice conversation.
TOPIC: {topic_data['topic_name']}
DESCRIPTION: {topic_data['description']}
ROLE & INSTRUCTIONS: {topic_data['prompt']}
PRACTICE TASKS:
{tasks_list}

IMPORTANT GUIDELINES:
- Speak primarily in Chinese (Simplified Chinese characters)
- Use appropriate vocabulary level for beginners learners
- Provide corrections and explanations when needed
- Encourage the student to practice the specific tasks mentioned above
- Be patient and supportive
- Speak in a natural, conversational tone
- Speak shortly like in the real conversation, just one or two sentences
- Provide cultural context when relevant
"""
    else:
        return """You are a Chinese language tutor helping students practice general conversation.
Speak primarily in Chinese (Simplified Chinese characters) and help students practice basic conversation skills.
Speak shortly like in the real conversation, just one or two sentences
Be patient, encouraging, and provide corrections when needed."""


def extract_topic_from_participant(participant) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
    """Extract topic information from participant metadata."""
    category_id = None
    topic_id = None
    topic_data = None
    
    if participant.metadata:
        try:
            participant_metadata = json.loads(participant.metadata)
            category_id = participant_metadata.get('category_id')
            topic_id = participant_metadata.get('topic_id')
            
            if category_id and topic_id:
                topic_data = get_topic_by_ids(category_id, topic_id)
                if topic_data:
                    print(f"📝 Topic: {topic_data['topic_name']} (Category: {topic_data['category_name']})")
                else:
                    print(f"⚠️ Topic not found for category_id: {category_id}, topic_id: {topic_id}")
            else:
                print("⚠️ Missing category_id or topic_id in metadata")
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid JSON in participant metadata: {e}")
    
    return category_id, topic_id, topic_data 