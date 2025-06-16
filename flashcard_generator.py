# flashcard_generator.py

import streamlit as st
from PyPDF2 import PdfReader
import json
import csv
import os
import google.generativeai as genai

# === GEMINI CONFIG ===
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")  # Updated model name

# === FLASHCARD GENERATOR ===
def generate_flashcards_with_gemini(text):
    prompt = (
        f"{text}"
    )
    try:
        response = model.generate_content(prompt)
        output = response.text
        # Try to extract JSON from the output
        json_start = output.find('[')
        json_end = output.rfind(']')
        if json_start != -1 and json_end != -1:
            output_json = output[json_start:json_end+1]
            return json.loads(output_json)
        else:
            return []
    except Exception as e:
        print("Error:", e)
        return []

# === GROUPING UTILS ===
def group_flashcards_by_topic(flashcards):
    grouped = {}
    for card in flashcards:
        topic = card.get('topic', 'General')
        if topic not in grouped:
            grouped[topic] = []
        grouped[topic].append(card)
    return grouped

# === FILE PARSERS ===
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# === EXPORT UTILS ===
def export_to_csv(flashcards, filename="flashcards.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['topic', 'question', 'answer', 'difficulty'])
        writer.writeheader()
        for card in flashcards:
            writer.writerow({
                'topic': card.get('topic', 'General'),
                'question': card.get('question', ''),
                'answer': card.get('answer', ''),
                'difficulty': card.get('difficulty', '')
            })
    return filename

# === STREAMLIT UI ===
# Custom CSS for single-line title and transparent navbar
st.markdown("""
    <style>
        /* Blur and opacity for Streamlit navbar/header */
        header, .st-emotion-cache-18ni7ap, .st-emotion-cache-1avcm0n, .st-emotion-cache-6qob1r {
            background: rgba(33, 33, 33, 0.7) !important;
            backdrop-filter: blur(4px) !important;
            -webkit-backdrop-filter: blur(4px) !important;
        }
        .block-container {padding-top: 2rem;}
        .custom-title-space {margin-top: 40px;}
    </style>
    <div class='custom-title-space' style='display: flex; align-items: center;'>
        <span style='font-size:44px; margin-right: 14px;'>📚</span>
        <h1 style='margin: 0; display: inline-block;'>LLM-Powered Flashcard Generator</h1>
    </div>
""", unsafe_allow_html=True)

# --- Mutually exclusive input fields ---
if 'user_text_active' not in st.session_state:
    st.session_state['user_text_active'] = False

uploaded_file = st.file_uploader(
    "Upload educational material (PDF/TXT):", 
    type=["pdf", "txt"], 
    disabled=st.session_state.get("user_text_active", False)
)
user_text = st.text_area(
    "Or paste your content below:", 
    disabled=uploaded_file is not None
)

# Track if user has entered text
if user_text and not uploaded_file:
    st.session_state["user_text_active"] = True
else:
    st.session_state["user_text_active"] = False

subject_type = st.selectbox("Optional: Select subject type", ["General", "Biology", "History", "Computer Science"])

if st.button("Generate Flashcards"):
    with st.spinner("Generating flashcards using Gemini..."):
        input_text = ""
        if uploaded_file:
            if uploaded_file.name.endswith(".pdf"):
                input_text = extract_text_from_pdf(uploaded_file)
            else:
                input_text = uploaded_file.read().decode("utf-8")
        elif user_text:
            input_text = user_text

        if not input_text.strip():
            st.warning("No valid input provided.")
        else:
            # Add subject_type and grouping instruction to the prompt for better context
            prompt_text = (
                f"Subject: {subject_type}\n"
                "Generate 15 flashcards from the following educational content. "
                "Each flashcard must include a question, an answer, a difficulty level (Easy, Medium, or Hard), "
                "and a topic field that reflects the detected topic header or section from the content. "
                "Return result as a JSON list, where each flashcard has 'topic', 'question', 'answer', and 'difficulty'.\n\n"
                f"Content: {input_text}\n"
            )
            flashcards = generate_flashcards_with_gemini(prompt_text)
            if flashcards:
                st.session_state["flashcards"] = flashcards  # Store in session state
                grouped = group_flashcards_by_topic(flashcards)
                st.success(f"Generated {len(flashcards)} flashcards grouped by topic.")
                question_number = 1
                for topic, cards in grouped.items():
                    st.markdown(f"### 🏷️ {topic}")
                    for card in cards:
                        st.markdown(f"**Q{question_number}:** {card.get('question', '')}")
                        st.markdown(f"**Ans:** {card.get('answer', '')}")
                        st.markdown(f"📌 Difficulty: *{card.get('difficulty', 'Unknown')}*")
                        st.markdown("---")
                        question_number += 1
            else:
                st.error("Failed to generate flashcards. Try a shorter input or check the model output.")

# Export button always available if flashcards exist
if "flashcards" in st.session_state and st.session_state["flashcards"]:
    if st.button("Export as CSV"):
        csv_path = export_to_csv(st.session_state["flashcards"])
        with open(csv_path, "rb") as f:
            st.download_button("Download CSV", f, file_name="flashcards.csv")
