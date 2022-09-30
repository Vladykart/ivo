import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode


def set_ggrid_options(df):
    gb = GridOptionsBuilder.from_dataframe(df)

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
    gb.configure_column("dateHourMinute", enableValue=True, enableRowGroup=False, aggFunc='sum', hide=True)
    gb.configure_column("date", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("time", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("country", enableValue=True, enableRowGroup=True, aggFunc='sum')
    # gb.configure_column("language", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("retail", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("pageTitle", enableValue=True, enableRowGroup=True, aggFunc='sum')
    gb.configure_column("uniqueEvents", enableValue=True, enableRowGroup=False, aggFunc='sum')
    gb.configure_column("eventValue", enableValue=True, enableRowGroup=False, aggFunc='sum')
    gb.configure_column("totalEvents", enableValue=True, enableRowGroup=False, aggFunc='sum')
    gb.configure_column("goalCompletionsAll", enableValue=True, enableRowGroup=False, aggFunc='sum')
    js_code = """
    function(params) {
        if (params.value === undefined) {
                                        
                                        
      """
    gb.configure_default_column(editable=False, groupable=True, value=True, enableRowGroup=True,
                                aggFunc='sum',
                                )


    return gb


def get_table(df, grid_options):
    selected_theme = 'streamlit'
    agrid_table = AgGrid(
        df,
        theme=selected_theme,
        gridOptions=grid_options,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        export_mode='serverSide',
        enable_enterprise_modules=True,
        suppressExcelExport=True,


    )
    return agrid_table
