from conftest import with_login
from pages.system_manage_page import SystemManagePage
from pages.login_page import LoginPage
from api.system_manage import delete_user_by_login_name, delete_dept_by_name, delete_role_by_name, add_user
import logging
import time
import allure


logger = logging.getLogger(__name__)

@allure.feature("系统管理")
@allure.story("数据构造")
@allure.title("数据构造")
def test_prepare_data(api_client):
    result = add_user(api_client, user_name = "UITest", login_name = "UITest", password = "123456")
    logger.info("add user UITest via api: %s", result)
    assert result.get("code") == 0

@allure.feature("系统管理")
@allure.story("新员工入职：分配部门和角色")
@allure.title("新员工入职：分配部门和角色")
@with_login
def test_open_dept_manage_from_system_menu(driver):
    page = SystemManagePage(driver)

    page.open_system()
    page.open_dept()
    page.add_dept("北京分公司", "3")
    page.open_role()
    page.add_role("Test")
    time.sleep(3)
    page.open_user()
    time.sleep(3)
    page.set_user_dept("UITest", "北京分公司")
    time.sleep(3)


@allure.feature("系统管理")
@allure.story("新员工入职：验证导航权限")
@allure.title("新员工入职：验证导航权限")
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


@allure.feature("系统管理")
@allure.story("数据清理：接口清除临时数据")
@allure.title("数据清理：接口清除临时数据")
def test_cleanup_dept_via_api(api_client):
    user_result = delete_user_by_login_name(api_client, "UITest")
    logger.info("cleanup user UITest via api: %s", user_result)
    dept_result = delete_dept_by_name(api_client, "北京分公司")
    logger.info("cleanup dept 北京分公司 via api: %s", dept_result)
    role_result = delete_role_by_name(api_client, "Test")
    logger.info("cleanup role Test via api: %s", role_result)

    assert user_result.get("code") == 0
    assert dept_result.get("code") == 0
    assert role_result.get("code") == 0
