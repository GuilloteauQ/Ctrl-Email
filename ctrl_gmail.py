import time
import json
import sys
import notify2
from datetime import datetime
import pid
import gmail_client

def extract_config(filename):
    controller = pid.PID()
    credentials_path = "credentials.json"
    with open(filename) as config_file:
        json_data = json.load(config_file)
        for key, val in json_data.items():
            if key == "kp":
               controller.kp = float(val)
            elif key == "ki":
               controller.ki = float(val)
            elif key == "kd":
               controller.kd = float(val)
            elif key == "initial":
               controller.variable = float(val)
            elif key == "max_value":
               controller.max_value = float(val)
            elif key == "credentials_path":
                credentials_path = val
            else:
                print("Unknown key value pair: ({}, {})".format(key, val))
    client = gmail_client.GmailClient(credentials_path = credentials_path)
    return (controller, client)


def main():
    args = sys.argv
    if len(args) > 1:
        config_file_name = args[1]
    else:
        config_file_name = "config.json"

    (controller, client) = extract_config(config_file_name)
    notify2.init("Ctrl-Gmail")
    notifyer = notify2.Notification(None, icon="")
    notifyer.set_urgency(notify2.URGENCY_NORMAL)
    notifyer.set_timeout(10000)

    sleep_time = controller.get()
    while True:
        # print(" [*] Sleeping for {} seconds".format(sleep_time))
        time.sleep(int(sleep_time))
        # print(" [*] Reading emails")
        (nb_new_emails, nb_unread_emails, error) = client.plant()
        # print(" [*] You have {} new message(s) and {} unread message(s)".format(nb_new_emails, nb_unread_emails))
        # print(" [*] Updating the controller (error: {})".format(error))
        controller.update(error)
        sleep_time = controller.get()
        if nb_new_emails + nb_unread_emails > 0:
            title = "Ctrl-Gmail: {} new and {} unread message(s)".format(nb_new_emails, nb_unread_emails )
            next_check = datetime.fromtimestamp(int(time.time() + sleep_time)).strftime("%H:%M:%S")
            description = "Next check at {}".format(next_check)
            notifyer.update(title, description) 
            notifyer.show()

if __name__ == '__main__':
    main()
