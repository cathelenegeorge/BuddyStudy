import streamlit as st
from core.file_utils import extract_text
from core.summarizer import generate_summary
from core.flashcards import generate_flashcards, export_flashcards_to_pptx
from core.ask_ai import ask_ai
from core.ppt_generator import generate_detailed_pptx
import difflib
import os


# --- Config & Branding ---
st.set_page_config(page_title="BuddyStudy", layout="wide")
st.sidebar.title("🎓 BuddyStudy")
st.sidebar.image("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDcwcG43c2gyMG93MTRtcWJnMmQxY2dpcjFnNGI3ZmEwd3licngxdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/fhAwk4DnqNgw8/giphy.gif", width=200)
st.sidebar.markdown("""
Welcome to **BuddyStudy!!👾** – Your AI-powered academic assistant.

🔹 Upload lecture notes  
🔹 Summarize them  
🔹 Create flashcards  
🔹 Ask smart questions  
🔹 Export auto-generated PPTs \n
🔹 Set Pomodoro Timer
                      
""")

# --- Utility: Fuzzy Answer Match ---
def is_similar(user_input, correct_answer, threshold=0.6):
    user_input = user_input.strip().lower()
    correct_answer = correct_answer.strip().lower()
    if user_input in correct_answer or correct_answer in user_input:
        return True
    overlap = set(user_input.split()) & set(correct_answer.split())
    return len(overlap) > 0 or difflib.SequenceMatcher(None, user_input, correct_answer).ratio() >= threshold

