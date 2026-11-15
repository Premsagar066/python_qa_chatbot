import streamlit as st
from chatbot import PythonQAChatbot

st.set_page_config(page_title="Python Q&A Bot", page_icon="🐍", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #306998 0%, #4b8bbe 50%, #ffd43b 100%);
    padding: 1.4rem 1.6rem;
    border-radius: 16px;
    margin-bottom: 1.2rem;
}
.hero h1 { color: white; margin: 0; font-size: 2rem; }
.hero p  { color: #f5f5f5; margin: 0.3rem 0 0 0; font-size: 0.95rem; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.78rem;
    font-weight: 600;
    color: white;
}
.high { background: #2e9e5b; }
.mid  { background: #e0a100; }
.low  { background: #d9534f; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_bot():
    return PythonQAChatbot()


bot = load_bot()

GREETING = {"role": "assistant",
            "content": "Hi! I'm your Python helper. Ask me a question about Python."}

if "messages" not in st.session_state:
    st.session_state.messages = [GREETING]

# ---------- Sidebar ----------
with st.sidebar:
    st.header("💡 Try asking")
    examples = [
        "What is a lambda function?",
        "How do I handle errors in Python?",
        "What is list comprehension?",
        "Difference between a list and a tuple",
        "How do I read a file?",
        "What is a decorator?",
    ]
    clicked = None
    for ex in examples:
        if st.button(ex, use_container_width=True):
            clicked = ex

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [GREETING]
        st.rerun()

    st.caption(f"Knowledge base: {len(bot.df)} questions")

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🐍 Python Q&A Chatbot</h1>
    <p>Ask about Python basics, functions, lists, OOP, NumPy or Pandas.</p>
</div>
""", unsafe_allow_html=True)


def badge(score):
    if score >= 0.6:
        return f'<span class="badge high">Confidence {score:.0%}</span>'
    if score >= 0.4:
        return f'<span class="badge mid">Confidence {score:.0%}</span>'
    return f'<span class="badge low">Confidence {score:.0%}</span>'


# ---------- Show history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🐍"):
        st.markdown(msg["content"], unsafe_allow_html=True)

# ---------- Handle new input ----------
typed = st.chat_input("Type your Python question here...")
user_input = clicked or typed

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    result = bot.get_answer(user_input)

    if result["found"]:
        reply = (f"{result['answer']}\n\n"
                 f"<small>Matched: *{result['matched_question']}*</small><br>"
                 f"{badge(result['score'])}")
    else:
        reply = "🤔 " + result["answer"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🐍"):
        st.markdown(reply, unsafe_allow_html=True)