import json
# first script to change the original data
# This is the code which outputs a filtered version of 'datasets-issues.jsonl' , and delets those issues which are pull requests 

# Path to the input JSONL file
input_file = 'datasets-issues.jsonl'
# Path to the output JSONL file
output_file = 'filtered_issues.jsonl'

# Initialize a counter to keep track of how many entries are saved
count = 0

# Open the input and output files
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    # Iterate over each line in the input file
    for line in infile:
        # Convert the JSON line to a Python dictionary
        data = json.loads(line)
        
        # Check if 'pull_request' is in the dictionary and if its value is null
        if 'pull_request' in data and data['pull_request'] is None:
            # Write the original JSON line to the output file
            outfile.write(json.dumps(data) + '\n')
            count += 1

print(f'Filtered {count} entries where pull_request is null into {output_file}') # output file named filtered_issues.jsonl will be saved to local.