import PS0 as PS0

# Quiz 1 Tests
quiz1Tests = [
    {
        'testCaseName': 'case1',
        'functions' : ['getBalance', 'deposit', 'getBalance', 'deposit', 'getBalance', 'withdraw', 'getBalance', 'deposit', 'getBalance'],
        'arguments' : [None, 100, None, 20, None, 50, None, 20, None],
        'assertions': [0, None, 100, None, 120, None, 70, None, 90]
    },
    {
        'testCaseName': 'case2',
        'functions' : ['getBalance', 'deposit', 'getBalance', 'withdraw', 'getBalance', 'withdraw', 'getBalance', 'deposit', 'getBalance'],
        'arguments' : [None, 500, None, 20, None, 50, None, 20, None],
        'assertions': [0, None, 500, None, 480, None, 430, None, 450]
    }

]

def quiz1_IsPassedSingleTest(testCase):
    try:
        account = PS0.Quiz1()
        method_mapping = {'getBalance': account.getBalance, 'deposit': account.deposit, 'withdraw': account.withdraw}
        for function, argument, assertion in zip(testCase['functions'], testCase['arguments'], testCase['assertions']):
            if assertion is not None:
                actual_value = method_mapping[function]()
                if  actual_value != assertion:
                    print(f"Quiz1, {testCase['testCaseName']}: Expected {assertion}, Got {actual_value}")
                    return False
            else:
                method_mapping[function](argument)
        return True
    except Exception as e:
        print(f"Quiz1, {testCase['testCaseName']}: Error e: {e}")
        return False


def testQuiz1():
    score, max_score = sum([ quiz1_IsPassedSingleTest(testCase) for testCase in quiz1Tests] ), len(quiz1Tests)
    print(f'Quiz 1: passed {score}/{max_score} test cases.')
    return score, max_score

# Quiz 2 Tests

quiz2Tests = [
    {
        'testCaseName': 'case1',
        'functions' : ['__init__', 'addCoins', 'getBalanceCents', 'getCoins', 'removeCoins', 'getCoins', 'getBalanceCents'],
        'arguments' : [{'dimes': 5}, {'dimes': 2, 'quarters': 10}, None, None, {'dimes': 2, 'quarters': 10}, None, None],
        'assertions': [None, None, 320,  {'dimes': 7, 'quarters': 10}, None, {'dimes': 5, 'quarters': 0}, 50]
    },

    {
        'testCaseName': 'case2',
        'functions' : ['__init__', 'getCoins', 'addCoins', 'getBalanceCents', 'getCoins', 'removeCoins', 'getCoins', 'getBalanceCents'],
        'arguments' : [{}, None, {'dimes': 20}, None, None, {'dimes': 5}, None, None],
        'assertions': [None, {'dimes': 0, 'quarters': 0}, None, 200,  {'dimes': 20, 'quarters': 0}, None, {'dimes': 15, 'quarters': 0}, 150]
    }
]

def quiz2_IsPassedSingleTest(testCase):
    try:
        account = PS0.Quiz2(testCase['arguments'][0])
        method_mapping = {'addCoins': account.addCoins, 'removeCoins': account.removeCoins, 'getBalanceCents': account.getBalanceCents, 'getCoins': account.getCoins}
        for function, argument, assertion in zip(testCase['functions'][1:], testCase['arguments'][1:], testCase['assertions'][1:]):
            if assertion is not None:
                actual_value = method_mapping[function]()
                if  actual_value != assertion:
                    print(f"Quiz 2, {testCase['testCaseName']}: Expected {assertion}, Got {actual_value}")
                    return False
            else:
                method_mapping[function](argument)
        return True
    except Exception as e:
        print(f"Quiz2, {testCase['testCaseName']}: Error e: {e}")
        return False

def testQuiz2():
    score, max_score = sum([ quiz2_IsPassedSingleTest(testCase) for testCase in quiz2Tests] ), len(quiz2Tests)
    print(f'Quiz 2: passed {score}/{max_score} test cases.')
    return score, max_score


