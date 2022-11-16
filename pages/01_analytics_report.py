import datetime
from pprint import pprint

import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

from aggrid_utils import set_ggrid_options, get_table
from st_auth import authentication
from ga_get_data import get_analysis_report
from prepare_data import prepare_report_by, group_by, add_custom_category
import pandas as pd
import io
import json

st.set_page_config(page_title="report", layout="wide")
st._config.set_option("theme.base", "dark")


def generate_date_range_form():
    with st.form(key="date_range_form"):
        col1, col2, col3 = st.columns([2, 2, 1])
        today = datetime.date.today()
        last_month = today - datetime.timedelta(days=30)

        with col1:
            date_from_input = st.date_input(
                "Select from date",
                min_value=datetime.datetime(2020, 1, 1),
                max_value=today,
                value=last_month,
            )
            date_from_input = datetime.datetime.combine(
                date_from_input, datetime.time.min
            )

        with col2:
            date_to_input = st.date_input(
                "Select to date",
                min_value=datetime.datetime(2020, 1, 1),
                max_value=today,
                value=today,
            )
            date_to_input = datetime.datetime.combine(date_to_input, datetime.time.min)
        with col3:
            frequency = st.selectbox(
                "Frequency", ["Hourly", "Daily", "Weekly", "Monthly", "Yearly"], index=1
            )
            frequency = {
                "Hourly": "H",
                "Daily": "D",
                "Weekly": "W",
                "Monthly": "M",
                "Yearly": "Y",
            }[frequency]
            st.write(frequency)
        # add st.expander for advanced options
        with st.expander("Advanced options"):
            col1, col2 = st.columns([2, 1])

            with col1:
                metrics = st.multiselect(
                    "Metrics",
                    [
                        "uniqueEvents",
                        "eventValue",
                        "totalEvents",
                        "goalCompletionsAll",
                    ],
                    default=[
                        "uniqueEvents",
                        "eventValue",
                        "totalEvents",
                        "goalCompletionsAll",
                    ],
                    key="metrics",
                    help="choose metrics",
                )
                custom_group_columns = st.multiselect(
                    "Custom group columns",
                    [
                        "dateHourMinute",
                        "date",
                        "retail",
                        "language",
                        "deviceCategory",
                        "browser",
                        "operatingSystem",
                        "country",
                        "region",
                        "city",
                        "continent",
                        "subContinent",
                        "metro",
                        "networkDomain",
                        "customVarValue1",
                        "customVarValue2",
                        "customVarValue3",
                        "customVarValue4",
                        "customVarValue5",
                        "customVarValue6",
                        "customVarValue7",
                    ],
                    default=["customVarValue1"],
                    key="custom_group_columns",
                    help="choose custom group columns",
                )

            with col2:
                dimensions = st.multiselect(
                    "Dimensions",
                    [
                        "date",
                        "time",
                        "year",
                        "month",
                        "weekday",
                        "eventCategory",
                        "eventAction",
                        "eventLabel",
                    ],
                    default=["date", "time", "eventCategory", "eventAction"],
                    key="dimensions",
                    help="choose dimensions",
                )
            col3, col4, col5 = st.columns([1, 1, 1])
            with col3:
                filters = st.multiselect(
                    "Filters",
                    [
                        "retail",
                        "language",
                        "deviceCategory",
                        "browser",
                        "operatingSystem",
                        "country",
                        "region",
                        "city",
                        "continent",
                        "subContinent",
                        "metro",
                        "networkDomain",
                        "customVarValue1",
                        "customVarValue2",
                        "customVarValue3",
                        "customVarValue4",
                        "customVarValue5",
                        "customVarValue6",
                        "customVarValue7",
                    ],
                    default=["customVarValue1"],
                    key="filters",
                    help="choose filters",
                )
            with col4:
                filters_operator = st.selectbox(
                    "Filters operator",
                    ["AND", "OR"],
                    index=0,
                    key="filters_operator",
                    help="choose filters operator",
                )
            with col5:
                filters_match_type = st.selectbox(
                    "Filters match type",
                    ["EXACT", "BEGINS_WITH", "ENDS_WITH", "PARTIAL", "REGEXP"],
                    index=0,
                    key="filters_match_type",
                    help="choose filters match type",
                )
            col7, col8 = st.columns([1, 1])
            with col7:
                sort = st.multiselect(
                    "Sort",
                    [
                        "date",
                        "time",
                        "year",
                        "month",
                        "weekday",
                        "eventCategory",
                        "eventAction",
                        "eventLabel",
                    ],
                    default=["date", "time", "eventCategory", "eventAction"],
                    key="sort",
                    help="choose sort",
                )
            with col8:
                sort_order = st.selectbox(
                    "Sort order",
                    ["ASCENDING", "DESCENDING"],
                    index=0,
                    key="sort_order",
                    help="choose sort order",
                )
            col9, col10, col11, col12 = st.columns([1, 1, 1, 1])
            with col9:
                limit = st.number_input(
                    "Limit", min_value=1, max_value=10000, value=10000, step=1
                )
            with col10:
                offset = st.number_input(
                    "Offset", min_value=0, max_value=100000, value=0, step=1
                )
            with col11:
                sampling_level = st.selectbox(
                    "Sampling level",
                    ["DEFAULT", "SMALL", "LARGE"],
                    index=0,
                    key="sampling_level",
                    help="choose sampling level",
                )
            with col12:
                include_empty_rows = st.selectbox(
                    "Include empty rows",
                    ["true", "false"],
                    index=0,
                    key="include_empty_rows",
                    help="choose include empty rows",
                )
        # add st.expander for advanced options

        st.form_submit_button("Submit")
    return date_from_input, date_to_input, frequency


