# 📄 DocuMind-AI

DocuMind-AI is an AI-powered PDF Question & Answer application that allows users to upload PDFs (text-based or scanned) and ask questions directly from the document content.

It supports **OCR for image-based PDFs**, works **offline**, and ensures answers are generated **only from the uploaded document**.

---

## 🚀 Features

- 📂 Upload any PDF (text or scanned)
- 🔍 Automatic text extraction using **PyPDF2**
- 🖼️ OCR fallback for scanned PDFs using **Tesseract**
- 🧠 Intelligent question answering based only on document content
- 📄 Large PDF handling via smart text chunking
- ⚡ Clean and readable answers
- 📴 Works fully offline (no vector DB required)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google GenAI**
- **PyPDF2**
- **pdf2image**
- **pytesseract**
- **Pillow**

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Vaishnavij-star/DocuMind-AI.git
cd DocuMind-AI


