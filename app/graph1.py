# Node implementations

# from typing import Annotated, List, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
# from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from pprint import pprint
from app.tech_questions import llm
import ast

from app.state import ChatbotState
from app.tech_questions import generate_tech_questions
from app.utils import validate_candidate_info
from app.prompts import (
    TECH_QUESTION_PROMPT,
    TECH_STACK_PROMPT,
    THANK_YOU_PROMPT,
    FALLBACK_PROMPT,
    GREETING_PROMPT,
    INFO_COLLECTION_PROMPT,
    VALIDATE_CANDIDATE_INFO_PROMPT
                         )

def greet_and_consent(state: ChatbotState) -> Command:
    print("---- GREETING ----")
    # last_msg = state["messages"][-1]
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        return Command(update=state, goto="end")
    if "consent" in user_input.lower():
        return Command(update=state, goto="collect_info")
    # new_msg = AIMessage(content=GREETING_PROMPT)
    # return Command(update={**state, "messages": state["messages"] + [new_msg]}, goto="greet_and_consent")
    return Command(update = state, goto= "collect_info")

# def collect_candidate_info(state: ChatbotState) -> Command:
#     print("---- COLLECT CANDIDATE INFO ----")
    
#     name = input('Name: ').strip()
#     if name.lower() == "exit":
#         return Command(update=state, goto="end")
    
#     email = input('Email: ').strip()
#     phone = input('Phone: ').strip()
#     years_experience = input('Years of experience: ').strip()
#     desired_position = input('Desired position: ').strip()
#     location = input('Location: ').strip()
    
#     candidate_info = {
#         "name": name,
#         "email": email,
#         "phone": phone,
#         "years_experience": years_experience,
#         "desired_position": desired_position,
#         "location": location
#     }
    
#     # ✅ Validate using LLM
#     validation_result = validate_candidate_info(candidate_info, llm)
    
#     if not validation_result.get("valid", False):
#         error_msg = validation_result.get("error", "Invalid input.")
#         print(f"❌ Validation Failed: {error_msg}")
#         # You could also append an AIMessage to the state["messages"] if needed
#         return Command(update=state, goto="collect_info")
    
#     # ✅ If valid, update and go to next
#     return Command(update={**state, "candidate_info": candidate_info}, goto="collect_tech_stack")

def collect_candidate_info(state: ChatbotState) -> Command:
    print("---- COLLECT CANDIDATE INFO ----")
    name = input('Name: ').strip()
    if name.lower() == "exit":
        return Command(update={}, goto="end")
    email = input('Email: ').strip()
    phone = input('Phone: ').strip()
    years_experience = input('Years of experience: ').strip()
    desired_position = input('Desired position: ').strip()
    location = input('Location: ').strip()
    candidate_info = {
        "name": name,
        "email": email,
        "phone": phone,
        "years_experience": years_experience,
        "desired_position": desired_position,
        "location": location
    }
    return Command(update={"candidate_info": candidate_info}, goto="validate_candidate_info")

def validate_candidate_info_node(state: ChatbotState) -> Command:
    candidate_info = state.get("candidate_info", {})
    validation_result = validate_candidate_info(candidate_info)
    if not validation_result.get("valid", False):
        error_msg = validation_result.get("error", "Invalid input.")
        print(f"❌ Validation Failed: {error_msg}")
        return Command(update={}, goto="collect_info")
    return Command(update={}, goto="collect_tech_stack")



def collect_tech_stack(state: ChatbotState) -> Command:
    print("---- COLLECT TECH STACK ----")
    user_input = input("Enter your tech stack (comma-separated) or type EXIT: ").strip()
    if user_input.lower() == "exit":
        return Command(update=state, goto="end")
    tech_stack = [t.strip() for t in user_input.split(',') if t.strip()]
    if not tech_stack:
        print("Error: No tech stack provided.")
        # new_msg = AIMessage(content="Please enter at least one technology.")
        return Command(update= state, goto="collect_tech_stack")
    return Command(update={**state, "tech_stack": tech_stack}, goto="generate_questions")

