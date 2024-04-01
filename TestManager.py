import importlib.util
import sys
from unittest import mock
from io import StringIO

class TestCase:
    def __init__(self, args: list, inputs: list, isEqual = None, isLogical: bool = None, isIn: list = None) -> None:
        self.args = args
        self.inputs = inputs
        if (isEqual):
            self.isEqual = isEqual
        if (isLogical):
            self.isTrue = isLogical
        if (isIn):
            self.isIn = isIn

class TestCases:
    def __init__(self) -> None:
        if (self.__class__.__name__ == "Super"):
            raise Exception("This is abstract class")
        self.test_functions = self.__get_test_method()

    def __get_test_method(self):
        return [getattr(self, method) for method in self.__dir__() if method.startswith("test_")]

class TestResult:
    def __init__(self, status: bool = True, message: str = "") -> None:
        self.status = "Pass" if status else "Fail"
        if not status:
            self.message = message

class TestManager:
    def __init__(self, testcase: TestCases) -> None:
        self.testcase = testcase

    def _setUp(self, module_path) -> None:
        spec = importlib.util.spec_from_file_location("custom_module", module_path)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["custom_module"] = self.module
        spec.loader.exec_module(self.module)

    @mock.patch('sys.stdout', new_callable=StringIO)
    def test_qa(self, func, qa, mock_stdout):
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

    def runTest(self, test_path: str):
        self._setUp(test_path)

        test = Test()

        self._tearDown()

    def runQATest(self, test_path: str):
        self._setUp(test_path)

        test = Test()

        self._tearDown()

    def runCustomTest(self, test_path: str, custom_function):
        self._setUp(test_path)
            
        test = Test(custom_function)

        self._tearDown()

    def _tearDown(self) -> None:
        del sys.modules["custom_module"]
        self.module = None

class Test:
    pass
