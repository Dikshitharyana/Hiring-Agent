import streamlit as st
import ast
from app.prompts import VALIDATE_CANDIDATE_INFO_PROMPT, TECH_QUESTION_PROMPT,VALIDATE_TECH_STACK_PROMPT
from app.tech_questions import llm
from app.utils import validate_candidate_info,validate_tech_stack
from app.tech_questions import generate_tech_questions
from langchain_core.messages import HumanMessage
from app.state import CandidateInfo
from app.data_handler import save_candidate_data

# --- Helper: Check for 'exit' command globally ---
def check_exit(user_input):
    if user_input and user_input.strip().lower() == "exit":
        st.warning("You have exited the chatbot. Goodbye!")
        st.stop()


# --- Streamlit App State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = "consent"
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {
        "name": "", "email": "", "phone": "",
        "years_experience": "", "desired_position": "", "location": ""
    }
if "tech_stack" not in st.session_state:
    st.session_state.tech_stack = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "error" not in st.session_state:
    st.session_state.error = ""
if "validating" not in st.session_state:
    st.session_state.validating = False

st.title("TalentScout Hiring Assistant")

# Step 1: Consent
if st.session_state.step == "consent":
    st.write("Welcome to TalentScout! Type 'I consent' to continue or 'exit' to quit.")
    consent = st.chat_input("Type 'I consent' to continue or 'exit' to quit.")
    check_exit(consent)
    if consent:
        if consent.strip().lower() == "i consent":
            st.session_state.step = "candidate_info"
            st.session_state.error = ""
            st.rerun()
        else:
            st.session_state.error = "Please type 'I consent' to proceed."
    if st.session_state.error:
        st.error(st.session_state.error)

# Step 2: Candidate Info Form
elif st.session_state.step == "candidate_info":
    st.write("Please fill in your details below.")
    with st.form("candidate_info_form"):
        name = st.text_input("Name", value=st.session_state.candidate_info["name"])
        check_exit(name)
        email = st.text_input("Email", value=st.session_state.candidate_info["email"])
        check_exit(email)
        phone = st.text_input("Phone", value=st.session_state.candidate_info["phone"])
        check_exit(phone)
        years_experience = st.text_input("Years of Experience", value=st.session_state.candidate_info["years_experience"])
        check_exit(years_experience)
        desired_position = st.text_input("Desired Position", value=st.session_state.candidate_info["desired_position"])
        check_exit(desired_position)
        location = st.text_input("Location", value=st.session_state.candidate_info["location"])
        check_exit(location)

        # Disable submit button during validation
        submit_disabled = st.session_state.get("validating", False)
        submitted = st.form_submit_button("Submit", disabled=submit_disabled)
        if submitted and not submit_disabled:
            st.session_state.validating = True
            st.rerun()

        # Show validating message if needed
        if st.session_state.get("validating", False):
            st.info("Validating your information, please wait...")
            # Only validate once per submission
            if not st.session_state.get("validated_this_run", False):
                candidate_info = {
                    "name": name, "email": email, "phone": phone,
                    "years_experience": years_experience,
                    "desired_position": desired_position,
                    "location": location
                }
                result = validate_candidate_info(candidate_info)
                st.session_state.validated_this_run = True

                if result.get("valid"):
                    st.session_state.candidate_info = candidate_info
                    st.session_state.step = "tech_stack"
                    st.session_state.error = ""
                    st.session_state.validating = False
                    st.session_state.validated_this_run = False
                    st.rerun()
                else:
                    st.session_state.error = (
                        f"❌ Validation failed: {result.get('error')}\n"
                        "Please enter correct details and resubmit."
                    )
                    st.session_state.validating = False
                    st.session_state.validated_this_run = False
                    st.rerun()
        elif st.session_state.error:
            st.error(st.session_state.error)

# # Step 3: Tech Stack
# elif st.session_state.step == "tech_stack":
#     st.write("Please list your tech stack (comma separated). Type 'exit' to quit.")
#     tech_stack_input = st.text_input("Tech Stack", value=", ".join(st.session_state.tech_stack))
#     check_exit(tech_stack_input)
#     if st.button("Submit Tech Stack"):
#         tech_stack = [t.strip() for t in tech_stack_input.split(',') if t.strip()]
#         if tech_stack:
#             st.session_state.tech_stack = tech_stack
#             st.session_state.step = "generate_questions"
#             st.session_state.error = ""
#             st.rerun()
#         else:
#             st.session_state.error = "Please enter at least one technology."
#     if st.session_state.error:
#         st.error(st.session_state.error)

