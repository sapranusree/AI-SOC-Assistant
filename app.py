import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

from threat_analyzer import analyze_threat
from log_parser import parse_logs
from ioc_extractor import extract_iocs
from report_generator import generate_report

import pandas as pd
import plotly.express as px

# --------------------
# CONFIG
# --------------------

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

st.set_page_config(
    page_title="AI SOC Assistant",
    page_icon="🛡️",
    layout="wide"
)

# --------------------
# SIDEBAR
# --------------------

st.sidebar.title(
    "🛡️ SOC Control Panel"
)

st.sidebar.success(
    "System Online"
)

st.sidebar.write(
    "Version: 2.0"
)

st.sidebar.write(
    "Threat Engine: Active"
)

st.sidebar.write(
    "AI Model: Gemini"
)

st.sidebar.divider()

st.sidebar.info(
    "AI-Powered Security Operations Center"
)

# --------------------
# HEADER
# --------------------

st.title(
    "🛡️ AI SOC Assistant"
)

st.caption(
    "AI-Powered Security Operations Center for Threat Analysis"
)

# --------------------
# DASHBOARD
# --------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Threats Scanned",
        "128"
    )

with col2:
    st.metric(
        "Critical Threats",
        "12"
    )

with col3:
    st.metric(
        "Detection Rate",
        "96%"
    )

st.divider()

# --------------------
# INPUT
# --------------------

uploaded_file = st.file_uploader(
    "📂 Upload Log or Email",
    type=["txt"]
)

file_content = ""

if uploaded_file:

    file_content = (
        uploaded_file.read()
        .decode("utf-8")
    )

user_input = st.text_area(
    "📝 Paste suspicious content",
    height=250
)

content = (
    file_content
    if file_content
    else user_input
)

# --------------------
# ANALYSIS
# --------------------

if st.button(
    "🔍 Analyze Threat"
):

    if not content.strip():

        st.warning(
            "Enter some content first."
        )

    else:

        findings = parse_logs(
            content
        )

        st.subheader(
            "⚙️ Rule-Based Findings"
        )

        for finding in findings:

            st.info(finding)

        iocs = extract_iocs(
            content
        )

        st.subheader(
            "🔎 Indicators of Compromise"
        )

        st.write(
            "### IP Addresses"
        )

        st.write(
            iocs["ips"]
        )

        st.write(
            "### URLs"
        )

        st.write(
            iocs["urls"]
        )

        st.write(
            "### Domains"
        )

        st.write(
            iocs["domains"]
        )

        st.write(
            "### Emails"
        )

        st.write(
            iocs["emails"]
        )

        result = analyze_threat(
            model,
            content
        )

        st.subheader(
            "🤖 AI Analysis"
        )

        st.markdown(result)

        risk_score = 50

        match = re.search(
            r"(\d+)",
            result
        )

        if match:

            risk_score = int(
                match.group(1)
            )

            if risk_score > 100:
                risk_score = 100

        st.subheader(
            "📊 Risk Score"
        )

        st.progress(
            risk_score
        )

        st.write(
            f"{risk_score}/100"
        )

        chart_data = pd.DataFrame(
            {
                "Category": [
                    "Risk",
                    "Safe"
                ],
                "Value": [
                    risk_score,
                    100-risk_score
                ]
            }
        )

        fig = px.pie(
            chart_data,
            names="Category",
            values="Value",
            title="Threat Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        pdf_file = generate_report(
            result
        )

        with open(
            pdf_file,
            "rb"
        ) as file:

            st.download_button(
                "📄 Download Report",
                file,
                file_name=pdf_file
            )