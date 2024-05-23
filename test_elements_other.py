import os
import time
import pytest
import requests
import urls
from conftest import get_url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_box_positive(selenium):
    get_url(selenium, urls.ELEMENTS_TEXT_BOX)
    WebDriverWait(selenium, 15).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, '//form[@id="userForm"]/div[not(@id="output")]')
        )
    )
    full_name_el = selenium.find_element(By.ID, "userName")
    current_address_el = selenium.find_element(By.ID, "currentAddress")
    permanent_address_el = selenium.find_element(By.ID, "permanentAddress")
    user_email_el = selenium.find_element(By.ID, "userEmail")
    current_address = "Suite 507 9326 Konopelski Ville, Lake Landon, MN 73686-1009"
    permanent_address = "34283 Schuppe Gateway, Schummmouth, LA 08800"

    full_name_el.send_keys("Han Solo")
    user_email_el.send_keys("han.solo@galaxy.net")
    current_address_el.send_keys(current_address)
    permanent_address_el.send_keys(permanent_address)
    submit_button = selenium.find_element(By.ID, "submit")

    selenium.execute_script("arguments[0].click();", submit_button)
    name_output = selenium.find_element(By.ID, "name")
    email_output = selenium.find_element(By.ID, "email")
    current_address_output = selenium.find_element(
        By.CSS_SELECTOR, 'p[id="currentAddress"]'
    )
    permanent_address_output = selenium.find_element(
        By.CSS_SELECTOR, 'p[id="permanentAddress"]'
    )

    assert name_output.is_displayed()
    assert "Han Solo" in name_output.get_attribute("innerHTML")
    assert email_output.is_displayed()
    assert "han.solo@galaxy.net" in email_output.get_attribute("innerHTML")
    assert current_address_output.is_displayed()
    assert current_address in current_address_output.get_attribute("innerHTML")
    assert permanent_address_output.is_displayed()
    assert permanent_address in permanent_address_output.get_attribute("innerHTML")


def test_box_no_data_submit(selenium):
    get_url(selenium, urls.ELEMENTS_TEXT_BOX)
    submit_button = selenium.find_element(By.XPATH, "//button[@id='submit']")
    selenium.execute_script("arguments[0].click();", submit_button)
    output = selenium.find_element(By.ID, "output")
    output_div = output.find_element(By.TAG_NAME, "div")
    assert output_div.get_attribute("innerHTML") == ""


def test_box_wrong_mail_submit(selenium):
    get_url(selenium, urls.ELEMENTS_TEXT_BOX)
    submit_button = selenium.find_element(By.XPATH, "//button[@id='submit']")
    user_email_el = selenium.find_element(By.ID, "userEmail")
    user_email_el.send_keys("nonsensical string")
    selenium.execute_script("arguments[0].click();", submit_button)
    output = selenium.find_element(By.ID, "output")
    output_div = output.find_element(By.TAG_NAME, "div")
    assert "field-error" in user_email_el.get_attribute("class")
    assert output_div.get_attribute("innerHTML") == ""


@pytest.mark.parametrize("by, locator", [["link text", "Home"], ["id", "dynamicLink"]])
def test_elements_new_card_link(selenium, by, locator):
    get_url(selenium, urls.ELEMENTS_LINKS)
    link = selenium.find_element(by, locator)
    current_handles = selenium.window_handles
    link.click()

    WebDriverWait(selenium, 30).until(EC.new_window_is_opened(current_handles))
    new_window_handle = [
        handle for handle in selenium.window_handles if handle not in current_handles
    ][0]

    selenium.switch_to.window(new_window_handle)
    time.sleep(0.25)
    assert selenium.current_url == urls.BASE_URL
    selenium.quit()


@pytest.mark.skip(reason="don't know how to test api calls")
def test_elements_links_created(selenium):
    get_url(selenium, urls.ELEMENTS_LINKS)
    link = selenium.find_element(By.ID, "created")
    link.click()
    WebDriverWait(selenium, 30).until(
        EC.text_to_be_present_in_element((By.ID, "linkResponse"), "Link has responded")
    )


