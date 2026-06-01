import os
import re

KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")

# Mapping keywords to specific files for high-precision retrieval
KEYWORD_MAPPING = {
    "ai_ml.txt": ["ai", "artificial intelligence", "ml", "machine learning", "deep learning", "neural", "computer vision", "nlp"],
    "data_science.txt": ["data science", "data scientist", "data analyst", "analytics", "statistics", "pandas", "numpy", "visualization", "power bi"],
    "software_development.txt": ["software", "developer", "development", "engineer", "programming", "coding", "java", "python", "c++", "web", "frontend", "backend", "fullstack", "full stack"],
    "cybersecurity.txt": ["cybersecurity", "cyber security", "security", "hacking", "hacker", "pentest", "penetration", "networking", "cryptography"],
    "agriculture_technology.txt": ["agri", "agriculture", "farming", "farm", "crop", "precision agriculture", "gis", "drone", "iot"],
    "food_technology.txt": ["food", "beverage", "nutrition", "processing", "safety", "haccp", "quality control", "iso 22000"],
    "business_management.txt": ["business", "management", "mba", "manager", "project management", "marketing", "finance", "operations"],
    "design_creative.txt": ["design", "creative", "ui", "ux", "figma", "adobe", "photoshop", "illustrator", "graphic", "art", "creative director"],
    "higher_education.txt": ["higher", "study", "studies", "abroad", "scholarship", "exam", "gre", "gate", "cat", "toefl", "ielts", "university", "specialization", "masters", "phd"]
}

def load_knowledge_base():
    """Loads all knowledge base files and returns a dictionary of filename -> content"""
    kb = {}
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        return kb
    
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(KNOWLEDGE_BASE_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    kb[filename] = f.read()
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return kb

def get_relevant_knowledge(query):
    """
    Scans the query against the keyword maps and returns relevant files content as text context.
    If no matches are found, returns a standard overview of the knowledge domains.
    """
    kb = load_knowledge_base()
    if not kb:
        return ""
    
    query_lower = query.lower()
    matched_files = set()
    
    # Check for direct keyword matches
    for filename, keywords in KEYWORD_MAPPING.items():
        for kw in keywords:
            # Use regex to match whole words or boundary patterns where appropriate
            if re.search(r'\b' + re.escape(kw) + r'\b', query_lower) or kw in query_lower:
                matched_files.add(filename)
                break
                
    # If no specific matches, try a simple term frequency match against file contents
    if not matched_files:
        for filename, content in kb.items():
            content_lower = content.lower()
            # Count overlap of key nouns or technical terms
            words = set(re.findall(r'\b\w{4,}\b', query_lower))  # words of 4+ characters
            overlap = 0
            for w in words:
                if w in content_lower:
                    overlap += 1
            if overlap >= 2:  # If at least two keywords overlap
                matched_files.add(filename)

    # Always include higher education if relevant words are mentioned
    if any(edu_term in query_lower for edu_term in ["study", "studies", "abroad", "scholarship", "masters", "phd", "university", "college", "exam"]):
        matched_files.add("higher_education.txt")
        
    # If still no matches, we can load a small overview of all available domains
    if not matched_files:
        # Load a few summary lines from each domain
        context = "Information available in the Knowledge Base:\n"
        for filename, content in kb.items():
            title_line = content.split('\n')[0] if content else filename
            context += f"- {title_line}\n"
        return context
    
    # Retrieve and merge content of all matched files
    context_blocks = []
    for filename in matched_files:
        if filename in kb:
            context_blocks.append(f"--- KNOWLEDGE SOURCE: {filename.upper()} ---\n{kb[filename]}\n")
            
    return "\n".join(context_blocks)
