from get_message_topics import get_tid_to_mail_dict, get_mail_message
import hashlib
import dateutil.parser
import os
import json
from email.utils import parseaddr

tiddir = 'threads'
maildir = 'mails'
topicdir = 'topics'

def get_topic(mail):
	with open(os.path.join(topicdir, mail)) as f:
		return f.read().strip()

def get_message_body(mail):
	msg = get_mail_message(mail)
	html = []
	text = []
	for part in msg.walk():
		if part.get_content_type() == "text/plain":
			text.append(part)
		elif part.get_content_type() == "text/html":
			html.append(part)
	if html:
		return html[0].get_payload(decode=True).decode("ISO-8859-1")
	elif text:
		return text[0].get_payload(decode=True).decode("ISO-8859-1")
	else:
		raise Exception('No suitable part found')

def get_messages():
	tid_to_mail = get_tid_to_mail_dict()
	tids = tid_to_mail.keys()
	ret = []
	for tid in tids[:10]:
		thread = []
		mails = tid_to_mail[tid]
		topic = get_topic(mails[0])
		for mail in mails:
			thread.append({
				'topic_id': tid,
				'post_id': mail,
				'topic': topic,
				'user_id': hashlib.md5(parseaddr(get_mail_message(mail)['From'])[1]).hexdigest(),
				'category': 15,
				'message': get_message_body(mail),
				'created_at': get_mail_message(mail)['Date']
			})
		thread.sort(key=lambda msg: dateutil.parser.parse(msg['created_at']))
		first_post_id = thread[0]['post_id']
		for post in thread:
			post['first_post_id'] = first_post_id
		ret.extend(thread)
	return ret

if __name__ == "__main__":
	with open('messages.json', 'w') as f:
		json.dump(get_messages(), f, indent=1)
