# Log Analyzer
# (Otus-Python-2018-02 Homework)

## Description

Utility for analyzing Nginx log. Helps to find the most slow-loading URLs


## Usage
Run from a command line. --config is an option (point to a configuration file).  
Example:
```
log_anlyzer.py --config "/tmp/config.file"
```

## Configuration file

File format is json. Example:
```
{
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TS_FILE": "./tmp/log_analyzer.ts"
}
```

### Configuration file details

Configuration file can contain following options:
```
REPORT_SIZE - Number of the most slow URLs in the report
REPORT_DIR - output directory for the report 
LOG_DIR - directory for the logs to be analyzed. Log filenames are expected  as "nginx-access-ui.log-YYYYMMDD"
SELF_LOG_FILE - path to the log_analyzer's self log file
TS_FILE - path to the timestamp file (last succesful run)
REPORT_TEMPLATE - path to HTML-template of the report
```

Default values:
"REPORT_SIZE": 1000
"REPORT_DIR": "./reports"
"LOG_DIR": "./log"
"SELF_LOG_FILE": "./tmp/log_analyzer.log"
"TS_FILE": "./tmp/log_analyzer.ts"
"REPORT_TEMPLATE": "./reports/report.html"
```

## Unit-test

To run unit-test use:
```
test_log_anlyzer.py
```