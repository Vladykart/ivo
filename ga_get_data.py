"""Hello Analytics Reporting API V4."""
from streamlit import cache
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from settings import GOOGLE_ANALYTICS_CREDENTIALS as GA_CREDENTIALS

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = GA_CREDENTIALS["credentials"]
VIEW_ID = GA_CREDENTIALS["view_id"]

# %%


def compare_request(date_from, date_to):
    # Use the Analytics Service Object to query the Analytics Reporting API V3.
    # prepare date_from and date_to to string for request
    date_from = date_from.strftime('%Y-%m-%d')
    date_to = date_to.strftime('%Y-%m-%d')
    request = {
        'reportRequests': [
            {
                'viewId': VIEW_ID,  # Add View ID from GA
                "pageSize": 10000,
                'dateRanges': [{'startDate': date_from, 'endDate': date_to}],
                'metrics': [{'expression': 'ga:totalEvents'},
                            {'expression': 'ga:uniqueEvents'},
                            {'expression': 'ga:eventValue'},
                            {'expression': 'ga:goalCompletionsAll'}],
                'dimensions': [
                    {'name': 'ga:dateHourMinute'},
                    {"name": 'ga:pagePath'},
                    {"name": 'ga:pageTitle'},
                    {'name': 'ga:eventCategory'},
                    {"name": 'ga:eventAction'},
                    {"name": 'ga:eventLabel'},
                    {"name": 'ga:country'},
                    ],
                "filtersExpression": "ga:eventCategory==Marketplace",

            }]
    }
    return request


# %%
def get_report(analytics, request):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
      request: The request to get report.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body=request).execute()


# %%
def initialize_analyticsreporting(KEY_FILE):
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE, SCOPES
    )

    # Build the service object.
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


# %%
def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    for report in response.get("reports", []):
        columnHeader = report.get("columnHeader", {})
        dimensionHeaders = columnHeader.get("dimensions", [])
        metricHeaders = columnHeader.get("metricHeader", {}).get(
            "metricHeaderEntries", []
        )
        rows = report.get("data", {}).get("rows", [])

        for row in rows:
            dimensions = row.get("dimensions", [])
            dateRangeValues = row.get("metrics", [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ": " + dimension)

            for i, values in enumerate(dateRangeValues):
                print("Date range: " + str(i))
                for metricHeader, value in zip(metricHeaders, values.get("values")):
                    print(metricHeader.get("name") + ": " + value)


# %%
def compare_reports(reports):

    rows = reports[0].get('data', {}).get('rows', [])
    l = []
    i = len(reports)
    for row in rows:
        d = {
            'dateHourMinute': row.get('dimensions')[0],
            'pagePath': row.get('dimensions')[1],
            'pageTitle': row.get('dimensions')[2],
            'uniqueEvents': row.get('metrics')[0].get('values')[0],
            'eventValue': row.get('metrics')[0].get('values')[1],
            'totalEvents': row.get('metrics')[0].get('values')[2],
            'goalCompletionsAll': row.get('metrics')[0].get('values')[3],
            'eventCategory': row.get('dimensions')[3],
            'eventAction': row.get('dimensions')[4],
            'eventLabel': row.get('dimensions')[5],
            'country': row.get('dimensions')[6],

        }
        l.append(d)
        i -= 1
    return l
# %%


@cache
def get_analysis_report(date_from, date_to, KEY_FILE):
    request = compare_request(date_from, date_to)
    analytics = initialize_analyticsreporting(KEY_FILE)
    response = get_report(analytics, request)
    data = compare_reports(response.get('reports', []))
    df = pd.DataFrame(data)
    return df


# %%




# %%

