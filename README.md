# 📘 BuddyStudy

**Your AI-powered academic assistant, built to make studying smarter, not harder.**

---

## 🌟 Overview

**BuddyStudy** is a fully responsive, Streamlit-based app designed to help students focus and enhance their study experience. Whether it’s summarizing lecture notes, generating flashcards, clearing doubts, or exporting auto-generated PPTs, BuddyStudy has your back — now with Pomodoro productivity power too!

---

## 🚀 Features

🔹 **Upload Lecture Notes**  
Upload `.pdf` or `.docx` files (up to 200MB) and get started instantly.

🔹 **Summary**  
Get a clean, section-wise summary and topic-wise breakdown of your entire file.

🔹 **Flashcards Quiz Mode**  
- Specify number of flashcards  
- Quiz-style format  
- Correct = appreciation + quote  
- Incorrect = correct answer + explanation + encouragement 💪

🔹 **Ask AI Anything**  
Ask contextual questions based on your uploaded notes. Receive clear, concise, and detailed answers — like a tutor in your pocket.

🔹 **PPT Generator**  
Auto-generate beautifully structured PowerPoint slides based on:
- Headings
- Main topics
- Grouped subtopics

🔹 **Pomodoro Timer**  
Track study sessions using the Pomodoro method.  
🎈 Balloon pop-ups appear on successful completion, and streaks are recorded!

🔹 **Theme Adaptability**  
Switch between light ☀️ and dark 🌙 modes seamlessly.

---

## 🛠️ Built With

- **Python**
- **Streamlit**
- **OpenAI GPT-4 API**
- **LangChain (for Ask AI feature)**
- **PPTX (python-pptx for slide creation)**

---

## 📦 Deployment

Done on **Streamlit Cloud** ☁️  

---

## ✨ How to Run Locally

```bash
git clone https://github.com/your-username/BuddyStudy.git
cd BuddyStudy
pip install -r requirements.txt
streamlit run app.py
