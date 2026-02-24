# ================================
# AI RESUME ANALYZER (Cloud Safe)
# ================================

import streamlit as st
import pandas as pd
import os
import base64
import random
import time
import datetime
import io

# ================================
# 🔥 NLTK FIX FOR STREAMLIT CLOUD
# ================================

import nltk

nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", download_dir=nltk_data_path)

# IMPORTANT: import AFTER nltk fix
from pyresparser import ResumeParser

# PDF Extract
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter

# =================================
# HELPER FUNCTIONS
# =================================

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh):
            page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text


def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


# =================================
# STREAMLIT CONFIG
# =================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

# =================================
# MAIN APP
# =================================

def run():

    st.title("🚀 AI Resume Intelligence")
    st.markdown("Smart Resume Analysis • Cloud Compatible Version")

    menu = ["User", "About"]
    choice = st.sidebar.selectbox("Choose Option", menu)

    # ==========================
    # USER SECTION
    # ==========================
    if choice == "User":

        name = st.text_input("Your Name")
        email = st.text_input("Your Email")

        uploaded_file = st.file_uploader("Upload Resume (PDF Only)", type=["pdf"])

        if uploaded_file is not None:

            os.makedirs("Uploaded_Resumes", exist_ok=True)

            file_path = os.path.join("Uploaded_Resumes", uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("Resume Uploaded Successfully!")

            with st.spinner("Analyzing Resume..."):
                time.sleep(2)

                resume_data = ResumeParser(file_path).get_extracted_data()

                if resume_data:

                    resume_text = pdf_reader(file_path)

                    st.subheader("📊 Resume Analysis")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("Name:", resume_data.get("name"))
                        st.write("Email:", resume_data.get("email"))
                        st.write("Mobile:", resume_data.get("mobile_number"))

                    with col2:
                        st.write("Degree:", resume_data.get("degree"))
                        st.write("Pages:", resume_data.get("no_of_pages"))
                        st.write("Skills:", resume_data.get("skills"))

                    # ==========================
                    # RESUME SCORING
                    # ==========================
                    score = 0
                    text_lower = resume_text.lower()

                    if "objective" in text_lower or "summary" in text_lower:
                        score += 10
                    if "education" in text_lower:
                        score += 10
                    if "experience" in text_lower:
                        score += 20
                    if "project" in text_lower:
                        score += 20
                    if "skill" in text_lower:
                        score += 15
                    if "certification" in text_lower:
                        score += 10
                    if "achievement" in text_lower:
                        score += 15

                    st.subheader("📝 Resume Score")
                    st.progress(score)
                    st.success(f"Your Resume Score: {score}/100")

                    # ==========================
                    # EXPERIENCE LEVEL
                    # ==========================
                    if score >= 70:
                        st.success("🔥 Excellent Resume!")
                    elif score >= 40:
                        st.warning("👍 Good Resume, Improve More!")
                    else:
                        st.error("⚠️ Resume Needs Improvement")

                else:
                    st.error("Could not parse resume. Try another PDF.")

    # ==========================
    # ABOUT SECTION
    # ==========================
    else:
        st.subheader("About This Tool")
        st.write("""
        This AI Resume Analyzer extracts information from resumes
        using Natural Language Processing and provides scoring insights.
        
        Cloud Compatible Version.
        """)

# Run App
run()
