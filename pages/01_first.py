import datetime
from pprint import pprint

import streamlit as st

from aggrid_utils import set_ggrid_options, get_table
from st_auth import authentication
from ga_get_data import get_analysis_report
from prepare_data import prepare_report_by, group_by
from settings import google_key
import pandas as pd
import io
import json

st.set_page_config(page_title="report", layout="wide")
st._config.set_option('theme.base', 'dark')


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
            frequency = st.selectbox("Frequency", ["Hourly", "Daily", "Weekly", "Monthly", "Yearly"], index=1)
            frequency = {"Hourly": "H", "Daily": "D", "Weekly": "W", "Monthly": "M", "Yearly": "Y"}[frequency]
            st.write(frequency)
        st.form_submit_button("Submit")
    return date_from_input, date_to_input, frequency


def group_by_form(*args):
    with st.form(key="group_by_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            group_order = st.multiselect("Group", args, default=args, key="group_order", help="choose group order")
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
    st.session_state['key_file'] = google_key
    default_columns = ['dateHourMinute',
                       'date', 'time',
                       'country', 'retail',
                       'language', 'pageTitle',
                       'uniqueEvents', 'eventValue',
                       'totalEvents', 'goalCompletionsAll']

    agg_by = {'uniqueEvents': 'sum',
              'eventValue': 'sum',
              'totalEvents': 'sum',
              'goalCompletionsAll': 'sum'}

    st.markdown("# get analytics report")
    st.sidebar.markdown("# get analytics report")
    date_from_input, date_to_input, freq = generate_date_range_form()
    st.write(date_from_input, date_to_input)
    df = get_analysis_report(date_from_input, date_to_input, google_key)

    df = prepare_report_by(df, freq)
    # df = group_by(df, group_by_form(df.columns), agg_by)
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


app()

