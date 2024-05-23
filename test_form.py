import os
import urls
from textwrap import dedent
from conftest import get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


def test_practice_form(selenium):
    get_url(selenium, urls.FORMS_PRACTICE_FORM)
    name = selenium.find_element(By.ID, "firstName")
    lastname = selenium.find_element(By.ID, "lastName")
    selenium.implicitly_wait(3)
    name.send_keys("Yan")
    lastname.send_keys("Yolo")

    email = selenium.find_element(By.ID, "userEmail")
    email.send_keys("yanyol@y.net")

    male = selenium.find_element(By.XPATH, '//label[@for="gender-radio-1"]')
    male.click()

    number = selenium.find_element(By.ID, "userNumber")
    number.send_keys("6" * 10)

    datepicker_wrapper = selenium.find_element(
        By.CLASS_NAME, "react-datepicker-wrapper"
    )
    datepicker_wrapper.click()

    WebDriverWait(selenium, 30).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select"))
    )

    month_select_el = selenium.find_element(
        By.CLASS_NAME, "react-datepicker__month-select"
    )
    month_select = Select(month_select_el)
    month_select.select_by_value("6")
    year_select_el = selenium.find_element(
        By.CLASS_NAME, "react-datepicker__year-select"
    )
    year_select = Select(year_select_el)
    year_select.select_by_value("1995")
    day = selenium.find_element(By.CLASS_NAME, "react-datepicker__day--028")
    day.click()

    auto_complete = selenium.find_element(
        By.CLASS_NAME, "subjects-auto-complete__control"
    )
    action_chain = ActionChains(selenium)
    auto_complete.click()
    action_chain.send_keys("Computer Science")
    action_chain.perform()
    option_cs = selenium.find_element(By.ID, "react-select-2-option-0")
    option_cs.click()
    auto_complete.click()
    ActionChains(selenium).send_keys("Arts").perform()
    option_arts = selenium.find_element(By.ID, "react-select-2-option-0")
    option_arts.click()

    hobby_sports = selenium.find_element(By.XPATH, '//label[@for="hobbies-checkbox-1"]')
    hobby_sports.click()
    hobby_reading = selenium.find_element(
        By.XPATH, '//label[@for="hobbies-checkbox-2"]'
    )
    hobby_reading.click()
    hobby_music = selenium.find_element(By.XPATH, '//label[@for="hobbies-checkbox-3"]')
    hobby_music.click()

    file_el = selenium.find_element(By.ID, "uploadPicture")
    file_el.send_keys(os.getcwd() + "/img/image.jpeg")

    address_content = """\
    House No. 123, Sector 14
    Karnal, Haryana 132001
    India"""
    address_content = dedent(address_content)
    address_el = selenium.find_element(By.ID, "currentAddress")
    address_el.send_keys(address_content)

    state_el = selenium.find_element(By.ID, "state")
    selenium.execute_script("arguments[0].scrollIntoView();", state_el)
    state_el.click()
    state_option = selenium.find_element(By.XPATH, '//div[text()="Haryana"]')
    state_option.click()
    city_el = selenium.find_element(By.ID, "city")
    city_el.click()
    city_option = selenium.find_element(By.XPATH, '//div[text()="Karnal"]')
    city_option.click()
    submit = selenium.find_element(By.ID, "submit")
    submit.click()

    output_table_datas = selenium.find_elements(By.CSS_SELECTOR, "td:last-child")
    assert output_table_datas[0].text == "Yan Yolo"
    assert output_table_datas[1].text == "yanyol@y.net"
    assert output_table_datas[2].text == "Male"
    assert output_table_datas[3].text == "6666666666"
    assert output_table_datas[4].text == "28 June,1995"
    assert output_table_datas[5].text == "Computer Science, Arts"
    assert output_table_datas[6].text == "Sports, Reading, Music"
    assert output_table_datas[7].text == "image.jpeg"
    assert output_table_datas[8].text == address_content.replace("\n", " ")
    assert output_table_datas[9].text == "Haryana Karnal"
