# Selenium Show

## Overview

This project is designed to test various components of a web application using Python. The project is structured to test different elements such as checkboxes, forms, web tables, and widgets. It also includes configurations and URL management for testing purposes.

## File Structure

- `conftest.py`: Configuration and fixture setup for the tests.
- `test_checkbox.py`: Contains tests related to checkbox elements.
- `test_elements_other.py`: Contains tests for various other elements.
- `test_form.py`: Contains tests for form-related elements.
- `test_webtable.py`: Contains tests for web table elements.
- `test_widgets.py`: Contains tests for widget elements.
- `urls.py`: Manages the URLs used in the tests.

## Prerequisites

- Python 3.x
- `pytest`
- Any other dependencies required for the specific elements being tested.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yanazPL/selenium-show.git
    ```
2. Navigate to the project directory:
    ```sh
    cd selenium-show
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Tests

To run the tests, simply execute:
```sh
pytest --driver [Firefox|Chrome|Edge|Safari]
```

This will run all the tests in the project. You can also run specific test files by specifying their names:
```sh
pytest test_checkbox.py --driver [Firefox|Chrome|Edge|Safari]
pytest test_form.py --driver [Firefox|Chrome|Edge|Safari]
```

## Configuration

The `conftest.py` file contains configurations and fixtures used across the tests. You can modify this file to add or update fixtures as per your requirements.

## Writing Tests

To write a new test, create a new file with the prefix `test_` followed by the component you are testing. For example, to test a new widget, you could create `test_new_widget.py`.

## Example Test

Here is an example of a simple test case:

```python
def test_example():
    assert 1 + 1 == 2
```

Place your test cases within functions prefixed with `test_` to ensure that `pytest` recognizes and executes them.

## Contribution

If you wish to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Open a pull request.


