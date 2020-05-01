import imaplib
import email
import datetime
import time

class IMAPClient:
    def __init__(self, host, user, password, inbox = "Inbox"):
        self.host = host
        self.user = user
        self.password = password
        self.inbox = inbox
        self.seen_message_ids = set()
        self.imap = None
        self.current_time = int(time.time())
        self.time_stamp_most_recent_message = self.current_time

    def connect(self):
        self.imap = imaplib.IMAP4_SSL(self.host)
        self.imap.login(self.user, self.password)

    def disconnect(self):
        self.imap.close()
        self.imap.logout()

    def get_unseen_ids(self):
        self.imap.select(self.inbox)
        tmp, data = self.imap.search(None, '(UNSEEN)')
        ids = data[0].split()
        return ids

    def get_all_ids(self):
        self.imap.select(self.inbox)
        tmp, data = self.imap.search(None, 'ALL')
        ids = data[0].split()
        return ids

    def extract_data_for_analysis(self, filename):
        self.connect()
        message_ids = self.get_all_ids()

        data_file = open(filename, "w")
        l = len(message_ids)
        for (i, msg_id) in enumerate(message_ids):
            print("{}/{}".format(i, l))
            timestamp = self.get_message_internal_date(msg_id, False)  
            data_file.write(str(timestamp) + "\n")
        data_file.close()
        self.disconnect()

    def get_message_internal_date(self, message_id, to_unseen):
        tmp, data = self.imap.fetch(message_id, '(RFC822)')
        if to_unseen:
            self.imap.store(message_id, '-FLAGS', '\\SEEN')
        msg = email.message_from_bytes(data[0][1])
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        local_date = email.utils.mktime_tz(date_tuple)
        return local_date

    def do_i_know_you(self, message_id):
        return (message_id in self.seen_message_ids)

    def remember_message(self, message_id, internal_date_message):
        self.seen_message_ids.add(message_id)
        if internal_date_message > self.time_stamp_most_recent_message:
            self.time_stamp_most_recent_message = internal_date_message

    def refresh_time(self):
        self.current_time = int(time.time())

    def plant(self):
        ids = self.get_unseen_ids()
        self.refresh_time()
        new_emails = 0
        unread_emails = 0
        for message_id in ids:
            if not self.do_i_know_you(message_id):
                internal_date_message = self.get_message_internal_date(message_id, True)
                new_emails += 1
                self.remember_message(message_id, internal_date_message)
            else:
                unread_emails += 1
        return (new_emails, unread_emails,  (1 - 2 * int(new_emails == 0)) * (self.time_stamp_most_recent_message - self.current_time))
