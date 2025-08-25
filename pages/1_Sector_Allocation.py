# pages/1_Sector_Allocation.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sector Allocation", layout="wide")
st.title("📊 Sector Allocation Analysis")

# --- Explanation Section ---
st.header("What is Sector Allocation?")
st.markdown("""
Sector allocation is the strategy of dividing your investment portfolio among different economic sectors (e.g., Technology, Healthcare, Financials). The goal is to optimize your risk-to-return ratio by diversifying your assets. 

**Why it matters:**
- **Risk Mitigation:** If one sector performs poorly, your investments in other, better-performing sectors can help cushion the blow.
- **Capturing Growth:** Different sectors thrive in different economic conditions. A well-allocated portfolio allows you to capture growth wherever it occurs.
- **Avoiding Concentration Risk:** Putting too much money into a single sector makes your portfolio vulnerable.

Below is the sector breakdown of your current portfolio as determined by the AI.
""")

# Check if the analysis has been run
if "analysis_report" not in st.session_state or st.session_state.analysis_report is None:
    st.warning("Please go to the main page to upload and analyze your portfolio first.")
else:
    report = st.session_state.analysis_report
    allocation_data = report.get("sector_allocation")

    if allocation_data:
        st.header("Your Portfolio's Sector Breakdown")
        df = pd.DataFrame(allocation_data)

        # Display data table
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "sector": st.column_config.TextColumn("Sector"),
                         "investment": st.column_config.NumberColumn("Investment", format="$%.2f"),
                         "percentage": st.column_config.ProgressColumn("Percentage", format="%.2f%%", min_value=0, max_value=100)
                     })

        # Display interactive pie chart
        fig = px.pie(df, names='sector', values='percentage', title='Sector Allocation by Percentage')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Could not display sector allocation. The data may be missing from the AI's analysis.")