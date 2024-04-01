import os
import importlib.util
from io_unittest import scoring_qa
import argparse
from SubmissionManager import SubmissionManager
from TestManager import TestManager, TestCases, TestCase

FUNCTION_COUNT_MAX = 8

def generate_function_list(name):
    return [f"{name}{i}" for i in range(1, FUNCTION_COUNT_MAX + 1)]

submission_list = {}
function_list = [f"Exercise_{i}" for i in range(1, FUNCTION_COUNT_MAX + 1)]

# def scoring_submission(submission_name, submission_path):
#     spec = importlib.util.spec_from_file_location("module", submission_path)
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)

#     candidate_function_list = generate_function_list("Exercise_")
#     for index, exercise in enumerate(function_list):
#         try:
#             func = getattr(module, candidate_function_list[index])
#             test_case_list = load_test_case_qa(exercise)
#             if (len(test_case_list) > 0):
#                 score, failures = scoring_qa(func, test_case_list)
#                 submission_list[submission_name]["score"] += score
#                 submission_list[submission_name]["failures"][exercise] = failures
#         except ArithmeticError:
#             print(f"Function '{exercise}' not found in the module.")
#         except AttributeError as error:
#             print(error)

class CustomTestCase(TestCases):
    def __init__(self, custom_testcase: str = None) -> None:
        super().__init__(custom_testcase)

    #the TestManager will automatically pass the function from the test file to this func parameter, so just call it as you want
    #but if you use default/our test function, just define the test function, we will test it automatically
    def test_Exercise_1(self):
        return [
            TestCase([], [1, 2], isIn=["3"])
        ]

def init_argparser():
    parser = argparse.ArgumentParser(description= "Scoring command line")

    parser.add_argument("exercise_dir", default="Exercises")
    parser.add_argument("-t", "--test_cases", default="Test cases")
    parser.add_argument("-o", "--output", default="Result")

    return parser

if __name__ == "__main__":
    parser = init_argparser()
    args = parser.parse_args()
    args.exercise_dir = args.exercise_dir.strip('"')
    
    if (not os.path.exists(args.exercise_dir)):
        print(f"Not found {args.exercise_dir}")
    else:
        submission_manager = SubmissionManager(args.exercise_dir)
        # testcase = TestCaseBase()
        # submission_manager.attachTestcase(testcase)

        
        # submission_manager.runTest()
        # testcases = TestCases(args.test_cases)
        # test_result = testcases.run()
        # print(test_result)
        # unittest.main()
        

        # print("Scoring...")
        # for submission_name, submission in submission_list.items():
        #     scoring_submission(submission_name, submission["path"])
        
        # print("Saving  result...")
        # json.dump(submission_list, open("scoring table.json", "w"), indent=3)

        # print("Done!!!")
        # for submission_name, submission in submission_list.items():
        #     print(submission_name, submission)