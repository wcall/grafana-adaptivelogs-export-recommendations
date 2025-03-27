import json
import sys

# Check if the file name is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python3 prettify-json.py <json_file>")
    sys.exit(1)

json_file = sys.argv[1]

# Read and prettify the JSON file
with open(json_file, 'r') as f:
    data = json.load(f)

with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)