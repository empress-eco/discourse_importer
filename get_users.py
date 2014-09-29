import csv
import hashlib
import datetime
import json

reader = csv.DictReader(open('erpnext-developer-forum.csv'))
members = []
for row in reader:
	members.append({
		'email': row['Email address'],
		'username': row['Email address'],
		'id': hashlib.md5(row['Email address']).hexdigest(),
		'created_at': datetime.datetime(int(row['Join year']), int(row['Join month']), int(row['Join day'])).isoformat()
	})

with open('users.json', 'w') as f:
	json.dump(members, f, indent=1)
