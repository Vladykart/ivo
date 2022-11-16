import datetime
from pprint import pprint

import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

from aggrid_utils import get_table, set_ggrid_options
from apps.ui_elements.forms import (
    generate_google_analytics_query_form,
    generate_whitelist_form,
    generate_group_by_form,
    generate_add_custom_category_form,
    generate_save_to_form,
    generate_custom_group_form,
    group_by_form
)
from prepare_data import prepare_report_by, group_by, add_custom_category, parse_retails_from_event_label, \
    prepare_column_names, parse_language

from st_auth import authentication
from apps.data.ga_get_data import compare_request, get_report, get_df_from_response
from settings import VIEW_ID, AGRID_OPTIONSS
from settings import GOOGLE_KEY

st.set_page_config(page_title="report", layout="wide")
st._config.set_option("theme.base", "dark")


@authentication
def app():

    st.session_state["key_file"] = GOOGLE_KEY

    if "agrid_selected_theme" not in st.session_state:
        st.session_state.agrid_selected_theme = "dark"

    if "agrid_options" not in st.session_state:
        st.session_state.agrid_options = AGRID_OPTIONSS

    agrid_available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material"]
    agrid_selected_theme = st.sidebar.selectbox(
        "Theme", agrid_available_themes, index=2
    )
    st.session_state.agrid_selected_theme = agrid_selected_theme
    st.sidebar.markdown("# Google Analytics report")
    google_analytics_query_form = generate_google_analytics_query_form()  # type: dict
    if "report" not in st.session_state:
        st.session_state.report = {}

    query = compare_request(
        VIEW_ID[0],
        google_analytics_query_form.get("date_from_input"),
        google_analytics_query_form.get("date_to_input"),
        google_analytics_query_form.get("frequency"),
        google_analytics_query_form.get("request"),
    )

    report = get_report(query, st.session_state.key_file)
    # st.json(report)
    df = get_df_from_response(report)
    columns = df.columns
    group_form = generate_custom_group_form(df)

    unique_names = df["ga:eventLabel"].unique()
    colq_1, colq_2 = st.columns([21, 10])

    with colq_2:
        st.markdown("Modifications")

        whitelist_name = generate_whitelist_form(df)
        generate_group_by_form(df)
        generate_add_custom_category_form(df)
        generate_save_to_form(df)

    with colq_1:

        # tab1, tab2, tab3 = st.tabs(["Table", "Chart", "Settings"])
        # with tab1:
        st.markdown("Report")
        df = df[df["ga:eventLabel"].isin(st.session_state.multiselect_names)]
        df = prepare_column_names(df)
        df = parse_retails_from_event_label(df)
        df = parse_language(df)

        custom_group_name = list(group_form.keys())[0]
        # get on column from group form
        on_column = group_form.get(custom_group_name).get("on_column")
        # get custom groups from group form
        custom_groups = group_form.get(custom_group_name).get("custom_groups")

        def get_group(x, custom_groups, on_column):
            for custom_group in custom_groups:
                if x[on_column] in custom_groups.get(custom_group):
                    return custom_group
            return "other"

        # df[custom_group_name] = df.apply(lambda x: get_group(x, custom_groups, on_column), axis=1)



        # df to aggrid options
        gb = GridOptionsBuilder.from_dataframe(df)

        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc="sum", wide="true"
        )
        gridOption = set_ggrid_options(df)
        gridOptions = gb.build()
        grid_response = get_table(df, gridOptions)


app()
