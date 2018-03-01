#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import argparse
from datetime import datetime
import json
import os
import re
import sys

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TS_FILE": "./tmp/log_analyzer.ts"
}


def merge_configs(config, config_file):

    try:
        if os.stat(config_file).st_size == 0:
            return config
        with open(config_file) as f:
            conf_from_file = json.load(f) # TODO: if file is empty continue to work
    except:
        print("Error reading config file")  # TODO: make logging instead all print statements
        sys.exit(1)

    for key in conf_from_file.keys():
        config[key] = conf_from_file[key]

    return config


def choose_log_file(log_dir, ts_file):
    LOG_SAMPLE = "nginx-access-ui.log-"
    comp = re.compile(r'%s[0-9]{8}' % LOG_SAMPLE)
    max_date = datetime.strptime("19010101", "%Y%m%d")

    for f in os.listdir(log_dir):
        tmp = comp.match(f)
        if tmp is not None:
            date = datetime.strptime(tmp.string[len(LOG_SAMPLE):len(LOG_SAMPLE)+8], "%Y%m%d")
            max_date = date if date > max_date else max_date

    if max_date == datetime.strptime("19010101", "%Y%m%d"):
        print("Nothing to parse: exiting")
        sys.exit(0)

    if LOG_SAMPLE + max_date.strftime("%Y%m%d") + ".gz" in os.listdir(log_dir):
        log_file = LOG_SAMPLE + max_date.strftime("%Y%m%d") + ".gz"
    else:
        log_file = LOG_SAMPLE + max_date.strftime("%Y%m%d")

    mtime = os.path.getmtime(log_dir + "/" + log_file)

    try:
        with open(ts_file) as f:
            ts = f.readline()
            ts_mtime = float(ts)
    except:
        return log_file

    if ts_mtime > mtime:
        print("Nothing to parse: exiting")
        sys.exit(0)
    else:
        return log_file


def parse_log(log_file, log_dir):
    pass


def main():
    '''
    1. Read config file
        1.1 if fail - exit with error
        1.2 else - merge with config var
    2. Get log file
        2.1 if fail - exit
        2.2 else - pass to parser
    3. Parse file, count statistics, including error stat
        3.1 if error level > acceptable - exit
    4. Generate html report
    5. Update/create ts-file
    '''
    parser = argparse.ArgumentParser(description='Log Analyzer')
    parser.add_argument('-c', '--config',
                        dest='config',
                        default="./config/log_analyzer.conf",
                        required=False,
                        help='Path to config file')
    args = parser.parse_args()

    conf = merge_configs(config, args.config)

    log_file = choose_log_file(conf["LOG_DIR"], conf["TS_FILE"])

    statistics = parse_log(log_file, conf["LOG_DIR"])



if __name__ == "__main__":
    main()
