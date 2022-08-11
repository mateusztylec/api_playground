from app.calculations import add, multiply, divide, substract, BankAccount, InsufficientFound
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount(0)


@pytest.fixture
def bank_account():
    print("\ninitialize bank account")
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5), (1, 2, 3), (4, 5, 9)])
def test_add(num1, num2, expected):
    print("testing add function")
    print(__name__)
    assert add(num1, num2) == expected


def test_subtract():
    assert substract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divide():
    assert divide(10, 2) == 5


def test_bank_set_inicial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdrow(bank_account):
    bank_account.withdrow(10)
    assert bank_account.balance == 40


def test_bank_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 60


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [(200, 100, 100), (50, 10, 40), (1200, 200, 1000)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdrow(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_amount(bank_account):
    with pytest.raises(InsufficientFound):
        bank_account.withdrow(200)
