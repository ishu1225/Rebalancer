# pages/2_Diversification_Assessment.py
import streamlit as st

st.set_page_config(page_title="Diversification Assessment", layout="wide")
st.title("⚖️ Diversification Assessment")

# --- Explanation Section ---
st.header("What is Diversification and Concentration Risk?")
st.markdown("""
**Diversification** is the practice of spreading your investments across various assets to minimize risk. The principle is simple: "Don't put all your eggs in one basket."

**Concentration Risk** is the opposite. It is the threat of loss from having too much of your portfolio invested in a single asset or sector. While concentration can lead to high returns, it can also lead to devastating losses.

A well-diversified portfolio is more resilient to market shocks. This page shows the AI's assessment of your portfolio's diversification based on your chosen risk profile.
""")

# Check if the analysis has been run
if "analysis_report" not in st.session_state or st.session_state.analysis_report is None:
    st.warning("Please go to the main page to upload and analyze your portfolio first.")
else:
    report = st.session_state.analysis_report
    assessment_text = report.get("diversification_assessment")

    if assessment_text:
        st.header("AI's Assessment of Your Portfolio")
        st.info(assessment_text)
    else:
        st.error("Could not display diversification assessment. The data may be missing from the AI's analysis.")
