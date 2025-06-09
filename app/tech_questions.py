from langchain_core.messages import HumanMessage
from app.prompts import TECH_QUESTION_PROMPT
from langchain_together import ChatTogether
from app.config import TOGETHER_API_KEY

llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")


def generate_tech_questions(tech_stack, num_questions=3):
    prompt = TECH_QUESTION_PROMPT.format(num_questions=num_questions, tech_stack=", ".join(tech_stack))
    # Wrap prompt in a HumanMessage and pass as a list
    response = llm.invoke([HumanMessage(content=prompt)])
    # The model's response is a message object; get its .content
    questions = response.content
    return questions


if __name__ == "__main__":
    question_list = generate_tech_questions(['Python', 'java'])
    print(question_list)