def generate_tech_questions_node(state: ChatbotState) -> Command:
    print("---- GENERATE TECH QUESTIONS ----")
    tech_stack = state.get("tech_stack", [])
    llm_output = generate_tech_questions(tech_stack)
    # Robust parsing
    if isinstance(llm_output, str):
        try:
            question_list = ast.literal_eval(llm_output)
        except Exception as e:
            print(f"Error parsing LLM output: {e}")
            question_list = []
    elif isinstance(llm_output, list):
        question_list = llm_output
    else:
        question_list = []

    # # Now you can safely use question_list[0]
    if question_list:
        print(question_list[0])
    else:
        print("No questions found.")
    # if not isinstance(question_list, list) or not question_list:
    #     print("Error: Failed to generate questions.")
    #     new_msg = AIMessage(content="Could not generate questions. Please re-enter your tech stack.")
    #     return Command(update={"messages": state["messages"] + [new_msg]}, goto="collect_tech_stack")
    first_question = question_list[0]
    # new_msg = AIMessage(content=first_question)
    return Command(update={"questions": question_list, "current_question": 0}, goto="handle_answers")


def ask_questions_and_collect_answers(state: ChatbotState) -> Command:
    print("---- TECHNICAL QUESTIONS ----")
    questions = state.get("questions", [])
    if not questions:
        print("No questions to ask.")
        return Command(update={}, goto="end")

    answers = []
    messages = state.get("messages", []).copy()

    for idx, question in enumerate(questions):
        print(f"Question {idx + 1}: {question}")
        user_answer = input("Your answer (or type EXIT): ").strip()
        if user_answer.lower() == "exit":
            print("Exiting as per user request.")
            # Optionally, record unanswered questions as empty or break
            return Command(
                update={
                    "answers": answers,
                    "current_question": idx,  # Number of questions answered
                    # "messages": messages + [AIMessage(content=question), HumanMessage(content=user_answer)],
                },
                goto="end"
            )
        answers.append(user_answer)
        messages.append(AIMessage(content=question))
        messages.append(HumanMessage(content=user_answer))

    return Command(
        update={
            "answers": answers,
            "current_question": len(questions),
            # "messages": messages,
        },
        goto="end"
    )



def fallback_response(state: ChatbotState) -> Command:
    new_msg = AIMessage(content=FALLBACK_PROMPT)
    print(FALLBACK_PROMPT)
    return Command(update={**state, "messages": state["messages"] + [new_msg]}, goto="fallback")

def end_conversation(state: ChatbotState) -> Command:
    new_msg = AIMessage(content=THANK_YOU_PROMPT)
    print("=== Conversation Ended ===")
    pprint(state)
    return Command(update={**state, "messages": state["messages"] + [new_msg]}, goto=END)


# Build Workflow
workflow = StateGraph(state_schema=ChatbotState)
workflow.add_node("greet_and_consent", greet_and_consent)
workflow.add_node("collect_info", collect_candidate_info)
workflow.add_node("collect_tech_stack", collect_tech_stack)
workflow.add_node("generate_questions", generate_tech_questions_node)
workflow.add_node("handle_answers", ask_questions_and_collect_answers)
# workflow.add_node("fallback", fallback_response)
workflow.add_node("validate_candidate_info",validate_candidate_info_node)
workflow.add_node("end", end_conversation)

# workflow.add_edge("greet_and_consent", "collect_info")
# workflow.add_edge("collect_info", "collect_tech_stack")
# workflow.add_edge("collect_tech_stack", "generate_questions")
# workflow.add_edge("generate_questions", "handle_answers")
# workflow.add_edge("handle_answers", "end")
# workflow.add_edge("fallback", "end")
workflow.set_entry_point("greet_and_consent")
compiled_workflow = workflow.compile()


if __name__ == "__main__":
    input_message = {"role": "user", "content": "Hi"}
    initial_state = {
        "messages": [input_message],
        "answers": [],
        "current_question": 0,
        "questions": [],
        "tech_stack": [],
        "candidate_info": {
            "name": "", "email": "", "phone": "",
            "years_experience": "", "desired_position": "", "location": ""
        }
    }
    result = compiled_workflow.invoke(initial_state)