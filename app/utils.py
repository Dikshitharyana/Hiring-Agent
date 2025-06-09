import ast
from app.prompts import VALIDATE_CANDIDATE_INFO_PROMPT,VALIDATE_TECH_STACK_PROMPT
from app.state import CandidateInfo
from langchain_core.messages import HumanMessage
from app.tech_questions import llm

def validate_candidate_info(candidate_info: CandidateInfo) -> dict:
    """
    Uses an LLM to validate candidate info.
    Returns {'valid': True} or {'valid': False, 'error': '...'}
    """
    prompt = VALIDATE_CANDIDATE_INFO_PROMPT.format(
        name=candidate_info.get("name", ""),
        email=candidate_info.get("email", ""),
        phone=candidate_info.get("phone", ""),
        years_experience=candidate_info.get("years_experience", ""),
        desired_position=candidate_info.get("desired_position", ""),
        location=candidate_info.get("location", "")
    )
    # Call the LLM (using invoke for synchronous call)
    response = llm.invoke([HumanMessage(content=prompt)])
    # The LLM should return a string like "{'valid': True}" or "{'valid': False, 'error': '...'}"
    content = response.content if hasattr(response, "content") else str(response)
    try:
        result = ast.literal_eval(content)
        # Ensure result is a dict with 'valid' key
        if isinstance(result, dict) and "valid" in result:
            return result
    except Exception as e:
        # Fallback if LLM output is not as expected
        return {'valid': False, 'error': f"Could not parse LLM output: {content}"}
    return {'valid': False, 'error': "Unknown LLM error."}

def validate_tech_stack(tech_stack) -> dict:
    """
    Uses an LLM to validate the provided tech stack.
    Returns {'valid': True} if the LLM understands the tech stack,
    or {'valid': False, 'error': '...'} with a constructive message.
    """
    tech_stack_str = ", ".join(tech_stack)
    prompt = VALIDATE_TECH_STACK_PROMPT.format(tech_stack=tech_stack_str)
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content if hasattr(response, "content") else str(response)
    try:
        result = ast.literal_eval(content)
        if isinstance(result, dict) and "valid" in result:
            return result
    except Exception:
        return {
            'valid': False,
            'error': (
                f"Sorry, there was an issue understanding your tech stack: {content}.\n"
                "Please check your entries or try rephrasing your technologies."
            )
        }
    return {
        'valid': False,
        'error': (
            "Unknown error while validating your tech stack. "
            "Please enter commonly used technologies (e.g., Python, React, AWS)."
        )
    }



if __name__ == "__main__":
    # Assume llm is your loaded LLM object (e.g., OpenAI, Together, etc.)
    candidate_info = {
        "name": "Jane Doe",
        "email": "jane@example.in",
        "phone": "1234567890",
        "years_experience": "5",
        "desired_position": "Software Engineer",
        "location": "New York"
    }
    # result = validate_candidate_info(candidate_info, llm)
    # print(result)  # {'valid': True} or {'valid': False, 'error': '...'}
    # if result["valid"]:
    #     print("yes")
    tech_stack = ["Python", "Langoggg", "Streamt"]
    result = validate_tech_stack(tech_stack, llm)
    print(result)
    if result.get("valid"):
        print("Tech stack is valid and understood by the LLM.")
    else:
        print(f"Validation failed: {result.get('error')}")