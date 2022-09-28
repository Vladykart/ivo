from datetime import datetime
from settings import GOOGLE_ANALYTICS_CREDENTIALS as GA_CREDENTIALS
from settings import LOCAL_DATA_PATH
import gapy.client


# %%


KEY_FILE_LOCATION = GA_CREDENTIALS["key_file_location"].as_posix()
VIEW_ID = GA_CREDENTIALS["view_id"]
# %%
# For a service account
client = gapy.client.from_private_key(
    "your account name",
    private_key=KEY_FILE_LOCATION,
    storage_path=LOCAL_DATA_PATH)
# %%
# For a web or installed application
# client = gapy.client.from_secrets_file(KEY_FILE_LOCATION, storage_path=LOCAL_DATA_PATH)
# %%
dimensions = ['dateHourMinute',
              'pagePath',
              'pageTitle',
              'eventCategory',
              'eventAction',
              'eventLabel']

metrics = ['totalEvents',
           'uniqueEvents',
           'eventValue']

filters = "eventCategory==Marketplace"

reach_data = client.query.get(ids=['179865976'],
                              start_date=datetime(2012, 1, 1),
                              end_date=datetime(2012, 1, 1),
                              metrics=metrics,
                              dimensions=dimensions,
                              filters=filters,
                              max_results=10000
                              )

print(KEY_FILE_LOCATION)
