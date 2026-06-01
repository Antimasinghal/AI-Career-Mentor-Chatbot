import os
import google.generativeai as genai
from prompts import SYSTEM_PROMPT, ROADMAP_PROMPT, INTERVIEW_PROMPT, RESUME_FEEDBACK_PROMPT
from knowledge_retriever import get_relevant_knowledge

# Secure default key (fallback if none is set via env/UI)
CURRENT_KEY = os.getenv("GOOGLE_API_KEY")

def configure_api(api_key=None):
    """
    Configures the Google Generative AI API client.
    Remembers and persists custom keys across all modular backend calls.
    """
    global CURRENT_KEY
    if api_key:
        CURRENT_KEY = api_key.strip()
    if not CURRENT_KEY:
        CURRENT_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    if not CURRENT_KEY:
        raise ValueError("Gemini API key is required. Set GEMINI_API_KEY in .env or enter it in the sidebar.")
    genai.configure(api_key=CURRENT_KEY)
    print(f"Using Gemini API Key: {CURRENT_KEY}")  # Debug log
    return CURRENT_KEY


def get_response(user_input, chat_history=None, user_profile=None, model_name="gemini-3.5-flash"):
    """
    Generates a conversational response for the career mentor.
    Integrates RAG context and user profiles.
    
    chat_history: list of dicts with {"role": "user"|"model", "content": str}
    user_profile: dict with user details (education, goal, skills, time_avail)
    """
    # 1. Configure the API client
    configure_api()
    
    # 2. Get RAG context from the knowledge base based on the query
    kb_context = get_relevant_knowledge(user_input)
    
    # 3. Format user profile context if available
    profile_context = ""
    if user_profile:
        p_edu = user_profile.get("education", "Not specified")
        p_goal = user_profile.get("goal", "Not specified")
        p_skills = user_profile.get("skills", "Not specified")
        p_time = user_profile.get("time_avail", "Not specified")
        
        profile_context = f"""
Student Profile:
- Current Education: {p_edu}
- Target Career Goal: {p_goal}
- Existing Skills: {p_skills}
- Time Availability: {p_time}
"""

    # 4. Construct the full system instruction
    full_system_instruction = f"""
{SYSTEM_PROMPT}

{profile_context}

Knowledge Base Reference Context:
{kb_context}
"""

    # 5. Initialize the generative model with system instructions
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=full_system_instruction
    )

    # 6. Build the full conversation history for the Gemini API
    cumulative_messages = []
    if chat_history:
        for msg in chat_history:
            history_role = "assistant" if msg["role"] == "model" else msg["role"]
            if history_role in ["user", "assistant"]:
                cumulative_messages.append({
                    "role": history_role,
                    "parts": [msg["content"]]
                })

    cumulative_messages.append({
        "role": "user",
        "parts": [user_input]
    })

    # 7. Generate response using the stateless conversation API
    response = model.generate_content(cumulative_messages)
    response_text = response.text 
    print(f"LLM Response: {response_text}")  # Debug log

    if not response_text.strip():
        return "I could not generate a response. Please try again or recheck your API key."

    return response_text

def generate_roadmap(goal, education, skills, time_avail, model_name="gemini-3.5-flash"):
    """
    Calls the LLM to generate a career roadmap in JSON format.
    """
    configure_api()
    
    # Retrieve RAG knowledge context based on the goal
    kb_context = get_relevant_knowledge(goal)
    
    model = genai.GenerativeModel(model_name=model_name)
    
    prompt = ROADMAP_PROMPT.format(
        goal=goal,
        education=education,
        skills=skills,
        time_avail=time_avail,
        kb_context=kb_context
    )
    
    # Request JSON generation
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    return response.text

def get_resume_feedback(resume_text, target_role, model_name="gemini-3.5-flash"):
    """
    Calls the LLM to analyze the resume text and generate structured feedback.
    """
    configure_api()
    
    kb_context = get_relevant_knowledge(target_role)
    
    model = genai.GenerativeModel(model_name=model_name)
    
    prompt = RESUME_FEEDBACK_PROMPT.format(
        target_role=target_role,
        kb_context=kb_context,
        resume_text=resume_text
    )
    
    response = model.generate_content(prompt)
    return response.text

def run_interview_turn(user_answer, role, level, chat_history=None, model_name="gemini-3.5-flash"):
    """
    Runs a turn of the interview simulation.
    
    user_answer: The user's response to the last question. If empty/None, start the interview.
    chat_history: list of previous questions and answers in this interview.
    """
    configure_api()
    
    model = genai.GenerativeModel(model_name=model_name)
    
    # Format current chat history
    history_str = ""
    if chat_history:
        for msg in chat_history:
            history_str += f"{msg['role'].upper()}: {msg['content']}\n"
            
    system_instruction = INTERVIEW_PROMPT.format(role=role, level=level)
    
    if not user_answer:
        # Start of interview
        prompt = f"""
        {system_instruction}
        
        Candidate has entered the interview room. Greet them and ask the first question.
        """
    else:
        # Mid-interview
        prompt = f"""
        {system_instruction}
        
        Previous Conversation Logs:
        {history_str}
        
        Candidate's Latest Answer:
        "{user_answer}"
        
        Evaluate this answer (Strengths, Flaws/Improvements, Score out of 10), then ask the NEXT question.
        """
        
    response = model.generate_content(prompt)
    return response.text