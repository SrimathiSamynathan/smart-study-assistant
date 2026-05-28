import streamlit as st
import PyPDF2
from groq import Groq
from datetime import datetime

client = Groq(api_key="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")

def clean_text(text):
    text = text.replace("**", "")
    text = text.replace("##", "")
    text = text.replace("# ", "")
    text = text.replace("* ", "• ")
    text = text.replace("*", "")
    text = text.replace("---", "─" * 50)
    return text

st.set_page_config(
    page_title="Smart Study Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Smart Study Assistant")
st.write("Upload your notes and get AI-powered help!")

with st.sidebar:
    st.title("📚 Menu")
    feature = st.radio("Choose Feature",
                       ["📄 Summarizer",
                        "📝 Quiz Generator",
                        "🃏 Flashcard Generator",
                        "🎯 Key Points Extractor",
                        "⚡ Difficulty Level Quiz",
                        "💬 Chat with Notes"])

uploaded_file = st.file_uploader(
    "Upload your notes (PDF)",
    type="pdf"
)

if uploaded_file is not None:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    short_text = text[:4000]

    st.success("✅ Notes uploaded successfully!")

    with st.expander("👀 View Extracted Text"):
        st.write(text)

    if feature == "📄 Summarizer":
        st.subheader("✨ AI Summary")
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user",
                         "content": f"Summarize these notes clearly without using any markdown symbols:\n\n{short_text}"}
                    ]
                )
                summary = response.choices[0].message.content
                st.write(summary)
                st.divider()
                st.download_button(
                    label="📥 Download Summary",
                    data=clean_text(summary),
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    if feature == "📝 Quiz Generator":
        st.subheader("📝 AI Quiz")
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user",
                         "content": f"Create 10 MCQ questions with answers from these notes without using any markdown symbols:\n\n{short_text}"}
                    ]
                )
                quiz = response.choices[0].message.content
                st.write(quiz)
                st.divider()
                st.download_button(
                    label="📥 Download Quiz",
                    data=clean_text(quiz),
                    file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    if feature == "🃏 Flashcard Generator":
        st.subheader("🃏 AI Flashcards")
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user",
                         "content": f"""Create exactly 15 flashcards from these notes.
Use this exact format for each flashcard:
QUESTION: write the question here
ANSWER: write the answer here

Separate each flashcard with a blank line.
Do not use any markdown symbols.
Notes:
{short_text}"""}
                    ]
                )
                flashcards_text = response.choices[0].message.content
                cards = flashcards_text.strip().split("\n\n")
                st.write("### Click each card to reveal the answer!")
                count = 1
                download_text = ""
                for card in cards:
                    lines = card.strip().split("\n")
                    question = ""
                    answer = ""
                    for line in lines:
                        if line.startswith("QUESTION:"):
                            question = line.replace("QUESTION:", "").strip()
                        elif line.startswith("ANSWER:"):
                            answer = line.replace("ANSWER:", "").strip()
                    if question and answer:
                        with st.expander(f"🃏 Card {count}: {question}"):
                            st.success(f"💡 {answer}")
                        download_text += f"Card {count}\nQ: {question}\nA: {answer}\n\n"
                        count += 1
                st.divider()
                st.download_button(
                    label="📥 Download Flashcards",
                    data=clean_text(download_text),
                    file_name=f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    if feature == "🎯 Key Points Extractor":
        st.subheader("🎯 Key Points from Your Notes")
        if st.button("Extract Key Points"):
            with st.spinner("Extracting key points..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user",
                         "content": f"""Extract the most important key points from these notes.
Use this exact format:
POINT: write the key point here
EXPLANATION: write a brief explanation here

Extract 10 key points and separate each with a blank line.
Do not use any markdown symbols.
Notes:
{short_text}"""}
                    ]
                )
                points_text = response.choices[0].message.content
                points = points_text.strip().split("\n\n")
                st.write("### 🎯 Most Important Points!")
                count = 1
                download_text = ""
                for point in points:
                    lines = point.strip().split("\n")
                    title = ""
                    explanation = ""
                    for line in lines:
                        if line.startswith("POINT:"):
                            title = line.replace("POINT:", "").strip()
                        elif line.startswith("EXPLANATION:"):
                            explanation = line.replace(
                                "EXPLANATION:", "").strip()
                    if title and explanation:
                        st.info(f"🎯 **Point {count}:** {title}")
                        st.write(f"📖 {explanation}")
                        st.divider()
                        download_text += f"Point {count}: {title}\nExplanation: {explanation}\n\n"
                        count += 1
                st.download_button(
                    label="📥 Download Key Points",
                    data=clean_text(download_text),
                    file_name=f"keypoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    if feature == "⚡ Difficulty Level Quiz":
        st.subheader("⚡ Choose Your Difficulty Level")
        difficulty = st.selectbox(
            "Select Difficulty Level",
            ["🟢 Easy", "🟡 Medium", "🔴 Hard"]
        )
        if difficulty == "🟢 Easy":
            level_prompt = """Create 10 EASY MCQ questions for beginners.
Do not use any markdown symbols.
Format each question like:
Q1. question here
a) option1
b) option2
c) option3
d) option4
Answer: correct answer"""
        elif difficulty == "🟡 Medium":
            level_prompt = """Create 10 MEDIUM difficulty MCQ questions.
Do not use any markdown symbols.
Format each question like:
Q1. question here
a) option1
b) option2
c) option3
d) option4
Answer: correct answer"""
        else:
            level_prompt = """Create 10 HARD MCQ questions for advanced students.
Do not use any markdown symbols.
Format each question like:
Q1. question here
a) option1
b) option2
c) option3
d) option4
Answer: correct answer"""
        if st.button("Generate Difficulty Quiz"):
            with st.spinner(f"Generating {difficulty} quiz..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "user",
                         "content": f"{level_prompt}\n\nNotes:\n{short_text}"}
                    ]
                )
                quiz = response.choices[0].message.content
                if difficulty == "🟢 Easy":
                    st.success("🟢 Easy Level Quiz")
                elif difficulty == "🟡 Medium":
                    st.warning("🟡 Medium Level Quiz")
                else:
                    st.error("🔴 Hard Level Quiz")
                st.write(quiz)
                st.divider()
                st.download_button(
                    label="📥 Download Quiz",
                    data=clean_text(quiz),
                    file_name=f"difficulty_quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

    if feature == "💬 Chat with Notes":
        st.subheader("💬 Chat with Your Notes")
        st.write("Ask any question about your uploaded notes!")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])

        user_question = st.chat_input("Ask anything about your notes...")

        if user_question:
            st.chat_message("user").write(user_question)
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system",
                         "content": f"You are a helpful study assistant. Answer questions only based on these notes. Do not use markdown symbols in your answers:\n\n{short_text}"},
                        *st.session_state.chat_history
                    ]
                )
                answer = response.choices[0].message.content
                st.chat_message("assistant").write(answer)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
