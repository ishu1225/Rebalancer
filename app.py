# app.py
import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import io
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Portfolio Rebalancer",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Gemini API Functions ---
def get_gemini_analysis(api_key, risk_profile, portfolio_data=None, portfolio_image=None):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        json_structure = """
        {{
          "identified_country": "e.g., India",
          "sector_allocation": [
            {{"sector": "Sector Name", "investment": 15000, "percentage": 30.0}}
          ],
          "diversification_assessment": "A text summary of the portfolio's diversification.",
          "recommendations": {{
            "summary": "A brief summary of the rebalancing strategy.",
            "action_items": ["An actionable recommendation point."],
            "suggested_etfs": [
              {{"ticker": "NIFTYBEES.NS", "name": "Nifty 50 ETF", "reason": "For broad market diversification in India."}}
            ],
            "suggested_companies": [
              {{"ticker": "HDFCBANK.NS", "name": "HDFC Bank Ltd.", "reason": "To add exposure to the stable financial sector."}}
            ]
          }}
        }}
        """

        if portfolio_image:
            prompt_parts = [
                f"""You are an expert global financial analyst AI. Your task is to analyze the provided portfolio screenshot. First, perform OCR to extract all tickers and their values. Then, perform a full financial analysis and return the result as a single, clean JSON object. Do not include any text or markdown before or after the JSON.

                **Analysis Requirements:**
                1.  **OCR and Data Extraction:** Read all tickers and investment values from the image.
                2.  **Country Identification:** Determine the primary stock market country from the tickers.
                3.  **Sector Analysis:** Perform a sector allocation analysis.
                4.  **Diversification Assessment:** Provide an assessment based on a '{risk_profile}' risk profile.
                5.  **Country-Specific Recommendations:** All suggested ETFs and companies MUST be relevant to the identified country's stock market.

                **Required JSON Output Structure:**
                {json_structure}
                """,
                portfolio_image
            ]
        elif portfolio_data:
            prompt_parts = [
                f"""You are an expert global financial analyst AI. Your task is to analyze the provided portfolio data (in CSV format) and return your analysis as a single, clean JSON object. Do not include any text or markdown before or after the JSON.

                **Portfolio Data:**
                ```csv
                {portfolio_data}
                ```
                **Analysis Requirements:**
                1.  **Country Identification:** Determine the primary stock market country from the tickers.
                2.  **Sector Analysis:** Perform a sector allocation analysis.
                3.  **Diversification Assessment:** Provide an assessment based on a '{risk_profile}' risk profile.
                4.  **Country-Specific Recommendations:** All suggested ETFs and companies MUST be relevant to the identified country's stock market.

                **Required JSON Output Structure:**
                {json_structure}
                """
            ]
        else:
            return None

        response = model.generate_content(prompt_parts)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)

    except Exception as e:
        st.error(f"An error occurred while communicating with the Gemini API: {e}", icon="🚨")
        st.info("Common issues include an incorrect API key or network problems. Please verify your key and try again.")
        return None

# --- Main Page UI ---
st.title("🤖 AI Portfolio Rebalancer")
st.markdown("Welcome! Analyze your portfolio by uploading an Excel/CSV file or a clear screenshot. Start by providing your details below.")

if 'analysis_report' not in st.session_state:
    st.session_state.analysis_report = None

with st.sidebar:
    st.header("⚙️ Configuration")
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except:
        st.error("Gemini API key not found. Please add it to your Streamlit secrets.", icon="🚨")
        api_key = None

    uploaded_file = st.file_uploader(
        "Upload your Portfolio File or Screenshot",
        type=["xlsx", "csv", "png", "jpg", "jpeg"]
    )
    risk_profile = st.selectbox("Select your risk profile", ('Conservative', 'Moderate', 'Aggressive'))
    analyze_button = st.button("Analyze Portfolio", type="primary")

if analyze_button:
    if not api_key:
        st.warning("Cannot proceed without a configured Gemini API key.", icon="⚠️")
    elif not uploaded_file:
        st.warning("Please upload your portfolio file or screenshot.", icon="⚠️")
    else:
        with st.spinner("The AI is analyzing your portfolio... This may take a moment..."):
            try:
                file_type = uploaded_file.type
                
                if "image" in file_type:
                    image = Image.open(uploaded_file)
                    st.session_state.analysis_report = get_gemini_analysis(api_key=api_key, risk_profile=risk_profile.lower(), portfolio_image=image)
                else:
                    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
                    portfolio_string = df.to_csv(index=False)
                    st.session_state.analysis_report = get_gemini_analysis(api_key=api_key, risk_profile=risk_profile.lower(), portfolio_data=portfolio_string)

                if st.session_state.analysis_report:
                    st.switch_page("pages/1_Sector_Allocation.py")

            except Exception as e:
                # This is the line that was corrected. The 's' has been removed.
                st.error(f"An error occurred while processing your file: {e}", icon="🚨")