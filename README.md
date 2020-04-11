# Ctrl-Gmail
PID controlled application querying your Gmail account for new messages

## The idea

Checks periodically for new emails in your Gmail.

The period between 2 queries is regulated by a [PID Controller](https://en.wikipedia.org/wiki/PID_controller).

## Installation

### NiXOS

TODO

### Others

```bash
git clone https://github.com/GuilloteauQ/Ctrl-Gmail.git
```

## Setup

### Gmail API

To use ``Ctrl-Gmail`` you will need your credentials for your Gmail account ([see here](https://developers.google.com/gmail/api/quickstart/python)).

Clic on ``Enable the Gmail API`` and save the credentials.

### Python

TODO

## Running

```bash
python ctrl_gmail.py config.json
```

## Configuration

You can modify the configuation of the PID Controller through a configuration file

```json
# config.json
{
  "kp": 0.1,
  "ki": 0.1,
  "kd": 0.1,
  "max_value": 1000,
  "initial": 100
}
```

* ``kp``: Proportional Gain of the PID Controller (default ``0``)

* ``ki``: Integral Gain of the PID Controller (default ``0``)

* ``kd``: Derivative Gain of the PID Controller (default ``0``)

* ``max_value``: Upper bound of possible output of the controller

* ``initial``: Intial value for starting the controller
