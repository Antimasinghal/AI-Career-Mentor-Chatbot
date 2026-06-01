# 🎓 EduPath AI Career Mentor Chatbot

EduPath AI is a state-of-the-art, feature-rich conversational career counseling assistant built using **Streamlit** and **Google Gemini 2.5 Flash**. It provides automated RAG-based career advice, resume analysis, mock interviews, interactive roadmaps, and administrative tools in a beautiful obsidian-glass themed interface.

---

## 🌟 Key Features

1. **💬 AI Career Mentor Chat**
   - RAG-powered knowledge base grounding (Data Science, AI, SoftDev, Cyber, AgriTech, FoodTech, Business, and Design).
   - Keeps track of multi-turn chat history.
   - Context-aware student profile custom settings (education, skills, goals).
   
2. **🗺️ Interactive Roadmap Architect**
   - Form-based timeline generator.
   - Generates a customized, step-by-step roadmap in JSON, rendered as a beautiful vertical timeline using custom HSL card structures.
   
3. **📄 Resume Gap Coach**
   - Seamless PDF and TXT file uploads.
   - Extracts resume parameters (skills, formatting, certifications).
   - Generates an objective Match Score and list of skill gaps, suggestions, and improvement metrics.

4. **🤝 Mock Interview Prep Arena**
   - Simulated role-specific mock interviewer.
   - Question-by-question response parsing.
   - Highlights strengths, flaws, and tracks interview scores dynamically.

5. **⚙️ KB Admin Console (CRUD)**
   - Administrative file browser for the local knowledge base directory.
   - Easily modify, save, delete, or create new text profiles inside the UI.

6. **🔊 Browser-Native Audio Services**
   - **Text-To-Speech (TTS)**: Automatically reads out mentor outputs using HTML5 SpeechSynthesis.
   - **Speech-To-Text (STT)**: Dictate inputs through a browser microphone button using HTML5 SpeechRecognition.
   - **100% Free** & requires no costly API setups or heavy python dependencies!

7. **🌐 Multi-Language Support**
   - Real-time translations. Engage with the AI mentor in English, Hindi, Spanish, French, German, Mandarin, or Arabic!

---

## 🏗️ Technical Stack

- **Frontend Framework**: Streamlit
- **Cognitive Model**: Google Gemini (Gemini 2.5 Flash / 1.5 Pro)
- **Document Retrievers**: Custom Keyword & overlap TF-IDF RAG system
- **PDF Text Extractor**: PyPDF2
- **Audio Service Layer**: HTML5 Web Speech Browser API

---

## 📥 Local Installation Guide

### Prerequisites
- Python 3.9, 3.10, or 3.11 installed on your local machine.

### Step 1: Clone the Repository
```bash
git clone <repository_link>
cd career_mentor_chatbot
```

### Step 2: Install Dependencies
Install all standard dependencies using `pip`:
```bash
pip install -r requirement.txt
```

### Step 3: Configure API Keys
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```
*(Alternatively, you can input your API key directly into the secure textbox in the Streamlit Sidebar during execution).*

### Step 4: Run the Application
Launch the Streamlit dev server:
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 💡 Example Prompts & Outputs

### 1. General Career Domain Guidance
- **Prompt**: *"What are the career opportunities in Agriculture Technology?"*
- **Response**: The assistant accesses `agriculture_technology.txt`, explains Precision Agriculture, GIS, and Drone Operations, and lists roles like AgriTech Engineer and Farm Technology Consultant.

### 2. Certifications & Resources
- **Prompt**: *"Suggest certifications for Food Technology."*
- **Response**: The assistant reads `food_technology.txt` and suggests industry-recognized certifications like HACCP, ISO 22000, and NPTEL/Coursera courses.

### 3. Study Abroad & Higher Studies
- **Prompt**: *"Explain scholarship and exams for MS in AI abroad."*
- **Response**: The assistant reads `higher_education.txt` and lists DAAD, Erasmus Mundus, Fulbright scholarships, GRE/TOEFL requirements, and AI specializations like Computer Vision and Robotics.

---

## 📂 Project Structure

```text
career_mentor_chatbot/
│
├── knowledge_base/            # Grounding text files for RAG retriever
│   ├── ai_ml.txt
│   ├── data_science.txt
│   ├── software_development.txt
│   ├── cybersecurity.txt
│   ├── agriculture_technology.txt
│   ├── food_technology.txt
│   ├── business_management.txt
│   ├── design_creative.txt
│   └── higher_education.txt
│
├── app.py                     # Main Streamlit Frontend Application
├── chatbot.py                 # Core AI & Gemini Interface
├── prompts.py                 # Prompt templates
├── resume_parser.py           # PyPDF2 parsing library
├── knowledge_retriever.py     # Local keyword RAG retriever
├── requirement.txt            # Python library list
├── documentation.md           # Extensive system architecture details
└── README.md                  # Project instructions
```
