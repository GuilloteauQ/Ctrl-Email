import sys
from app import pid, normal_controller
from random import randint, random, gauss
from math import log
import scipy.stats

def expo_law(l):
    y = random()
    x = -log(1 - y) / l
    return int(x)

def get_max_time(emails):
    if len(emails) > 0:
        return emails[-1]
    return 0

def simulate_normal(controller, emails, filename):
    sleep_time = controller.get()
    current_time = 0
    timestamp_last_email_received = 0
    max_time = get_max_time(emails)
    data_file = open(filename, "w")
    data_file.write("time, nb_new_emails, error, sleep_time\n")

    cumulated_error = 0
    nb_requests = 0

    while current_time < 24 * 60 * 60:
        # print("Current time: {}, sleep time: {}".format(current_time, sleep_time))
        # The controller wakes up
        current_time += sleep_time
        # We look if we have mail
        new_emails = [e_time for e_time in emails if e_time <= current_time and e_time > current_time - sleep_time]
        nb_new_emails = len(new_emails)
        nb_requests += 1
        if nb_new_emails == 0:
            # then the error is the distance between now
            # and the last email received
            error = current_time - timestamp_last_email_received
        else:
            # in this case the error is the distance between
            # now and the first new email received
            error = new_emails[0] - current_time
            timestamp_last_email_received = new_emails[-1]
        cumulated_error += error * error
        data_file.write("{}, {}, {}, {}\n".format(current_time, nb_new_emails, error, sleep_time))
        # controller.update(error)
        controller.update(current_time)
        sleep_time = controller.get()
    data_file.close()
    return (cumulated_error, nb_requests)

def simulate(controller, emails, filename):
    sleep_time = controller.get()
    current_time = 0
    timestamp_last_email_received = 0
    max_time = get_max_time(emails)
    data_file = open(filename, "w")
    data_file.write("time, nb_new_emails, error, sleep_time\n")

    cumulated_error = 0
    nb_requests = 0

    while current_time < 24 * 60 * 60:
        # print("Current time: {}, sleep time: {}".format(current_time, sleep_time))
        # The controller wakes up
        current_time += sleep_time
        # We look if we have mail
        new_emails = [e_time for e_time in emails if e_time <= current_time and e_time > current_time - sleep_time]
        nb_new_emails = len(new_emails)
        nb_requests += 1
        if nb_new_emails == 0:
            # then the error is the distance between now
            # and the last email received
            error = current_time - timestamp_last_email_received
        else:
            # in this case the error is the distance between
            # now and the first new email received
            error = new_emails[0] - current_time
            timestamp_last_email_received = new_emails[-1]
        cumulated_error += error * error
        data_file.write("{}, {}, {}, {}\n".format(current_time, nb_new_emails, error, sleep_time))
        controller.update(error)
        sleep_time = controller.get()
    data_file.close()
    return (cumulated_error, nb_requests)

def generate_emails_time(l, mu, sigma):
    exp_law_lambda = 0.2515152
    mean = 42802.32
    sd = 18138.12
    exp_law_lambda = l
    mean = mu
    sd = sigma
    nb_emails = expo_law(exp_law_lambda)
    # emails = [int(gauss(mean, sd)) for _ in range(nb_emails)]
    emails = []
    for _ in range(nb_emails):
        timestamp = -1
        while timestamp < 0:
            timestamp = int(gauss(mean, sd))
        emails.append(timestamp)
    emails.sort()

    return emails

def experiment_normal(min_value, max_value, fixed_values, data_file, l, mu, sigma):
    emails = generate_emails_time(l, mu, sigma)
    # ctrl = pid.PID(kp = kp, ki = ki, kd = kd, variable = min_value, min_value = min_value, max_value = max_value)
    ctrl = normal_controller.NormalController(mean = mu, sd = sigma, min_value = min_value, max_value = max_value, variable = 1)

    data_file.write("{}, {}".format(min_value, max_value))

    (error_ctrl, nb_requests_ctrl) = simulate_normal(ctrl, emails, "/dev/null")
    data_file.write(", {}, {}".format(error_ctrl, nb_requests_ctrl))
    for fixed_value in fixed_values:
        fixed = pid.PID(variable = fixed_value, min_value = fixed_value, max_value = fixed_value)
        (error, nb_requests) = simulate(fixed, emails, "/dev/null")
        data_file.write(", {}, {}".format(error, nb_requests))
    data_file.write("\n")