# --- Upload File ---
uploaded_file = st.file_uploader("📤 Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file and "doc_text" not in st.session_state:
    with st.spinner("📖 Extracting document content..."):
        st.session_state.doc_text = extract_text(uploaded_file)

doc_text = st.session_state.get("doc_text", "")
summary = st.session_state.get("summary", "")

# --- TABS Layout ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Summary", "🧠 Flashcards", "💬 Ask AI", "📽️ PPT Generator","⏳Pomodoroo"])

# === 📝 TAB 1: SUMMARY ===
with tab1:
    st.subheader("📄 Document Summary")
    if st.button("Generate Summary", key="generate_summary_btn"):
        if not uploaded_file:
            st.warning("📄 Please upload a file first.")
        else:
            with st.spinner("🧠 Summarizing document..."):
                st.session_state.summary = generate_summary(doc_text)

    if "summary" in st.session_state:
        with st.expander("🔍 Click to View Summary"):
            st.markdown(st.session_state.summary)
    else:
        st.info("Click the **Generate Summary** button after uploading to get a summary.")

# === 🧠 TAB 2: FLASHCARDS ===
with tab2:
    st.subheader("🧠 Interactive Flashcards")
    num_cards = st.number_input("How many flashcards?", min_value=1, max_value=20, value=5, key="num_cards_input")

    if st.button("Generate Flashcards", key="generate_flashcards_btn"):
        if not uploaded_file:
            st.warning("📄 Please upload a file first.")
        else:
            with st.spinner("🧠 Creating flashcards..."):
                source_text = st.session_state.get("summary", doc_text)
                all_flashcards = generate_flashcards(source_text, 20)
                filtered = [fc for fc in all_flashcards if fc[0] and fc[1] and fc[2]]
                st.session_state.flashcards = filtered[:num_cards]
                st.session_state.current_card = 0
                st.session_state.score = 0
                st.session_state.missed = []
                st.session_state.answered = False

    if "flashcards" in st.session_state and st.session_state.flashcards:
        idx = st.session_state.current_card
        flashcards = st.session_state.flashcards

        if idx < len(flashcards):
            q, a, explanation = flashcards[idx]
            st.markdown(f"**Q{idx + 1}:** {q}")

            if f"user_input_{idx}" not in st.session_state:
                st.session_state[f"user_input_{idx}"] = ""

            user_ans = st.text_input("Your Answer:", key=f"ans_{idx}", value=st.session_state[f"user_input_{idx}"])
            st.session_state[f"user_input_{idx}"] = user_ans

            if st.button("Submit", key=f"submit_{idx}") and not st.session_state.get("answered", False):
                if is_similar(user_ans, a):
                    st.session_state.score += 1
                    st.success("✅ Correct! Great job, you're awesome! ✨")
                else:
                    st.session_state.missed.append((q, a, explanation))
                    st.error(f"❌ Incorrect\n\n**Answer:** {a}\n\n**Explanation:** {explanation}\n\nKeep learning 🚀")
                st.session_state.answered = True

            if st.session_state.get("answered", False):
                if st.button("Next", key=f"next_{idx}"):
                    st.session_state.current_card += 1
                    st.session_state.answered = False

        else:
            st.success(f"🎉 Quiz Completed! Score: {st.session_state.score}/{len(flashcards)}")
            if st.session_state.missed:
                st.warning("You missed a few. Retry them?")
                if st.button("Retry Missed Flashcards"):
                    st.session_state.flashcards = st.session_state.missed
                    st.session_state.current_card = 0
                    st.session_state.score = 0
                    st.session_state.missed = []
                    st.session_state.answered = False

    if st.button("Export Flashcards to PPTX"):
        if "flashcards" not in st.session_state:
            st.warning("📄 Please generate flashcards first.")
        else:
            pptx_path = export_flashcards_to_pptx(st.session_state.flashcards)
            with open(pptx_path, "rb") as f:
                st.download_button("📥 Download Flashcards PPT", f, file_name="BuddyStudy_Flashcards.pptx")

# === 💬 TAB 3: ASK AI ===
with tab3:
    st.subheader("💬 Ask AI About Your Notes")
    user_query = st.text_input("Ask anything about the document:", key="ask_input")

    if st.button("Get Answer", key="ask_btn"):
        if not uploaded_file:
            st.warning("📄 Please upload a file first.")
        elif not user_query.strip():
            st.warning("❓ Please enter your question.")
        else:
            with st.spinner("🤖 Thinking..."):
                response = ask_ai(user_query, doc_text)
                st.session_state.last_ai_response = response

    if "last_ai_response" in st.session_state:
        with st.expander("🧠 View AI's Answer"):
            st.info(st.session_state.last_ai_response)

# === 📽️ TAB 4: PPT GENERATOR ===
with tab4:
    st.subheader("📽️ Generate Descriptive PPT from Summary")
    st.markdown("This will generate slides based on **headings, topics**, and **grouped subtopics** using GPT.")

    if st.button("Generate PPT", key="ppt_btn"):
        if not uploaded_file:
            st.warning("📄 Please upload a file first.")
        else:
            with st.spinner("📊 Preparing content..."):
                source_summary = st.session_state.get("summary", doc_text)
                progress_bar = st.progress(0)

                def update_progress(val):
                    progress_bar.progress(val)

                pptx_path = generate_detailed_pptx(
                    summary_text=source_summary,
                    descriptive=True,
                    progress_callback=update_progress
                )
                st.session_state.generated_pptx = pptx_path
                progress_bar.empty()

    if "generated_pptx" in st.session_state:
        with open(st.session_state.generated_pptx, "rb") as f:
            st.download_button("📥 Download Descriptive PPT", f, file_name="BuddyStudy_Topics_PPT.pptx")
# === 💬 TAB 5: POMODORO TIMER ===
import time

with tab5:
    st.subheader("⏱️ Pomodoro Timer")

    work_duration = st.number_input("Work duration (min)", 1, 60, 25)
    break_duration = st.number_input("Break duration (min)", 1, 30, 5)

    if "pomodoro_running" not in st.session_state:
        st.session_state.pomodoro_running = False
        st.session_state.current_phase = "Work"
        st.session_state.streak = 0
        st.session_state.pomodoro_start_time = 0

    ring_holder = st.empty()
    status_holder = st.empty()

    def draw_ring(phase_name, remaining_min, total_min):
        progress = 1 - (remaining_min / total_min)
        color = "#4caf50" if phase_name == "Work" else "#2196f3"
        if remaining_min <= 5:
            color = "#4caf50"  # warning orange near end
        minutes = int(remaining_min)
        seconds = int((remaining_min * 60) % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"


        ring_holder.markdown(
            f"""
            <style>
            @keyframes pulse {{
              0% {{ box-shadow: 0 0 0 0 {color}99; }}
              70% {{ box-shadow: 0 0 0 10px {color}00; }}
              100% {{ box-shadow: 0 0 0 0 {color}00; }}
            }}
            .pulse {{
              animation: pulse 2s infinite;
              display: inline-block;
              border-radius: 50%;
              padding: 10px;
            }}
            </style>
            <div style="text-align: center;">
              <div class="pulse">
                <svg width="90" height="90">
                  <circle cx="45" cy="45" r="35" stroke="#ddd" stroke-width="8" fill="none" />
                  <circle cx="45" cy="45" r="35" stroke="{color}" stroke-width="8" fill="none"
                    stroke-dasharray="220" stroke-dashoffset="{220 * (1 - progress)}"
                    transform="rotate(-90 45 45)" />
                  <text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="15" fill="white">{time_str}</text>
                </svg>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def run_pomodoro(duration, phase):
       st.session_state.pomodoro_start_time = time.time()
       end_time = time.time() + duration * 60

    # Sync music with Pomodoro phase
       if phase == "Work":
           st.session_state.selected_sound = "https://www.soundjay.com/nature/rain-01.mp3"
       elif phase == "Break":
           st.session_state.selected_sound = "https://www.soundjay.com/nature/ocean-wave-2.mp3"

       while time.time() < end_time:
            if not st.session_state.pomodoro_running:
                break
            remaining = (end_time - time.time()) / 60
            draw_ring(phase, remaining, duration)
            time.sleep(1)

       if st.session_state.pomodoro_running:
             st.session_state.pomodoro_running = False
             if phase == "Work":
                 st.session_state.streak += 1
                 status_holder.success("✅ Work complete! Break time!")
                 st.balloons()
             else:
                 st.session_state.selected_sound = None  # stop music
                 status_holder.info("☕ Break finished! Back to work.")

    c1, c2 = st.columns(2)
    if c1.button("▶️ Start Pomodoro"):
        st.session_state.pomodoro_running = True
        st.session_state.current_phase = "Work"
        run_pomodoro(work_duration, "Work")
        if st.session_state.pomodoro_running:
            st.session_state.pomodoro_running = True
            st.session_state.current_phase = "Break"
    if c2.button("⏹️ Reset"):
        st.session_state.pomodoro_running = False
        ring_holder.markdown("⏱️ Timer Reset", unsafe_allow_html=True)
        status_holder.empty()

    st.markdown(f"🔥 **Pomodoro Streaks Completed**: {st.session_state.streak}") 
