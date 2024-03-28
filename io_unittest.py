from unittest import mock
from io import StringIO

SAMPLE_QA = {
    "questions": [],
    "answer": [],
    "optional_answer": []
}

def Result(result, message = ""):
    return (result, message)

@mock.patch('sys.stdout', new_callable=StringIO)
def test(func, qa, mock_stdout):
    questions = [str(question) for question in qa["questions"]]
    with mock.patch('builtins.input', side_effect=questions):
        try:
            func()
            actual_answer = mock_stdout.getvalue()
            #checking required answer
            if (qa["answer"] and len(qa["answer"]) > 0):
                for answer in qa["answer"]:
                    if (str(answer) not in actual_answer):
                        return Result(False)
            else:
                return Result(False)
            #checking optional answer
            if (qa["optional_answer"]):
                for answer in qa["optional_answer"]:
                    if (str(answer) in actual_answer):
                        return Result(True)
            # elif 
                    
        except Exception as error:
            return (False, f'{func} has error: {error}')
                
        return Result(True)

def scoring(func, qas):
    score = 0
    for qa in qas:
        if test(func, qa):
            score += 1

    return (score * 10) / score


def sum():
    a = int(input('Input first number: '))
    b = int(input('Input first number: '))
    print(f"{a} + {b} = {a + b}")
    c = int(input('Input first number: '))
    print(f"{a} + {b} = {a + b}")

qa = {
    "questions": [1, 2, 3],
    "answer": [3],
    "optional_answer": []
}

result, message = test(sum, qa)
print(result)
# sum()