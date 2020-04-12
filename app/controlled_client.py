from app import pid
from app import imap_client
import time
import notify2
from datetime import datetime

class ControlledClient:
    def __init__(self, name, client, controller):
        self.name = name
        self.client = client
        self.controller = controller
        self.sleep_time = int(self.controller.get()) 
        self.new_emails = 0
        self.unread_emails = 0

    def sleep(self):
        time.sleep(self.sleep_time)

    def update(self):
        self.client.connect()
        (self.new_emails, self.unread_emails, error) = self.client.plant()
        self.client.disconnect()
        self.controller.update(error)
        self.sleep_time = self.controller.get()

    def notify_me(self, notifier):
        if self.new_emails + self.unread_emails > 0:
            title = "Ctrl-Gmail ({}): {} new and {} unread message(s)".format(self.name, self.new_emails, self.unread_emails )
            next_check = datetime.fromtimestamp(int(time.time() + self.sleep_time)).strftime("%H:%M:%S")
            description = "Next check at {}".format(next_check)
            notifier.update(title, description) 
            notifier.show()

