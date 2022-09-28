import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode


def set_ggrid_options(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=False, groupable=True, value=True, enableRowGroup=True,
                                aggFunc='sum')
    gb.configure_side_bar()

    gb.configure_grid_options(enableRangeSelection=True, domLayout='autoHeight', autoSizeAllColumns=True,
                              pagination=True, paginationPageSize=35, export_mode='serverSide',
                              suppressExcelExport=True, suppressCsvExport=True,
                              editable=True,
                              allow_unsafe_jscode=True, )

    # Export grid_response on baton click

    # gb.configure_pagination(paginationPageSize=75)
    gb.configure_columns("autoSizeAllColumns={skipHeader?: False}")
    # filters and sorting options for aggrid table columns
    gb.configure_column("dateHourMinute", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("date", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("time", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("country", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("language", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("retail", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("pageTitle", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("uniqueEvents", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("eventValue", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("totalEvents", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("goalCompletionsAll", enableValue=True, enableRowGroup=True, aggFunc='sum')
    # hide columns from aggrid table
    gb.configure_column("dateHourMinute", hide=True)
    # add pagination to aggrid table by 75 rows

    # add sorting to aggrid table
    # priont aggrid options
    # print(gb.build())
    return gb


def get_table(df, grid_options):
    selected_theme = 'streamlit'
    agrid_table = AgGrid(
        df,
        theme=selected_theme,
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        export_mode='serverSide',
        suppressExcelExport=True,

    )
    return agrid_table
