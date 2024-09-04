import requests
import matplotlib.pyplot as plt
import pandas as pd

# Replace with your Prometheus server URL
prometheus_url = "http://10.20.20.60:9090/api/v1/query_range"

# Define your Prometheus query
query = 'perftest_latency_seconds{quantile="0.99"}'  # Replace with your actual Prometheus query

# Define the start and end time for your query (replace with your actual timestamps)
start_time = "2024-09-01T13:05:03Z"
end_time = "2024-09-01T13:17:00Z"
step = "1s"  # Interval at which to fetch data (adjust based on your needs)

# Construct the query URL
url = f"{prometheus_url}?query={query}&start={start_time}&end={end_time}&step={step}"

# Send the request to Prometheus
response = requests.get(url)
data = response.json()

# Parse the response
timestamps = []
values = []

for result in data['data']['result']:
    for value in result['values']:
        timestamps.append(pd.to_datetime(value[0], unit='s'))
        values.append(float(value[1]))

# Convert to a Pandas DataFrame
df = pd.DataFrame({"Time": timestamps, "Value": values})

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df["Time"], df["Value"], label="End-to-end message latency", color='yellow')
plt.fill_between(df["Time"], df["Value"], color="green", alpha=0.3)
plt.xlabel("Time")
plt.ylabel("Latency (seconds)")
plt.title("End-to-end Message Latency")
plt.legend()
plt.grid(True)
plt.show()
