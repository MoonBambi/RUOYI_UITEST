from pages.login_page import LoginPage


def test_open_login_page(driver, config):
    page = LoginPage(driver)
    page.open(config["base_url"])
    assert page.is_loaded()


def test_login_form_elements_present(driver, config):
    page = LoginPage(driver)
    page.open(config["base_url"])
    assert page.find(*LoginPage.USERNAME)
    assert page.find(*LoginPage.PASSWORD)
    assert page.find(*LoginPage.CODE)
