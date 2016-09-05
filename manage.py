# <coding:utf-8>
# !/usr/bin/env python
import os
import sys
import opspro


def start_opspro():
    opspro.Start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visual.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    if sys.argv[1] == 'runserver':
        start_opspro()
