import json
import os

__TESTCASE_EXTENSION = ".json"

def load_test_case_lists():
    test_dir = os.path.join(os.path.abspath(os.path.curdir), "test cases")
    if (not os.path.exists(test_dir)):
        print("Test folder not found!!!")
    
    test_case_lists = {}
    for test_case_file in os.listdir(test_dir):
        with open(os.path.join(test_dir, test_case_file), "r") as f:
            test_case_lists[test_case_file[:-5]] = json.load(f)

    return test_case_lists

def load_test_case_qa(test_case_file):
    test_dir = os.path.join(os.path.abspath(os.path.curdir), "test cases")
    if (not os.path.exists(test_dir)):
        print("Test folder not found!!!")

    try:
        with open(os.path.join(test_dir, test_case_file + __TESTCASE_EXTENSION), "r") as f:
            return json.load(f)
    except FileNotFoundError as error:
        print(f"Can not load testcase {test_case_file} because of this error:\n{error}")
        return {}