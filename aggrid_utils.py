import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode


def set_ggrid_options(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_side_bar()

    gb.configure_grid_options(
        enableRangeSelection=True,
        domLayout="autoHeight",
        autoSizeAllColumns=True,
        pagination=True,
        paginationPageSize=35,
        export_mode="serverSide",
        suppressExcelExport=True,
        suppressCsvExport=True,
        editable=True,
        allow_unsafe_jscode=True,
    )

    # Export grid_response on baton click

    # gb.configure_pagination(paginationPageSize=75)
    gb.configure_columns("autoSizeAllColumns={skipHeader?: False}")
    # filters and sorting options for aggrid table columns
    gb.configure_column(
        "dateHourMinute",
        enableValue=True,
        enableRowGroup=False,
        aggFunc="count",
        hide=True,
    )
    gb.configure_column(
        "language",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=1,
        hide=True,
    )
    gb.configure_column(
        "country",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=2,
        hide=True,
    )
    gb.configure_column(
        "retail",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=3,
        hide=True,
    )
    gb.configure_column(
        "pageTitle",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=4,
        hide=True,
    )
    gb.configure_column(
        "date",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=6,
        hide=True,
    )
    gb.configure_column(
        "time",
        enableValue=True,
        rowGroup=True,
        aggFunc="count",
        rowGroupIndex=8,
        hide=True,
    )
    gb.configure_column(
        "uniqueEvents", enableValue=True, enableRowGroup=False, aggFunc="sum"
    )
    gb.configure_column(
        "eventValue", enableValue=True, enableRowGroup=False, aggFunc="sum"
    )
    gb.configure_column(
        "totalEvents", enableValue=True, enableRowGroup=False, aggFunc="sum"
    )
    gb.configure_column(
        "goalCompletionsAll", enableValue=True, enableRowGroup=False, aggFunc="sum"
    )
    gb.configure_column(
        "year", enableValue=True, enableRowGroup=False, aggFunc="count", hide=True
    )
    gb.configure_column(
        "month",
        enableValue=True,
        rowGroup=True,
        rowGroupIndex=5,
        hide=True,
        aggFunc="count",
    )
    gb.configure_column(
        "weekday",
        enableValue=True,
        rowGroup=True,
        rowGroupIndex=7,
        hide=True,
        aggFunc="count",
    )
    gb.configure_default_column(
        editable=False, groupable=True, value=True, enableRowGroup=True, aggFunc="count"
    )
    for col in df.columns:
        if str(col).startswith("custom_"):
            gb.configure_column(
                col,
                enableValue=True,
                rowGroup=True,
                aggFunc="count",
                rowGroupIndex=0,
                hide=True,
            )
    return gb


def get_table(df, grid_options):
    selected_theme = "streamlit"
    agrid_table = AgGrid(
        df,
        theme=selected_theme,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        export_mode="serverSide",
        enable_enterprise_modules=True,
        suppressExcelExport=True,
    )
    return agrid_table
