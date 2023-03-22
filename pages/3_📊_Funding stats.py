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
def get_2014_funding_data():
    df = pd.read_excel(
        io="ref_funding_data.xlsx",
        engine="openpyxl",
        sheet_name="2122byHEIbyUOA",
        usecols="A:V",
        nrows=4285,
    )
    return df

@st.cache
def get_2021_funding_data():
    df = pd.read_excel(
        io="ref_funding_data.xlsx",
        engine="openpyxl",
        sheet_name="2223byHEIbyUOA",
        usecols="A:V",
        nrows=4366,
    )
    return df

###### ---- DATA FRAMES --------###

df_detail_2014 = get_2014_funding_data()
df_detail_2021 = get_2021_funding_data()

#### -- SIDEBAR --- #

st.sidebar.markdown(css_icon + " Filter the data", unsafe_allow_html=True)

UOA = st.sidebar.selectbox(
    "Select UOA",
    options=sorted(df_detail_2021["UOA name"].unique()),
    index=12
)

HEI = st.sidebar.selectbox(
    "Select HEI:",
    options=sorted(df_detail_2021["Provider"].unique()),
    index=106
)

uoa_number = str(int(df_detail_2021.loc[df_detail_2021["UOA name"]==UOA, "UOA number"].values[0]))
main_panel = df_detail_2021.loc[df_detail_2021["UOA name"]==UOA, "Main panel"].values[0]

####### ---------- OVERVIEW ----------- #########
st.subheader("Overall shifts in funding variables between REF2014 and REF 2021")

#- metrics #
total_QR_2014 = df_detail_2014["Mainstream_QR"].sum()
total_QR_2021 = df_detail_2021["Mainstream_QR"].sum()
total_volume_2014 = df_detail_2014["Normalised_qual_vol"].sum()
total_volume_2021 = df_detail_2021["Normalised_qual_vol"].sum()
total_FTE_2014 = df_detail_2014["Eligible volume"].sum()
total_FTE_2021 = df_detail_2021["Eligible volume"].sum()
vol_per_FTE_2014 = total_volume_2014 / total_FTE_2014
vol_per_FTE_2021 = total_volume_2021 / total_FTE_2021
qr_per_FTE_2014 = total_QR_2014 / total_FTE_2014
qr_per_FTE_2021 = total_QR_2021 / total_FTE_2021

total_fund_change = total_QR_2021 / total_QR_2014 - 1
total_vol_change = total_volume_2021 / total_volume_2014 - 1
total_fte_change = total_FTE_2021 / total_FTE_2014 - 1
vol_per_fte_change = vol_per_FTE_2021 / vol_per_FTE_2014 - 1
qr_per_fte_change = qr_per_FTE_2021 / qr_per_FTE_2014 - 1

