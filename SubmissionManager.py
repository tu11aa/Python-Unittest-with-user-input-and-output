import os

class Submission:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.result = []
        self.score = 0

class SubmissionManager:
    def __init__(self, submission_dir: str) -> None:
        self.submissions = {}
        for submission_path in os.listdir(submission_dir):
            if submission_path.endswith(".py"):
                submission_name = submission_path[:-3]
                self.submissions[submission_name] = Submission(submission_name, os.path.join(os.path.abspath(submission_dir), submission_path))
                print(f"Found {submission_path}.")