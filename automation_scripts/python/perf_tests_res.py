import os

CSV_HEADER = ['file_name', 'time (s)', 'sent (msg/s)', 'received (msg/s)', 'min (us)', 'median (us)', '75th (us)', '95th (us)', '99th (us)']
TEST_AMOUNT = 10

for x in range(0, TEST_AMOUNT):
    try:
        input_file_path = f'Z:\\test{x}.txt'
        output_file_path = f'..\\..\\results\\basic\\result{x}.csv'

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
                    min_latency = latency[0]
                    median = latency[1]
                    seventy_fifth = latency[2]
                    ninety_fifth = latency[3]
                    ninety_ninth = latency[4]

                    # Write directly to the output file
                    output_file.write(';'.join([test_name, time, sent, received, min_latency, median, seventy_fifth, ninety_fifth, ninety_ninth]) + "\n")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