#-- charts --#
fig_bar_overview1 = px.bar(
    x=[
    "FTE",
    "Weighted volume",
    "QR funding allocation",
    "Weighted volume per FTE",
    "QR funding per FTE"
    ],
    y=[
    total_fte_change,
    total_vol_change,
    total_fund_change,
    vol_per_fte_change,
    qr_per_fte_change
    ]
)
fig_bar_overview1.update_traces(marker_color="cornflowerblue")
fig_bar_overview1.update_layout(
    title=dict(
        text="Percentage change",
        x=0.5,
        y=0.95,
        font=dict(
            family="Verdana",
            color='#000000'
            )
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title=None,
        xaxis=(dict(showgrid=False,)),
        yaxis=(dict(range=[-0.4, 0.8], tickformat=",.0%")),
)

df_bar_overview2 = pd.DataFrame(
    data={
        "REF":["REF 2014", "REF 2021"],
        "FTE":[total_FTE_2014, total_FTE_2021],
        "Weighted volume":[total_volume_2014, total_volume_2021],
        "QR funding allocation":[total_QR_2014, total_QR_2021],
        "Weighted volume per FTE":[vol_per_FTE_2014, vol_per_FTE_2021],
        "QR funding per FTE":[qr_per_FTE_2014, qr_per_FTE_2021]
    }
)

plot_cols = ["Weighted volume", "QR funding allocation", "Weighted volume per FTE", "QR funding per FTE"]

fig_bar_overview2 = make_subplots(rows=2, cols=2,
subplot_titles=("Total quality-weighted volume", "Total quality-related funding", "Quality-weighted volume per FTE", "Quality-related funding per FTE"))

col = 1
for i in plot_cols[:2]:
    fig_bar_overview2.add_trace(
    go.Bar(x=df_bar_overview2["REF"], y=df_bar_overview2[i]),
    row=1, col=col
    )
    col += 1

col = 1
for i in plot_cols[2:]:
    fig_bar_overview2.add_trace(
    go.Bar(x=df_bar_overview2["REF"], y=df_bar_overview2[i]),
    row=2, col=col,
    )
    col += 1

fig_bar_overview2.update_layout(
    title=dict(
        text="Absolute change",
        x=0.5,
        y=0.95,
        font=dict(
            family="Verdana",
            color='#000000'
            )
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title=None,
        xaxis=(dict(showgrid=False,))
)

### ------ FUNDING CHANGE ---- ####

# -- metrics -- ##

hei_uoa_vol_14 = df_detail_2014.loc[(df_detail_2014["Provider"]==HEI) & (df_detail_2014["UOA name"]==UOA), "Normalised_qual_vol"].sum()
hei_uoa_vol_21 = df_detail_2021.loc[(df_detail_2021["Provider"]==HEI) & (df_detail_2021["UOA name"]==UOA), "Normalised_qual_vol"].sum()
sector_uoa_vol_14 = df_detail_2014.loc[df_detail_2014["UOA name"]==UOA, "Normalised_qual_vol"].sum()
sector_uoa_vol_21 = df_detail_2021.loc[df_detail_2021["UOA name"]==UOA, "Normalised_qual_vol"].sum()
hei_panel_vol_14 = df_detail_2014.loc[(df_detail_2014["Provider"]==HEI) & (df_detail_2014["Main panel"]==main_panel), "Normalised_qual_vol"].sum()
hei_panel_vol_21 = df_detail_2021.loc[(df_detail_2021["Provider"]==HEI) & (df_detail_2021["Main panel"]==main_panel), "Normalised_qual_vol"].sum()
sector_panel_vol_14 = df_detail_2014.loc[df_detail_2014["Main panel"]==main_panel, "Normalised_qual_vol"].sum()
sector_panel_vol_21 = df_detail_2021.loc[df_detail_2021["Main panel"]==main_panel, "Normalised_qual_vol"].sum()
hei_vol_14 = df_detail_2014.loc[df_detail_2014["Provider"]==HEI, "Normalised_qual_vol"].sum()
hei_vol_21 = df_detail_2021.loc[df_detail_2021["Provider"]==HEI, "Normalised_qual_vol"].sum()

hei_uoa_fund_14 = df_detail_2014.loc[(df_detail_2014["Provider"]==HEI) & (df_detail_2014["UOA name"]==UOA), "Mainstream_QR"].sum()
hei_uoa_fund_21 = df_detail_2021.loc[(df_detail_2021["Provider"]==HEI) & (df_detail_2021["UOA name"]==UOA), "Mainstream_QR"].sum()
sector_uoa_fund_14 = df_detail_2014.loc[df_detail_2014["UOA name"]==UOA, "Mainstream_QR"].sum()
sector_uoa_fund_21 = df_detail_2021.loc[df_detail_2021["UOA name"]==UOA, "Mainstream_QR"].sum()
hei_panel_fund_14 = df_detail_2014.loc[(df_detail_2014["Provider"]==HEI) & (df_detail_2014["Main panel"]==main_panel), "Mainstream_QR"].sum()
hei_panel_fund_21 = df_detail_2021.loc[(df_detail_2021["Provider"]==HEI) & (df_detail_2021["Main panel"]==main_panel), "Mainstream_QR"].sum()
sector_panel_fund_14 = df_detail_2014.loc[df_detail_2014["Main panel"]==main_panel, "Mainstream_QR"].sum()
sector_panel_fund_21 = df_detail_2021.loc[df_detail_2021["Main panel"]==main_panel, "Mainstream_QR"].sum()
hei_fund_14 = df_detail_2014.loc[df_detail_2014["Provider"]==HEI, "Mainstream_QR"].sum()
hei_fund_21 = df_detail_2021.loc[df_detail_2021["Provider"]==HEI, "Mainstream_QR"].sum()

uoa_list = df_detail_2021["UOA name"].unique()
uoa_panels_list = [df_detail_2014.loc[df_detail_2014["UOA name"]==i, "Main panel"].iloc[0] for i in uoa_list]
uoa_fund_totals_2014 = [df_detail_2014.loc[df_detail_2014["UOA name"]==i, "Mainstream_QR"].sum() for i in uoa_list]
uoa_fund_totals_2021 = [df_detail_2021.loc[df_detail_2021["UOA name"]==i, "Mainstream_QR"].sum() for i in uoa_list]
uoa_FTE_totals_2014 = [df_detail_2014.loc[df_detail_2014["UOA name"]==i, "Eligible volume"].sum() for i in uoa_list]
uoa_FTE_totals_2021 = [df_detail_2021.loc[df_detail_2021["UOA name"]==i, "Eligible volume"].sum() for i in uoa_list]

df_funding_by_uoa = pd.DataFrame(
data={"UOAs": uoa_list, "Main panel":uoa_panels_list, "QR REF 2014": uoa_fund_totals_2014, "QR REF 2021": uoa_fund_totals_2021}
)
df_funding_by_uoa["Change"] = df_funding_by_uoa["QR REF 2021"] / df_funding_by_uoa["QR REF 2014"] - 1
df_funding_by_uoa.at[df_funding_by_uoa["UOAs"].loc[lambda x: x==UOA].index[0],"Main panel"] = UOA

df_perFTE_fund_by_uoa = pd.DataFrame(
data={"UOAs": uoa_list,
"Main panel":uoa_panels_list,
"FTE 2014": uoa_FTE_totals_2014,
"FTE 2021": uoa_FTE_totals_2021,
"QR 2014": uoa_fund_totals_2014,
"QR 2021": uoa_fund_totals_2021}
)
df_perFTE_fund_by_uoa["QR per FTE 2014"] = df_perFTE_fund_by_uoa["QR 2014"] / df_perFTE_fund_by_uoa["FTE 2014"]
df_perFTE_fund_by_uoa["QR per FTE 2021"] = df_perFTE_fund_by_uoa["QR 2021"] / df_perFTE_fund_by_uoa["FTE 2021"]
df_perFTE_fund_by_uoa["Change"] = df_perFTE_fund_by_uoa["QR per FTE 2021"] / df_perFTE_fund_by_uoa["QR per FTE 2014"] - 1
df_perFTE_fund_by_uoa.at[df_perFTE_fund_by_uoa["UOAs"].loc[lambda x: x==UOA].index[0],"Main panel"] = UOA

# -- charts --#

fig_uoa_overview1 = px.bar(df_funding_by_uoa, x="UOAs", y="Change", color="Main panel")

fig_uoa_overview1.update_layout(
    title=dict(
        text="% change in QR funding across UOAs between REF2014 and REF2021 (2022 prices)",
        x=0.5
        ),
        font=dict(
        family="Verdana",
        size=9
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title=None,
        yaxis=(dict(range=[-0.3, 0.6], tickformat=",.0%")),
)


fig_uoa_overview2 = px.bar(df_perFTE_fund_by_uoa, x="UOAs", y="Change", color="Main panel")

fig_uoa_overview2.update_layout(
    title=dict(
        text="% change in QR funding per FTE across UOAs between REF2014 and REF2021 (2022 prices)",
        x=0.5
        ),
        font=dict(
        family="Verdana",
        size=9
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title=None,
        yaxis_title=None,
        yaxis=(dict(range=[-0.4, 0.4], tickformat=",.0%")),
)


lcol_0, rcol_0 = st.columns(2)
with lcol_0:
    st.plotly_chart(fig_bar_overview1, use_container_width=True)
    st.plotly_chart(fig_uoa_overview1, use_container_width=True)
with rcol_0:
    st.plotly_chart(fig_bar_overview2, use_container_width=True)
    st.write(fig_uoa_overview2, use_container_width=True)


####---- UOA vs sector -- ######
st.markdown("---")
st.subheader(f"{HEI} UOA {uoa_number} vs UOA {uoa_number}, Main Panel {main_panel} and UK sector")


volume_table = pd.DataFrame(
data={
    "":[
    f"{HEI} UOA {uoa_number} weighted volume",
    f"UK sector UOA {uoa_number} weighted volume",
    f"{HEI} Main Panel {main_panel} weighted volume",
    f"UK sector Main Panel {main_panel} weighted volume",
    f"{HEI} weighted volume",
    "UK sector weighted volume"
    ],
    "REF 2014":[
    hei_uoa_vol_14,
    sector_uoa_vol_14,
    hei_panel_vol_14,
    sector_panel_vol_14,
    hei_vol_14,
    total_volume_2014
    ],
    "REF 2021":[
    hei_uoa_vol_21,
    sector_uoa_vol_21,
    hei_panel_vol_21,
    sector_panel_vol_21,
    hei_vol_21,
    total_volume_2021],
    "Factor of":[
    round(hei_uoa_vol_21 / hei_uoa_vol_14, 2),
    round(sector_uoa_vol_21 / sector_uoa_vol_14, 2),
    round(hei_panel_vol_21 / hei_panel_vol_14, 2),
    round(sector_panel_vol_21 / sector_panel_vol_14, 2),
    round(hei_vol_21 / hei_vol_14, 2),
    round(total_volume_2021 / total_volume_2014, 2)
    ]
    }
)

funding_table = pd.DataFrame(
data={
    "":[
    f"{HEI} UOA {uoa_number} QR funding",
    f"UK sector UOA {uoa_number} QR funding",
    f"{HEI} Main Panel {main_panel} QR funding",
    f"UK sector Main Panel {main_panel} QR funding",
    f"{HEI} QR funding",
    "UK sector QR funding"
    ],
    "REF 2014":[
    hei_uoa_fund_14,
    sector_uoa_fund_14,
    hei_panel_fund_14,
    sector_panel_fund_14,
    hei_fund_14,
    total_QR_2014
    ],
    "REF 2021":[
    hei_uoa_fund_21,
    sector_uoa_fund_21,
    hei_panel_fund_21,
    sector_panel_fund_21,
    hei_fund_21,
    total_QR_2021],
    "Factor of":[
    round(hei_uoa_fund_21 / hei_uoa_fund_14, 2),
    round(sector_uoa_fund_21 / sector_uoa_fund_14, 2),
    round(hei_panel_fund_21 / hei_panel_fund_14, 2),
    round(sector_panel_fund_21 / sector_panel_fund_14, 2),
    round(hei_fund_21 / hei_fund_14, 2),
    round(total_QR_2021 / total_QR_2014, 2)
    ]
    }
)

styler_vol = volume_table.style.hide_index().format(subset=[
    "REF 2014","REF 2021", "Factor of"],
    decimal='.',
    precision=2)

styler_fund = funding_table.style.hide_index().format(subset=[
    "REF 2014","REF 2021", "Factor of"],
    decimal='.',
    precision=2)

df_fund_2014 = pd.DataFrame(
    data={
    "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
    "Total QR":[hei_uoa_fund_14, sector_uoa_fund_14]
    }
)

df_fund_2021 = pd.DataFrame(
    data={
    "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
    "Total QR":[hei_uoa_fund_21, sector_uoa_fund_21]
    }
)

fig_fund_2014 = px.pie(df_fund_2014, values="Total QR", names="Level", hole = 0.4,
color_discrete_sequence=["lightblue", "cornflowerblue"])

fig_fund_2014.update_layout(
    title=dict(
        text=f"{HEI} UOA {uoa_number} funding share vs UOA {uoa_number} REF 2014",
        x=0.5,
        y=0.95,
        font=dict(
            family="Verdana",
            size=11,
            color='#000000'
        )
    )
)

fig_fund_2021 = px.pie(df_fund_2021, values="Total QR", names="Level", hole = 0.4,
color_discrete_sequence=["lightblue", "cornflowerblue"])

fig_fund_2021.update_layout(
    title=dict(
        text=f"{HEI} UOA {uoa_number} funding share vs UOA {uoa_number} REF 2021",
        x=0.5,
        y=0.95,
        font=dict(
            family="Verdana",
            size=11,
            color='#000000'
        )
    )
)

lcol, rcol = st.columns(2)

with lcol:
    st.table(styler_vol)
    st.plotly_chart(fig_fund_2014, use_container_width=True)
with rcol:
    st.table(styler_fund)
    st.plotly_chart(fig_fund_2021, use_container_width=True)

st.markdown("##")
st.write("Weighted volume = 4 x FourStarVolume(HEI) / 5 + ThreeStarVolume(HEI) / 5.", "[Four/Three]StarVolume = [four/three] star fraction x FTE")
