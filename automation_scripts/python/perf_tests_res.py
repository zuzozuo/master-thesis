import os
from consts import MESSAGE_SIZE, PRODUCER_CONSUMER, PRODUCER_CONSUMER_PUBLISH_RATE_100, PRODUCER_CONSUMER_PUBLISH_RATE_1000, PRODUCER_CONSUMER_PUBLISH_RATE_10000
import csv

INPUT_DIRECTORY_PATH = f'D:\\Studia\\PRACAMGR\\WYNIKI_TESTOW'
OUTPUT_DIRECTORY_PATH = f'D:\\Studia\\PRACAMGR\\EXCELKI_DO_MGR'

def generate_excel_files_from_txts(filedict):
    
    CSV_HEADER = ['file_name', 'time (s)', 'sent (msg/s)', 'received (msg/s)', 'min (s)', 'median (s)', '75th (s)', '95th (s)', '99th (s)']
    OUTPUT_DIR = f'{OUTPUT_DIRECTORY_PATH}\\{filedict["DIR"]}\\'
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")
        
    for x in filedict['FILE_NAMES']:
        try:
            input_file_path = f'{INPUT_DIRECTORY_PATH}\\{filedict['DIR']}\\{x}'
            output_file_path = f'{OUTPUT_DIRECTORY_PATH}\\{filedict['DIR']}\\{x}.csv'

            if not os.path.exists(input_file_path):
                print(f"File not found: {input_file_path}")
                continue

            with open(input_file_path, 'r') as my_res_file, open(output_file_path, 'w+') as output_file:
                output_file.write(';'.join(CSV_HEADER) + "\n")

                for line in my_res_file:
                    if 'time' in line and 'msg/s' in line and 'consumer latency' in line:
                        tmp = line.strip().split(',')
                        test_name = tmp[0].split()[1]
                        time = tmp[1].split()[1].replace(".", ",")
                        sent = tmp[2].split()[1].replace(".", ",")
                        received = tmp[3].split()[1].replace(".", ",")
                        latency = tmp[4].split()[3].split('/')
                        min_latency = str(int(latency[0])/1000000).replace(".", ",")
                        median = str(int(latency[1])/1000000).replace(".", ",")
                        seventy_fifth = str(int(latency[2])/1000000).replace(".", ",")
                        ninety_fifth = str(int(latency[3])/1000000).replace(".", ",")
                        ninety_ninth = str(int(latency[4])/1000000).replace(".", ",")
                        
                        # Write directly to the output file
                        output_file.write(';'.join([test_name, time, sent, received, min_latency, median, seventy_fifth, ninety_fifth, ninety_ninth]) + "\n")
    
        except FileNotFoundError:
            print(f"Error: The file {input_file_path} does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    print("All csv files were generated sucessfully.")
            
            
def generate_excel_summary(filedict):
    INPUT_DIR = f'{INPUT_DIRECTORY_PATH}\\{filedict['DIR']}\\'
    OUTPUT_DIR = f'{OUTPUT_DIRECTORY_PATH}\\{filedict["DIR"]}\\'
    OUTPUT_FILE_PATH =  f'{OUTPUT_DIR}\\{filedict['DIR']}.csv'

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    # Define CSV header
    CSV_HEADER = ['file_name', 'sending_rate_avg (msg/s)', 'receiving_rate_avg (msg/s)', 
                'min_latency (s)', 'median_latency (s)', '75th_latency (s)', 
                '95th_latency (s)', '99th_latency (s)']

    # Open the output CSV file for writing
    with open(OUTPUT_FILE_PATH, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(CSV_HEADER)  # Write the header row

        # Process each file
        for file_name in filedict['FILE_NAMES']:
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
    
    

generation_list = [PRODUCER_CONSUMER_PUBLISH_RATE_100, PRODUCER_CONSUMER_PUBLISH_RATE_1000, PRODUCER_CONSUMER_PUBLISH_RATE_10000]

for x in generation_list:
    generate_excel_files_from_txts(x)
    generate_excel_summary(x)
