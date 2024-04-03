import os
from io_unittest import scoring_qa
import argparse
from SubmissionManager import SubmissionManager
from TestManager import TestManager, TestCases, TestCase

class CustomTestCase(TestCases):
    def __init__(self) -> None:
        super().__init__()

    def test_Exercise_1(self):
        return [TestCase([], [1, 2], isIn=["3"])]

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
        testcases = CustomTestCase()
        test_manager = TestManager(testcases)

        submission_manager = SubmissionManager(args.exercise_dir)
        submission_manager.scoring(test_manager)
        submission_manager.save_test_results()