# Quiz 3 Tests

quiz3Tests = [
    {
        'testCaseName': 'case1',
        'functions' : ['__init__', 'addCoins', 'getBalanceCents', 'removeCoins', 'getBalanceCents'],
        'arguments' : [{'dimes': 5}, (2, 10), None, (2, 10), None],
        'assertions': [None, None, 320, None, 50]
    },
    {
        'testCaseName': 'case2',
        'functions' : ['__init__', 'addCoins', 'getBalanceCents', 'removeCoins', 'getBalanceCents', 'addCoins', 'getBalanceCents'],
        'arguments' : [{'dimes': 5, 'quarters': 1}, (2, 10), None, (2, 10), None, (0, 5), None],
        'assertions': [None, None, 345, None, 75, None, 200]
    },
]

def quiz3_IsPassedSingleTest(testCase):
    try:
        account = PS0.Quiz3(testCase['arguments'][0])
        method_mapping = {'addCoins': account.addCoins, 'removeCoins': account.removeCoins, 'getBalanceCents': account.getBalanceCents }
        for function, argument, assertion in zip(testCase['functions'][1:], testCase['arguments'][1:], testCase['assertions'][1:]):
            if assertion is not None:
                actual_value = method_mapping[function]()
                if  actual_value != assertion:
                    print(f"Quiz 3, {testCase['testCaseName']}: Expected {assertion}, Got {actual_value}")
                    return False
            else:
                method_mapping[function](argument)
        return True
    except Exception as e:
        print(f"Quiz3, {testCase['testCaseName']}: Error e: {e}")
        return False

def testQuiz3():
    score, max_score = sum([ quiz3_IsPassedSingleTest(testCase) for testCase in quiz3Tests] ), len(quiz3Tests)
    print(f'Quiz 3: passed {score}/{max_score} test cases.')
    return score, max_score

# Quiz 4 tests:

quiz4Tests = [
    {
        'testCaseName': 'case1',
        'functions' : ['__init__', 'displayBalance'],
        'arguments' : [{ 'Alex': (5, 10), 'Bob': (0, 2) }, None],
        'assertions': [None, '(Customer: Alex, Balance: 300)(Customer: Bob, Balance: 50)']
    },
    {
        'testCaseName': 'case1',
        'functions' : ['__init__', 'displayBalance'],
        'arguments' : [{ 'Alexa': (5, 10), 'Siri': (8, 2) }, None],
        'assertions': [None, '(Customer: Alexa, Balance: 300)(Customer: Siri, Balance: 130)']
    },
]

def quiz4_IsPassedSingleTest(testCase):
    try:
        account = PS0.Quiz4(testCase['arguments'][0])
        method_mapping = {'displayBalance': account.displayBalance }
        for function, argument, assertion in zip(testCase['functions'][1:], testCase['arguments'][1:], testCase['assertions'][1:]):
            if assertion is not None:
                actual_value = method_mapping[function]()
                if  actual_value != assertion:
                    print(f"Quiz 4, {testCase['testCaseName']}: Expected {assertion}, Got {actual_value}")
                    return False
            else:
                method_mapping[function](argument)
        return True
    except Exception as e:
        print(f"Quiz4, {testCase['testCaseName']}: Error e: {e}")
        return False

def testQuiz4():
    score, max_score = sum([ quiz4_IsPassedSingleTest(testCase) for testCase in quiz4Tests] ), len(quiz4Tests)
    print(f'Quiz 4: passed {score}/{max_score} test cases.')
    return score, max_score


if __name__ == "__main__":
    score1, max_score1 = testQuiz1()
    score2, max_score2 = testQuiz2()
    score3, max_score3 = testQuiz3()
    score4, max_score4 = testQuiz4()
    total = score1 / max_score1 + score2 / max_score2 + score3 / max_score3 + score4 / max_score4
    max_total = 4
    score = int(total * 100/max_total)
    print(f'Final score: {score}')
