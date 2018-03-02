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


def parse_log(log_file, log_dir, report_size):

    def parse_line(line):

        try:
            tmp_line = line.split('] "')[1] # GET /api/v2/internal/banner/24288647/info HTTP/1.1" 200 351 "-" "-" "-" "1498697423-2539198130-4708-9752780" "89f7f1be37d" 0.072
            request_time = float(tmp_line.split('" ')[-1])
            request = tmp_line.split('" ')[0]
            url = str(request.split(' ')[1])

            return url, request_time

        except:
            return None, None

    def calc_stats(numbers):
        numbers.sort()
        count = len(numbers)
        time_sum = 0
        for n in numbers:
            time_sum += n
        time_avg = time_sum*1.0/count
        time_max = numbers[-1]
        time_med = numbers[int(count/2)]

        return count, time_sum, time_avg, time_max, time_med

    try:
        f = open(log_dir+'/'+log_file)
    except:
        print("Error opening log file")  # TODO: make logging instead all print statements
        sys.exit(1)

    ERROR_LEVEL = 0.1  # acceptable error level during log parsing
    total_requests = 0
    total_time = 0
    lines_processed = 0
    errors = 0
    raw_data = {}

    for line in f:
        url, time = parse_line(line)
        if url is None or time is None:
            errors += 1
            if lines_processed > 100 and errors*1.0/lines_processed > ERROR_LEVEL:
                print("Too much errors, during parsing log file")
                sys.exit(1)
        else:
            total_requests += 1
            total_time += time
            if url not in raw_data.keys():
                raw_data[url] = []
            raw_data[url].append(time)
    f.close()

    statistics = []
    time_sums = []

    for k in raw_data.keys():
        d = {}
        d['url'] = k
        d['count'], d['time_sum'], d['time_avg'], d['time_max'], d['time_med'] = calc_stats(raw_data[k])
        d['count_perc'] = d['count']/total_requests
        d['time_perc'] = d['time_sum']/total_requests
        time_sums.append(d['time_sum'])
        statistics.append(d)
    print(statistics[0:3])
    if len(statistics) < report_size:
        return statistics
    else:
        time_sums.sort(reverse=True)
        timesum_border = time_sums[report_size]

        result = []
        for s in statistics:
            if s['time_sum'] >= timesum_border:
                result.append(s)
        return result


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

    statistics = parse_log(log_file, conf["LOG_DIR"], conf["REPORT_SIZE"])



if __name__ == "__main__":
    main()