# Step 3: Tech Stack
elif st.session_state.step == "tech_stack":
    st.write("Please list your tech stack (comma separated). Type 'exit' to quit.")

    # Track validation state
    if "tech_stack_validating" not in st.session_state:
        st.session_state.tech_stack_validating = False
    if "tech_stack_validated_this_run" not in st.session_state:
        st.session_state.tech_stack_validated_this_run = False

    # Disable input and button if validating
    input_disabled = st.session_state.tech_stack_validating

    tech_stack_input = st.text_input(
        "Tech Stack",
        value=", ".join(st.session_state.tech_stack),
        disabled=input_disabled
    )
    check_exit(tech_stack_input)

    submit_disabled = input_disabled
    submit = st.button("Submit Tech Stack", disabled=submit_disabled)

    # Handle submission
    if submit and not input_disabled:
        tech_stack = [t.strip() for t in tech_stack_input.split(',') if t.strip()]
        if tech_stack:
            st.session_state.tech_stack = tech_stack
            st.session_state.tech_stack_validating = True
            st.session_state.tech_stack_validated_this_run = False
            st.session_state.error = ""
            st.rerun()
        else:
            st.session_state.error = "Please enter at least one technology."

    # Validation in progress
    if st.session_state.tech_stack_validating:
        st.info("Validating your tech stack, please wait...")
        if not st.session_state.tech_stack_validated_this_run:
            # Call LLM validation
            result = validate_tech_stack(st.session_state.tech_stack)
            st.session_state.tech_stack_validated_this_run = True
            if result.get("valid"):
                st.info("Generating questions for your tech stack...")
                st.session_state.step = "generate_questions"
                st.session_state.tech_stack_validating = False
                st.session_state.tech_stack_validated_this_run = False
                st.session_state.error = ""
                st.rerun()
            else:
                st.session_state.error = (
                    f"❌ Tech stack validation failed: {result.get('error')}\n"
                    "Please re-enter your tech stack using commonly recognized technologies."
                )
                st.session_state.tech_stack_validating = False
                st.session_state.tech_stack_validated_this_run = False
                st.rerun()

    # Show error if present
    if st.session_state.error and not st.session_state.tech_stack_validating:
        st.error(st.session_state.error)


# Step 4: Generate Questions
elif st.session_state.step == "generate_questions":
    questions = generate_tech_questions(st.session_state.tech_stack)
    if isinstance(questions, str):
        try:
            questions = ast.literal_eval(questions)
        except Exception:
            questions = [q.strip() for q in questions.split('\n') if q.strip()]
    if not questions:
        st.session_state.error = "Could not generate questions. Please re-enter your tech stack."
        st.session_state.step = "tech_stack"
        st.rerun()
    else:
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.step = "handle_answers"
        st.rerun()

# Step 5: Handle Answers
elif st.session_state.step == "handle_answers":
    qidx = st.session_state.current_question
    questions = st.session_state.questions
    if qidx < len(questions):
        st.write(f"Question {qidx+1}: {questions[qidx]}")
        answer = st.text_input("Your answer", key=f"answer_{qidx}")
        check_exit(answer)
        if st.button("Submit Answer", key=f"submit_{qidx}"):
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(questions):
                st.session_state.step = "thankyou"
            st.rerun()
    else:
        st.session_state.step = "thankyou"
        st.rerun()

# Step 6: Thank You
elif st.session_state.step == "thankyou":
    # Prepare the data to save
    candidate_record = {
        "Candidate Info": st.session_state.candidate_info,
        "Tech Stack": st.session_state.tech_stack,
        "Questions": st.session_state.questions,
        "Answers": st.session_state.answers
    }
    # Save securely
    save_candidate_data(candidate_record)

    st.success("Thank you for your responses. We will review your application and contact you about next steps. Goodbye!")
    with st.expander("Show Collected Info"):
        st.json(candidate_record)
