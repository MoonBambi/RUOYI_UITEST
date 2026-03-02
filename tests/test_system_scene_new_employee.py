from conftest import with_login
from pages.system_manage_page import SystemManagePage
from pages.login_page import LoginPage
import time


@with_login
def test_open_dept_manage_from_system_menu(driver):
    page = SystemManagePage(driver)

    page.open_system()
    page.open_dept()
    page.add_dept("北京分公司", "3")
    page.open_role()
    page.add_role()
    time.sleep(3)
    page.open_user()
    time.sleep(3)
    page.set_user_dept("UITest", "北京分公司")


def test_login_as_uitest(driver, config):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.input_username("UITest")
    login_page.input_password("123456")
    login_page.login()
    login_page.dismiss_security_dialog()
    page = SystemManagePage(driver)
    assert page.get_main_nav_labels() == ["首页", "实例演示"]
    time.sleep(3)

