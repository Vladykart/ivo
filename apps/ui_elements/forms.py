import io

import pandas as pd
import streamlit as st
import datetime
from apps.ui_elements import shemas


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


def generate_profile_buttons(profiles):
    """
    Generates a list of buttons for each profile in the list
    :param profiles: list of profiles
    :type profiles: list
    :return: the selected profile
    :rtype: str
    """
    profile_buttons = []
    for profile in profiles:
        profile_buttons.append(st.button(profile))
    return profile_buttons


def generate_profiles_form(profiles):
    """
    Generates a form for the user to select the profile byn clicking on the profile button in the list
    Every button in list per st.columns(3) is a profile
    :param
    :type
    :return: the selected profile
    :rtype: str
    """

    profile_buttons = generate_profile_buttons(profiles)
    with st.form(key="profiles_form"):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if profile_buttons[0]:
                selected_profile = profiles[0]
        with col2:
            if profile_buttons[1]:
                selected_profile = profiles[1]
        with col3:
            if profile_buttons[2]:
                selected_profile = profiles[2]
        st.form_submit_button("Select profile")
    return selected_profile


def generate_google_analytics_query_form():
    """
    Generates a form for the user to select the date range
    and the metrics to be used in the query
    :return: a dictionary with the selected values
    :rtype: dict
    """

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

        # add profile button
        # add st.expander for Set query parameters
        with st.expander("Set query parameters", expanded=True):
            col1, col2 = st.columns([2, 1])

            with col1:
                default_dimensions = [
                    default_dimension
                    for default_dimension in shemas.default_schemas["dimensions"]
                ]

                default_metrics = [
                    default_metrics
                    for default_metrics in shemas.default_schemas["metrics"]
                ]
                dimensions = st.multiselect(
                    "Dimensions",
                    shemas.dimensions,
                    default=[s for s in shemas.dimensions if s in default_dimensions],
                    key="dimensions",
                    help="choose dimensions",
                )

                metrics = st.multiselect(
                    "Metrics",
                    shemas.metrics,
                    default=[s for s in shemas.metrics if s in default_metrics],
                    key="metrics",
                    help="choose metrics",
                )

            with col2:

                sort_form = st.multiselect(
                    "Sort",
                    shemas.sort_schemas,
                    default=None,
                    key="sort",
                    help="dimensions and metrics to sort query by",
                )

                sort_order = st.selectbox(
                    "Sort order",
                    ["ASCENDING", "DESCENDING"],
                    index=0,
                    key="sort_order",
                    help="choose sort order",
                )

            col3, col4, col5, col6 = st.columns([1, 1, 1, 1])
            with col3:
                filters = st.text_input(
                    "Filters",
                    shemas.default_schemas["filters"],
                    key="filters",
                    help="The filters to apply to the query.",
                )
            with col4:
                page_size = st.number_input(
                    "pageSize", min_value=1, max_value=10000, value=10000, step=1
                )
            with col5:
                offset = st.number_input(
                    "Offset", min_value=0, max_value=100000, value=0, step=1
                )
            with col6:
                sampling_level = st.selectbox(
                    "Sampling level",
                    ["DEFAULT", "SMALL", "LARGE"],
                    index=0,
                    key="sampling_level",
                    help="choose sampling level",
                )

            include_empty_rows = st.checkbox(
                "Include empty rows",
                key="include_empty_rows",
                help="Select to include empty rows",
            )

        # add st.expander for advanced options

        request = {
            "metrics": [{"expression": m} for m in metrics],
            "dimensions": [{"name": d} for d in dimensions],
            "filtersExpression": filters,
            "orderBys": sort_form,
            "pageSize": page_size,
            "offset": offset,
            "samplingLevel": sampling_level,
            "includeEmptyRows": include_empty_rows,
        }
        # st.json(request)
        st.form_submit_button("Run query")
    return {
        "date_from_input": date_from_input,
        "date_to_input": date_to_input,
        "frequency": frequency,
        "request": request,
    }


def to_excel(df) -> bytes:
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def generate_save_to_form(df):
    with st.expander("Export to:"):
        # export choose to session_state (excel, csv, json)
        export_choose = st.radio("File format", ["excel", "csv", "json"])

        st.session_state.export_choose = export_choose
        if export_choose == "excel":
            file_name = st.text_input("File name", "report.xlsx")
            st.session_state.file_name = file_name

            st.download_button(
                label="Download excel",
                data=to_excel(df),
                file_name="report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        elif export_choose == "csv":
            file_name = st.text_input("File name", "report.csv")
            st.session_state.file_name = file_name
            st.download_button(
                label="Download csv",
                data=df.to_csv(),
                file_name="report.csv",
                mime="text/csv",
            )

        elif export_choose == "json":
            file_name = st.text_input("File name", "report.json")
            st.session_state.file_name = file_name
            st.download_button(
                label="Download json",
                data=df.to_json(),
                file_name="report.json",
                mime="application/json",
            )


def generate_whitelist_form(df):
    unique_names = df["ga:eventLabel"].unique()
    with st.expander("Unique names"):
        multiselect_names = st.multiselect(
            "Select names", unique_names, default=unique_names
        )
        # multiselect_names to session_state
        st.session_state.multiselect_names = multiselect_names


def generate_group_by_form(df):
    with st.expander("Group by:"):
        group_by = st.radio("Group by", ["ga:eventLabel", "ga:eventAction"])
        st.session_state.group_by = group_by


def generate_add_custom_category_form(df):
    with st.expander("Add custom category:"):
        st.write("Add custom category to ga:eventLabel column")
        custom_category = st.text_input("Custom category", "custom_category")
        st.session_state.custom_category = custom_category
