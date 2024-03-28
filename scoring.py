import sys
import os
import json
import importlib.util
from test_cases import load_test_case_qa
from io_unittest import scoring_qa

FUNCTION_COUNT_MAX = 8

submission_list = {}
function_list = [f"Exercise_{i}" for i in range(1, FUNCTION_COUNT_MAX + 1)]

def load_all_submissions(submission_folder):
    for submission in os.listdir(submission_folder):
        if submission.endswith(".py"):
            submission_list[submission[:-3]] = {
                "path" : os.path.join(os.path.abspath(submission_folder), submission),
                "failures" : {},
                "score" : 0
            }
            print(f"Found {submission}.")

def scoring_submission(submission_name, submission_path):
    spec = importlib.util.spec_from_file_location("module", submission_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for exercise in function_list:
        try:
            func = getattr(module, exercise)
            test_case_list = load_test_case_qa(exercise)
            if (len(test_case_list) > 0):
                score, failures = scoring_qa(func, test_case_list)
                submission_list[submission_name]["score"] += score
                submission_list[submission_name]["failures"][exercise] = failures
        except ArithmeticError:
            print(f"Function '{exercise}' not found in the module.")

def save_result():
    pass

if __name__ == "__main__":
    dest_folder = os.path.abspath(sys.argv[1].strip('"'))
    
    if (not os.path.exists(dest_folder)):
        print(f"Not found {dest_folder}")
    else:
        print(f"Loading all submissions from {dest_folder} ...")
        load_all_submissions(dest_folder)

        print("Scoring...")
        for submission_name, submission in submission_list.items():
            scoring_submission(submission_name, submission["path"])
        
        print("Saving  result...")
        json.dump(submission_list, open("scoring table.json", "w"), indent=3)

        print("Done!!!")
        for submission_name, submission in submission_list.items():
            print(submission_name, submission)