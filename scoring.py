import sys
import os
import json
import importlib.util
from test_cases import load_test_case_qa
from io_unittest import scoring_qa
import argparse

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

def init_argparser():
    parser = argparse.ArgumentParser(description= "Scoring command line")

    parser.add_argument("exercise_dir", default="Exercises")
    parser.add_argument("-t", "--test_cases", default="Test cases")
    parser.add_argument("-o", "--output", default="Result")

    return parser

if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    
    if (not os.path.exists(args.exercise_dir)):
        print(f"Not found {args.exercise_dir}")
    else:
        print(f"Loading all submissions from {args.exercise_dir} ...")
        load_all_submissions(args.exercise_dir)

        print("Scoring...")
        for submission_name, submission in submission_list.items():
            scoring_submission(submission_name, submission["path"])
        
        print("Saving  result...")
        json.dump(submission_list, open("scoring table.json", "w"), indent=3)

        print("Done!!!")
        for submission_name, submission in submission_list.items():
            print(submission_name, submission)