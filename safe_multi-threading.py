from concurrent.futures import as_completed, ThreadPoolExecutor
from threading import Lock


class ThreadSafeATM:
    """
    We use monitor pattern here - each operation is guarded by the lock.
    Note: in add_funds we wrap add operation in a lock instead of a for loop only to have more chances for the code to
    fail if we comment out the with self.__balance_lock line...
    This way we can easier prove that the lock actually protects the _balance correctly.
    """
    def __init__(self, balance: int):
        self.__balance_lock = Lock()
        self._balance = balance

    def add_funds(self, amount: int):
        """
        We are deliberately doing this in this way to expose issues in multithreading (try to comment out line 21!!!).
        """
        with self.__balance_lock:
            for i in range(amount):
                self._balance += 1

    @property
    def balance(self):
        with self.__balance_lock:
            return self._balance


if __name__ == '__main__':
    initial_balance = 1000

    thread_safe_atm = ThreadSafeATM(initial_balance)
    number_of_concurrent_uses = 20
    amount_to_add_per_user = 10000

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(thread_safe_atm.add_funds, amount_to_add_per_user)
            for i in range(number_of_concurrent_uses)
        ]

    results = as_completed(futures)

    expected_balance = initial_balance + number_of_concurrent_uses * amount_to_add_per_user
    print(f'Final balance: {thread_safe_atm.balance}')
    print(f'Expected balance: {expected_balance}')
    print(f'Difference: {expected_balance - thread_safe_atm.balance}')
    assert thread_safe_atm.balance == expected_balance
