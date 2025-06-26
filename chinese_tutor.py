"""Chinese tutor agent class with student tracking capabilities."""

from typing import Dict, Optional
from livekit.agents import Agent, function_tool, RunContext
from topic_handler import create_instructions


class ChineseTutor(Agent):
    """Chinese language tutor agent with student tracking capabilities."""
    
    def __init__(self, topic_data: Optional[Dict] = None) -> None:
        instructions = create_instructions(topic_data)
        super().__init__(instructions=instructions)
        
        self.topic_data = topic_data
        self.topic_name = topic_data['topic_name'] if topic_data else "General Chinese"
        self._student_details = self._init_student_details()

    def _init_student_details(self) -> Dict[str, any]:
        """Initialize empty student details."""
        return {
            "name": "",
            "email": "",
            "level": "", 
            "goals": "",
            "lessons_completed": 0
        }

    def get_student_str(self) -> str:
        """Get formatted string of student details."""
        return "\n".join(f"{key}: {value}" for key, value in self._student_details.items())

    def has_student(self) -> bool:
        """Check if student details are available."""
        return bool(self._student_details["name"])

    @function_tool()
    async def get_encouragement(self, context: RunContext) -> str:
        """Provide encouragement and motivation for Chinese language learning.
        
        Returns:
            A motivational message for the student
        """
        return f"Great job practicing {self.topic_name}! Keep up the excellent work. Consistency is key to mastering Chinese!"

    @function_tool()
    async def set_student_name(self, context: RunContext, name: str) -> str:
        """Set the student's name for personalized interaction.
        
        Args:
            name: The name of the student
        """
        self._student_details["name"] = name
        return f"Nice to meet you, {name}! I'm here to help you learn Chinese. Let's start practicing!"

    @function_tool()
    async def get_topic_info(self, context: RunContext) -> str:
        """Get information about the current topic being practiced.
        
        Returns:
            Information about the current topic
        """
        if self.topic_data:
            description = self.topic_data.get('description', "Let's get started!")
            return f"We're practicing: {self.topic_name}. {description}"
        return "We're having a general Chinese conversation. Feel free to ask me anything!" 