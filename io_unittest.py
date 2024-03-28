from unittest import mock
from io import StringIO

SAMPLE_QA = {
    "questions": [],
    "answer": [],
    "optional_answer": []
}

def TestResult(result, message = ""):
    return (result, message)

@mock.patch('sys.stdout', new_callable=StringIO)
def test_qa(func, qa, mock_stdout):
    questions = [str(question) for question in qa["questions"]]
    with mock.patch('builtins.input', side_effect=questions):
        try:
            func()
            actual_answer = mock_stdout.getvalue()
            #checking required answer
            if (qa["answer"] and len(qa["answer"]) > 0):
                for answer in qa["answer"]:
                    if (str(answer) not in actual_answer):
                        return TestResult(False, "Wrong answer.")
            else:
                return TestResult(False)
            #checking optional answer
            if (qa["optional_answer"]):
                for answer in qa["optional_answer"]:
                    if (str(answer) in actual_answer):
                        return TestResult(True)
            # elif 
                    
        except Exception as error:
            return (False, f'{func} has error: {error}')
                
        return TestResult(True)

def scoring_qa(func, test_cases):
    fail_list = []
    for index, test_case in enumerate(test_cases["qa"]):
        result, message = test_qa(func, test_case)
        if not result:
            fail_list.append({f"Test case number {index}": message})

    return test_cases["score"] * (1 - (len(fail_list) / len(test_cases["qa"]))), fail_list