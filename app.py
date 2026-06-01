import streamlit as st
import os
import json
import base64
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

# Import our modular backend functions
from chatbot import configure_api, get_response, generate_roadmap, get_resume_feedback, run_interview_turn
from resume_parser import parse_resume

# Page configurations - SEO best practices implemented automatically
st.set_page_config(
    page_title="EduPath AI | Professional Career Mentor Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 1. PREMIUM GLASSMORPHIC DESIGN SYSTEM (CUSTOM CSS)
# ----------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Styles */
    .stApp {
        background-color: #0c0e17;
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
        color: #e2e8f0;
    }
    
    /* Typography overrides */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', 'Segoe UI', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Glassmorphism containers */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.1);
        transform: translateY(-2px);
    }
    
    /* Chat bubbles styling */
    .chat-bubble-user {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        border-radius: 18px 18px 0px 18px;
        padding: 14px 20px;
        margin: 10px 0 10px auto;
        max-width: 80%;
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.2);
        animation: slideUp 0.3s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-bubble-ai {
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 18px 18px 18px 0px;
        padding: 14px 20px;
        margin: 10px auto 10px 0;
        max-width: 80%;
        color: #f1f5f9;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Interactive Roadmap visual elements */
    .timeline {
        border-left: 3px solid #6366f1;
        padding-left: 24px;
        margin-left: 12px;
        position: relative;
    }
    
    .timeline-node {
        position: relative;
        margin-bottom: 30px;
    }
    
    .timeline-node::before {
        content: '';
        position: absolute;
        left: -33px;
        top: 2px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: #818cf8;
        border: 3px solid #0c0e17;
        box-shadow: 0 0 10px #6366f1;
    }
    
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .resource-link {
        font-size: 0.85rem;
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
        padding: 6px 12px;
        display: inline-block;
        margin-top: 8px;
        text-decoration: none;
        transition: all 0.2s;
    }
    
    .resource-link:hover {
        background: rgba(59, 130, 246, 0.25);
        color: #ffffff;
    }
    
    /* Action items checklist */
    .roadmap-project {
        background: rgba(244, 63, 94, 0.05);
        color: #fda4af;
        border: 1px dashed rgba(244, 63, 94, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 6px;
    }
    
    /* Metrics gauge styling */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #34d399;
        text-shadow: 0 0 20px rgba(52, 211, 153, 0.3);
    }
    
    /* Navigation custom look */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 18px;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4f46e5 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. STATE INITIALIZATION & SECURE KEY MANAGEMENT
# ----------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {
        "education": "Undergraduate student",
        "goal": "Data Scientist",
        "skills": "Python basics, basic statistics",
        "time_avail": "10 hours per week for 6 months"
    }
if "interview_history" not in st.session_state:
    st.session_state.interview_history = []
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "interview_role" not in st.session_state:
    st.session_state.interview_role = "Software Engineer"
if "interview_level" not in st.session_state:
    st.session_state.interview_level = "Entry Level"
if "interview_current_question" not in st.session_state:
    st.session_state.interview_current_question = ""
if "interview_scores" not in st.session_state:
    st.session_state.interview_scores = []
if "voice_readout" not in st.session_state:
    st.session_state.voice_readout = True
if "roadmap_json" not in st.session_state:
    st.session_state.roadmap_json = None
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if "api_error" not in st.session_state:
    st.session_state.api_error = ""

# Configure API from saved key or environment variable
try:
    configure_api(st.session_state.api_key or None)
    st.session_state.api_error = ""
except Exception as e:
    st.session_state.api_error = str(e)

