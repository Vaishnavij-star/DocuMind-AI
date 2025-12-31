import streamlit as st
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
import re
import torch

from sentence_transformers import SentenceTransformer, util

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="DocuMind AI - Offline PDF Q&A",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocuMind AI - PDF Q&A (Offline/Free, OCR Enabled)")
st.write("Upload PDFs and ask unlimited questions. Works fully offline.")

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# -----------------------------
# Clean Text
# -----------------------------
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

# -----------------------------
# Sentence Split (NO nltk)
# -----------------------------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

# -----------------------------
# PDF Text + OCR
# -----------------------------
def extract_text_from_pdf(file_bytes):
    text = ""

    try:
        reader = PdfReader(file_bytes)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except:
        pass

    if not text.strip():
        images = convert_from_bytes(file_bytes)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    return clean_text(text)

# -----------------------------
# Answer Question (Sentence Level)
# -----------------------------
def answer_question(text, question, top_k=3):
    sentences = split_sentences(text)

    if not sentences:
        return "No readable content found."

    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    question_embedding = model.encode(question, convert_to_tensor=True)

    scores = util.cos_sim(question_embedding, sentence_embeddings)[0]
    top_results = torch.topk(scores, k=min(top_k, len(sentences)))

    best_sentences = [sentences[idx] for idx in top_results.indices]
    return " ".join(best_sentences)

# -----------------------------
# Upload PDFs
# -----------------------------
uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    pdf_texts = {}

    for file in uploaded_files:
        text = extract_text_from_pdf(file.read())
        if text:
            pdf_texts[file.name] = text

    st.success(f"✅ Loaded {len(pdf_texts)} PDF(s) successfully.")

    selected_pdf = st.selectbox(
        "Select a PDF to ask questions about",
        list(pdf_texts.keys())
    )

    question = st.text_input("Enter your question:")

    if question:
        with st.spinner("Finding answer..."):
            answer = answer_question(pdf_texts[selected_pdf], question)

        st.subheader("🤖 Answer:")
        st.write(answer)

else:
    st.info("Please upload at least one PDF to begin.")
