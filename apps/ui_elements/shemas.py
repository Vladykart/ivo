import json
import requests
from pprint import pprint

url = "https://www.googleapis.com/analytics/v3/metadata/ga/columns"

response = requests.get(url)
data = response.json()
items = data["items"]
metrics = []
dimensions = []

for item in items:
    if item["attributes"]["type"] == "METRIC":
        metrics.append(str(item["id"]))
    elif item["attributes"]["type"] == "DIMENSION":
        dimensions.append(str(item["id"]))

default_schemas = {
    "name": "default_1",
    "metrics": [
        "ga:totalEvents",
        "ga:uniqueEvents",
        "ga:eventValue",
        "ga:goalCompletionsAll",
    ],
    "dimensions": [
        "ga:dateHourMinute",
        "ga:pagePath",
        "ga:pageTitle",
        "ga:eventCategory",
        "ga:eventAction",
        "ga:eventLabel",
        "ga:country",
    ],
    "sort": [],
    "filters": "ga:eventCategory==Marketplace",
    "pageSize": 10000,
}


sort_schemas = [
    "+ga:dateHourMinute",
    "-ga:dateHourMinute",
    "+ga:totalEvents",
    "-ga:totalEvents",
    "+ga:uniqueEvents",
    "-ga:uniqueEvents",
    "+ga:eventValue",
    "-ga:eventValue",
    "+ga:dimension1",
    "-ga:dimension1",
    "+ga:minute",
    "-ga:minute",
    "+ga:date",
    "-ga:date",
    "+ga:hour",
    "-ga:hour",
    "+ga:minute",
    "-ga:minute",
    "+ga:eventAction",
    "-ga:eventAction",
    "+ga:eventLabel",
    "-ga:eventLabel",
]
