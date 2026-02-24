# Developed by dnoobnerd | Modified & Fixed Version

import streamlit as st
import pandas as pd
import base64
import random
import time
import datetime
import os
import socket
import platform
import secrets
import io
import plotly.express as px

# Database (safe import)
try:
    import pymysql
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

# Geo
try:
    import geocoder
    from geopy.geocoders import Nominatim
except:
    pass

# Resume parsing
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter

from streamlit_tags import st_tags
from PIL import Image

import nltk
from nltk.corpus import stopwords

# FIX: Safe NLTK download
try:
    stopwords.words('english')
except:
    nltk.download('stopwords')

#########################################
# SAFE DATABASE CONNECTION
#########################################

connection = None
cursor = None

if DB_AVAILABLE:
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='Rohith@91',
            db='cv',
            port=3306
        )
        cursor = connection.cursor()
    except:
        connection = None
        cursor = None

#########################################
# HELPER FUNCTIONS
#########################################

def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'


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


#########################################
# STREAMLIT CONFIG
#########################################

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

#########################################
# MAIN APP
#########################################

def run():

    st.title("🚀 AI Resume Intelligence")

    menu = ["User", "About"]
    choice = st.sidebar.selectbox("Select Option", menu)

    ###################################
    # USER SIDE
    ###################################
    if choice == "User":

        name = st.text_input("Name")
        email = st.text_input("Email")

        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

        if uploaded_file is not None:

            os.makedirs("Uploaded_Resumes", exist_ok=True)

            file_path = os.path.join("Uploaded_Resumes", uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success("Resume Uploaded Successfully!")

            resume_data = ResumeParser(file_path).get_extracted_data()

            if resume_data:

                resume_text = pdf_reader(file_path)

                st.subheader("Resume Analysis")

                st.write("Name:", resume_data.get("name"))
                st.write("Email:", resume_data.get("email"))
                st.write("Mobile:", resume_data.get("mobile_number"))
                st.write("Pages:", resume_data.get("no_of_pages"))

                ###################################
                # FIXED RESUME SCORE LOGIC
                ###################################
                score = 0

                if "objective" in resume_text.lower() or "summary" in resume_text.lower():
                    score += 10

                if "education" in resume_text.lower():
                    score += 10

                if "experience" in resume_text.lower():
                    score += 20

                if "project" in resume_text.lower():
                    score += 20

                if "skill" in resume_text.lower():
                    score += 15

                if "certification" in resume_text.lower():
                    score += 10

                st.subheader("Resume Score")
                st.progress(score)
                st.success(f"Your Resume Score: {score}/100")

                ###################################
                # DATABASE INSERT (SAFE)
                ###################################
                if cursor:
                    try:
                        insert_sql = """
                        INSERT INTO user_data (sec_token, act_name, act_mail, resume_score, Timestamp)
                        VALUES (%s,%s,%s,%s,%s)
                        """
                        cursor.execute(insert_sql, (
                            secrets.token_urlsafe(8),
                            name,
                            email,
                            score,
                            str(datetime.datetime.now())
                        ))
                        connection.commit()
                    except:
                        pass

            else:
                st.error("Could not parse resume.")

    ###################################
    # ABOUT
    ###################################
    else:
        st.write("""
        This tool analyzes resumes using NLP and provides insights.
        """)

run()
