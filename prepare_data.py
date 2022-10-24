import pandas as pd
from streamlit import cache
from settings import LOCAL_DATA_PATH
import pathlib


# # Read the data
# data = pd.read_csv(LOCAL_DATA_PATH.joinpath(r'C:\Users\user\PycharmProjects\ivo\ga_data.csv'))


# %%
CUSTOM_CATEGORY_JSON = {
    "first":['selleriedesnacres.fr', 'equiness.fr'],
    "second":['agradi.de', 'lepaturon.com'],
}
# %%



def split_date_and_time(data):
    data["date"] = data["dateHourMinute"].dt.date
    data["time"] = data["dateHourMinute"].dt.time
    data["weekday"] = data["dateHourMinute"].dt.weekday
    data["month"] = data["dateHourMinute"].dt.month
    data["year"] = data["dateHourMinute"].dt.year

    return data


def parse_language(data):
    data["language"] = data["pagePath"].str.split("/").str[1]
    return data


def parse_retails_from_event_label(data):
    data["eventLabel"] = data["eventLabel"].str.replace("https://", "")
    data["retail"] = data["eventLabel"].str.split("/").str[0]
    # replace www. if exists
    data["retail"] = data["retail"].str.replace("www.", "")
    return data


def drop_columns(data):
    return data.drop(columns=["eventCategory", "eventAction"], axis=1)


def rename_columns(data):
    return data.rename(
        columns={
            "dateHourMinute": "Date and time",
            "pageTitle": "Page title",
            "uniqueEvents": "Unique events",
            "eventValue": "Event value",
            "totalEvents": "Total events",
            "goalCompletionsAll": "Goal completions all",
            "eventLabel": "Event label",
        }
    )


def prepare_report_dtypes(data):
    data["dateHourMinute"] = pd.to_datetime(data["dateHourMinute"])
    data["uniqueEvents"] = data["uniqueEvents"].astype(int)
    data["eventValue"] = data["eventValue"].astype(int)
    data["totalEvents"] = data["totalEvents"].astype(int)
    data["goalCompletionsAll"] = data["goalCompletionsAll"].astype(int)
    return data


@cache
def select_columns(data, *args):
    return data[args]


def group_by(data, *args, **kwargs):
    """Group data by [args] and {kwargs}
    Example form: group_by(data, ['date', 'retail', 'language'], agg_by=agg_by
    group_by = ['date', 'retail', 'language']
    agg_by = {'uniqueEvents': 'sum',
              'eventValue': 'sum'
              'totalEvents': 'sum',
                'goalCompletionsAll': 'sum'}
    """
    if args and kwargs:
        data = data.groupby(args).agg(kwargs)
        data = data.reset_index()
        data = rename_columns(data)
        return data
    else:
        raise Exception("No arguments passed")


def set_time_frequency(data, freq="H"):
    """Set time frequency for date and time and ceep all other columns
    freq = 'H' - hourly
    freq = 'D' - daily
    freq = 'M' - monthly
    """
    return data
    data = data.set_index(["dateHourMinute"])
    data = data.resample(freq).sum()
    data = data.reset_index()
    return data


def add_custom_category(data, new_category_column_name, column, **kwargs):
    """Add custom category column to dataframe if it exists in kwargs
    Example form: add_custom_category(data, 'custom_category_name', 'column_in_dataframe', {'category':['value1', 'value2']})
    """
    if kwargs:
        for key, value in kwargs.items():
            data[new_category_column_name] = data[column].apply(
                lambda x: key if x in value else "Other"
            )
    else:
        raise Exception("No arguments passed")
    return data



def prepare_report_by(data, freq):
    """Prepare report by [args] and {kwargs}
    Example form: prepare_report_by(data, ['date', 'retail', 'language'], agg_by=agg_by
    group_by = ['date', 'retail', 'language']
    agg_by = {'uniqueEvents': 'sum',
              'eventValue': 'sum'
              'totalEvents': 'sum',
                'goalCompletionsAll': 'sum'}
    """
    data = drop_columns(data)
    data = parse_language(data)
    data = prepare_report_dtypes(data)
    data = parse_retails_from_event_label(data)
    data = set_time_frequency(data, freq=freq)
    data = prepare_report_dtypes(data)
    data = split_date_and_time(data)
    # data = rename_columns(data)
    return data


# %%



# %%