def test_broken_images(selenium):
    get_url(selenium, urls.ELEMENTS_BROKEN_LINKS)
    existing_image_loc = (By.XPATH, '//p[text()="Valid image"]/following-sibling::img')
    WebDriverWait(selenium, 15).until(
        EC.visibility_of_element_located(existing_image_loc)
    )
    existing_image = selenium.find_element(*existing_image_loc)
    broken_image = selenium.find_element(
        By.XPATH, '//p[text()="Broken image"]/following-sibling::img'
    )
    assert broken_image.get_attribute("src"), "img src broken"
    assert existing_image.get_attribute("src"), "img src broken"
    assert existing_image.get_attribute != "0", "img broken"
    assert broken_image.get_attribute("naturalWidth") != "0", "img broken"


def test_broken_links(selenium):
    get_url(selenium, urls.ELEMENTS_BROKEN_LINKS)
    valid_link = selenium.find_element(By.LINK_TEXT, "Click Here for Valid Link")
    broken_link = selenium.find_element(By.LINK_TEXT, "Click Here for Broken Link")
    valid_response = requests.get(valid_link.get_attribute("href"))
    broken_reseponse = requests.get(broken_link.get_attribute("href"))
    assert valid_response.status_code == 200, "link broken"
    assert broken_reseponse.status_code == 200, "link broken"


def test_dynamic_properties(selenium):
    get_url(selenium, urls.ELEMENTS_DYNAMIC_PROPERTIES)
    text = selenium.find_element(By.XPATH, '//p[text()="This text has random Id"]')
    enable_after_btn = selenium.find_element(By.ID, "enableAfter")
    color_change_btn = selenium.find_element(By.ID, "colorChange")
    color_change_btn_class = color_change_btn.get_attribute("class")

    assert not enable_after_btn.is_enabled()
    assert "text-danger" not in color_change_btn_class
    WebDriverWait(selenium, 10).until(
        EC.all_of(
            EC.element_to_be_clickable(enable_after_btn),
            EC.visibility_of_element_located((By.ID, "visibleAfter")),
        )
    )
    color_change_btn_class = color_change_btn.get_attribute("class")
    assert enable_after_btn.is_enabled()
    assert text.is_displayed()
    assert "text-danger" in color_change_btn_class


@pytest.mark.parametrize(
    "name, radio_id", [["Yes", "yesRadio"], ["Impressive", "impressiveRadio"]]
)
def test_radio_buttons(selenium, name, radio_id):
    get_url(selenium, urls.ELEMENTS_RADIO_BUTTON)
    radio_label = selenium.find_element(By.CSS_SELECTOR, f'label[for="{radio_id}"')
    radio_label.click()
    output = selenium.find_element(By.CLASS_NAME, "text-success")
    assert output.get_attribute("innerHTML") == name


def test_radio_no(selenium):
    get_url(selenium, urls.ELEMENTS_RADIO_BUTTON)
    radio = selenium.find_element(By.ID, "noRadio")
    assert not radio.is_enabled()


def test_elements_button_right_click(selenium):
    get_url(selenium, urls.ELEMENTS_BUTTONS)
    button = selenium.find_element(By.ID, "rightClickBtn")
    ActionChains(selenium).context_click(button).perform()
    output = selenium.find_element(By.ID, "rightClickMessage")
    assert "right click" in output.get_attribute("innerHTML")


def test_elements_buttons_double_click(selenium):
    get_url(selenium, urls.ELEMENTS_BUTTONS)
    button = selenium.find_element(By.ID, "doubleClickBtn")
    ActionChains(selenium).double_click(button).perform()
    output = selenium.find_element(By.ID, "doubleClickMessage")
    assert "double click" in output.get_attribute("innerHTML")


def test_elements_buttons_dynamic(selenium):
    get_url(selenium, urls.ELEMENTS_BUTTONS)
    button = selenium.find_element(By.XPATH, '//button[text()="Click Me"]')
    button.click()
    output = selenium.find_element(By.ID, "dynamicClickMessage")
    assert "dynamic click" in output.get_attribute("innerHTML")


def test_elements_upload(selenium):
    get_url(selenium, urls.ELEMENTS_UPLOAD_DOWNLOAD)
    file_input = selenium.find_element(By.ID, "uploadFile")
    file_input.send_keys(os.getcwd() + "/img/image.jpeg")


def test_elements_download(selenium):
    get_url(selenium, urls.ELEMENTS_UPLOAD_DOWNLOAD)
    if os.path.exists(urls.DOWNLOAD_FILE):
        os.remove(urls.DOWNLOAD_FILE)
    download_button = selenium.find_element(By.ID, "downloadButton")
    download_button.click()
    time.sleep(1)
    assert os.path.exists(urls.DOWNLOAD_FILE)
