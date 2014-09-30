#! /bin/bash
mkdir -p mails threads topics
echo 'fetching emails'
python fetch_via_imap.py
echo 'fetching threads'
python fetch_thread_ids.py
echo 'processsing topic names'
python get_message_topics.py
echo 'exporting everything to JSON'
python export_messages.py 
