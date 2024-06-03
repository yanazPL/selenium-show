from selenium.webdriver.support.select import Select
import pytest
import urls
from conftest import get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def wait_until_percent_is(driver, x):
    WebDriverWait(driver, timeout=100, poll_frequency=0.1).until(
        EC.text_to_be_present_in_element((By.ID, "progressBar"), text_=f"{x}%")
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


def test_accordian(selenium):
    get_url(selenium, urls.WIDGETS_ACCORDIAN)
    section_1_heading = selenium.find_element(By.ID, "section1Heading")
    section_2_heading = selenium.find_element(By.ID, "section2Heading")
    section_3_heading = selenium.find_element(By.ID, "section3Heading")
    section_1_content = selenium.find_element(By.ID, "section1Content")
    section_2_content = selenium.find_element(By.ID, "section2Content")
    section_3_content = selenium.find_element(By.ID, "section3Content")
    if section_1_content.is_displayed():
        section_1_heading.click()
    if section_2_content.is_displayed():
        section_2_heading.click()
    if section_3_content.is_displayed():
        section_3_heading.click()
    # Now accordian is fully collapsed
    section_1_heading.click()
    assert section_1_content.is_displayed()
    section_1_heading.click()

    WebDriverWait(selenium, 1).until_not(EC.visibility_of(section_1_content))
    assert not section_1_content.is_displayed()

    section_2_heading.click()
    assert section_2_content.is_displayed()
    section_2_heading.click()
    assert not section_2_content.is_displayed()

    section_3_heading.click()
    assert section_3_content.is_displayed()
    section_3_heading.click()
    assert not section_3_content.is_displayed()


def test_auto_complete(selenium):
    get_url(selenium, urls.WIDGET_AUTO_COMPLETE)
    COLORS = [
        "Blue",
        "Black",
        "Green",
        "Indigo",
        "Magenta",
        "Purple",
        "Red",
        "Voilet",
        "White",
        "Yellow",
    ]
    auto_complete_multiple, auto_complete_single = selenium.find_elements(
        By.CLASS_NAME, "auto-complete__control"
    )
    auto_complete_multiple.click()
    action_chains = ActionChains(selenium)
    for color in COLORS:
        # Sending first three letters
        action_chains.send_keys(color[:3])
        action_chains.perform()
        WebDriverWait(selenium, 0.05).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "auto-complete__menu"))
        )
        action_chains.send_keys(Keys.ENTER)
        action_chains.perform()
        assert color in auto_complete_multiple.text
    for color in COLORS:
        remove_div = selenium.find_element(
            By.XPATH, f'//div[text()="{color}"]/following-sibling::div[1]'
        )
        remove_div.click()
        assert color not in auto_complete_multiple.text
    auto_complete_single.click()
    for color in COLORS:
        # sending first three letters
        action_chains.send_keys(color[:3])
        action_chains.perform()
        WebDriverWait(selenium, 0.05).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "auto-complete__menu"))
        )
        action_chains.send_keys(Keys.ENTER)
        action_chains.perform()
        assert color in auto_complete_single.text


