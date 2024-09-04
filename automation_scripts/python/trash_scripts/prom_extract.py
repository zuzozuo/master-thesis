import requests
import pandas as pd
from datetime import datetime, timedelta

# Configuration
PROMETHEUS_URL = "http://10.20.20.60:9090/api/v1/query_range"
METRIC_NAME = "your_metric_name"
START_TIME = "2024-08-24T12:00:00Z"  # Start time in ISO 8601 format
END_TIME = "2024-08-25T12:00:00Z"    # End time in ISO 8601 format
STEP = "60s"  # Query step duration (e.g., 60s for one data point per minute)

# Define the query parameters
params = {
    "query": METRIC_NAME,
    "start": START_TIME,
    "end": END_TIME,
    "step": STEP
}

# Send the request to the Prometheus API
response = requests.get(PROMETHEUS_URL, params=params)

# Check for errors
if response.status_code != 200:
    raise Exception(f"Error querying Prometheus: {response.status_code}, {response.text}")

# Parse the JSON response
data = response.json()
print(f"Full Response: {data}")  # Print full response for debugging

# Check if there's an error in the response
if 'status' in data and data['status'] == 'error':
    raise Exception(f"Error from Prometheus: {data['errorType']}, {data['error']}")

# Extract the time series data
if 'data' in data and 'result' in data['data']:
    results = data['data']['result']
    for result in results:
        metric = result['metric']
        values = result['values']
        
        # Convert to a pandas DataFrame for easier analysis
        df = pd.DataFrame(values, columns=['timestamp', 'value'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['value'] = pd.to_numeric(df['value'])
        
        # Print the first few rows of the data
        print(f"Metric: {metric}")
        print(df.head())
else:
    print("No data found for the specified query and time range.")
