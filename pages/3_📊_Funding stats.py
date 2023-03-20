import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

title = "Funding data"
st.title(":bar_chart:" + title)

# filter icon #
css_icon = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<i class="fa fa-filter"></i>
'''

## -- READ EXCEL -- ##

@st.cache
def get_MainPanel_data():
    df = pd.read_excel(
        io="ref_funding_data.xlsx",
        engine="openpyxl",
        sheet_name="MainPanel_Analysis",
        usecols="A:P",
        nrows=6,
    )
    return df

@st.cache
def get_UOA_data():
    df = pd.read_excel(
        io="ref_funding_data.xlsx",
        engine="openpyxl",
        sheet_name="UOA_Analysis",
        usecols="A:P",
        nrows=35,
    )
    return df

@st.cache
def get_HEI_data():
    df = pd.read_excel(
        io="ref_funding_data.xlsx",
        engine="openpyxl",
        sheet_name="HEI_Analysis",
        usecols="A:P",
        nrows=159,
    )
    return df

###### ---- DATA FRAMES --------###
df_MainPanel_funding_data = get_MainPanel_data()
df_uoa_funding_data = get_UOA_data()
df_hei_funding_data = get_HEI_data()

#### -- SIDEBAR --- #

st.sidebar.markdown(css_icon + " Filter the data", unsafe_allow_html=True)

UOA = st.sidebar.selectbox(
    "Select UOA",
    options=df_uoa_funding_data["UOA"],
    index=12
)

data = {
    "REF": ["2014", "2021"],
    "Total quality-related funding": [
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "2122_Funding"].iloc[0],
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "2223_Funding"].iloc[0]
    ],
    "Total quality-weighted volume": [
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "WeightedVolume_2014"].iloc[0],
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "WeightedVolume_2021"].iloc[0]
    ],
    "Quality-related funding per FTE": [
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "Funding_perFTE_2014"].iloc[0],
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "Funding_perFTE_2021"].iloc[0]
    ],
    "Quality-weighted volume per FTE":[
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "Volume_perFTE_2014"].iloc[0],
    df_MainPanel_funding_data.loc[df_MainPanel_funding_data["Main_Panel"]=="Total", "Volume_perFTE_2021"].iloc[0]
    ]
    }

df_overview = pd.DataFrame(data)

overview_cols = ["Total quality-weighted volume", "Total quality-related funding", "Quality-weighted volume per FTE", "Quality-related funding per FTE"]

fig_overview = px.bar(df_overview, x="REF", y="Total quality-related funding")

fig_overview = make_subplots(rows=2, cols=2,
subplot_titles=("Total quality-weighted volume", "Total quality-related funding", "Quality-weighted volume per FTE", "Quality-related funding per FTE"))

col = 1
for i in overview_cols[:2]:
    fig_overview.add_trace(
    go.Line(x=df_overview["REF"], y=df_overview[i]),
    row=1, col=col
    )
    col += 1

col = 1
for i in overview_cols[2:]:
    fig_overview.add_trace(
    go.Line(x=df_overview["REF"], y=df_overview[i]),
    row=2, col=col
    )
    col += 1



st.write(df_overview)
#
st.plotly_chart(fig_overview, use_container_width=True)
