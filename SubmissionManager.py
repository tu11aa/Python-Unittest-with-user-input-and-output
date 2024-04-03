import os
import json

class Submission:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.score = 0
        self.result = []

class SubmissionManager:
    def __init__(self, submission_dir: str = "Submissions") -> None:
        self.submissions = {}
        for submission_path in os.listdir(submission_dir):
            if submission_path.endswith(".py"):
                submission_name = submission_path[:-3]
                self.submissions[submission_name] = Submission(submission_name, os.path.join(os.path.abspath(submission_dir), submission_path))
                print(f"Found {submission_path}.")

    def scoring(self, test_manager):
        for submission in self.submissions.values():
            result = test_manager.runTest(submission.path)
            self.submissions[submission.name].result = result

            score = 0
            for r in result:
                score += (r["success"] * 10)/(r["success"] + r["fail"])
            self.submissions[submission.name].score = score

    def save_test_results(self, result_dir: str = "Result"):
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        summary = {}
        for submission in self.submissions.values():
            result_path = os.path.join(result_dir, submission.name + ".json")
            with open(result_path, "w") as f:
                json.dump(submission.__dict__, f, indent=3)

            summary[submission.name] = submission.score

        with open(os.path.join(result_dir, "Summary.json"), "w") as f:
            json.dump(summary, f, indent=3, sort_keys=True)