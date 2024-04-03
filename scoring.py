import os
import argparse
from SubmissionManager import SubmissionManager
from TestManager import TestManager, TestCases, TestCase

class CustomTestCase(TestCases):
    def __init__(self) -> None:
        super().__init__()

    def test_Exercise_1(self):
        return [
            TestCase([], [1, 2], isContain=["3"])
        ]
    
    def test_Exercise_2(self):
        return [
            TestCase([], [1, 0, -1], isContain=["-1", "1"])
        ]
    
    def test_Exercise_3(self):
        return [
            TestCase([], ["anna"], isContain=["palindrome"])
        ]
    
    def test_Exercise_4(self):
        return [
            TestCase([], ["Pho", "y", "Bun"], isContain=[7400000, ])
        ]
    
    def test_Exercise_5(self):
        return [
            TestCase([], ["Vsmart", 8000000], isContain=[7400000,"Oppo 93", "Vsmart", "Vivo"])
        ]
    
    def test_Exercise_6(self):
        return [
            TestCase([], [838790], isContain=[6])
        ]
    
    def test_Exercise_7(self):
        return [
            TestCase([], [], isContain=["-1 1 5 8 30 92"])
        ]
    
    def test_Exercise_8(self):
        return [
            TestCase([], [5], isContain=["1 1 2 3 5"])
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
        testcases = CustomTestCase()
        test_manager = TestManager(testcases)

        submission_manager = SubmissionManager(args.exercise_dir)
        submission_manager.scoring(test_manager)
        submission_manager.save_test_results()