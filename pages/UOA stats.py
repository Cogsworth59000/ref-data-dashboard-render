import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from REF_data import get_data_from_excel, get_2014_data_from_excel

# st.set_page_config(
#     page_title="REF Results Dashboard",
#     page_icon=":bar_chart:",
#     layout="wide"
# )

## --- StreamlitAPIException: set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script. --- ##

#--TITLE--#
title = "UOA dashboard"
st.title(":bar_chart:" + title)

# filter icon #
css_icon = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<i class="fa fa-filter"></i>
'''
#-- FUNCTIONS --#
def show_grid():
    df = df_uoa.sort_values("4*")[::-1][:20]
    styler = df.style.hide_index().format(subset=[
        "GPA","FTE", "4*", "3*", "2*", "1*", "U/C", "Doctoral awards"],
        decimal='.',
        precision=2)
    st.dataframe(styler)

def unshow_grid():
    return

@st.cache
def get_2021_averages():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="2021_averageProfiles",
        usecols="A:K",
        nrows=137,
    )
    return df

@st.cache
def get_2014_averages():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="2014_averageProfiles",
        usecols="A:K",
        nrows=145,
    )
    return df

@st.cache
def get_2021_quartiles():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="2021_quartiles",
        usecols="A:K",
        nrows=409,
    )
    return df

@st.cache
def get_2014_quartiles():
    df = pd.read_excel(
        io="all_ref_results.xlsx",
        engine="openpyxl",
        sheet_name="2014_quartiles",
        usecols="A:K",
        nrows=433,
    )
    return df

#--READ EXCEL DATA--#
df = get_data_from_excel()
df2014 = get_2014_data_from_excel()
df_2021Average = get_2021_averages()
df_2014Average = get_2014_averages()
df_2021Quartiles = get_2021_quartiles()
df_2014Quartiles = get_2014_quartiles()

df_display = df[[
    "Institution name",
    "Main panel",
    "UOA number",
    "UOA name",
    "Profile",
    "FTE",
    "4*", "3*", "2*", "1*", "U/C", "GPA",
    "REF2021_weighted_volume",
    "Income (GBP)", "Doctoral awards"
]]

df_2014 = df2014[[
    "Institution name",
    "Main panel",
    "UOA number",
    "UOA name",
    "Profile",
    "FTE",
    "4*", "3*", "2*", "1*", "U/C", "GPA",
    "weighted_volume",
    "Income (GBP)", "Doctoral awards"
]]

# df_2014.rename(columns={"REF2014_total_ResearchIncome_forHEIforUOA_5years": "REF2014 income (GBP)", "REF2014_DoctoralAwards_5years": "REF2014 doctoral awards"}, inplace=True)

#---- SIDEBAR ----#
st.sidebar.markdown(css_icon + " Filter the data", unsafe_allow_html=True)

UOA = st.sidebar.selectbox(
    "Select UOA",
    options=sorted(df["UOA name"].unique()),
    index=13
)

HEI = st.sidebar.selectbox(
    "Select HEI:",
    options=sorted(df["Institution name"].unique()),
    index=127
)

profile = st.sidebar.selectbox(
    "Select Profile:",
    options=df["Profile"].unique()
)

df_selection = df_display.query(
    "Profile == @profile & `UOA name` == @UOA & `Institution name` == @HEI"
)

df_selection_2014 = df_2014.query(
    "Profile == @profile & `UOA name` == @UOA & `Institution name` == @HEI"
)

df_uoa = df_display.query("`UOA name` == @UOA & Profile == @profile")
df_uoa_2014 = df_2014.query("`UOA name` == @UOA & Profile == @profile")

uoa_number = str(df_uoa["UOA number"].unique()[0])
main_panel_2021 = df_selection["Main panel"].unique()[0]
main_panel_2014 = df_selection_2014["Main panel"].unique()[0]

show_table = st.sidebar.button("Show top 20", help="Show top twenty by 4* by UOA and profile in a sortable table", on_click=show_grid)
hide_table = st.sidebar.button("Hide top 20", help="Hide the table", on_click=unshow_grid)

# ------- MAINPAGE ------ #
st.markdown("##") # new paragraph
st.markdown("---")

# -- Metrics --- #
st.header(f"REF 2021: {UOA} (UOA {uoa_number})")

df_uoa["Income (GBP)"] = df_uoa["Income (GBP)"].map(lambda x: float(x))
df_uoa_2014["Income (GBP)"] = df_uoa_2014["Income (GBP)"].map(lambda x: float(x))

uoa_submissions = df_uoa["Institution name"].count()
uoa_size = round(df_uoa["FTE"].sum(), 2)
uoa_size_2014 = round(df_uoa_2014["FTE"].sum(), 2)
average_size = round(df_uoa["FTE"].mean(), 2)
average_income = int(df_uoa["Income (GBP)"].mean())
uoa_income = round(df_uoa["Income (GBP)"].sum(),2)
uoa_income_2014 = round(df_uoa_2014["Income (GBP)"].sum(),2)
uoa_volume_2021 = round(df_uoa["REF2021_weighted_volume"].sum(), 2)
uoa_volume_2014 = round(df_uoa_2014["weighted_volume"].sum(), 2)
average_phds = round(df_uoa["Doctoral awards"].mean(), 2)

left_col, middle_col1, middle_col2, middle_col3, right_col = st.columns(5)
with left_col:
    st.subheader("HEIs submitted:")
    st.subheader(f"{uoa_submissions}")
with middle_col1:
    st.subheader("UOA size:")
    st.subheader(f"{uoa_size} FTE")
with middle_col2:
    st.subheader("Average FTE:")
    st.subheader(f"{average_size} FTE")
with middle_col3:
    st.subheader("Average income:")
    st.subheader(f"£{average_income:,}")
with right_col:
    st.subheader("Average PhDs:")
    st.subheader(f"{average_phds}")

st.markdown("---")

st.subheader("Quality profile:")

    # ---- DATA FRAMES ---- #

try:
    average_profile_2021_data = df_2021Average.loc[(df_2021Average["UOA name"]==UOA) & (df_2021Average["Profile Type"]==profile), ["4*", "3*", "2*", "1*", "u/c"]]
    average_profile_2014_data = df_2014Average.loc[(df_2014Average["UOA name"]==UOA) & (df_2014Average["Profile Type"]==profile), ["4*", "3*", "2*", "1*", "u/c"]]
    hei_profile_2021_data = df_selection[["4*", "3*", "2*", "1*", "U/C"]]
    hei_profile_2014_data = df_selection_2014[["4*", "3*", "2*", "1*", "U/C"]]
    quartile_2021_data = df_2021Quartiles.loc[(df_2021Quartiles["UOA name"]==UOA) & (df_2021Quartiles["Profile Type"]==profile), ["Quality level", "Median"]]
    quartile_2014_data = df_2014Quartiles.loc[(df_2014Quartiles["UOA name"]==UOA) & (df_2014Quartiles["Profile Type"]==profile), ["Quality level", "Median"]]
    hei_quartile_2021_data = pd.DataFrame(data ={"4*":hei_profile_2021_data["4*"], "4* and 3*":hei_profile_2021_data["4*"] + hei_profile_2021_data["3*"], "4*, 3* and 2*":hei_profile_2021_data["4*"] + hei_profile_2021_data["3*"] + hei_profile_2021_data["2*"]})
    hei_quartile_2014_data = pd.DataFrame(data ={"4*":hei_profile_2014_data["4*"], "4* and 3*":hei_profile_2014_data["4*"] + hei_profile_2014_data["3*"], "4*, 3* and 2*":hei_profile_2014_data["4*"] + hei_profile_2014_data["3*"] + hei_profile_2014_data["2*"]})

    df_quality_2021 = pd.DataFrame(
    data={
        "Profile":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "4*":[hei_profile_2021_data["4*"].iloc[0], average_profile_2021_data["4*"].iloc[0]],
        "3*":[hei_profile_2021_data["3*"].iloc[0], average_profile_2021_data["3*"].iloc[0]],
        "2*":[hei_profile_2021_data["2*"].iloc[0], average_profile_2021_data["2*"].iloc[0]],
        "1*":[hei_profile_2021_data["1*"].iloc[0], average_profile_2021_data["1*"].iloc[0]],
        "U/C":[hei_profile_2021_data["U/C"].iloc[0], average_profile_2021_data["u/c"].iloc[0]]
        }
    )

    df_quality_2014 = pd.DataFrame(
    data={
        "Profile":[f"{HEI}", f"UK sector, UOA {uoa_number}"],
        "4*":[hei_profile_2014_data["4*"].iloc[0], average_profile_2014_data["4*"].iloc[0]],
        "3*":[hei_profile_2014_data["3*"].iloc[0], average_profile_2014_data["3*"].iloc[0]],
        "2*":[hei_profile_2014_data["2*"].iloc[0], average_profile_2014_data["2*"].iloc[0]],
        "1*":[hei_profile_2014_data["1*"].iloc[0], average_profile_2014_data["1*"].iloc[0]],
        "U/C":[hei_profile_2014_data["U/C"].iloc[0], average_profile_2014_data["u/c"].iloc[0]]
        }
    )

    df_quartile_2021 = pd.DataFrame(
    data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "4*":[hei_quartile_2021_data["4*"].iloc[0], quartile_2021_data.loc[(quartile_2021_data["Quality level"]=="4*"),["Median"]]["Median"].iloc[0]],
        "4* and 3*":[hei_quartile_2021_data["4* and 3*"].iloc[0], quartile_2021_data.loc[(quartile_2021_data["Quality level"]=="4* and 3*"),["Median"]]["Median"].iloc[0]],
        "4*, 3* and 2*":[hei_quartile_2021_data["4*, 3* and 2*"].iloc[0], quartile_2021_data.loc[(quartile_2021_data["Quality level"]=="4*, 3* and 2*"),["Median"]]["Median"].iloc[0]]
        }
    )

    df_quartile_2014 = pd.DataFrame(
    data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "4*":[hei_quartile_2014_data["4*"].iloc[0], quartile_2014_data.loc[(quartile_2014_data["Quality level"]=="4*"),["Median"]]["Median"].iloc[0]],
        "4* and 3*":[hei_quartile_2014_data["4* and 3*"].iloc[0], quartile_2014_data.loc[(quartile_2014_data["Quality level"]=="4* and 3*"),["Median"]]["Median"].iloc[0]],
        "4*, 3* and 2*":[hei_quartile_2014_data["4*, 3* and 2*"].iloc[0], quartile_2014_data.loc[(quartile_2014_data["Quality level"]=="4*, 3* and 2*"),["Median"]]["Median"].iloc[0]]
        }
    )

    df_size_2021 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "FTE":[df_selection["FTE"].iloc[0], uoa_size]
        }
    )

    df_size_2014 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "FTE":[df_selection_2014["FTE"].iloc[0], uoa_size_2014]
        }
    )

    df_income_2021 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "Income (GBP)":[df_selection["Income (GBP)"].iloc[0], uoa_income]
        }
    )

    df_income_2014 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "Income (GBP)":[df_selection_2014["Income (GBP)"].iloc[0], uoa_income_2014]
        }
    )

    df_volume_2021 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "REF2021_weighted_volume":[df_selection["REF2021_weighted_volume"].iloc[0], uoa_volume_2021]
        }
    )

    df_volume_2014 = pd.DataFrame(
        data={
        "Level":[f"{HEI}",  f"UK sector, UOA {uoa_number}"],
        "weighted_volume":[df_selection_2014["weighted_volume"].iloc[0], uoa_volume_2014]
        }
    )

    cols_2021 = ["FTE", "GPA", "Income (GBP)", "Doctoral awards", "REF2021_weighted_volume"]
    cols_2014 = ["FTE", "GPA", "Income (GBP)", "Doctoral awards", "weighted_volume"]

    scatter_df_2021_panel = df.loc[(df["Profile"] == "Overall") & (df["Main panel"] == main_panel_2021)][cols_2021]
    scatter_df_2014_panel = df2014.loc[(df2014["Profile"] == "Overall") & (df2014["Main panel"] == main_panel_2014)][cols_2014]

    scatter_df_2021_uoa = df.loc[(df["Profile"] == "Overall") & (df["UOA name"] == UOA)][cols_2021]
    scatter_df_2014_uoa = df2014.loc[(df2014["Profile"] == "Overall") & (df2014["UOA name"] == UOA)][cols_2014]

    # -------------- CHARTS ------------------ #

    l_col1, r_col1 = st.columns(2)

    fig_profile_2021 = px.bar(df_quality_2021, y="Profile", x=["4*", "3*", "2*", "1*", "U/C"], orientation="h",
    color_discrete_sequence=["lightslategray", "cornflowerblue", "darkturquoise", "lightblue", "white"],
    text_auto=True
    )

    fig_profile_2021.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} quality profile vs UOA average profile, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        ),
        xaxis_title="% of submission meeting quality level",
        yaxis_title=None,
        bargap=0.6,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(autorange="reversed")),
        legend_title_text="Quality level"
    )

    fig_profile_2014 = px.bar(df_quality_2014, y="Profile", x=["4*", "3*", "2*", "1*", "U/C"], orientation="h",
    color_discrete_sequence=["lightslategray", "cornflowerblue", "darkturquoise", "lightblue", "white"],
    text_auto=True
    )

    fig_profile_2014.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} quality profile vs UOA average profile, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        ),
        xaxis_title="% of submission meeting quality level",
        yaxis_title=None,
        bargap=0.6,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(autorange="reversed")),
        legend_title_text="Quality level"
    )

    fig_median_2021 = px.bar(df_quartile_2021, x=["4*", "4* and 3*", "4*, 3* and 2*"], y="Level", barmode="group",
    color_discrete_sequence=["lightslategray", "cornflowerblue", "darkturquoise"],
    text_auto=True
    )

    fig_median_2021.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} quality profile vs UK sector UOA {uoa_number} median quality levels, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        ),
        xaxis_title="median % at quality level",
        yaxis_title=None,
        bargap=0.2,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(autorange="reversed")),
        legend_title_text="Quality level"
    )

    fig_median_2014 = px.bar(df_quartile_2014, x=["4*", "4* and 3*", "4*, 3* and 2*"], y="Level", barmode="group",
    color_discrete_sequence=["lightslategray", "cornflowerblue", "darkturquoise"],
    text_auto=True
    )

    fig_median_2014.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} quality profile vs UK sector UOA {uoa_number} median quality levels, REF 2014",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        ),
        xaxis_title="median % at quality level",
        yaxis_title=None,
        bargap=0.2,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
        yaxis=(dict(autorange="reversed")),
        legend_title_text="Quality level"
    )

    with l_col1:
        st.plotly_chart(fig_profile_2021, use_container_width=True)
        st.plotly_chart(fig_median_2021, use_container_width=True)

    with r_col1:
        st.plotly_chart(fig_profile_2014, use_container_width=True)
        st.plotly_chart(fig_median_2014, use_container_width=True)

    st.markdown("---")

    st.subheader(f"Market share, {HEI} vs UOA {uoa_number}:")

    l_col2, r_col2 = st.columns(2)


    fig_SizeShare_2021 = px.pie(df_size_2021, values="FTE", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_SizeShare_2021.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} FTE as a fraction of UOA {uoa_number} total FTE, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    fig_SizeShare_2014 = px.pie(df_size_2014, values="FTE", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_SizeShare_2014.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} FTE as a fraction of UOA {uoa_number} total FTE, REF 2014",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    fig_IncomeShare_2021 = px.pie(df_income_2021, values="Income (GBP)", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_IncomeShare_2021.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} income as a fraction of UOA {uoa_number} total income, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    fig_IncomeShare_2014 = px.pie(df_income_2014, values="Income (GBP)", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_IncomeShare_2014.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} income as a fraction of UOA {uoa_number} total income, REF 2014",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    fig_VolumeShare_2021 = px.pie(df_volume_2021, values="REF2021_weighted_volume", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_VolumeShare_2021.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} weighted volume as a fraction of UOA {uoa_number} total volume, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    fig_VolumeShare_2014 = px.pie(df_volume_2014, values="weighted_volume", names="Level", hole = 0.4,
    color_discrete_sequence=["lightblue", "cornflowerblue"])

    fig_VolumeShare_2014.update_layout(
        title=dict(
            text=f"{HEI} UOA {uoa_number} weighted volume as a fraction of UOA {uoa_number} total volume, REF 2014",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        )
    )

    with l_col2:
        st.plotly_chart(fig_SizeShare_2021, use_container_width=True)
        st.plotly_chart(fig_IncomeShare_2021, use_container_width=True)
        st.plotly_chart(fig_VolumeShare_2021, use_container_width=True)

    with r_col2:
        st.plotly_chart(fig_SizeShare_2014, use_container_width=True)
        st.plotly_chart(fig_IncomeShare_2014, use_container_width=True)
        st.plotly_chart(fig_VolumeShare_2014, use_container_width=True)

    st.write("Weighted volume = 4 x FourStarVolume(HEI) / 5 + ThreeStarVolume(HEI) / 5.       [Four/Three]StarVolume = [four/three] star fraction x FTE")

    st.markdown("---")

    st.subheader("Correlations:")

    fig_panel_corr_2021 = make_subplots(rows=1, cols=4,
    subplot_titles=("[FTE]", "[GPA]", "[Income]", "[PhDs]"))

    row, col = 1, 1
    for i in cols_2021[:-1]:
        fig_panel_corr_2021.add_trace(
        go.Scatter(x=scatter_df_2021_panel[i], y=scatter_df_2021_panel["REF2021_weighted_volume"]),
        row=row, col=col
        )
        col += 1

    fig_panel_corr_2021.update_layout(
        title=dict(
            text=f"Relationship of weighted volume to other variables, Main panel {main_panel_2021}, REF 2021",
            x=0.5,
            y=0.95,
            font=dict(
                family="Verdana",
                size=11,
                color='#000000'
            )
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
        )

    fig_panel_corr_2021.update_yaxes(title_text="Funding volume", row=1, col=1)

    st.write(f"Main Panel {main_panel_2021}:")
    st.plotly_chart(fig_panel_corr_2021, use_container_width=True)


except:
    st.error("No data for selected HEI. Try selecting different UOA or different HEI.", icon="🚨")

# --------- HIDE STREAMLIT STYLE ----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)
