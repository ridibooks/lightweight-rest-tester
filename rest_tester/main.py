import glob
import json
import os
import unittest

from rest_tester.function import TestFunctionBuilderFactory
from rest_tester.function.fail import FailTestFunctionBuilder
from rest_tester.setting import TestSetting


def identify_files_in_dir(path):
    """Identify the json files in the given directory recursively."""
    return [target for file_path in os.walk(path) for target in glob.glob(os.path.join(file_path[0], '*.json'))]


def add_function_to_container(test_container, test_function):
    """Add test functions with their name to container"""
    setattr(test_container, test_function.name, test_function.test_function)


def generate_test_functions(test_container, test_suites_dir, options):
    for test_case_file in identify_files_in_dir(test_suites_dir):

        def add_fail_function(msg):
            file_name = os.path.basename(test_case_file)
            fail_function_builder = FailTestFunctionBuilder(msg, file_name)
            fail_function = fail_function_builder.build()
            add_function_to_container(test_container, fail_function)

        try:
            with open(test_case_file, 'r') as json_file:
                json_data = json.load(json_file)
        except BaseException as file_error:
            add_fail_function('Cannot parse the json file: %s' % str(file_error))
            continue

        try:
            setting = TestSetting(json_data, options)
        except BaseException as setting_error:
            add_fail_function(str(setting_error))
            continue

        test_function_builder = TestFunctionBuilderFactory.get_builder(setting)
        test_function_list = test_function_builder.build()
        for test_function in test_function_list:
            add_function_to_container(test_container, test_function)


def run_test_functions(test_container):
    suite = unittest.makeSuite(test_container)
    return unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
