import os
import csv
from consts import MESSAGE_SIZE, PRODUCER_CONSUMER

INPUT_DIR = f'D:\\Studia\\PRACAMGR\\WYNIKI_TESTOW\\{MESSAGE_SIZE['DIR']}\\'
OUTPUT_FILE_PATH =  f'D:\\Studia\\PRACAMGR\\EXCELKI_DO_MGR\\{MESSAGE_SIZE['DIR']}\\{MESSAGE_SIZE['DIR'].lower()}.csv'

# Define CSV header
CSV_HEADER = ['file_name', 'sending_rate_avg (msg/s)', 'receiving_rate_avg (msg/s)', 
              'min_latency (s)', 'median_latency (s)', '75th_latency (s)', 
              '95th_latency (s)', '99th_latency (s)']

# Open the output CSV file for writing
with open(OUTPUT_FILE_PATH, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerow(CSV_HEADER)  # Write the header row

    # Process each file
    for file_name in MESSAGE_SIZE['FILE_NAMES']:
        input_file_path = os.path.join(INPUT_DIR, file_name)

        if not os.path.exists(input_file_path):
            print(f"File not found: {input_file_path}")
            continue

        with open(input_file_path, 'r') as file:
            sending_rate = ""
            receiving_rate = ""
            min_latency = ""
            median_latency = ""
            seventy_fifth_latency = ""
            ninety_fifth_latency = ""
            ninety_ninth_latency = ""

            for line in file:
                if 'sending rate avg' in line:
                    sending_rate = line.split(':')[2].strip().split()[0]
                elif 'receiving rate avg' in line:
                    receiving_rate = line.split(':')[2].strip().split()[0]
                elif 'consumer latency min/median/75th/95th/99th' in line:
                    latencies = line.split(':')[1].strip().split('/')
                    min_latency = int(latencies[4].split()[1].strip())/1000000
                    median_latency = int(latencies[5].strip())/1000000
                    seventy_fifth_latency = int(latencies[6].strip())/1000000
                    ninety_fifth_latency = int(latencies[7].strip())/1000000
                    ninety_ninth_latency = int(latencies[8].split()[0].strip())/1000000
                    
            # Write the extracted data to the CSV file
            csvwriter.writerow([file_name, sending_rate, receiving_rate, min_latency, 
                                median_latency, seventy_fifth_latency, ninety_fifth_latency, 
                                ninety_ninth_latency])

print("Data extraction and CSV generation completed successfully.")
