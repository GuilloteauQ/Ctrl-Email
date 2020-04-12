from __future__ import print_function
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailClient:
    def __init__(self, credentials_path="credentials.json"):

        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.seen_message_ids = set()
        self.messages = None
        self.current_time = int(time.time())
        self.time_stamp_most_recent_message = self.current_time

    def fetch_unread_messages(self):
        try:
            self.messages = self.service.users().messages().list(userId='me', labelIds=["UNREAD", "INBOX", "CATEGORY_PERSONAL"]).execute()["messages"]
        except:
            self.messages = []

    def get_message(self, message_id):
        return self.service.users().messages().get(userId='me', id=message_id).execute()

    def get_message_internal_date(self, message_id):
        msg = self.get_message(message_id)
        return int(msg["internalDate"][:-3])

    def do_i_know_you(self, message_id):
        return (message_id in self.seen_message_ids)

    def remember_message(self, message_id, internal_date_message):
        self.seen_message_ids.add(message_id)
        if internal_date_message > self.time_stamp_most_recent_message:
            self.time_stamp_most_recent_message = internal_date_message

    def refresh_time(self):
        self.current_time = int(time.time())

    def plant(self):
        self.fetch_unread_messages()
        self.refresh_time()
        new_emails = 0
        unread_emails = 0
        for m in self.messages:
            message_id = m["id"]
            if not self.do_i_know_you(message_id):
                internal_date_message = self.get_message_internal_date(message_id)
                new_emails += 1
                self.remember_message(message_id, internal_date_message)
            else:
                unread_emails += 1
        return (new_emails, unread_emails,  (1 - 2 * int(new_emails == 0)) * (self.time_stamp_most_recent_message - self.current_time))

