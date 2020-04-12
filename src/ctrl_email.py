import time
import json
import sys
import notify2
from datetime import datetime
import pid
import gmail_client
import imap_client
import controlled_client

def json_to_client(json_obj):
    imap_host = json_obj["host"]
    imap_user = json_obj["user"]
    imap_pass = json_obj["pass"]
    return imap_client.IMAPClient(imap_host, imap_user, imap_pass)

def json_to_controller(json_obj):
    kp = float(json_obj["kp"])
    ki = float(json_obj["ki"])
    kd = float(json_obj["kd"])
    initial = float(json_obj["initial"])
    max_value = float(json_obj["max_value"])
    return pid.PID(kp = kp, ki = ki, kd = kd, variable = initial, max_value = max_value)

def json_to_controlled_client(json_obj):
    name = json_obj["name"]
    client = json_to_client(json_obj["client"])
    controller = json_to_controller(json_obj["controller"])
    return controlled_client.ControlledClient(name, client, controller)

def extract_config(filename):
    with open(filename) as config_file:
        json_data = json.load(config_file)
        return [json_to_controlled_client(json_cclient) for json_cclient in json_data["cclients"]]


def main():
    args = sys.argv
    if len(args) > 1:
        config_file_name = args[1]
    else:
        config_file_name = "config.json"

    cclients = extract_config(config_file_name)

    notify2.init("Ctrl-Gmail")
    notifyer = notify2.Notification(None, icon="")
    notifyer.set_urgency(notify2.URGENCY_NORMAL)
    notifyer.set_timeout(10000)

    while True:
        min_sleep_time = min(map(lambda c: c.sleep_time, cclients))
        time.sleep(min_sleep_time)
        for client in cclients:
            client.sleep_time -= min_sleep_time
            if client.sleep_time == 0:
                client.update()
                client.notify_me(notifyer)

if __name__ == '__main__':
    main()