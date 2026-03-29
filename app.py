import streamlit as st
import os
from dotenv import load_dotenv
from summarizer import summarize_text
from scraper import scrape_url

load_dotenv()

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Text Summarizer")
st.caption("Powered by Claude · Paste text, enter a URL, or upload a file")

# --- Format toggle ---
format_option = st.radio(
    "Summary format",
    ["Structured (title + summary + bullets)", "Paragraph", "Bullet points only"],
    horizontal=True
)

format_map = {
    "Structured (title + summary + bullets)": "structured",
    "Paragraph": "paragraph",
    "Bullet points only": "bullets",
}
selected_format = format_map[format_option]

# --- Input method tabs ---
tab1, tab2, tab3 = st.tabs(["📋 Paste Text", "🌐 URL", "📁 Upload File"])

input_text = None

with tab1:
    pasted = st.text_area("Paste your text here", height=250, placeholder="Paste any article, document, or text...")
    if pasted:
        input_text = pasted

with tab2:
    url = st.text_input("Enter a URL", placeholder="https://example.com/article")
    if url:
        with st.spinner("Fetching page content..."):
            try:
                input_text = scrape_url(url)
                st.success(f"Fetched {len(input_text.split())} words from URL.")
            except Exception as e:
                st.error(f"Could not fetch URL: {e}")

with tab3:
    uploaded = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    if uploaded:
        if uploaded.type == "text/plain":
            input_text = uploaded.read().decode("utf-8")
        elif uploaded.type == "application/pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(uploaded)
                input_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                st.success(f"Extracted {len(input_text.split())} words from PDF.")
            except Exception as e:
                st.error(f"Could not read PDF: {e}")

# --- Summarize button ---
st.divider()

if st.button("✨ Summarize", type="primary", disabled=not input_text):
    if not os.getenv("GROQ_API_KEY"):
        st.error("No GROQ_API_KEY found. Add it to your .env file.")
    else:
        with st.spinner("Summarizing..."):
            try:
                result = summarize_text(input_text, selected_format)

                st.subheader("Summary")

                if selected_format == "structured":
                    st.markdown(result)
                elif selected_format == "paragraph":
                    st.write(result)
                else:
                    st.markdown(result)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
