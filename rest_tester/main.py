import glob
import json
import os
import unittest
import sys

from rest_tester.test_info import TestInfo
from rest_tester.parameters import ParameterSet
from rest_tester.test_function import TestFunction, TestFailFunction


class TestsContainer(unittest.TestCase):
    """The test container for dynamically generated test cases."""
    longMessage = True


def identify_files_in_dir(path):
    """Identify the json files in the given directory recursively."""
    return [target for file_path in os.walk(path) for target in glob.glob(os.path.join(file_path[0], '*.json'))]


if __name__ == '__main__':
    # Read test_suites_dir from the arguments.
    try:
        script, test_suites_dir = sys.argv
    except ValueError:
        print('Please specify the test suite directory for testing.')
        raise

    for test_case_file in identify_files_in_dir(test_suites_dir):
        print('Working on %s ...' % test_case_file)
        try:
            json_file = open(test_case_file)
        except FileNotFoundError:
            test_function_name = TestFailFunction.generate_name(os.path.basename(test_case_file))
            test_function = TestFailFunction.make('Cannot find the json file.')
            setattr(TestsContainer, test_function_name, test_function)
            continue

        try:
            json_data = json.load(json_file)
        except Exception:
            test_function_name = TestFailFunction.generate_name(os.path.basename(test_case_file))
            test_function = TestFailFunction.make('Cannot parse the json file.')
            setattr(TestsContainer, test_function_name, test_function)
            continue

        try:
            url, params, timeout, test_cases = TestInfo.read(json_data)
        except KeyError as e:
            test_function_name = TestFailFunction.generate_name(os.path.basename(test_case_file))
            test_function = TestFailFunction.make('Essential test information is missing: %s' % str(e))
            setattr(TestsContainer, test_function_name, test_function)
            continue

        param_set_list = ParameterSet.generate(params)

        file_name = os.path.basename(test_case_file)
        for param_set in param_set_list:
            for test_key in test_cases.keys():
                test_function_name = TestFunction.generate_name(file_name, test_key, param_set)
                test_function = TestFunction.make(url, param_set, timeout, test_key, test_cases[test_key])
                setattr(TestsContainer, test_function_name, test_function)

                print('%s is added to the test container.' % test_function_name)

    suite = unittest.makeSuite(TestsContainer)
    unittest.TextTestRunner(verbosity=1).run(suite)
