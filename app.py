# -*- coding: utf-8 -*-
import streamlit as st
from news import extract_article_content, summarize_article
from pdfs import extract_text_from_pdf, summarize_pdf
from summary import elaborate_summary
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="QuickPeek",
    page_icon="🔎",
    layout="wide"
)

# Animated SVG background
st.markdown(
    '''
    <style>
    body {
        background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%) fixed;
    }
    .main-header {
        background: linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%);
        color: #2d2d2d;
        padding: 2.5rem 1rem 1.5rem 1rem;
        border-radius: 1.5rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 6px 24px rgba(252,182,159,0.15);
        text-align: center;
        position: relative;
    }
    .mascot {
        font-size: 3.5rem;
        position: absolute;
        left: 1.5rem;
        top: 1.2rem;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    .option-card {
        background: #fff6e9;
        border-radius: 1.2rem;
        padding: 2.2rem 1.7rem;
        box-shadow: 0 3px 12px rgba(252,182,159,0.13);
        margin-bottom: 2.2rem;
        border: 2px dashed #fcb69f;
        position: relative;
    }
    .stButton>button {
        background: linear-gradient(90deg, #fcb69f 0%, #ffecd2 100%);
        color: #2d2d2d;
        border: none;
        border-radius: 0.7rem;
        padding: 0.6rem 1.7rem;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 1.2rem;
        box-shadow: 0 2px 8px rgba(252,182,159,0.13);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ffecd2 0%, #fcb69f 100%);
        color: #ff6f00;
        transform: scale(1.05);
    }
    .confetti {
        font-size: 2rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .footer {
        margin-top: 2.5em;
        padding: 1.2em 0 0.5em 0;
        text-align: center;
        color: #888;
        font-size: 1.1em;
    }
    .footer a { color: #ff6f00; text-decoration: none; font-weight: bold; }
    .footer a:hover { text-decoration: underline; }
    </style>
    <svg width="100%" height="120" style="position:fixed;top:0;left:0;z-index:-1;" xmlns="http://www.w3.org/2000/svg">
      <circle cx="60" cy="60" r="50" fill="#fcb69f" fill-opacity="0.18">
        <animate attributeName="cx" values="60;90;60" dur="6s" repeatCount="indefinite" />
      </circle>
      <circle cx="90%" cy="40" r="30" fill="#ffecd2" fill-opacity="0.18">
        <animate attributeName="cy" values="40;80;40" dur="7s" repeatCount="indefinite" />
      </circle>
      <circle cx="30%" cy="100" r="20" fill="#fcb69f" fill-opacity="0.13">
        <animate attributeName="cx" values="30%;70%;30%" dur="8s" repeatCount="indefinite" />
      </circle>
    </svg>
    ''',
    unsafe_allow_html=True
)

# Playful font
st.markdown(
    """
    <style>@import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    html, body, [class*='css']  { font-family: 'Fredoka One', cursive !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-header">'
    '<span class="mascot">🦉</span>'
    '<h1 style="margin-bottom:0.1em; font-size:2.7rem; letter-spacing:1px;">QuickPeek <span style="font-size:1.5rem;">🔎</span></h1>'
    '<h4 style="font-weight:400; margin-bottom:0.2em;">Your fun, fast, and friendly AI Summarizer for News, PDFs, and More!</h4>'
    '<div class="confetti">🎉✨📚📰🦉✨🎉</div>'
    '</div>',
    unsafe_allow_html=True
)

# Use tabs for a modern, card-like experience
TABS = ["📰 News Peek", "📄 PDF Peek", "✨ Summary Glow-Up"]
tab1, tab2, tab3 = st.tabs(TABS)

with tab1:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    st.subheader("📰 News Peek")
    st.write("Paste a news article URL and let <b>QuickPeek</b> give you the scoop in seconds! 🦉", unsafe_allow_html=True)
    url = st.text_input("Enter news article URL:", placeholder="https://example.com/news-article", key="news-url")
    if st.button("Peek & Summarize! 📰", key="news-btn"):
        if not url:
            st.warning("Please enter a valid URL.")
        else:
            with st.spinner("QuickPeeking at your article..."):
                try:
                    title, content = extract_article_content(url)
                    if not content or len(content.strip()) < 50:
                        st.error("Could not extract enough content. Try another URL!")
                    else:
                        summary = summarize_article(content)
                        st.success("Here’s your QuickPeek! 🦉")
                        st.markdown(f"<b>Title:</b> {title}", unsafe_allow_html=True)
                        st.markdown(f"<b>Summary:</b> {summary}", unsafe_allow_html=True)
                        st.balloons()
                except Exception as e:
                    st.error(f"Oops! Something went wrong: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    st.subheader("📄 PDF Peek")
    st.write("Drop a PDF and let <b>QuickPeek</b> work its magic! 📄✨", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        if st.button("Peek & Summarize PDF! 📄", key="pdf-btn"):
            with st.spinner("Peeking into your PDF..."):
                try:
                    text = extract_text_from_pdf(tmp_path)
                    if not text or len(text.strip()) < 50:
                        st.error("Couldn’t find enough text in this PDF. Try another!")
                    else:
                        summary = summarize_pdf(text)
                        st.success("Here’s your QuickPeek! 🦉")
                        st.markdown(f"<b>Summary:</b> {summary}", unsafe_allow_html=True)
                        st.snow()
                except Exception as e:
                    st.error(f"Oops! Something went wrong: {str(e)}")
        os.remove(tmp_path)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="option-card">', unsafe_allow_html=True)
    st.subheader("✨ Summary Glow-Up")
    st.write("Paste a summary and let <b>QuickPeek</b> jazz it up for you! ✨🦉", unsafe_allow_html=True)
    summary_text = st.text_area("Paste your summary to glow up:", key="elab-text")
    if st.button("Glow Up My Summary! ✨", key="elab-btn"):
        if not summary_text or len(summary_text.strip()) < 10:
            st.warning("Please enter a summary to glow up!")
        else:
            with st.spinner("Giving your summary a QuickPeek Glow-Up..."):
                try:
                    elaborated = elaborate_summary(summary_text)
                    st.success("Here’s your Glow-Up! 🦉✨")
                    st.markdown(f"<b>Elaborated Summary:</b> {elaborated}", unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Oops! Something went wrong: {str(e)}")
    st.markdown('</div>', unsafe_allow_html=True)

# Custom footer
st.markdown(
    """
    <hr style='margin-top:2em; margin-bottom:1em;'>
    <div class='footer'>
        Made with 🦉 and Streamlit ·
        <a href='https://github.com/Dee0216/QuickPeek' target='_blank'>GitHub</a> ·
        <a href='mailto:deepikamuniyor2003@gmail.com'>Contact</a>
    </div>
    """,
    unsafe_allow_html=True
)
