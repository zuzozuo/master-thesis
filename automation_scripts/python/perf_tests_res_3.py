import os
import csv
import numpy as np

# Define the file names
#FILE_NAMES = ['1producer_1consumer_1mb.txt', '1producer_1consumer_small_1kb.txt',
 #             '1producer_1consumer_10kb.txt', '1producer_1consumer_100kb.txt']
 
 
FN_PRODUCER_CONSUMER_RATIO = ['1producer_1consumer.txt','1producer_10consumers.txt', '10producer_1consumers.txt', '10producer_10consumer.txt', '1producer_100consumers.txt', '100producers_10consumers.txt' ]
# Define the CSV header
CSV_HEADER = ['file_name', 'time (s)', 'sent (msg/s)', 'received (msg/s)', 
              'min_latency (s)', 'median_latency (s)', '75th_latency (s)', 
              '95th_latency (s)', '99th_latency (s)', 
              'min_time', 'max_time', 'avg_time', 
              'min_sent', 'max_sent', 'avg_sent', 
              'min_received', 'max_received', 'avg_received',
              'min_latency_min', 'max_latency_min', 'avg_latency_min',
              'min_latency_median', 'max_latency_median', 'avg_latency_median',
              'min_latency_75th', 'max_latency_75th', 'avg_latency_75th',
              'min_latency_95th', 'max_latency_95th', 'avg_latency_95th',
              'min_latency_99th', 'max_latency_99th', 'avg_latency_99th']

# Iterate over each file
for x in FN_PRODUCER_CONSUMER_RATIO:
    try:
        input_file_path = f'D:\\Studia\\PRACAMGR\\WYNIKI_TESTOW\\PROD_CONS_RATIO\\{x}'
        output_file_path = f'D:\\Studia\\PRACAMGR\\EXCELKI_DO_MGR\\PROD_CONS_RATIO\\{x}.csv'

        if not os.path.exists(input_file_path):
            print(f"File not found: {input_file_path}")
            continue

        # Initialize lists to store values for statistics
        times = []
        sent_rates = []
        received_rates = []
        min_latencies = []
        median_latencies = []
        seventy_fifth_latencies = []
        ninety_fifth_latencies = []
        ninety_ninth_latencies = []

        with open(input_file_path, 'r') as my_res_file, open(output_file_path, 'w+') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            csv_writer.writerow(CSV_HEADER)

            for line in my_res_file:
                if 'time' in line and 'msg/s' in line and 'consumer latency' in line:
                    tmp = line.strip().split(',')
                    test_name = tmp[0].split()[1]
                    time = float(tmp[1].split()[1].replace(",", "."))
                    sent = float(tmp[2].split()[1].replace(",", "."))
                    received = float(tmp[3].split()[1].replace(",", "."))
                    latency = tmp[4].split()[3].split('/')
                    min_latency = int(latency[0]) / 1_000_000  # Convert from µs to s
                    median = int(latency[1]) / 1_000_000  # Convert from µs to s
                    seventy_fifth = int(latency[2]) / 1_000_000  # Convert from µs to s
                    ninety_fifth = int(latency[3]) / 1_000_000  # Convert from µs to s
                    ninety_ninth = int(latency[4]) / 1_000_000  # Convert from µs to s

                    # Append values to lists for statistics
                    times.append(time)
                    sent_rates.append(sent)
                    received_rates.append(received)
                    min_latencies.append(min_latency)
                    median_latencies.append(median)
                    seventy_fifth_latencies.append(seventy_fifth)
                    ninety_fifth_latencies.append(ninety_fifth)
                    ninety_ninth_latencies.append(ninety_ninth)

                    # Write the values to the CSV file
                    csv_writer.writerow([test_name, time, sent, received, min_latency, 
                                         median, seventy_fifth, ninety_fifth, ninety_ninth])

            # Calculate and write min, max, avg for each metric
            csv_writer.writerow(['Min/Max/Avg',
                                 min(times), max(times), np.mean(times),
                                 min(sent_rates), max(sent_rates), np.mean(sent_rates),
                                 min(received_rates), max(received_rates), np.mean(received_rates),
                                 min(min_latencies), max(min_latencies), np.mean(min_latencies),
                                 min(median_latencies), max(median_latencies), np.mean(median_latencies),
                                 min(seventy_fifth_latencies), max(seventy_fifth_latencies), np.mean(seventy_fifth_latencies),
                                 min(ninety_fifth_latencies), max(ninety_fifth_latencies), np.mean(ninety_fifth_latencies),
                                 min(ninety_ninth_latencies), max(ninety_ninth_latencies), np.mean(ninety_ninth_latencies)])

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

print("Data extraction and CSV generation completed successfully.")
