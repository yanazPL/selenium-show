from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from conftest import Person, get_url
import urls
from selenium.webdriver.common.action_chains import ActionChains


def extract_people_from_table(driver):
    rows = driver.find_elements(By.CSS_SELECTOR, 'div[role="row"]')
    people = []
    for row in rows[1:]:
        cells = row.find_elements(By.CSS_SELECTOR, "*")
        if cells[0].get_attribute("innerHTML").startswith("<span>"):
            break
        people.append(
            Person(
                first_name=cells[0].get_attribute("innerHTML"),
                last_name=cells[1].get_attribute("innerHTML"),
                age=int(cells[2].get_attribute("innerHTML")),
                email=cells[3].get_attribute("innerHTML"),
                salary=int(cells[4].get_attribute("innerHTML")),
                department=cells[5].get_attribute("innerHTML"),
            )
        )
    return people


def clear_table(driver):
    while delete_spans := driver.find_elements(By.CSS_SELECTOR, 'span[title="Delete"]'):
        delete_spans[0].click()


def fill_person_data(driver, person):
    first_name_input = driver.find_element(By.ID, "firstName")
    last_name_input = driver.find_element(By.ID, "lastName")
    email_input = driver.find_element(By.ID, "userEmail")
    age_input = driver.find_element(By.ID, "age")
    salary_input = driver.find_element(By.ID, "salary")
    department_input = driver.find_element(By.ID, "department")
    submit_btn = driver.find_element(By.ID, "submit")

    first_name_input.clear()
    last_name_input.clear()
    email_input.clear()
    age_input.clear()
    salary_input.clear()
    department_input.clear()
    first_name_input.send_keys(person.first_name)
    last_name_input.send_keys(person.last_name)
    email_input.send_keys(person.email)
    age_input.send_keys(person.age)
    salary_input.send_keys(person.salary)
    department_input.send_keys(person.department)
    submit_btn.click()


def edit_topmost_person(driver, new_person):
    edit_buttons = driver.find_elements(By.CSS_SELECTOR, 'span[title="Edit"]')
    edit_buttons[0].click()
    fill_person_data(driver, new_person)


def add_people_to_table(driver, people):
    add_button = driver.find_element(By.ID, "addNewRecordButton")
    for person in people:
        add_button.click()
        fill_person_data(driver, person)


def page_jump(driver, page_nr):
    page_input = driver.find_element(By.CSS_SELECTOR, ".-pageJump input")
    page_input.clear()
    page_input.send_keys(str(page_nr))


def change_rows(driver, count):
    change_rows_el = driver.find_element(
        By.CSS_SELECTOR, 'select[aria-label="rows per page"'
    )
    original_x, original_y = (
        driver.get_window_position()["x"],
        driver.get_window_position()["y"],
    )
    x_offset, y_offset = (
        int(change_rows_el.rect["x"] - float(original_x)),
        int(change_rows_el.rect["y"] - float(original_y)),
    )
    ActionChains(driver).scroll_by_amount(x_offset, y_offset).perform()
    select = Select(change_rows_el)
    select.select_by_value(str(count))
    add_button = driver.find_element(By.ID, "addNewRecordButton")
    driver.execute_script("arguments[0].scrollIntoView();", add_button)


def next_table_page(driver):
    button = driver.find_element(By.CSS_SELECTOR, ".-next button")
    assert button.is_displayed()


def previous_table_page(driver):
    button = driver.find_element(By.CSS_SELECTOR, ".-previous button")
    assert button.is_displayed()


def search_table(driver, string):
    searchbox = driver.find_element(By.ID, "searchBox")
    searchbox.send_keys(string)


def clear_searchbox(driver):
    searchbox = driver.find_element(By.ID, "searchBox")
    searchbox.clear()


