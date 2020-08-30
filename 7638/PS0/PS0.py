from typing import Dict, Tuple

class Quiz1:
    def __init__(self):
        '''
        Initialize the account balance to zero.
        '''


    def deposit(self, amount: int):
        '''
        :param amount: the amount to be added to the existing balance
        :return: None
        '''


    def withdraw(self, amount: int):
        '''

        :param amount: the amount to be removed from the existing balance
        :return: None
        '''


    def getBalance(self) -> int:
        '''
        :return: the balance
        '''



class Quiz2:
    def __init__(self, dimes_and_quarters: Dict[str, int] = None):
        '''
        Initialize the number of dimes and quarters to the provided numbers. A dime is equal to 10-cents, i.e., $ 0.10, whereas a quarter is equal 25-cents, i.e., $ 0.25.
        :param dimes_and_quarters: a optional dictionary containing the initial number of dimes and quarters, with the keys 'dimes' and/or 'quarters', eg: {'dimes': 5, 'quarters': 10}.
            Note that the input parameter dimes_and_quarters can contain zero, one or two keys from 'dimes' and 'quarters'.
            If a key is not provided in the input parameter dimes_and_quarters, initialize its value to zero.

            Example value: dimes_and_quarters = {'dimes': 5, 'quarters': 10} means that we are starting with 5 dimes and 10 quarters.
            Another example value: dimes_and_quarters = {'quarters': 10} means that we are starting with no dimes and 10 quarters.
            Another example value: dimes_and_quarters = {} or dimes_and_quarters = None means that we are starting with 0 dimes and 0 quarters.
        '''


    def addCoins(self, dimes_and_quarters: Dict[str, int]) -> None:
        '''
        :param dimes_and_quarters: a dictionary containing the number of dimes and quarters to be added, with the keys 'dimes' and/or 'quarters', eg: {'dimes': 5, 'quarters': 10}.
                Note that the input parameter dimes_and_quarters can contain zero, one or two keys from 'dimes' and 'quarters'.
                If a key is not provided in the input parameter dimes_and_quarters, that means the coins of that type are not added, i.e., consider the number of that type of coins to be added as zero.

                Example value: dimes_and_quarters = {'dimes': 5, 'quarters': 10} means that we are adding with 5 dimes and 10 quarters.
                Another example value: dimes_and_quarters = {'quarters': 10} means that we are adding 0 dimes and 10 quarters.
                Another example value: dimes_and_quarters = {} means that we are not adding any dimes or quarters.
        :return: None
        '''


    def removeCoins(self, dimes_and_quarters: Dict[str, int]) -> None:
        '''

        :param dimes_and_quarters: a dictionary containing the number of dimes and quarters to be removed, with the keys 'dimes' and/or 'quarters', eg: {'dimes': 5, 'quarters': 10}.
                Note that the input parameter dimes_and_quarters can contain zero, one or two keys from 'dimes' and 'quarters'.
                If a key is not provided in the input parameter dimes_and_quarters, that means the coins of that type are not removed, i.e., consider the number of that type of coins to be removed as zero.

                Example value: dimes_and_quarters = {'dimes': 5, 'quarters': 10} means that we are removing with 5 dimes and 10 quarters.
                Another example value: dimes_and_quarters = {'quarters': 10} means that we are removing 0 dimes and 10 quarters.
                Another example value: dimes_and_quarters = {} means that we are not removing any dimes or quarters.
        :return: None
        '''


    def getCoins(self) -> Dict[str, int]:
        '''
        :return: dimes and quarters collected till now in a dictionary of the form eg: {'dimes': 5, 'quarters': 10}.
                Note that the output dictionary needs to have both the keys. If suppose the quarters are zero and dimes are 2, the return value should be {'dimes': 2, 'quarters': 0}.
        '''


    def getBalanceCents(self) -> int:
        '''
        :return: the balance amount (in cents), taking into account the value of each type of coin.
                Eg: if we have 5 dimes and 2 quarters in the balance, then the return value should be 5 * 10 + 2 * 25 = 100.
        '''



class Quiz3:
    def __init__(self, dimes_and_quarters: Dict[str, int] = None):
        '''
        Initialize the number of dimes and quarters to the provided numbers. A dime is equal to 10-cents, i.e., $ 0.10, whereas a quarter is equal 25-cents, i.e., $ 0.25.
        :param dimes_and_quarters: a optional dictionary containing the initial number of dimes and quarters, with the keys 'dimes' and/or 'quarters', eg: {'dimes': 5, 'quarters': 10}.
            Note that the input parameter dimes_and_quarters can contain zero, one or two keys from 'dimes' and 'quarters'.
            If a key is not provided in the input parameter dimes_and_quarters, initialize its value to zero.

            Example value: dimes_and_quarters = {'dimes': 5, 'quarters': 10} means that we are starting with 5 dimes and 10 quarters.
            Another example value: dimes_and_quarters = {'quarters': 10} means that we are starting with no dimes and 10 quarters.
            Another example value: dimes_and_quarters = {} or dimes_and_quarters = None means that we are starting with 0 dimes and 0 quarters.
        '''


    def addCoins(self, dimes_and_quarters: Tuple[int, int]) -> None:
        '''
        :param dimes_and_quarters: a tuple of the number of dimes and quarters to be added to the existing list of coins.
                This will always be a tuple of exactly two numbers, (dimes and quarters respectively).
                Example value: dimes_and_quarters = (5, 6) means that there are 5 dimes and 6 quarters to be added.
                Another Example value: dimes_and_quarters = (5, 0) means that there are 5 dimes and no quarters to be added.
        :return: None
        '''


    def removeCoins(self, dimes_and_quarters: Tuple[int, int]) -> None:
        '''

        :param dimes_and_quarters: a tuple of the number of dimes and quarters to be removed from the existing list of coins.
                This will always be a tuple of exactly two numbers, (dimes and quarters respectively).
                Example value: dimes_and_quarters = (5, 6) means that there are 5 dimes and 6 quarters to be removed.
                Another Example value: dimes_and_quarters = (0, 5) means that there are no dimes and 5 quarters to be removed.
        :return: None
        '''


    def getBalanceCents(self) -> int:
        '''
        :return: the balance amount (in cents), taking into account the value of each type of coin.
                Eg: if we have 5 dimes and 2 quarters in the balance, then the return value should be 5 * 10 + 2 * 25 = 100.
        '''



class Quiz4:
    # Identify and fix the errors
    def __init__(self, accounts: Dict[str, Tuple[int, int]]):
        '''
        :param accounts: contains accounts of multiple people of the form {'CustomerName': [dimes, quarters]} . Eg value: { 'Alex': (5, 10), 'Bob': (0, 2) }
        '''
        self.accounts = accounts

    def displayBalance(self) -> str:
        '''
        You have to make a minor change to get rid of the error.
        :return: balance string: Expected output example: (Customer: Alex, Balance: 300)(Customer: Bob, Balance: 50)
        '''
        output = ''
        for customer_name, account_info in self.accounts.items():
            customer_name, dimes, quarters = account_info
            balance = dimes * 10 + quarters * 25
            output = output + f'(Customer: {customer_name}, Balance: {balance})'
        return output

