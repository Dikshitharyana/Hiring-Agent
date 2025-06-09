#Prompts
TECH_QUESTION_PROMPT = (
    "Generate {num_questions} technical interview questions for a candidate skilled in {tech_stack}. "
    "Return ONLY a valid Python list of strings that is iterable as questions[0] give first question in python, with each question as a separate string in the list. "
    "Do not include any explanations, formatting, or code blocks—just the Python list."
)
GREETING_PROMPT = "Welcome to TalentScout! I am your Hiring Assistant. Before we proceed, please review our privacy policy and consent to data collection. Type 'I consent' to continue."
INFO_COLLECTION_PROMPT = "Let's get started. Please provide the following details:\nFull Name:\nEmail Address:\nPhone Number:\nYears of Experience:\nDesired Position(s):\nCurrent Location:"
TECH_STACK_PROMPT = "Please list the programming languages, frameworks, databases, and tools you are proficient in."
FALLBACK_PROMPT = "I'm sorry, I didn't understand that. Could you please rephrase or provide more details?"
THANK_YOU_PROMPT = "Thank you for your responses. We will review your application and contact you about next steps. Goodbye!"

VALIDATE_CANDIDATE_INFO_PROMPT = (
    "You are an assistant that checks candidate information for a job application. "
    "Given the following details:\n"
    "Name: {name}\n"
    "Email: {email}\n"
    "Phone: {phone}\n"
    "Years of Experience: {years_experience}\n"
    "Desired Position: {desired_position}\n"
    "Location: {location}\n\n"
    "Return ONLY a valid Python dictionary. "
    "If all fields are filled and the email is valid (contains '@'), return {{'valid': True}}. "
    "If any field is missing or the email is invalid, return {{'valid': False, 'error': 'Describe the issue clearly'}}. "
    "Do not include explanations, formatting, or code blocks—just the Python dictionary."
)

VALIDATE_TECH_STACK_PROMPT = (
    "You are an AI assistant helping with technical interviews. "
    "Given the following tech stack: {tech_stack}, can you generate relevant technical questions? "
    "Respond with a Python dictionary: '{{'valid': True}}' if you can, or "
    "{{'valid': False, 'error': 'explanation'}} if you cannot, with a constructive, friendly message.and do not give any exptra information keep the output as the minimal dictionary"
)
