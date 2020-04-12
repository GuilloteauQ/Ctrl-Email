# Ctrl-Email
PID controlled application querying your Email accounts for new messages

## The idea

Checks periodically for new emails using IMAPS.

The period between 2 queries is regulated by a [PID Controller](https://en.wikipedia.org/wiki/PID_controller).

## Installation

### NiXOS

TODO

### Others

```bash
git clone https://github.com/GuilloteauQ/Ctrl-Email.git
```

## Running

```bash
python ctrl_email.py config.json
```

## Configuration

You can modify the configuation of the PID Controller through a configuration file

```json
# config.json

{
    "cclients":[
        {
            "name": "Perso",
            "controller": {
                "kp": 0.1,
                "ki": 0.1,
                "kd": 0.1,
                "initial": 10,
                "max_value": 3000
            },
            "client": {
                "host": "imap.gmail.com",
                "user": "name.surname@gmail.com",
                "pass": "securedpassword"
            }
        },
        {
            "name": "Work",
            "controller": {
                "kp": 0.3,
                "ki": 0.0,
                "kd": 0.1,
                "initial": 10,
                "max_value": 1800
            },
            "client": {
                "host": "imap.work.fr",
                "user": "name.surname@awesome_company.fr",
                "pass": "another_password_to_remember"
            }
        }
    ]
}
```

* ``kp``: Proportional Gain of the PID Controller

* ``ki``: Integral Gain of the PID Controller

* ``kd``: Derivative Gain of the PID Controller

* ``max_value``: Upper bound of possible output of the controller

* ``initial``: Intial value for starting the controller