def experiment(kp, ki, kd, min_value, max_value, fixed_values, data_file, l, mu, sigma):
    emails = generate_emails_time(l, mu, sigma)
    ctrl = pid.PID(kp = kp, ki = ki, kd = kd, variable = min_value, min_value = min_value, max_value = max_value)

    data_file.write("{}, {}, {}, {}, {}".format(kp, ki, kd, min_value, max_value))

    (error_ctrl, nb_requests_ctrl) = simulate(ctrl, emails, "/dev/null")
    data_file.write(", {}, {}".format(error_ctrl, nb_requests_ctrl))

    for fixed_value in fixed_values:
        fixed = pid.PID(variable = fixed_value, min_value = fixed_value, max_value = fixed_value)
        (error, nb_requests) = simulate(fixed, emails, "/dev/null")
        data_file.write(", {}, {}".format(error, nb_requests))

    data_file.write("\n")

def all_kp_ki_kd_couples(start, end, inc, iterations, min_value, max_value, fixed_values, data_file, l, mu, sigma):
    for kp in range(start, end):
        for ki in range(start, end):
            for kd in range(start, end):
                for i in range(iterations):
                    experiment(kp*inc, ki*inc, kd*inc, min_value, max_value, fixed_values, data_file, l, mu, sigma)

def single_kp_ki_kd_couple(kp, ki, kd, min_value, max_value, iterations, fixed_values, data_file, l, mu, sigma):
    for i in range(iterations):
        experiment(kp, ki, kd, min_value, max_value, fixed_values, data_file, l, mu, sigma)

def single_normal(min_value, max_value, iterations, fixed_values, data_file, l, mu, sigma):
    for i in range(iterations):
        experiment_normal(min_value, max_value, fixed_values, data_file, l, mu, sigma)

def main():
    args = sys.argv
    expe_type = args[1]
    l = float(args[2])
    mu = float(args[3])
    sigma = float(args[4])
    k_opti = int(args[5])
    iterations = int(args[6])
    min_value = float(args[7])
    max_value = float(args[8])
    filename = args[9]

    data_file = open(filename, "w")

    if expe_type == "all_pid":
        start = int(args[10])
        end = int(args[11])
        inc = float(args[12])
        all_kp_ki_kd_couples(start, end, inc, iterations, min_value, max_value, [k_opti, 10*60, 30*60], data_file, l, mu, sigma)
    elif expe_type == "single_pid":
        kp = float(args[10])
        ki = float(args[11])
        kd = float(args[12])
        single_kp_ki_kd_couple(kp, ki, kd, min_value, max_value, iterations, [k_opti, 10*60, 30*60], data_file, l, mu, sigma)
    elif expe_type == "normal":
        single_normal(min_value, max_value, iterations, [k_opti, 10*60, 30*60], data_file, l, mu, sigma)
    else:
        print("Unknown experiment !")




    # l = 0.3037975
    # mu = 42802.3173382
    # sigma = 18138.1238776
    # k_opti = 43200#58904#10034
    # # filename = "values_of_k.csv"
    # filename = "data_experiment.csv"

    # max_value = 12 * 60 * 60 # seconds
    # min_value = 20466 #60 * 60 # seconds

    # fixed_values = [k_opti]

    # # fixed_values = [60 * 10 * i for i in range(1, 24*60*6)]

    # iterations = 1000
    # data_file = open(filename, "w")

    # start = 0
    # inc = 0.1
    # end = int(2 / inc)

    # for i in range(iterations):
    #     print("{}%".format(i * 100 / iterations))
    #     emails = generate_emails_time(l, mu, sigma)
    #     for fixed_value in fixed_values:
    #         fixed = pid.PID(variable = fixed_value, min_value = fixed_value, max_value = fixed_value)
    #         (error, nb_requests) = simulate(fixed, emails, "/dev/null")
    #         data_file.write("{}, {}, {}, {}\n".format(i, fixed_value, error, nb_requests))


    data_file.close()

    return 0

if __name__ == "__main__":
    main()
