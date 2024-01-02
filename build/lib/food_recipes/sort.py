import json

# Read JSON data from file with specified encoding
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Sort JSON array based on "page_number"
sorted_data = sorted(data, key=lambda x: x['page_number'])

# Write sorted JSON data to result.json
with open('result.json', 'w', encoding='utf-8') as result_file:
    json.dump(sorted_data, result_file, indent=2)

print("Sorting and saving completed. Check result.json for the sorted data.")
