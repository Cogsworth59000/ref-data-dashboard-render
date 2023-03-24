import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

st.subheader("# Welcome 👋")
st.markdown("##")
st.write("This is an interactive dashboard for comparing Research Excellence Framework (REF) results across UK universities and disciplines.")
st.markdown("##")
st.write("Comparisons between REF 2021 and the previous exercise, REF 2014, are enabled by harmonization of HEI (Higher Education Institution) and UOA (Unit of Assessment) names.")
st.markdown("##")
st.write("For example, UOAs 12, 13, 14, and 15 in REF 2014 (Aeronautical, Mechanical, Chemical and Manufacturing Engineering, Electrical and Electronic Engineering, Metallurgy and Materials, Civil and Construction Engineering, and General Engineering) are grouped for comparison with UOA 12, Engineering, in REF 2021.")
st.markdown("##")
st.write("The dashboard allows exploration of all results and submissions data ('REF Overview data'), subject-specific comparisons ('UOA stats'), and shifts in QR funding outcomes ('Funding stats').")
st.markdown("##")
st.write("REF 2014 submissions and results data are [here](https://results.ref.ac.uk/).")
st.write("REF 2021 submissions and results data are [here](https://results2021.ref.ac.uk/).")
st.write("2021/22 funding data are [here](https://www.ukri.org/publications/quality-related-research-qr-funding-supporting-information-for-2021-to-2022/) (coverage: England).")
st.write("2022/23 funding data are [here](https://www.ukri.org/publications/qr-funding-supporting-information-for-2022-to-2023/) (coverage: England).")
st.markdown("##")
st.write("Tom Palmer")
st.write("2022")

##### ---- FUNCTIONS ---- ####

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="REF2021",
        skiprows=6,
        usecols="A:BD",
        nrows=7559,
    )
    df.set_index("Institution name")
    df["GPA"] = df["GPA"].round(2)
    df["FTE"] = df["FTE"].round(2)
    df["UOA number"] = df["UOA number"].astype("Int64")
    # df['total_ResearchIncome_forHEIforUOA_7years'] = df['total_ResearchIncome_forHEIforUOA_7years'].map(lambda x: f"£{x/1000:,.1f}k")
    # -- that was causing issues when trying to calculate on those numbers below (though back-conversion should be easy somehow)
    # df["REF2021_total_ResearchIncome_forHEIforUOA_7years"] = df["REF2021_total_ResearchIncome_forHEIforUOA_7years"].map(lambda x: f"{round(x / 1000, 1)}")
    df.rename(columns={"REF2021_total_ResearchIncome_forHEIforUOA_7years": "Income (GBP)", "REF2021_DoctoralAwards_7years": "Doctoral awards"}, inplace=True)
    return df

@st.cache
def get_2014_data_from_excel():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="REF2014",
        skiprows=7,
        usecols="A:AZ",
        nrows=7652,
    )
    df.set_index("Institution name")
    df["GPA"] = df["GPA"].round(2)
    df["FTE"] = df["FTE"].round(2)
    df["UOA number"] = df["UOA number"].astype("Int64")
    # df['total_ResearchIncome_forHEIforUOA_7years'] = df['total_ResearchIncome_forHEIforUOA_7years'].map(lambda x: f"£{x/1000:,.1f}k")
    # -- that was causing issues when trying to calculate on those numbers below (though back-conversion should be easy somehow)
    # df["total_ResearchIncome_forHEIforUOA_5years"] = df["total_ResearchIncome_forHEIforUOA_5years"].map(lambda x: f"{round(x / 1000, 1)}")
    df.rename(columns={"total_ResearchIncome_forHEIforUOA_5years": "Income (GBP)", "DoctoralAwards_5years": "Doctoral awards"}, inplace=True)
    return df