#


def generate_custom_group_form(data):
    """
    Generate custom group form based on data from Google Analytics
    return {
    "group_column_name": {
        "on_column_name": {
            "custom_group_name":[
            "unique_value_1", "unique_value_n"]
        }
            }
                }
    """
    default_groups = ["customVarValue1", "customVarValue2", "customVarValue3"]
    # callback for custom group form
    with st.expander("Custom grouper"):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            custom_group_preset_name = st.text_input(
                "Custom group preset name", value="custom_group_preset_1"
            )
            st.session_state["custom_group_on_col"] = st.selectbox(
                "Custom grop on column",
                data.columns,
                index=2,
                key="custom_grop_on_column",
                help="choose custom grop on column",
            )
            st.session_state["Custom groups name"] = st.text_area(
                "Custom groups name",
                value=default_groups,
                key="custom_groups_name",
                help="choose custom groups name",
                on_change=None,
            )
        with col2:
            custom_groups = {}
            # string to list

            custom_group_names = (
                st.session_state["custom_groups_name"]
                .strip("[]")
                .replace(" ", "")
                .split(",")
            )
            for g in custom_group_names:
                values = data[st.session_state["custom_group_on_col"]].unique()
                group = st.multiselect(
                    g,
                    values,
                    default=[],
                    key=g,
                    help="choose values for custom group",
                )

                if [x for x in values if x not in group]:
                    custom_groups[g] = [x for x in values if x not in group]
                custom_groups[g] = group



        with col3:
            st.session_state["groups_mappers"] = {
                custom_group_preset_name: {
                    "on_column": st.session_state["custom_group_on_col"],
                    "custom_groups": custom_groups,
                }
            }
            # get first key from dict

            # st.json(st.session_state["groups_mappers"])
        return st.session_state["groups_mappers"]


def group_by_form(*args):
    with st.form(key="group_by_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            group_order = st.multiselect(
                "Group",
                args,
                default=args,
                key="group_order",
                help="choose group order",
            )
        with col2:

            st.form_submit_button("Submit", key="group_by_form_submit")
    return group_order


def to_excel(df) -> bytes:
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


@authentication
def app():
    from settings import google_key

    st.session_state["key_file"] = google_key
    default_columns = [
        "dateHourMinute",
        "date",
        "time",
        "country",
        "retail",
        "language",
        "pageTitle",
        "uniqueEvents",
        "eventValue",
        "totalEvents",
        "goalCompletionsAll",
    ]

    agg_by = {
        "uniqueEvents": "sum",
        "eventValue": "sum",
        "totalEvents": "sum",
        "goalCompletionsAll": "sum",
    }

    st.markdown("# get analytics report")
    st.sidebar.markdown("# get analytics report")
    date_from_input, date_to_input, freq = generate_date_range_form()
    st.write(date_from_input, date_to_input)
    df = get_analysis_report(
        date_from_input, date_to_input, st.session_state["key_file"]
    )

    df = prepare_report_by(df, freq)
    # generate group by form
    group_form = generate_custom_group_form(df)
    # df[list(st.session_state['groups_mappers'].keys())[0]] = df.apply(
    #     lambda x: get_group(x, st.session_state['groups_mappers']), axis=1

    # df[list(group_form.keys())] = df[list(group_form.get("on_column"))]

    # st.dataframe(df[group_form.get(group_form.keys()[0]).get("on_column")])
    # get first key from dict
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


    df[custom_group_name] = df.apply(lambda x: get_group(x, custom_groups, on_column), axis=1)

    gb = set_ggrid_options(df)
    print(gb.__dict__)
    grid_options = gb.build()

    # Add aggrid table to display dataframe
    grid_response = get_table(df, grid_options)



    output_data = grid_response["data"]

    st.download_button(
        "Download as excel",
        data=to_excel(output_data),
        file_name="output{}-{}.xlsx".format(date_from_input, date_to_input),
        mime="application/vnd.ms-excel",
    )


    df = grid_response
    st.dataframe(df["data"])
    st.write(grid_options)




app()
