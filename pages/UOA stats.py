import streamlit as st
from REF_data import get_data_from_excel

# st.set_page_config(
#     page_title="REF Results Dashboard",
#     page_icon=":bar_chart:",
#     layout="wide"
# )

## --- StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script. --- ##

title = "UOA dashboard"
st.title(":bar_chart:" + title)
st.sidebar.markdown(":bar_chart: Filter the data")

df = get_data_from_excel()

UOA = st.sidebar.selectbox(
    "Select UOA",
    options=df["UOA name"].unique())
