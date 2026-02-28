from conftest import with_login
from pages.system_manage_page import SystemManagePage


@with_login
def test_open_dept_manage_from_system_menu(driver):
    page = SystemManagePage(driver)

    page.open_system_manage()
    page.open_dept_manage()
    page.add_dept_with_keyboard("北京分公司", "3")
    page.search_and_delete_dept_by_name("北京分公司")

