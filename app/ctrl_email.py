import time
import os.path
import json
import sys
import notify2
from datetime import datetime
import app
from app import pid
from app import gmail_client
from app import imap_client
from app import controlled_client

def json_to_imap_client(json_obj):
    imap_host = json_obj["host"]
    imap_user = json_obj["user"]
    imap_pass = json_obj["pass"]
    return imap_client.IMAPClient(imap_host, imap_user, imap_pass)

def json_to_gmail_client(json_obj):
    credentials_path = json_obj["credentials_path"]
    return gmail_client.GmailClient(credentials_path)

def json_to_controller(json_obj):
    kp = float(json_obj["kp"])
    ki = float(json_obj["ki"])
    kd = float(json_obj["kd"])
    initial = float(json_obj["initial"])
    max_value = float(json_obj["max_value"])
    return pid.PID(kp = kp, ki = ki, kd = kd, variable = initial, max_value = max_value)

def json_to_controlled_client(json_obj):
    name = json_obj["name"]
    json_client = json_obj["client"]
    if json_client["type"] == "Gmail":
        client = json_to_gmail_client(json_client)
    else:
        client = json_to_imap_client(json_client)
    controller = json_to_controller(json_obj["controller"])
    return controlled_client.ControlledClient(name, client, controller)

def extract_config(filename):
    with open(filename) as config_file:
        json_data = json.load(config_file)
        return [json_to_controlled_client(json_cclient) for json_cclient in json_data["cclients"]]


def main():
    path_config_folder = "/home/quentin/.config/ctrl_email/config.json"
    path_home_folder = "~/.ctrl_email.json"
    if os.path.exists(path_config_folder):
        config_file_path = path_config_folder
    elif os.path.exists(path_home_folder):
        config_file_path = path_home_folder
    else:
        print("Config file must be either in {} or in {}".format(path_home_folder, path_config_folder))
        return 1

    cclients = extract_config(config_file_path)

    notify2.init("Ctrl-Email")
    notifyer = notify2.Notification(None, icon="")
    notifyer.set_urgency(notify2.URGENCY_NORMAL)
    notifyer.set_timeout(10000)

    for cclient in cclients:
        cclient.client.extract_data_for_analysis("{}.csv".format(cclient.name))

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
