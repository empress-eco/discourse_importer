import imaplib
import getpass
import os
import email

maildir = 'mails'

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('pdvyas@gmail.com', getpass.getpass())
try:
	mail.select('erpnext-dev-forum')
	result, data = mail.uid('search', 'All')
	ids = data[0]

	id_list = ids.split()
	maildir_list = os.listdir(maildir)
	to_fetch = set(id_list) - set(maildir_list)

	for mail_id in to_fetch:
		result, data = mail.uid('fetch', mail_id, "(RFC822)")
		raw_email = data[0][1]
		with open(os.path.join(maildir, mail_id),'w') as f:
			f.write(raw_email)
		print 'processed', mail_id
	mail.close()
finally:
	mail.logout()
