#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}


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

if __name__ == "__main__":
    main()
