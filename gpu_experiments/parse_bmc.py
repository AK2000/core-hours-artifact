import json
import sys
from datetime import datetime
from statistics import mean

def parse_timestamp(timestamp_str):
    # Extract the time part after 'T' and before '+'
    time_str = timestamp_str.split('T')[1].split('+')[0]
    # Parse the time string to a datetime object
    return datetime.strptime(time_str, "%H:%M:%S.%f")

def process_file(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract timestamps
    timestamps = [parse_timestamp(entry['timestamp']) for entry in data]

    # Calculate job duration
    start_time = min(timestamps)
    end_time = max(timestamps)
    duration = (end_time - start_time).total_seconds()

    # Extract bmc_node_power_watt values
    bmc_node_power_watt_values = [entry['value'] for entry in data if entry['metric_id'] == 'bmc_node_power_watt']

    # Calculate mean value of bmc_node_power_watt
    if bmc_node_power_watt_values:
        mean_bmc_node_power_watt = mean(bmc_node_power_watt_values)
    else:
        mean_bmc_node_power_watt = None  # Handle case where there are no values

    # Prepare the output line
    output_line = f"{input_file},{duration},{mean_bmc_node_power_watt},0\n"

    # Append the output to the output file
    with open(output_file, 'a') as file:
        file.write(output_line)

    print(f"Data has been appended to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_file(input_file, output_file)
