import json
import os

def load_test_case_lists():
    test_dir = os.path.join(os.path.abspath(os.path.curdir), "test cases")
    if (not os.path.exists(test_dir)):
        print("Test folder not found!!!")
    
    test_case_lists = {}
    for test_case_file in os.listdir(test_dir):
        with open(os.path.join(test_dir, test_case_file), "r") as f:
            test_case_lists[test_case_file[:-4]] = json.load(f)

    return test_case_lists