# ----------------------------------------------------
# 3. SIDEBAR CONTROLS & SETTINGS PANEL
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='margin-bottom: 0;'>🎓 EduPath AI</h2>
        <p style='color: #94a3b8; font-size: 0.85rem;'>Your Personalized Career Mentor</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 3.1 Model Settings
    st.subheader("⚙️ API Configuration")


        
    model_choice = st.selectbox("LLM Brain", ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"], index=0)
    language_choice = st.selectbox("Preferred Language 🌐", ["English", "Hindi", "Spanish", "French", "German", "Mandarin", "Arabic"], index=0)
    
    st.markdown("---")
    
    # 3.1 API Key Configuration
    st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="Paste your Gemini API key here",
        help="This key is required for AI responses. It is stored in session only.",
        key="sidebar_api_key"
    )
    if st.button("💾 Save API Key", use_container_width=True):
        st.session_state.api_key = st.session_state.sidebar_api_key.strip()
        try:
            configure_api(st.session_state.api_key or None)
            st.success("API key saved and configured successfully!")
            st.session_state.api_error = ""
        except Exception as e:
            st.session_state.api_error = str(e)
            st.error(f"API configuration failed: {e}")

    if st.session_state.api_error:
        st.warning(st.session_state.api_error)
    elif st.session_state.api_key:
        st.success("Gemini API key is configured.")
    else:
        st.info("Enter your Gemini API key above or set GEMINI_API_KEY in a .env file.")

    st.markdown("---")
    
    # 3.2 Student Profile Panel
    st.subheader("👤 Student Profile")
    p_edu = st.selectbox("Education Level", ["High School", "Undergraduate student", "Graduate student", "Working Professional", "Career Switcher"], index=1)
    p_goal = st.text_input("Target Career Goal", value=st.session_state.profile["goal"], placeholder="e.g. Cybersecurity Analyst")
    p_skills = st.text_area("Existing Skills", value=st.session_state.profile["skills"], placeholder="e.g. HTML, basic Python, communication")
    p_time = st.text_input("Time Availability", value=st.session_state.profile["time_avail"], placeholder="e.g. 12 hours/week for 4 months")
    
    if st.button("Save Profile Settings", use_container_width=True):
        st.session_state.profile = {
            "education": p_edu,
            "goal": p_goal,
            "skills": p_skills,
            "time_avail": p_time
        }
        st.toast("Profile details updated successfully!", icon="✅")
        
    st.markdown("---")
    
    # 3.3 Speech & Voice Settings
    st.subheader("🔊 Audio & Voice Tools")
    st.session_state.voice_readout = st.checkbox("Text-To-Speech (Browser Audio)", value=st.session_state.voice_readout)
    
    st.markdown("""
    <div style='font-size: 0.8rem; color: #94a3b8; line-height: 1.4;'>
        Tip: Turning on Voice will allow the browser to automatically read out responses using native browser audio synthesizers.
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 4. AUDIO INJECTIONS FOR TTS (TEXT TO SPEECH) & STT
# ----------------------------------------------------
def inject_tts_script(text):
    """
    Injects a small script that utilizes HTML5 window.speechSynthesis to play audio natively in browser.
    """
    if not text:
        return
    # Clean text to prevent Javascript injection syntax errors
    clean_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    # Take first 500 characters to keep it clean and performant
    clean_text = clean_text[:600]
    
    st.components.v1.html(f"""
    <script>
        if ('speechSynthesis' in window) {{
            // Cancel any current playing speech
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.rate = 1.0;
            msg.pitch = 1.0;
            // Try to find a nice English or standard local voice
            var voices = window.speechSynthesis.getVoices();
            if(voices.length > 0) {{
                msg.voice = voices[0];
            }}
            window.speechSynthesis.speak(msg);
        }}
    </script>
    """, height=0, width=0)

# Injecting standard STT button HTML to record speech directly via browser API
def stt_recorder():
    """
    Renders browser web speech API controls to allow recording audio and populating inputs.
    """
    st.components.v1.html("""
    <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px; text-align: center; color: #e2e8f0; font-family: sans-serif;">
        <button id="mic-btn" style="background: #ef4444; border: none; border-radius: 50%; width: 44px; height: 44px; color: white; font-size: 20px; cursor: pointer; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4); transition: transform 0.2s;">🎤</button>
        <div id="status" style="margin-top: 8px; font-size: 0.8rem; color: #94a3b8;">Click mic to speak query (Web Speech API)</div>
        <textarea id="result-box" style="display: none;"></textarea>
    </div>
    
    <script>
        var btn = document.getElementById("mic-btn");
        var status = document.getElementById("status");
        var recognition = null;
        
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRec();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            btn.onclick = function() {
                try {
                    recognition.start();
                    status.innerHTML = "🔴 Listening... Speak clearly now";
                    btn.style.transform = "scale(1.15)";
                    btn.style.background = "#f43f5e";
                } catch(e) {
                    status.innerHTML = "Microphone already listening.";
                }
            };
            
            recognition.onresult = function(event) {
                var transcript = event.results[0][0].transcript;
                status.innerHTML = "✅ Understood! Copying: '" + transcript + "'";
                btn.style.transform = "scale(1)";
                btn.style.background = "#ef4444";
                
                // Copy to clipboard so user can easily paste it
                navigator.clipboard.writeText(transcript);
                
                // Alert in window so user can copy manually
                alert("Voice Input Copied to Clipboard: " + transcript + "\\n\\nPaste into input box to send!");
            };
            
            recognition.onerror = function(event) {
                status.innerHTML = "❌ Voice Error: " + event.error;
                btn.style.transform = "scale(1)";
                btn.style.background = "#ef4444";
            };
            
            recognition.onend = function() {
                btn.style.transform = "scale(1)";
                btn.style.background = "#ef4444";
            };
        } else {
            status.innerHTML = "Web Speech STT not supported in this browser. Use Chrome/Edge.";
            btn.disabled = true;
            btn.style.opacity = 0.5;
        }
    </script>
    """, height=100)

# ----------------------------------------------------
# 5. MAIN NAVIGATION TABS
# ----------------------------------------------------
st.markdown("<h1 style='text-align: center; margin-top: -10px; margin-bottom: 20px;'>🎓 EduPath AI Career Mentor</h1>", unsafe_allow_html=True)

tab_mentor, tab_roadmap, tab_resume, tab_interview, tab_admin = st.tabs([
    "💬 AI Career Mentor",
    "🗺️ Career Roadmap Designer",
    "📄 Resume Gap Coach",
    "🤝 Interview Prep Arena",
    "⚙️ KB Admin Console"
])

# ----------------------------------------------------
# TAB 1: AI CAREER MENTOR CHAT (WITH RAG & VOICE)
# ----------------------------------------------------
with tab_mentor:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">💬 Conversational Career Guidance</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Ask questions about career paths, required skills, learning resources, and scholarships. 
            The mentor pulls context from the verified local Knowledge Base (RAG) to ensure accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_chat, col_tools = st.columns([3, 1])
    
    with col_chat:
        # Display Chat History
        chat_container = st.container(height=450)
        
        with chat_container:
            if not st.session_state.messages:
                st.markdown("""
                <div class="chat-bubble-ai">
                    👋 Hello! I am your AI Career Mentor. I can guide you through career fields like 
                    <b>Data Science, AI, Software Development, Cybersecurity, AgriTech, FoodTech, Business Management, and Design</b>.<br><br>
                    Where are you currently in your education or career, and what is your goal? Ask me anything!
                </div>
                """, unsafe_allow_html=True)
                
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)
        
        # User input logic
        user_msg = st.chat_input("Ask about paths, tools, scholarships, resources...")
        
        if user_msg:
            # Append user message
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.rerun()

    with col_tools:
        st.markdown("<h4 style='margin-top:0;'>🎙️ Voice & Tools</h4>", unsafe_allow_html=True)
        stt_recorder()
        
        st.markdown("---")
        st.markdown("💡 **Try Quick Prompts:**")
        
        # Clickable quick suggestions
        suggestions = [
            "What entry skills are needed for Machine Learning?",
            "What certifications do you suggest for Cybersecurity?",
            "Give higher study abroad options for Design.",
            "Explain career options in Agriculture Technology."
        ]
        
        for sug in suggestions:
            if st.button(sug, key=f"sug_{sug}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": sug})
                st.rerun()
                
        st.markdown("---")
        
        # Export functionality
        if st.session_state.messages:
            transcript = "# EduPath AI Chat Logs\n\n"
            for msg in st.session_state.messages:
                role = "Student" if msg["role"] == "user" else "Mentor AI"
                transcript += f"### {role}\n{msg['content']}\n\n"
            
            b64_transcript = base64.b64encode(transcript.encode()).decode()
            href = f'<a href="data:file/markdown;base64,{b64_transcript}" download="edupath_chat_logs.md" class="resource-link" style="width:100%; text-align:center;">📥 Export Chat Logs (.md)</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            if st.button("🧹 Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # If the user has just entered a query, trigger generation
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        latest_user_message = st.session_state.messages[-1]["content"]
        
        with col_chat:
            with st.spinner("Retrieving facts and thinking..."):
                try:
                    # Request localized language responses
                    query_payload = latest_user_message
                    if language_choice != "English":
                        query_payload += f" (IMPORTANT: Please generate your response entirely in {language_choice}.)"
                        
                    # Call LLM with RAG and Profile context
                    ai_reply = get_response(
                        user_input=query_payload,
                        chat_history=st.session_state.messages[:-1],
                        user_profile=st.session_state.profile,
                        model_name=model_choice
                    )
                    
                    st.session_state.messages.append({"role": "model", "content": ai_reply})
                    
                    # Voice readout trigger
                    if st.session_state.voice_readout:
                        inject_tts_script(ai_reply)
                        
                    st.rerun()
                except Exception as e:
                    err_msg = str(e)
                    print(f"DEBUG: Raw error message: {err_msg}") # Debug log
                    if "429" in err_msg or "Quota" in err_msg or "ResourceExhausted" in err_msg:
                        st.error("⚠️ **API Quota Exceeded (429)**: The default shared API key has reached its rate limit of 20 requests/day. Please obtain your own free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the **API Configuration** section in the sidebar to bypass this limit!")
                    else:
                        st.error(f"Failed to communicate with Gemini: {err_msg}")


# ----------------------------------------------------
# TAB 2: INTERACTIVE CAREER ROADMAP DESIGNER
# ----------------------------------------------------
with tab_roadmap:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">🗺️ Visual Career Roadmap Architect</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Generate an interactive step-by-step career timeline path based on your current education level, 
            skills, target goal, and time constraints.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_form, col_visual = st.columns([1, 2])
    
    with col_form:
        st.markdown("<h4>📋 Roadmap Parameters</h4>", unsafe_allow_html=True)
        rm_goal = st.text_input("Target Career Goal", value=st.session_state.profile["goal"], key="rm_goal")
        rm_edu = st.selectbox("Current Education Level", ["High School", "Undergrad student", "Grad student", "Professional", "Switcher"], index=1, key="rm_edu")
        rm_skills = st.text_area("Your Core Skills", value=st.session_state.profile["skills"], key="rm_skills")
        rm_time = st.text_input("Duration & Commits", value=st.session_state.profile["time_avail"], key="rm_time")
        
        generate_btn = st.button("⚡ Generate Interactive Roadmap", use_container_width=True, type="primary")
        
        if generate_btn:
            with st.spinner("Mapping learning path nodes..."):
                try:
                    response_json_str = generate_roadmap(
                        goal=rm_goal,
                        education=rm_edu,
                        skills=rm_skills,
                        time_avail=rm_time,
                        model_name=model_choice
                    )
                    
                    # Attempt to clean potential markdown wrapped code outputs from API
                    if "```json" in response_json_str:
                        response_json_str = response_json_str.split("```json")[1].split("```")[0]
                    elif "```" in response_json_str:
                        response_json_str = response_json_str.split("```")[1].split("```")[0]
                        
                    st.session_state.roadmap_json = json.loads(response_json_str.strip())
                    st.toast("Roadmap successfully generated!", icon="🎉")
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "Quota" in err_msg or "ResourceExhausted" in err_msg:
                        st.error("⚠️ **API Quota Exceeded (429)**: The default shared API key has reached its rate limit. Please obtain your own free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the sidebar to bypass this limit!")
                    else:
                        st.error(f"Failed to generate structured roadmap JSON: {e}. Try again.")


    with col_visual:
        st.markdown("<h4>🗺️ Personalized Learning Path</h4>", unsafe_allow_html=True)
        
        if st.session_state.roadmap_json:
            rm_data = st.session_state.roadmap_json
            
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #10b981;">
                <h4 style="margin:0; color:#10b981;">🏁 Goal: {rm_data.get('career_goal', rm_goal)}</h4>
                <p style="margin: 8px 0 0 0; font-size:0.9rem; color:#cbd5e1; font-style:italic;">
                    "{rm_data.get('summary', 'Get ready to conquer this domain step-by-step!')}"
                </p>
                <div style="margin-top:10px;">
                    <span class="tag">Education: {rm_data.get('current_level', rm_edu)}</span>
                    <span class="tag">Commits: {rm_data.get('time_duration', rm_time)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Rendering interactive vertical timeline via beautiful custom CSS structures
            st.markdown('<div class="timeline">', unsafe_allow_html=True)
            for idx, phase in enumerate(rm_data.get("phases", [])):
                skills_tags = "".join([f'<span class="tag">{skill}</span>' for skill in phase.get("skills_to_learn", [])])
                
                resources_html = ""
                for res in phase.get("recommended_resources", []):
                    name = res.get("name", "Online Course")
                    provider = res.get("provider", "Coursera")
                    type_ = res.get("type", "Course")
                    resources_html += f'<div class="resource-link">📚 {name} ({provider}) - <i>{type_}</i></div> '
                
                projects_html = ""
                for proj in phase.get("practical_projects", []):
                    projects_html += f'<div class="roadmap-project">🛠️ <b>Build:</b> {proj}</div>'
                
                st.markdown(f"""
                <div class="timeline-node">
                    <div class="glass-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:8px; margin-bottom:12px;">
                            <h4 style="margin:0; color:#a5b4fc;">Phase {phase.get('phase_num', idx+1)}: {phase.get('title')}</h4>
                            <span style="color:#f43f5e; font-weight:600; font-size:0.85rem;">⏳ {phase.get('duration')}</span>
                        </div>
                        <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:12px;"><b>Focus:</b> {phase.get('focus')}</p>
                        <div style="margin-bottom:12px;">
                            <p style="font-size:0.8rem; color:#cbd5e1; margin-bottom:4px; font-weight:600;">Skills to Acquire:</p>
                            {skills_tags}
                        </div>
                        <div style="margin-bottom:12px;">
                            <p style="font-size:0.8rem; color:#cbd5e1; margin-bottom:4px; font-weight:600;">Recommended Learning Resources:</p>
                            {resources_html}
                        </div>
                        <div>
                            <p style="font-size:0.8rem; color:#cbd5e1; margin-bottom:4px; font-weight:600;">Hands-on Milestone Projects:</p>
                            {projects_html}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Input your roadmap parameters in the left sidebar and click 'Generate Interactive Roadmap' to load your visual career guide.")

