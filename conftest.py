import random
import time
import pytest
import faker
from collections import namedtuple


RETRIES = 3
TIMEOUT = 5
Person = namedtuple("Person", ["first_name", "last_name", "age", "email", "salary", "department"])


def get_url(driver, url):
    ERRORS = ["502 Bad Gateway"]
    for _ in range(RETRIES):
        driver.get(url)
        if ERRORS[0] in driver.title:
            print(f"retry for {url}")
            time.sleep(TIMEOUT)
        else:
            break


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    selenium.maximize_window()
    return selenium


@pytest.fixture
def table_data():
    def prepare_table_data(size):
        fake = faker.Faker()
        departments = ("Insurance", "Compliance", "Legal")
        results = []
        for _ in range(size):
            results.append(
                Person(
                    first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    age = random.randint(0, 100),
                    email = fake.email(),
                    salary = random.randint(2_500, 10_000),
                    department = random.choice(departments),
                )
            )
        return results
    return prepare_table_data