def order_records(driver, header, order="asc"):
    content_xpath = f'//div[@class="rt-resizable-header-content" and text()="{header}"]'
    content_el = driver.find_element(By.XPATH, content_xpath)
    header_xpath = f"{content_xpath}/.."
    header_el = driver.find_element(By.XPATH, header_xpath)
    if order == "asc":
        if "-sort-asc" not in header_el.get_attribute("class"):
            content_el.click()
    if order == "desc":
        if "-sort-desc" not in header_el.get_attribute("class"):
            content_el.click()


def test_webtables_clear(selenium):
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    clear_table(selenium)
    table_data_list = selenium.find_elements(By.CLASS_NAME, "rt-td")
    for td in table_data_list:
        children = td.find_elements(By.CSS_SELECTOR, "*")
        assert len(children) == 1
        assert (
            children[0].tag_name == "span"
            and children[0].get_attribute("innerHTML") == "&nbsp;"
        )
        assert not extract_people_from_table(selenium)


def test_table_data_fixture(table_data):
    people = table_data(3)
    for person in people:
        assert isinstance(person, Person)


def test_table_add_one(selenium):
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    clear_table(selenium)
    data = [
        Person(
            first_name="Jan",
            last_name="Kowalski",
            age=30,
            email="jan.kowalski@abc.pl",
            salary=6500,
            department="IT",
        )
    ]
    add_people_to_table(selenium, data)
    result = extract_people_from_table(selenium)
    assert result.pop() == data[0]


def test_table_add_ten(selenium, table_data):
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    clear_table(selenium)
    data = table_data(10)
    add_people_to_table(selenium, data)
    result = extract_people_from_table(selenium)
    assert len(result) == 10
    assert result == data


def test_edit_topmost(selenium, table_data):
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    clear_table(selenium)
    initial_person = table_data(1)
    add_people_to_table(selenium, initial_person)
    new_person = Person(
        "Adam",
        "Żuk",
        age=25,
        email="adam.zuk@zuky.net",
        salary=250000,
        department="CEO",
    )
    edit_topmost_person(selenium, new_person)
    people = extract_people_from_table(selenium)
    assert people[0] == new_person


