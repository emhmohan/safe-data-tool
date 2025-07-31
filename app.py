import streamlit as st
import pandas as pd
from modules import privacy, risk, utility, report

st.title("🛡️ SAFE DATA TOOL: Interactive Privacy Advisor")

st.sidebar.header("STEP 1: Security Preferences")
priority = st.sidebar.selectbox("Main security concern:",
                               ["Re-identification", "Data theft", "Maximum data utility"])
privacy_level = st.sidebar.radio("Privacy level needed:",
                                ["Maximum Privacy", "Balanced", "Maximum Utility"])
law = st.sidebar.selectbox("Compliance focus:", ["DPDP Act", "GDPR", "Research Ethics"])

st.sidebar.header("STEP 2: Upload Data")
file = st.sidebar.file_uploader("CSV file", type="csv")

if file:
    df = pd.read_csv(file)
    st.subheader("First 5 rows of your Data")
    st.write(df.head())

    st.header("STEP 3: Configure Columns")
    quasi_ids = st.multiselect("Select quasi-identifier columns (used for risk)", df.columns)
    sensitive = st.selectbox("Select a sensitive numeric column", df.columns)

    st.header("STEP 4: Privacy Pipeline")
    if st.button("Run Privacy Pipeline"):
        if not quasi_ids:
            st.error("Please select at least one quasi-identifier column.")
        else:
            df1 = df.copy()
            risk_before = risk.k_anonymity(df1, quasi_ids)
            user_choices = dict(priority=priority, privacy_level=privacy_level, law=law)

            if privacy_level == "Maximum Privacy":
                df2 = privacy.generalize_age(df1, "age") if "age" in quasi_ids else df1
                df2 = privacy.suppress_rare(df2, quasi_ids[0], threshold=20)
                df2 = privacy.dp_noise(df2, sensitive, epsilon=0.5)
            elif privacy_level == "Balanced":
                df2 = privacy.generalize_age(df1, "age") if "age" in quasi_ids else df1
                df2 = privacy.suppress_rare(df2, quasi_ids[0], threshold=10)
                df2 = privacy.dp_noise(df2, sensitive, epsilon=1.0)
            else:
                df2 = privacy.dp_noise(df1, sensitive, epsilon=3.0)

            risk_after = risk.k_anonymity(df2, quasi_ids)
            util = utility.ks_table(df1, df2, [sensitive])

            st.markdown(report.make_summary(user_choices, risk_before, risk_after, util), unsafe_allow_html=True)
            st.download_button("Download Protected Data", df2.to_csv(index=False), "protected.csv")

st.info("Each run produces tailored privacy/utility output — unique for every dataset and preference.")
