import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(
    page_title="REF Results Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# title #
title = "REF 2021 results and submissions data"
st.title(":bar_chart:" + title)

# filter icon #
css_icon = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<i class="fa fa-filter"></i>
'''

# --------- FUNCTIONS ---------- #
def show_grid():
    styler = df_selection.style.hide_index().format(subset=[
        "GPA","FTE", "4*", "3*", "2*", "1*", "U/C", "Doctoral awards"],
        decimal='.',
        precision=0)
    st.dataframe(styler)

def unshow_grid():
    return


# --------- READ EXCEL --------- #
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


df = get_data_from_excel()
df2014 = get_2014_data_from_excel()

# -- there is an issue about rounding decimal places. You can do it in pandas but streamlit won't display it with its .dataframe or .write methods for some reason. It works with AgGrid#

df_display = df[[
    "Institution name",
    "Main panel",
    "UOA number",
    "UOA name",
    "Profile",
    "FTE",
    "4*", "3*", "2*", "1*", "U/C", "GPA",
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
    "Income (GBP)", "Doctoral awards"
]]

# df_2014.rename(columns={"REF2014_total_ResearchIncome_forHEIforUOA_5years": "REF2014 income (GBP)", "REF2014_DoctoralAwards_5years": "REF2014 doctoral awards"}, inplace=True)

#---- SIDEBAR ----#
st.sidebar.markdown(css_icon + " Filter the data", unsafe_allow_html=True)

main_panel = st.sidebar.selectbox(
    "Select Main Panel:",
    options=sorted(df_display["Main panel"].unique()),
    index=1
)

uoa_slice = df.loc[(df["Main panel"]==main_panel),["UOA name"]]
uoa_options = uoa_slice["UOA name"].unique()

profile = st.sidebar.multiselect(
    "Select Profile:",
    options=df_display["Profile"].unique(),
    default= "Overall"
)

UOA = st.sidebar.selectbox(
    "Select Unit of Assessment:",
    options=sorted(uoa_options),
    index=1
)

HEI = st.sidebar.multiselect(
    "Select HEI:",
    options=sorted(df["Institution name"].unique()),
    default=[
            "University of Oxford",
            "Imperial College London",
            "University of Cambridge"
            ]
)

df_selection = df_display.query(
    "`Main panel` == @main_panel & Profile ==@profile & `UOA name` == @UOA & `Institution name` == @HEI"
)

df_selection_2014 = df_2014.query(
    "`Main panel` == @main_panel & Profile ==@profile & `UOA name` == @UOA & `Institution name` == @HEI"
)

show_table = st.sidebar.button("Show table", help="Show selected results in table", on_click=show_grid)
hide_table = st.sidebar.button("Hide table", help="Hide the table", on_click=unshow_grid)


# ------- MAINPAGE ------ #
st.markdown("##") # new paragraph
st.markdown("---")
st.write("Averages over filtered selection:")
# -- Metrics

# df_selection["Income (GBP)"] = df_selection["Income (GBP)"].map(lambda x: float(x) * 1000)
try:
    average_FourStar = int(df_selection["4*"].mean())
    average_size = round(df_selection["FTE"].mean(), 2)
    average_income = int(df_selection["Income (GBP)"].mean())
    average_phds = round(df_selection["Doctoral awards"].mean(), 2)

    left_col, middle_col1, middle_col2, right_col = st.columns(4)
    with left_col:
        st.subheader("Average 4* fraction:")
        st.subheader(f"{average_FourStar}%")
    with middle_col1:
        st.subheader("Average FTE:")
        st.subheader(f"{average_size} FTE")
    with middle_col2:
        st.subheader("Average research income:")
        st.subheader(f"£{average_income:,}")
    with right_col:
        st.subheader("Average doctoral awards:")
        st.subheader(f"{average_phds}")


    st.markdown("---")

    # ---- CHARTS ----

    l_col1, r_col1 = st.columns(2)

    four_star2021_slice = df_selection[["Institution name", "4*", "Profile"]].sort_values(by="4*")
    four_star2014_slice = df_selection_2014[["Institution name", "4*","Profile"]].sort_values(by="4*")

    fig2021 = px.bar(four_star2021_slice, x="Institution name", color="Profile",
                 y="4*",
                 title="4* fraction by institution, REF2021 (sub-profile view)",
                 barmode='group',
                 facet_col="Profile",
                 color_discrete_sequence=["lightslategray", "cornflowerblue", "lightblue", "gainsboro"]
                 )

    fig2021.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_range=[0,100]
        )

    fig2021.update_xaxes(minor_showgrid=False)


    fig2014 = px.bar(four_star2014_slice, x="Institution name", color="Profile",
                 y="4*",
                 title="4* fraction by institution, REF2014 (sub-profile view)",
                 barmode='group',
                 facet_col="Profile",
                 color_discrete_sequence=["lightslategray", "cornflowerblue", "lightblue", "gainsboro"]
                 )

    fig2014.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_range=[0,100]
    )

    fig2014.update_xaxes(minor_showgrid=False)

    fig_2021fourstar = px.bar(
        four_star2021_slice,
        x="4*",
        y="Institution name",
        color="Profile",
        orientation="h",
        title="4* fraction by institution, REF2021 (grouped view)",
        color_discrete_sequence=["lightslategray", "cornflowerblue", "lightblue", "gainsboro"]
    )

    fig_2021fourstar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    fig_2014fourstar = px.bar(
        four_star2014_slice,
        x="4*",
        y="Institution name",
        color="Profile",
        orientation="h",
        title="4* fraction by institution, REF2014 (grouped view)",
        color_discrete_sequence=["lightslategray", "cornflowerblue", "lightblue", "gainsboro"]
    )

    fig_2014fourstar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    with l_col1:
        st.plotly_chart(fig_2021fourstar, use_container_width=True)
        st.plotly_chart(fig2021, use_container_width=True)

    with r_col1:
        st.plotly_chart(fig_2014fourstar, use_container_width=True)
        st.plotly_chart(fig2014, use_container_width=True)

    st.markdown("---")

    l_col2, r_col2 = st.columns(2)

    income2021_slice = df_selection.loc[(df_selection["Profile"]=="Overall"),["Institution name", "Income (GBP)"]].sort_values(by="Income (GBP)")
    fig_2021income = px.bar(
        income2021_slice,
        x="Income (GBP)",
        y="Institution name",
        orientation="h",
        title="Income by institution, REF2021",
        color_discrete_sequence=["cornflowerblue"] * len(income2021_slice),
    )

    fig_2021income.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    with l_col2:
        st.plotly_chart(fig_2021income, use_container_width=True)

    income2014_slice = df_selection_2014.loc[(df_selection_2014["Profile"]=="Overall"),["Institution name", "Income (GBP)"]].sort_values(by="Income (GBP)")
    fig_2014income = px.bar(
        income2014_slice,
        x="Income (GBP)",
        y="Institution name",
        orientation="h",
        title="Income by institution, REF2014",
        color_discrete_sequence=["lightblue"] * len(income2021_slice),
    )

    fig_2014income.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    with r_col2:
        st.plotly_chart(fig_2014income, use_container_width=True)

    st.markdown("---")

    l_col3, r_col3 = st.columns(2)

    phd2021_slice = df_selection.loc[(df_selection["Profile"]=="Overall"),["Institution name", "Doctoral awards"]].sort_values(by="Doctoral awards")
    fig_2021phd = px.bar(
        phd2021_slice,
        x="Doctoral awards",
        y="Institution name",
        orientation="h",
        title="Doctoral awards by institution, REF2021",
        color_discrete_sequence=["cornflowerblue"] * len(phd2021_slice),
    )

    fig_2021phd.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    with l_col2:
        st.plotly_chart(fig_2021phd, use_container_width=True)

    phd2014_slice = df_selection_2014.loc[(df_selection_2014["Profile"]=="Overall"),["Institution name", "Doctoral awards"]].sort_values(by="Doctoral awards")
    fig_2014phd = px.bar(
        phd2014_slice,
        x="Doctoral awards",
        y="Institution name",
        orientation="h",
        title="Doctoral awards by institution, REF2014",
        color_discrete_sequence=["lightblue"] * len(phd2014_slice),
    )

    fig_2014phd.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    with r_col2:
        st.plotly_chart(fig_2014phd, use_container_width=True)

except ValueError:
    st.error("No UOA data for selected institution(s). Try selecting different UOA or different institutions.", icon="🚨")

# --------- HIDE STREAMLIT STYLE ----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)
