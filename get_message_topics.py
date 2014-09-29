import os
import email
from multiprocessing.dummy import Pool

tiddir = 'threads'
maildir = 'mails'
topicdir = 'topics'
tids = None
tid_to_mail = None
topic_cache = {}

def invert_dict(ddict):
	ret = {}
	for k,v in ddict.iteritems():
		if not ret.get(v):
			ret[v] = [k]
		else:
			ret[v].append(k)
	return ret

def get_mails():
	return os.listdir(maildir)

def get_tids():
	global tids
	if tids:
		return tids
	ret={}
	for mail in get_mails():
		with open(os.path.join(tiddir, mail)) as f:
			tid = f.read()
			ret[mail] = tid
	tids = ret
	return tids

def get_tid_to_mail_dict():
	global tid_to_mail
	if tid_to_mail:
		return tid_to_mail
	mail_tids = get_tids()
	tid_to_mail = invert_dict(tids)
	return tid_to_mail

def get_mail_message(mail):
	with open(os.path.join(maildir, mail)) as f:
		return email.message_from_file(f)

def sanitize_topic(topic):
	prefixes = ['[wnframework] ', '[erpnext-dev] ', '[erpnext-user-form] ']
	for prefix in prefixes:
		if topic.startswith(prefix):
			return topic.split(prefix)[1]
	return topic.strip()

def get_thread_topic(tid):
	if topic_cache.get(tid):
		return topic_cache[tid]
	mails = get_tid_to_mail_dict()[tid]
	subjects = [get_mail_message(mail)['Subject'] for mail in mails]
	subjects.sort(key=len)
	topic = subjects[0]
	topic = sanitize_topic(topic)
	topic_cache[tid] = topic
	return topic

def mails_to_topics():
	ret = {}
	for mail in get_mails():
		tid = get_tids()[mail]
		ret[mail] = get_thread_topic(tid)
	return ret

def main():
	for mail, topic in mails_to_topics().iteritems():
		with open(os.path.join(topicdir, mail), 'w') as f:
			f.write(topic + '\n')

if __name__ == "__main__":
	main()

