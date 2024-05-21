import urls
from conftest import get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_until_percent_is(driver, x):
    WebDriverWait(driver, timeout=100, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element(
            (By.ID, "progressBar"),
            text_=f"{x}%"
        )
    )
def test_progress_bar(selenium):
    get_url(selenium, urls.WIDGETS_PROGRESS_BAR)
    start_stop_button = selenium.find_element(By.ID, "startStopButton")
    progress_bar = selenium.find_element(By.ID, "progressBar")
    assert start_stop_button.text == "Start"
    assert not progress_bar.text
    start_stop_button.click()
    assert start_stop_button.text == "Stop"
    wait_until_percent_is(selenium, 45)
    start_stop_button.click()
    assert start_stop_button.text == "Start"
    start_stop_button.click()
    assert start_stop_button.text == "Stop"
    wait_until_percent_is(selenium, 70)
    start_stop_button.click()
    assert start_stop_button.text == "Start"
    start_stop_button.click()
    assert start_stop_button.text == "Stop"
    wait_until_percent_is(selenium, 100)

    reset_button = selenium.find_element(By.ID, "resetButton")
    assert reset_button.is_displayed()
    assert reset_button.text == "Reset"
    reset_button.click()
    start_stop_button = selenium.find_element(By.ID, "startStopButton")
    assert start_stop_button.text == "Start"