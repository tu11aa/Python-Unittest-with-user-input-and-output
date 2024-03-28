import sys
import os
import importlib.util

EXIRCISE_MAX = 8

submission_list = {}
exercise_list = [f"Exercise_{i}" for i in range(1, EXIRCISE_MAX + 1)]

def load_all_submissions(submission_folder):
    for submission in os.listdir(submission_folder):
        if submission.endswith(".py"):
            submission_list[submission[:-3]] = {"path" : os.path.join(os.path.abspath(submission_folder), submission)}
            print(f"Found {submission}.")

def scoring_submission(submission_path):
    spec = importlib.util.spec_from_file_location("module", submission_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for exercise in exercise_list:
        try:
            func = getattr(module, exercise)
            func()
        except ArithmeticError:
            print(f"Function '{exercise_list[0]}' not found in the module.")

if __name__ == "__main__":
    dest_folder = os.path.abspath(sys.argv[1].strip('"'))
    
    if (not os.path.exists(dest_folder)):
        print(f"Not found {dest_folder}")
    else:
        print(f"Checking {dest_folder} ...")
        load_all_submissions(dest_folder)

        for submission in submission_list.values():
            scoring_submission(submission["path"])