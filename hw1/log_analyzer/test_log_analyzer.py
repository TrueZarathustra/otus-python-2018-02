#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
from log_analyzer import merge_configs, choose_log_file, parse_log, create_report, update_ts

TEST_FOLDER = "./test"
FILES_FOR_TESTS = "./test_base"


class MergeConfigTests(unittest.TestCase):

    def setUp(self):

        #  set config
        self.config = {
            "REPORT_SIZE": 1000,
            "REPORT_DIR": "./test",
            "LOG_DIR": "./test",
            "SELF_LOG_FILE": "./test/log_analyzer.log",
            "TS_FILE": "./test/log_analyzer.ts",
            "REPORT_TEMPLATE": "./test/report.html"
        }

        #  create directory if not exists
        if not os.path.exists(TEST_FOLDER):
            os.makedirs(TEST_FOLDER)

        #  copy basic files needed for tests
        src_files = os.listdir(FILES_FOR_TESTS)
        for f in src_files:
            full_file_name = os.path.join(FILES_FOR_TESTS, f)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, TEST_FOLDER)

    def test_correct_config(self):
        result = merge_configs(self.config, TEST_FOLDER + "/log_analyzer.conf")
        self.assertTrue(result is not None)

    def test_incorrect_config(self):
        result = merge_configs(self.config, TEST_FOLDER + "/log_analyzer_incorrect.conf")
        self.assertTrue(result == self.config)

    def test_empty_config(self):
        result = merge_configs(self.config, TEST_FOLDER + "/log_analyzer_empty.conf")
        self.assertTrue(result == self.config)

    def tearDown(self):
        for f in os.listdir(TEST_FOLDER):
            file_path = os.path.join(TEST_FOLDER, f)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    unittest.main()
