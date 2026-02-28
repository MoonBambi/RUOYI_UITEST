from pages.login_page import LoginPage


def test_login_default_account_fields(driver, config):
    page = LoginPage(driver)
    page.open(config["base_url"])
    username_element = page.find(*LoginPage.USERNAME)
    password_element = page.find(*LoginPage.PASSWORD)
    assert username_element.get_attribute("value")
    assert password_element.get_attribute("value")
