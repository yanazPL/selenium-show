import pytest
from conftest import get_url
import urls
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture
def get_page_and_expand(selenium):
    get_url(selenium, urls.ELEMENTS_CHECK_BOX)
    expand_icon = selenium.find_element(By.CLASS_NAME, "rct-icon-expand-all")
    expand_icon.click()    

def click_checkbox(driver, *checbox_names):
    for name in checbox_names:
        checkbox = driver.find_element(By.XPATH, f'//span[@class="rct-title" and text()="{name}"]')
        driver.execute_script("arguments[0].scrollIntoView();", checkbox)
        checkbox.click()
            # checkbox.click()
  

def assert_names_in_results(driver, *names):
    for name in names:
        result_span = driver.find_element(By.XPATH, f'//span[@class="text-success" and text()="{name}"]')
        assert result_span.is_displayed()

def assert_no_results(driver):
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.ID, "result")

def assert_checkboxes_displayed(driver, *checkbox_names):
    for name in checkbox_names:
        checkbox = driver.find_element(By.XPATH, f'//span[@class="rct-title" and text()="{name}"]')
        assert checkbox.is_displayed

def test_checkbox_collapse_all(selenium):
    selenium.get(urls.ELEMENTS_CHECK_BOX)
    collapse_icon = selenium.find_element(By.CLASS_NAME, 'rct-option-collapse-all')
    collapse_icon.click()
    checkbox_titles = selenium.find_elements(By.CLASS_NAME, "rct-title")
    assert len(checkbox_titles) == 1

def test_expand_one_by_one(selenium):
    selenium.get(urls.ELEMENTS_CHECK_BOX)
    collapse_icon = selenium.find_element(By.CLASS_NAME, 'rct-option-collapse-all')
    collapse_icon.click()
    while (expand_icons := selenium.find_elements(By.CLASS_NAME, 'rct-icon-expand-close')):
        for icon in expand_icons:
            icon.click()

    assert_checkboxes_displayed(
        selenium,
        'Notes', 'Commands', 'React', 'Angular', 'Veu','Public',
        'Home', 'Desktop', 'Documents', 'WorkSpace', 'Office', 'Downloads',
        'Private', 'Classified', 'General', 'Word File.doc', 'Excel File.doc'
    )

def test_checkbox_check_all(selenium, get_page_and_expand):
    click_checkbox(
        selenium,
        'Notes', 'Commands', 'React', 'Angular', 'Veu','Public',
        'Private', 'Classified', 'General', 'Word File.doc', 'Excel File.doc'
    )
    assert_names_in_results(
        selenium,
        'notes', 'commands', 'react', 'angular', 'veu', 'public',
        'private', 'classified', 'general', 'wordFile', 'excelFile'
    )
    assert_checkboxes_displayed(
        selenium,
        'Notes', 'Commands', 'React', 'Angular', 'Veu','Public',
        'Home', 'Desktop', 'Documents', 'WorkSpace', 'Office', 'Downloads',
        'Private', 'Classified', 'General', 'Word File.doc', 'Excel File.doc'
    )

def test_checkbox_uncheck_all(selenium, get_page_and_expand):
    click_checkbox(
        selenium,
        'Notes', 'Commands', 'React', 'Angular', 'Veu','Public',
        'Private', 'Classified', 'General', 'Word File.doc', 'Excel File.doc'
    )
    click_checkbox(
        selenium,
        'Notes', 'Commands', 'React', 'Angular', 'Veu','Public',
        'Private', 'Classified', 'General', 'Word File.doc', 'Excel File.doc'
    )
    assert_no_results(selenium)


def test_checkbox_check_inner_folders(selenium, get_page_and_expand):
    """Checks all folders except for root - Home"""
    click_checkbox(selenium, 'Desktop', 'WorkSpace', 'Office', 'Downloads')
    assert_names_in_results(
        selenium,
        'notes', 'commands', 'react', 'angular', 'veu', 'public',
        'private', 'classified', 'general', 'wordFile', 'excelFile'
    )

def test_checkbox_click_desktop(selenium, get_page_and_expand):
    click_checkbox(selenium, "Desktop")
    assert_names_in_results(selenium, 'desktop', 'notes', 'commands')
