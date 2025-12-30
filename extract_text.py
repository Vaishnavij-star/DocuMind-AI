import fitz  # PyMuPDF
import streamlit as st

def extract_text_from_pdf(uploaded_file):
    full_text = ""

    # Read PDF from memory
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text = page.get_text()
            if text:
                full_text += text + "\n"

    return full_text


# --------- Streamlit UI ---------
st.set_page_config(page_title="DocuMind AI PDF Reader", layout="wide")
st.title("📄 DocuMind AI PDF Reader")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    if extracted_text.strip():
        st.subheader("Extracted Text")
        st.text_area("Text from PDF", extracted_text, height=400)

        st.download_button(
            label="⬇️ Download Extracted Text",
            data=extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
    else:
        st.warning("No text found in this PDF (it may be scanned).")
else:
    st.info("Please upload a PDF to start.")
