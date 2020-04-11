from __future__ import print_function
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class PID:
    def __init__(self, variable = 0, kp = 0, ki = 0, kd = 0, delta_t = 1):
        self.variable = variable
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.cumulated_error = 0
        self.previous_error = 0
        self.delta_t = delta_t

    def update(self, error):
        self.cumulated_error += error
        proportional_term = self.kp * error
        integral_term = self.ki * self.cumulated_error * self.delta_t
        derivative_term = self.kd * (error - self.previous_error) / self.delta_t

        u = self. variable + proportional_term + integral_term + derivative_term

        if u < 0:
            u = 0

        self.previous_error = error
        self.variable = u

    def get(self):
        return self.variable


def how_many_new_emails(timestamp_oldest_message):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=["UNREAD", "INBOX", "CATEGORY_PERSONAL"]).execute()

    new_emails = 0
    current_time = int(time.time())
    error = 0

    try:
        for m in results["messages"]:
            msg_id = m["id"]
            mess = service.users().messages().get(userId='me', id=msg_id).execute()
            new_emails += 1
            msg_time = int(mess["internalDate"][:-3])
            if msg_time > timestamp_oldest_message:
                timestamp_oldest_message = msg_time
            if msg_time - current_time < error:
                error = msg_time - current_time
        if new_emails == 0:
            error = current_time - timestamp_oldest_message
        return (new_emails, error, timestamp_oldest_message)
    except:
        error = current_time - timestamp_oldest_message
        return (new_emails, error, timestamp_oldest_message)

def main():
    controller = PID(variable = 10, kp = 0.3, ki = 0.1, kd = 0.1)
    timestamp_oldest_message = int(time.time())
    while True:
        sleep_time = controller.get()
        print(" [*] Sleeping for {} seconds".format(sleep_time))
        time.sleep(int(sleep_time))
        print(" [*] Reading emails")
        (nb_new_emails, error, timestamp_oldest_message) = how_many_new_emails(timestamp_oldest_message)
        print(" [*] You have {} new message(s)".format(nb_new_emails))
        print(" [*] Updating the controller (error: {})".format(error))
        controller.update(error)

if __name__ == '__main__':
    main()