months = [
    None,  # Placeholder for 0
    "January",  # month[1]
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def month_to_int(month: str):
    return months.index(month)


def date_split(date: str):
    month, day, year = date.split("/")
    month = months[int(month)]
    return month, day, year


def is_past(current_year, current_month, year, month):
    return (int(current_year), month_to_int(current_month)) < (
        int(year),
        month_to_int(month),
    )


def pick_date_by_next(driver, datepicker, date: str):
    month, day, year = date_split(date)
    label = datepicker.find_element(By.CLASS_NAME, "react-datepicker__current-month")
    prev = datepicker.find_element(
        By.CLASS_NAME, "react-datepicker__navigation--previous"
    )
    next = datepicker.find_element(By.CLASS_NAME, "react-datepicker__navigation--next")
    current_month, current_year = label.text.split()
    while True:
        current_month, current_year = label.text.split()
        if is_past(current_year, current_month, year, month):
            next.click()
        elif (year, month) == (current_year, current_month):
            break
        else:
            prev.click()
    day_button = datepicker.find_element(
        By.CSS_SELECTOR,
        f".react-datepicker__day--{'0' + day}:not(.react-datepicker__day--outside-month)",
    )
    driver.execute_script("arguments[0].click();", day_button)


def pick_time(driver, datepicker, time_):
    time_li = datepicker.find_element(
        By.XPATH,
        f'.//li[contains(@class, "react-datepicker__time-list-item") and text()="{time_}"]',
    )
    driver.execute_script("arguments[0].click();", time_li)


def pick_date_by_select(driver, datepicker, date: str):
    month, day, year = date_split(date)
    select_month_el = datepicker.find_element(
        By.CLASS_NAME, "react-datepicker__month-select"
    )
    select_month = Select(select_month_el)
    select_month.select_by_visible_text(month)
    select_year_el = datepicker.find_element(
        By.CLASS_NAME, "react-datepicker__year-select"
    )
    select_year = Select(select_year_el)
    select_year.select_by_value(year)
    day_button = datepicker.find_element(
        By.CSS_SELECTOR,
        f".react-datepicker__day--{'0' + day}:not(.react-datepicker__day--outside-month)",
    )
    driver.execute_script("arguments[0].click();", day_button)


def convert_year(year: str):
    return int("".join([char for char in year if char in "0123456789"]))


def pick_date_by_select_for_datetime(driver, datetime_picker, date: str):
    month, day, year = date_split(date)

    # Select the month
    month_container = datetime_picker.find_element(
        By.CLASS_NAME, "react-datepicker__month-dropdown-container"
    )
    month_container.click()
    month_option = month_container.find_element(
        By.XPATH,
        f'.//div[@class="react-datepicker__month-option" and text()="{month}"]',
    )
    driver.execute_script("arguments[0].click();", month_option)
    # Select the year
    year_container = datetime_picker.find_element(
        By.CLASS_NAME, "react-datepicker__year-dropdown-container"
    )
    year_container.click()
    dropdown = year_container.find_element(
        By.CLASS_NAME, "react-datepicker__year-dropdown"
    )

    # Find the navigation elements
    upcoming = dropdown.find_element(By.XPATH, "./*[1]")
    previous = dropdown.find_element(By.XPATH, "./*[last()]")
    # Find shown year boundaries
    upmost = upcoming.find_element(By.XPATH, "./following-sibling::div")
    downmost = dropdown.find_element(By.XPATH, "./div[position() = (last() - 1)]")
    upmost_year = convert_year(upmost.text)
    downmost_year = convert_year(downmost.text)

    # Scroll years
    while int(year) > upmost_year:
        driver.execute_script("arguments[0].click();", upcoming)
        upmost = upcoming.find_element(By.XPATH, "./following-sibling::div")
        upmost_year = convert_year(upmost.text)
    while int(year) < downmost_year:
        driver.execute_script("arguments[0].click();", previous)
        downmost = dropdown.find_element(By.XPATH, "./div[position() = (last() - 1)]")
        downmost_year = convert_year(downmost.text)
    driver.implicitly_wait(1)

    try:
        year_div = dropdown.find_element(By.XPATH, f'./div[text()="{year}"]')
    except NoSuchElementException:
        # Selected year has different structure - year text is nested in <span>
        #  unreachable with text(), reachable with .text
        selected_span = dropdown.find_element(
            By.CLASS_NAME, "react-datepicker__year-option--selected_year"
        )
        if year in selected_span.text:
            year_div = selected_span

    driver.execute_script("arguments[0].click();", year_div)
    day_button = datetime_picker.find_element(
        By.CSS_SELECTOR,
        f".react-datepicker__day--{'0' + day}:not(.react-datepicker__day--outside-month)",
    )
    driver.execute_script("arguments[0].click();", day_button)


@pytest.mark.parametrize(
    "pick_date, pick_date_for_datetime",
    [
        (pick_date_by_next, pick_date_by_next),
        (pick_date_by_select, pick_date_by_select_for_datetime),  # second arg tmp
    ],
)
def test_pick_date(selenium, pick_date, pick_date_for_datetime):
    get_url(selenium, urls.WIDGETS_DATE_PICKER)
    date_input = selenium.find_element(By.ID, "datePickerMonthYearInput")
    date_input.click()
    date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date(selenium, date_picker_el, "01/12/2022")
    past_date = date_input.get_attribute("value")
    date_input.click()

    date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date(selenium, date_picker_el, "11/11/2026")
    future_date = date_input.get_attribute("value")

    datetime_input = selenium.find_element(By.ID, "dateAndTimePickerInput")
    datetime_input.click()

    datetime_date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date_for_datetime(selenium, datetime_date_picker_el, "03/01/2024")
    pick_time(selenium, datetime_date_picker_el, "13:00")
    past_datetime = datetime_input.get_attribute("value")

    datetime_input.click()
    datetime_date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date_for_datetime(selenium, datetime_date_picker_el, "11/26/2025")
    pick_time(selenium, datetime_date_picker_el, "08:00")
    future_datetime = datetime_input.get_attribute("value")

    datetime_input.click()
    datetime_date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date_for_datetime(selenium, datetime_date_picker_el, "03/01/2017")
    pick_time(selenium, datetime_date_picker_el, "13:00")
    far_past_datetime = datetime_input.get_attribute("value")
    datetime_input.click()

    datetime_date_picker_el = selenium.find_element(By.CLASS_NAME, "react-datepicker")
    pick_date_for_datetime(selenium, datetime_date_picker_el, "11/26/2033")
    pick_time(selenium, datetime_date_picker_el, "08:00")
    far_future_datetime = datetime_input.get_attribute("value")

    assert past_date == "01/12/2022"
    assert future_date == "11/11/2026"
    assert past_datetime == "March 1, 2024 1:00 PM"
    assert future_datetime == "November 26, 2025 8:00 AM"
    assert far_past_datetime == "March 1, 2017 1:00 PM"
    assert far_future_datetime == "November 26, 2033 8:00 AM"
