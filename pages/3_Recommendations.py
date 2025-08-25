
import streamlit as st

st.set_page_config(page_title="AI Recommendations", layout="wide")
st.title("🚀 AI Rebalancing Recommendations")

# --- Explanation Section ---
st.header("What is Portfolio Rebalancing?")
st.markdown("""
**Rebalancing** is the process of realigning the weights of a portfolio of assets. This involves periodically buying or selling assets to maintain your original desired level of asset allocation and risk.

**Why Rebalance?**
- **Maintain Risk Profile:** Over time, some investments grow faster than others, shifting your portfolio's balance and potentially making it riskier than you intended.
- **Disciplined Investing:** Rebalancing forces you to "buy low and sell high." You trim your winners and add to your underperformers.

Below are the AI-generated recommendations to help align your portfolio with your chosen risk profile.
""")

# Check if the analysis has been run
if "analysis_report" not in st.session_state or st.session_state.analysis_report is None:
    st.warning("Please go to the main page to upload and analyze your portfolio first.")
else:
    report = st.session_state.analysis_report
    recommendations = report.get("recommendations")

    if recommendations:
        st.header("Your Personalized Action Plan")

        with st.container(border=True):
            st.subheader("Strategy Summary")
            st.write(recommendations.get("summary", "No summary provided."))

        with st.container(border=True):
            st.subheader("Action Items")
            action_items = recommendations.get("action_items", [])
            if action_items:
                for item in action_items:
                    st.markdown(f"- {item}")
            else:
                st.write("No specific action items provided.")

        with st.container(border=True):
            st.subheader("Suggested ETFs for Diversification")
            etfs = recommendations.get("suggested_etfs", [])
            if etfs:
                for etf in etfs:
                    st.markdown(f"**{etf.get('ticker', 'N/A')} ({etf.get('name', 'N/A')}):** {etf.get('reason', 'No reason provided.')}")
            else:
                st.write("No specific ETFs were suggested.")
    else:
        st.error("Could not display recommendations. The data may be missing from the AI's analysis.")