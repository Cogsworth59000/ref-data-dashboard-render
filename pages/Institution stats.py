import streamlit as st

# st.set_page_config(
#     page_title="REF Results Dashboard",
#     page_icon=":bar_chart:",
#     layout="wide"
# )

## --- StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script. --- ##

st.title(":bar_chart: Institution dashboard")
st.sidebar.markdown(":bar_chart: Filter the data")