def test_order_table(selenium):
    """Test doesn't pass, because there is actual salary order bug"""
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    close_fixedban = selenium.find_elements(By.ID, "close-fixedban")
    if close_fixedban:
        close_fixedban[0].click()
    change_rows(selenium, 5)
    clear_table(selenium)
    people = [
        Person(
            "Adam",
            "Żuk",
            age=25,
            email="adam.zuk@zuky.net",
            salary=250000,
            department="CEO",
        ),
        Person(
            "Anna",
            "Kowalska",
            age=30,
            email="anna.kowalska@example.com",
            salary=5000,
            department="Compliance",
        ),
        Person(
            "Michał",
            "Nowak",
            age=40,
            email="michal.nowak@example.com",
            salary=35000,
            department="Legal",
        ),
    ]
    add_people_to_table(selenium, people)
    order_records(selenium, "First Name", order="asc")
    people_by_first_name_asc = extract_people_from_table(selenium)
    assert len(people_by_first_name_asc) == 3
    assert people_by_first_name_asc[0].first_name == "Adam"
    assert people_by_first_name_asc[1].first_name == "Anna"
    assert people_by_first_name_asc[2].first_name == "Michał"

    order_records(selenium, "First Name", order="desc")
    people_by_first_name_desc = extract_people_from_table(selenium)
    assert len(people_by_first_name_desc) == 3
    assert people_by_first_name_desc[0].first_name == "Michał"
    assert people_by_first_name_desc[1].first_name == "Anna"
    assert people_by_first_name_desc[2].first_name == "Adam"

    order_records(selenium, "Last Name", order="asc")
    people_by_last_name_asc = extract_people_from_table(selenium)
    assert people_by_last_name_asc[0].last_name == "Kowalska"
    assert people_by_last_name_asc[1].last_name == "Nowak"
    assert people_by_last_name_asc[2].last_name == "Żuk"

    order_records(selenium, "Last Name", order="desc")
    people_by_last_name_desc = extract_people_from_table(selenium)
    assert people_by_last_name_desc[0].last_name == "Żuk"
    assert people_by_last_name_desc[1].last_name == "Nowak"
    assert people_by_last_name_desc[2].last_name == "Kowalska"

    order_records(selenium, "Age", order="asc")
    people_by_age_asc = extract_people_from_table(selenium)
    assert people_by_age_asc[0].age == 25
    assert people_by_age_asc[1].age == 30
    assert people_by_age_asc[2].age == 40

    order_records(selenium, "Age", order="desc")
    people_by_age_desc = extract_people_from_table(selenium)
    assert people_by_age_desc[0].age == 40
    assert people_by_age_desc[1].age == 30
    assert people_by_age_desc[2].age == 25

    order_records(selenium, "Email", order="asc")
    people_by_email_asc = extract_people_from_table(selenium)
    assert people_by_email_asc[0].email == "adam.zuk@zuky.net"
    assert people_by_email_asc[1].email == "anna.kowalska@example.com"
    assert people_by_email_asc[2].email == "michal.nowak@example.com"

    order_records(selenium, "Email", order="desc")
    people_by_email_desc = extract_people_from_table(selenium)
    assert people_by_email_desc[0].email == "michal.nowak@example.com"
    assert people_by_email_desc[1].email == "anna.kowalska@example.com"
    assert people_by_email_desc[2].email == "adam.zuk@zuky.net"

    order_records(selenium, "Salary", order="asc")
    people_by_salary_asc = extract_people_from_table(selenium)
    assert people_by_salary_asc[0].salary == 5000  # BUG -> here
    assert people_by_salary_asc[1].salary == 35000
    assert people_by_salary_asc[2].salary == 250000

    order_records(selenium, "Salary", order="desc")
    people_by_salary_desc = extract_people_from_table(selenium)
    assert people_by_salary_desc[0].salary == 250000
    assert people_by_salary_desc[1].salary == 35000
    assert people_by_salary_desc[2].salary == 5000

    order_records(selenium, "Department", order="asc")
    people_by_department_asc = extract_people_from_table(selenium)
    assert people_by_department_asc[0].department == "CEO"
    assert people_by_department_asc[1].department == "Compliance"
    assert people_by_department_asc[2].department == "Legal"

    order_records(selenium, "Department", order="desc")
    people_by_department_desc = extract_people_from_table(selenium)
    assert people_by_department_desc[0].department == "Legal"
    assert people_by_department_desc[1].department == "Compliance"
    assert people_by_department_desc[2].department == "CEO"


def test_search_table(selenium):
    get_url(selenium, urls.ELEMENTS_WEBTABLES)
    change_rows(selenium, 5)
    clear_table(selenium)
    people = [
        Person(
            "Adam",
            "Żuk",
            age=25,
            email="adam.zuk@zuky.net",
            salary=50000,
            department="Compliance",
        ),
        Person(
            "Adam",
            "Kowalski",
            age=30,
            email="adam.kowalski@example.com",
            salary=5000,
            department="Compliance",
        ),
        Person(
            "Michał",
            "Żuk",
            age=25,
            email="michal.zuk@example.com",
            salary=35000,
            department="Legal",
        ),
    ]
    add_people_to_table(selenium, people)
    search_table(selenium, "Adam")
    adams = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, "Żuk")
    zuk = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, "25")
    age_25 = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, "Compliance")
    ceo_and_compliance = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, ".com")
    com_domain = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, "5000")
    salary_with_5000 = extract_people_from_table(selenium)
    clear_searchbox(selenium)
    search_table(selenium, "50000")
    salary_with_50000 = extract_people_from_table(selenium)

    assert len(adams) == 2
    assert len(zuk) == 2
    assert len(age_25) == 2
    assert len(ceo_and_compliance) == 2
    assert len(com_domain) == 2
    assert len(salary_with_5000) == 3
    assert len(salary_with_50000) == 1
