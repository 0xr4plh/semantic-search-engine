import json
# second script to change the original data
# This code only selects the fields required to make search engine , and dropping other columns.

# Path to the filtered JSONL file
input_file = 'filtered_issues.jsonl'
# Path to the output JSONL file with selected fields
output_file = 'selected_fields_issues.jsonl'

# Open the input and output files
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    # Iterate over each line in the input file
    for line in infile:
        # Convert the JSON line to a Python dictionary
        data = json.loads(line)
        
        # Extract only the selected fields
        selected_data = {
            'html_url': data.get('html_url', ''),
            'title': data.get('title', ''),
            'comments': data.get('comments', 0),
            'body': data.get('body', ''),
            'number': data.get('number', 0)
        }
        
        # Write the filtered data to the output file
        outfile.write(json.dumps(selected_data) + '\n')

print(f'Created {output_file} with selected fields.') # saves the selected_fields_issues.jsonl to the local