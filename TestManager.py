import importlib.util
import sys
from unittest import mock
from io import StringIO

class TestCase:
    def __init__(self, args: list, inputs: list, isEqual = None, isTrue: bool = None, isIn: list = None) -> None:
        self.args = args
        self.inputs = inputs
        self.isEqual = isEqual
        self.isTrue = isTrue
        self.isIn = isIn

class TestCases:
    """
    Just define your custom testcase in a function with "test_" prefix\n
    We will automatically test the function with the same name (removed test_ prefix) as the function defined in this testcases\n
    Ex:\n
    def test_Exercise_1(self):
        return [
            TestCase([], [1, 2], isIn=["3"])
        ]
    will test function Exercise_1 with no args, 2 inputs and check if the result contain isIn
    """
    def __init__(self) -> None:
        if (self.__class__.__name__ == "TestCases"):
            raise Exception("This is abstract class")

    def runTest(self, function_to_test, test_function):
        print(f"\nTesting {function_to_test.__name__} ...")
        results = TestResult(function_to_test.__name__)
        try:
            testcases = getattr(self, f"test_{function_to_test.__name__}")()
            print("Test case: ", len(testcases))
            for testcase in testcases:
                results.addResult(test_function(function_to_test, testcase))
        except AttributeError:
            results.addResult(Result(False, f"No test case for function {function_to_test.__name__}"))
        return results
    
class Result:
    def __init__(self, status: bool = True, message: str = "") -> None:
        self.status = status
        if status:
            self.message = "Pass" + (f": {message}" if len(message) > 0 else "")
        else:
            self.message = "Fail: " + message

class TestResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.results = []
        self.success = 0
        self.fail = 0

    def addResult(self, result: Result):
        self.results.append(result.__dict__)
        if result.status:
            self.success += 1
        else:
            self.fail += 1    

class TestManager:
    def __init__(self, testcases: TestCases) -> None:
        self.testcases = testcases

    def _setUp(self, module_path) -> None:
        spec = importlib.util.spec_from_file_location("custom_module", module_path)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["custom_module"] = self.module
        spec.loader.exec_module(self.module)

    @classmethod
    @mock.patch('sys.stdout', new_callable=StringIO)
    def test(cls, function_to_test, testcase: TestCase, mock_stdout):
        questions = [str(question) for question in testcase.inputs]
        with mock.patch('builtins.input', side_effect=questions):
            try:
                function_to_test(*testcase.args)
                actual_answer = mock_stdout.getvalue()
                #checking required answer
                if testcase.isTrue is None and testcase.isEqual is None and testcase.isIn is None:
                    return Result(True, "Warning: Empty testcase")

                if (testcase.isTrue):
                    pass

                if (testcase.isEqual):
                    if (str(answer) != actual_answer):
                        return Result(False, f"{answer} is not equal to {actual_answer}")

                if (testcase.isIn):
                    for answer in testcase.isIn:
                        if (str(answer) not in actual_answer):
                            return Result(False, f"Not found {answer} in {actual_answer}")
                        
            except Exception as error:
                return Result(False, f'{function_to_test} has error: {error}')
 
            return Result(True)

    def runTest(self, test_path: str):
        self._setUp(test_path)

        functions_to_test =  [function for function in self.module.__dir__() if not function.startswith("__")]
        
        results = []
        for function in functions_to_test:
            results.append(self.testcases.runTest(getattr(self.module, function), TestManager.test).__dict__)

        self._tearDown()
        return results

    def runCustomTest(self, test_path: str, custom_function):
        self._setUp(test_path)

        functions_to_test =  [function for function in self.module.__dir__() if not function.startswith("__")]
        
        for function in functions_to_test:
            result = self.testcases.runTest(getattr(self.module, function), custom_function)

        self._tearDown()
        return result
    
    def _tearDown(self) -> None:
        del sys.modules["custom_module"]
        self.module = None