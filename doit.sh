#! /bin/bash
mkdir -p mails threads topics
python fetch_via_imap.py
python fetch_thread_ids.py