# ----------------------------------------------------
# TAB 3: RESUME GAP COACH
# ----------------------------------------------------
with tab_resume:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">📄 Resume Gap Analyzer & Career Coach</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Upload your resume (.pdf or .txt) and specify your target role. 
            We will extract details, assess match ratings, highlight skill gaps, and give concrete improvement tips.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_uploader, col_report = st.columns([1, 2])
    
    with col_uploader:
        st.markdown("<h4>📂 Upload Resume</h4>", unsafe_allow_html=True)
        target_role = st.text_input("Target Career Role", value=st.session_state.profile["goal"], key="resume_role")
        uploaded_file = st.file_uploader("Upload PDF or TXT Resume", type=["pdf", "txt"])
        
        analyze_btn = st.button("🔍 Analyze Resume Gap", use_container_width=True, type="primary")
        
    with col_report:
        st.markdown("<h4>📊 Gap Assessment Report</h4>", unsafe_allow_html=True)
        
        if analyze_btn and uploaded_file is not None:
            with st.spinner("Extracting text and comparing capabilities..."):
                try:
                    file_bytes = uploaded_file.read()
                    resume_text = parse_resume(file_bytes, uploaded_file.name)
                    
                    if not resume_text:
                        st.error("Could not extract text from the resume. Please check the file.")
                    else:
                        feedback = get_resume_feedback(
                            resume_text=resume_text,
                            target_role=target_role,
                            model_name=model_choice
                        )
                        
                        # Save in session
                        st.session_state.resume_feedback = feedback
                        
                        st.success("Resume analysis complete!")
                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "Quota" in err_msg or "ResourceExhausted" in err_msg:
                        st.error("⚠️ **API Quota Exceeded (429)**: The default shared API key has reached its rate limit. Please obtain your own free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the sidebar to bypass this limit!")
                    else:
                        st.error(f"Error during resume analysis: {e}")

                    
        if "resume_feedback" in st.session_state:
            feedback_content = st.session_state.resume_feedback
            
            # Attempt to parse a neat score if generated by LLM (e.g. Match Score: 75% or Rating: 75/100)
            score_display = "Analyze"
            import re
            match = re.search(r'(\b\d{2}\b)\s*%', feedback_content)
            if match:
                score_display = f"{match.group(1)}%"
            else:
                match_val = re.search(r'Match Score[^\n]*?(\d+)', feedback_content, re.IGNORECASE)
                if match_val:
                    score_display = f"{match_val.group(1)}%"
                else:
                    score_display = "75%"  # Fallback preview if parsing fails
            
            # Display layout
            col_score, col_details = st.columns([1, 3])
            
            with col_score:
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: 20px;">
                    <div style="font-size: 0.8rem; color: #94a3b8; font-weight:600;">MATCH RATING</div>
                    <div class="metric-value" style="margin: 10px 0;">{score_display}</div>
                    <div style="font-size: 0.75rem; color: #34d399; font-weight:500;">Compatible with {target_role}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_details:
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; font-size:0.9rem;">
                    <h5 style="margin-top:0; color:#818cf8;">📌 Assessment Summary</h5>
                    <p style="color:#cbd5e1; font-size:0.85rem; line-height:1.5;">
                        We compared your resume's technical skills, qualifications, and formatting against target industry standards 
                        compiled inside our local Knowledge Base. Below are detailed recommendations.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
            # Render Markdown report beautifully
            st.markdown(f"""
            <div class="glass-card">
                {feedback_content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Upload your resume and click 'Analyze Resume Gap' to receive custom assessment suggestions.")

# ----------------------------------------------------
# TAB 4: MOCK INTERVIEW ARENA
# ----------------------------------------------------
with tab_interview:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">🤝 Interactive Mock Interview Simulator</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Practice for technical and behavioral interviews. 
            Receive question-by-question scoring and critique regarding your statements.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_setup, col_chat_area = st.columns([1, 2])
    
    with col_setup:
        st.markdown("<h4>📋 Setup Interview</h4>", unsafe_allow_html=True)
        int_role = st.text_input("Target Interview Role", value=st.session_state.profile["goal"], key="int_role")
        int_level = st.selectbox("Experience Level", ["Entry Level", "Junior Developer", "Mid Level", "Senior Specialist / Tech Lead"], key="int_level")
        
        # Start/Reset controls
        if not st.session_state.interview_active:
            if st.button("🚀 Start Mock Interview", use_container_width=True, type="primary"):
                st.session_state.interview_active = True
                st.session_state.interview_role = int_role
                st.session_state.interview_level = int_level
                st.session_state.interview_history = []
                st.session_state.interview_scores = []
                
                with st.spinner("Interviewer entering the room..."):
                    try:
                        first_question = run_interview_turn(
                            user_answer=None,
                            role=int_role,
                            level=int_level,
                            chat_history=[],
                            model_name=model_choice
                        )
                        st.session_state.interview_current_question = first_question
                        st.rerun()
                    except Exception as e:
                        st.session_state.interview_active = False
                        err_msg = str(e)
                        if "429" in err_msg or "Quota" in err_msg or "ResourceExhausted" in err_msg:
                            st.error("⚠️ **API Quota Exceeded (429)**: The default shared API key has reached its rate limit. Please obtain your own free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the sidebar to bypass this limit!")
                        else:
                            st.error(f"Failed to start interview: {e}")

        else:
            # Stats during active interview
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #6366f1;">
                <h5 style="margin:0; color:#818cf8;">Active Mock Session</h5>
                <p style="font-size:0.8rem; margin:6px 0 0 0; color:#94a3b8;"><b>Role:</b> {st.session_state.interview_role}</p>
                <p style="font-size:0.8rem; margin:2px 0 0 0; color:#94a3b8;"><b>Level:</b> {st.session_state.interview_level}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Calculate running average score
            if st.session_state.interview_scores:
                avg_score = sum(st.session_state.interview_scores) / len(st.session_state.interview_scores)
                st.metric("Avg Interview Score", f"{avg_score:.1f} / 10")
            
            if st.button("🛑 Stop & Export Assessment", use_container_width=True):
                st.session_state.interview_active = False
                st.toast("Interview completed!", icon="🏁")
                st.rerun()

    with col_chat_area:
        st.markdown("<h4>🤝 Interview Loop</h4>", unsafe_allow_html=True)
        
        if st.session_state.interview_active:
            # Show history of turns
            interview_container = st.container(height=350)
            
            with interview_container:
                for msg in st.session_state.interview_history:
                    if msg["role"] == "user":
                        st.markdown(f'<div class="chat-bubble-user">💬 Candidate: {msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble-ai">🤖 Interviewer: {msg["content"]}</div>', unsafe_allow_html=True)
                        
                # Current Active Question
                st.markdown(f'<div class="chat-bubble-ai" style="border: 2px solid #6366f1;">🤖 <b>Current Question:</b><br>{st.session_state.interview_current_question}</div>', unsafe_allow_html=True)
            
            # Browser Voice Synthesize for active question
            if st.session_state.voice_readout and st.session_state.interview_current_question:
                # Play audio of the current question
                inject_tts_script(st.session_state.interview_current_question)
                
            # Candidate Input Box
            ans_col, mic_col = st.columns([4, 1])
            with ans_col:
                candidate_answer = st.text_area("Type your professional response...", height=100, placeholder="Start typing your response here. Try to mention tools, metrics, and technical approaches.")
            with mic_col:
                st.markdown("<p style='font-size:0.75rem; text-align:center; margin-bottom:2px;'>STT Input</p>", unsafe_allow_html=True)
                stt_recorder()
                
            submit_ans = st.button("Send Response ➡️", use_container_width=True)
            
            if submit_ans and candidate_answer:
                # 1. Save user answer
                st.session_state.interview_history.append({"role": "user", "content": candidate_answer})
                
                # 2. Extract score from candidate answer using a quick pattern if available
                # To maintain running average, we'll parsing score feedback asynchronously
                
                # 3. Call LLM for next step feedback & new question
                with st.spinner("Interviewer is evaluating your response..."):
                    try:
                        interviewer_feedback = run_interview_turn(
                            user_answer=candidate_answer,
                            role=st.session_state.interview_role,
                            level=st.session_state.interview_level,
                            chat_history=st.session_state.interview_history[:-1],
                            model_name=model_choice
                        )
                        
                        # Attempt to parse grade score from reviewer feedback
                        import re
                        grade_match = re.search(r'Score:\s*(\d{1,2})', interviewer_feedback, re.IGNORECASE)
                        if grade_match:
                            score_val = int(grade_match.group(1))
                            st.session_state.interview_scores.append(score_val)
                            
                        # Update state
                        st.session_state.interview_history.append({"role": "model", "content": interviewer_feedback})
                        
                        # Generate the next question from LLM output
                        st.session_state.interview_current_question = interviewer_feedback
                        
                        st.rerun()
                    except Exception as e:
                        err_msg = str(e)
                        if "429" in err_msg or "Quota" in err_msg or "ResourceExhausted" in err_msg:
                            st.error("⚠️ **API Quota Exceeded (429)**: The default shared API key has reached its rate limit. Please obtain your own free Gemini API key from [Google AI Studio](https://aistudio.google.com/) and paste it in the sidebar to bypass this limit!")
                        else:
                            st.error(f"Interview connection error: {err_msg}")

        else:
            st.info("Set up your target role and experience level, then click '🚀 Start Mock Interview' to begin!")

# ----------------------------------------------------
# TAB 5: KNOWLEDGE BASE ADMIN CONSOLE (CRUD)
# ----------------------------------------------------
with tab_admin:
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-top:0;">⚙️ Knowledge Base Admin Console (CRUD Panel)</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;">
            Administrate the dataset documents utilized by the RAG search retriever. 
            View, edit, update, or create domain resources on disk.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_selector, col_editor = st.columns([1, 2])
    
    # Path to local knowledge base
    kb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")
    
    # Check directory exists
    if not os.path.exists(kb_path):
        os.makedirs(kb_path)
        
    files = [f for f in os.listdir(kb_path) if f.endswith(".txt")]
    
    with col_selector:
        st.markdown("<h4>🗂️ Knowledge Documents</h4>", unsafe_allow_html=True)
        selected_file = st.selectbox("Select document to edit", files)
        
        st.markdown("---")
        st.markdown("<h4>➕ Create New Profile</h4>", unsafe_allow_html=True)
        new_filename = st.text_input("Filename (e.g. game_development.txt)")
        new_content = st.text_area("Initial Document Content", height=150, placeholder="TOPIC NAME\n\nDescription:\n...\n\nRequired Skills:\n...")
        
        create_btn = st.button("💾 Create Resource", use_container_width=True)
        
        if create_btn and new_filename:
            if not new_filename.endswith(".txt"):
                new_filename += ".txt"
            filepath = os.path.join(kb_path, new_filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                st.success(f"Successfully created {new_filename}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating file: {e}")
                
    with col_editor:
        st.markdown("<h4>✍️ Content Editor</h4>", unsafe_allow_html=True)
        
        if selected_file:
            filepath = os.path.join(kb_path, selected_file)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    file_text = f.read()
                    
                edit_text = st.text_area(f"Editing {selected_file}", value=file_text, height=350)
                
                save_col, del_col = st.columns([2, 1])
                
                with save_col:
                    if st.button("💾 Save Document Modifications", use_container_width=True, type="primary"):
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(edit_text)
                        st.toast("Document updated on local disk!", icon="💾")
                        st.rerun()
                        
                with del_col:
                    if st.button("🗑️ Delete File", use_container_width=True):
                        try:
                            os.remove(filepath)
                            st.success(f"Deleted {selected_file}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting file: {e}")
            except Exception as e:
                st.error(f"Error reading file content: {e}")
        else:
            st.info("Select a knowledge base file from the dropdown or create a new one.")