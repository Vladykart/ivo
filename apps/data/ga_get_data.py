"""Hello Analytics Reporting API V4."""
from streamlit import cache
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from settings import GOOGLE_KEY, VIEW_ID

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


# %%

@cache
def get_df_from_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    df = pd.DataFrame()
    for report in response.get("reports", []):
        columnHeader = report.get("columnHeader", {})
        dimensionHeaders = columnHeader.get("dimensions", [])
        metricHeaders = columnHeader.get("metricHeader", {}).get(
            "metricHeaderEntries", []
        )
        rows = report.get("data", {}).get("rows", [])

        for row in rows:
            dimensions = row.get("dimensions", [])
            metrics = row.get("metrics", [])
            values = []
            for metric in metrics:
                values = values + metric.get("values", [])
            df = df.append(pd.Series(dimensions + values), ignore_index=True)
        df.columns = dimensionHeaders + [metricHeader.get("name") for metricHeader in metricHeaders]
    return df


def compare_request(VIEW_ID, date_from, date_to, frequency, request):
    # Use the Analytics Service Object to query the Analytics Reporting API V3.
    # prepare date_from and date_to to string for request
    date_from = date_from.strftime("%Y-%m-%d")
    date_to = date_to.strftime("%Y-%m-%d")
    request = {
        "reportRequests": [
            {
                "viewId": VIEW_ID,  # Add View ID from GA
                "pageSize": request["pageSize"],
                "dateRanges": [{"startDate": date_from, "endDate": date_to}],
                "metrics": request["metrics"],
                "dimensions": request["dimensions"],
                "filtersExpression": request["filtersExpression"],
            }
        ]
    }
    return request


def initialize_analyticsreporting(KEY_FILE):
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(KEY_FILE, SCOPES)

    # Build the service object.
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


def get_report(request, KEY_FILE=GOOGLE_KEY):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
      request: The request to get report.
    Returns:
      The Analytics Reporting API V4 response.
    """
    analytics = initialize_analyticsreporting(KEY_FILE)
    return analytics.reports().batchGet(body=request).execute()







