import streamlit as st
from google.genai import Client
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_bytes

# -------------------------------
# Helper: Chunk text safely
# -------------------------------
def chunk_text(text, chunk_size=1200, overlap=200):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

# -------------------------------
# OCR helper (cached)
# -------------------------------
@st.cache_data(show_spinner=False)
def run_ocr(pdf_bytes):
    images = convert_from_bytes(pdf_bytes, dpi=300, fmt="png")
    ocr_text = ""
    config = "--oem 3 --psm 6"
    for img in images:
        ocr_text += pytesseract.image_to_string(img, config=config) + "\n"
    return ocr_text

# -------------------------------
# Initialize GenAI client
# -------------------------------
client = Client()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="📄 DocuMind AI", layout="wide")
st.title("📄 DocuMind AI")
st.write("Upload any PDF document (text or scanned) and ask questions. The AI will answer based only on your document.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file:
    text = ""

    # ---------- Try PyPDF2 text extraction ----------
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # ---------- OCR fallback ----------
    if not text.strip():
        st.warning("No text detected. Using OCR fallback...")
        with st.spinner("Running OCR (may take 20–30 seconds for large PDFs)..."):
            text = run_ocr(uploaded_file.getvalue())

    # ---------- Hard fail if no text ----------
    if not text.strip():
        st.error("❌ Unable to extract any text from this PDF.")
        st.stop()

    # ---------- Optional OCR Preview ----------
    if st.checkbox("Show raw extracted text"):
        st.text_area("Extracted Text Preview", text[:5000], height=250)

    st.success("PDF processed successfully!")

    # ---------- Chunking ----------
    chunks = chunk_text(text)
    st.write(f"📚 Document split into {len(chunks)} chunks for model processing")

    # ---------- Auto-select compatible model ----------
    selected_model = None
    for model in client.models.list():
        try:
            client.models.generate_content(model=model.name, contents="Hello")
            selected_model = model.name
            break
        except Exception:
            continue

    if not selected_model:
        st.error("❌ No compatible GenAI model found.")
        st.stop()

    st.write(f"✅ Using model: {selected_model}")

    # ---------- Question input ----------
    st.info("💡 Ask any question about the PDF (summary, facts, or details)")
    user_question = st.text_input("Your question:")

    if user_question:
        # Use keyword matching to select relevant chunks
        keywords = user_question.lower().split()
        relevant_chunks = [c for c in chunks if any(k in c.lower() for k in keywords)]
        if not relevant_chunks:
            # fallback: use first 3 chunks
            relevant_chunks = chunks[:3]
        context = "\n\n".join(relevant_chunks[:3])

        prompt = f"""
Answer ONLY using the document below.

DOCUMENT:
{context}

QUESTION:
{user_question}
"""
        with st.spinner("Generating answer..."):
            response = client.models.generate_content(
                model=selected_model,
                contents=prompt
            )

        st.subheader("Answer")
        st.write(response.text)