from concurrent.futures import as_completed, ThreadPoolExecutor


class ThreadUnsafeATM:
    def __init__(self, balance: int):
        self._balance = balance

    def add_funds(self, amount: int):
        """We are deliberately doing this in this way to expose issues in multithreading."""
        for i in range(amount):
            self._balance += 1

    @property
    def balance(self):
        return self._balance


if __name__ == '__main__':
    initial_balance = 1000

    thread_unsafe_atm = ThreadUnsafeATM(initial_balance)
    number_of_concurrent_uses = 20
    amount_to_add_per_user = 10000

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(thread_unsafe_atm.add_funds, amount_to_add_per_user)
            for i in range(number_of_concurrent_uses)
        ]

    results = as_completed(futures)

    expected_balance = initial_balance + number_of_concurrent_uses * amount_to_add_per_user
    print(f'Final balance: {thread_unsafe_atm.balance}')
    print(f'Expected balance: {expected_balance}')
    print(f'Difference: {expected_balance - thread_unsafe_atm.balance}')
    assert thread_unsafe_atm.balance == expected_balance
