import os
from consts import MESSAGE_SIZE, PRODUCER_CONSUMER

CSV_HEADER = ['file_name', 'time (s)', 'sent (msg/s)', 'received (msg/s)', 'min (s)', 'median (s)', '75th (s)', '95th (s)', '99th (s)']

for x in MESSAGE_SIZE['FILE_NAMES']:
    try:
        input_file_path = f'D:\\Studia\\PRACAMGR\\WYNIKI_TESTOW\\{MESSAGE_SIZE['DIR']}\\{x}'
        output_file_path = f'D:\\Studia\\PRACAMGR\\EXCELKI_DO_MGR\\{MESSAGE_SIZE['DIR']}\\{x}.csv'

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
                    min_latency = str(int(latency[0])/1000000)
                    median = str(int(latency[1])/1000000)
                    seventy_fifth = str(int(latency[2])/1000000)
                    ninety_fifth = str(int(latency[3])/1000000)
                    ninety_ninth = str(int(latency[4])/1000000)
                    
                    # Write directly to the output file
                    output_file.write(';'.join([test_name, time, sent, received, min_latency, median, seventy_fifth, ninety_fifth, ninety_ninth]) + "\n")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
