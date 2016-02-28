import json

file_directory = "data.json"
json_data=open(file_directory).read()
data = json.loads(json_data)

first_key= data.keys()[0]
keys = data[first_key].keys()
with open('data.csv', 'w') as f:
	f.write(','.join(keys) + '\n')
	for car in data:
		results = []
		for k in keys:
			if k in data[car]:
				results.append(data[car][k].encode('utf8'))
			else:
				results.append('NA')
		f.write(','.join(results) + '\n')
