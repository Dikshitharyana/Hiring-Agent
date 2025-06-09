from typing import Annotated, List, TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

# State definitions
class CandidateInfo(TypedDict):
    name: str
    email: str
    phone: str
    years_experience: str
    desired_position: str
    location: str

class ChatbotState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    candidate_info: CandidateInfo
    tech_stack: List[str]
    questions: List[str]
    current_question: int
    answers: List[str]