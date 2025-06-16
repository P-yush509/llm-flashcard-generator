# LLM-Powered Flashcard Generator

A Streamlit web app that generates flashcards from educational content (PDF or text) using Google Gemini LLM.

---

## Features
- 📚 Upload PDF or paste text to generate flashcards
- 🏷️ Flashcards are grouped by detected topic/section
- ❓ Each flashcard includes question, answer, difficulty, and topic
- 📥 Export flashcards as CSV

---

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies
```bash
pip install streamlit google-generativeai PyPDF2
```

### 3. Set up Gemini API key
- Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a `.streamlit/secrets.toml` file:
```
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

---

## Usage

```bash
streamlit run flashcard_generator.py
```
- Upload a PDF or paste text
- Select subject type (optional)
- Click "Generate Flashcards"
- View and export grouped flashcards

---

## Sample Screenshots

### App Title & Upload
![App Title](assets/Screenshot%202025-06-17%20024719.png)

### PDF Uploaded
![PDF Uploaded](assets/Screenshot%202025-06-17%20024843.png)

### Flashcards Generated
![Flashcards Generated](assets/Screenshot%202025-06-17%20024918.png)

### Grouped by Topic
![Grouped by Topic](assets/Screenshot%202025-06-17%20024932.png)

### Export as CSV
![Export as CSV](assets/Screenshot%202025-06-17%20025001.png)

---

## Sample Execution

1. Upload a textbook chapter PDF or paste a section of text.
2. Click "Generate Flashcards".
3. Flashcards are displayed, grouped by topic, and can be exported as CSV.

---

## License
MIT
