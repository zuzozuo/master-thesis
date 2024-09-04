import requests
import matplotlib.pyplot as plt
import pandas as pd

# Replace with your Prometheus server URL
prometheus_url = "http://10.20.20.60:9090/api/v1/query_range"

# Define the different time ranges and corresponding queue lengths
time_ranges = [
    ("2024-09-01T13:05:03Z", "2024-09-01T13:17:00Z", "queue length=1"),
    ("2024-09-01T14:36:03Z", "2024-09-01T14:47:00Z", "queue length=4"),
    ("2024-09-01T16:07:03Z", "2024-09-01T16:20:00Z", "queue length=10"),
    ("2024-09-01T17:38:03Z", "2024-09-01T17:50:00Z", "queue length=100"),
    ("2024-09-01T19:08:03Z", "2024-09-01T19:20:00Z", "queue length=200")
]

# Define your Prometheus query
query = 'perftest_latency_seconds{quantile="0.99"}'  # Replace with your actual Prometheus query

# Plot the data
plt.figure(figsize=(10, 6))

for start_time, end_time, legend_label in time_ranges:
    # Construct the query URL
    url = f"{prometheus_url}?query={query}&start={start_time}&end={end_time}&step=1s"
    
    # Send the request to Prometheus
    response = requests.get(url)
    data = response.json()

    # Check if the response contains data
    if 'data' not in data or 'result' not in data['data'] or len(data['data']['result']) == 0:
        print(f"No data returned for time range {start_time} to {end_time}.")
        continue
    
    # Parse the response
    timestamps = []
    values = []
    
    for result in data['data']['result']:
        for value in result['values']:
            timestamps.append(pd.to_datetime(value[0], unit='s'))
            values.append(float(value[1]) * 1000)

    # Check if timestamps list is empty
    if not timestamps:
        print(f"No timestamps found for time range {start_time} to {end_time}.")
        continue
    
    # Normalize the time by subtracting the first timestamp to align at t=0 seconds
    initial_time = timestamps[0]
    normalized_times = [(time - initial_time).total_seconds() for time in timestamps]
    
    # Convert to a Pandas DataFrame
    df = pd.DataFrame({"Time (s)": normalized_times, "Value": values})
    
    # Plot each time range
    plt.plot(df["Time (s)"], df["Value"], label=legend_label)
    plt.fill_between(df["Time (s)"], df["Value"], alpha=0)

# Customize the plot
plt.xlabel("Time (seconds)")
plt.ylabel("Latency (seconds)")
plt.title("End-to-End Message Latency")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
    
#     for result in data['data']['result']:
#         for value in result['values']:
#             timestamps.append(pd.to_datetime(value[0], unit='s'))
#             values.append(float(value[1]))
    
#     # Convert to a Pandas DataFrame
#     df = pd.DataFrame({"Time": timestamps, "Value": values})
    
#     # Plot each time range
#     plt.plot(df["Time"], df["Value"], label=legend_label)
#     plt.fill_between(df["Time"], df["Value"], alpha=0.3)

# # Customize the plot
# plt.xlabel("Time")
# plt.ylabel("Latency (seconds)")
# plt.title("End-to-End Message Latency (Quantile 0.99)")
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.show()