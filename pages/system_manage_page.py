import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui
import allure

from .base_page import BasePage
from utils_image_locator import ImageLocator


class SystemManagePage(BasePage):
    SYSTEM_MANAGE = (
        By.XPATH,
        "//span[@class='nav-label' and normalize-space()='系统管理']/parent::a",
    )
    DEPT_MANAGE = (
        By.XPATH,
        "//a[contains(@class,'menuItem') and contains(@href,'/system/dept')]",
    )
    ROLE_MANAGE = (
        By.XPATH,
        "//a[contains(@class,'menuItem') and contains(@href,'/system/role')]",
    )
    USER_MANAGE = (
        By.XPATH,
        "//a[@class='menuItem' and @href='/system/user' and normalize-space()='用户管理']",
    )
    DEPT_IFRAME = (
        By.XPATH,
        "//iframe[contains(@class,'RuoYi_iframe') and @data-id='/system/dept']",
    )
    ROLE_IFRAME = (
        By.XPATH,
        "//iframe[contains(@class,'RuoYi_iframe') and @data-id='/system/role']",
    )
    USER_IFRAME = (
        By.XPATH,
        "//iframe[contains(@class,'RuoYi_iframe') and @data-id='/system/user']",
    )
    TOOLBAR_ADD_BUTTON = (
        By.XPATH,
        "//div[@id='toolbar']//a[contains(@class,'btn-success')]",
    )
    ADD_DEPT_TITLE = (
        By.XPATH,
        "//div[contains(@class,'layui-layer-title') and contains(.,'添加部门')]",
    )
    ADD_CONFIRM_BUTTON = (
        By.XPATH,
        "//div[@class='layui-layer-btn']/a[@class='layui-layer-btn0' and normalize-space()='确定']",
    )
    SEARCH_TOGGLE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'btn-group') and contains(@class,'tool-right')]//button[@name='search' or @title='搜索']",
    )
    DEPT_NAME_INPUT = (
        By.XPATH,
        "//form[@id='dept-form']//input[@name='deptName']",
    )
    DEPT_SEARCH_BUTTON = (
        By.XPATH,
        "//form[@id='dept-form']//a[contains(@class,'btn-primary') and contains(.,'搜索')]",
    )
    ROW_BY_NAME_XPATH = "//tr[.//td[contains(normalize-space(), '{name}')]]"
    ROW_DELETE_BUTTON = (
        By.XPATH,
        ".//a[contains(@class,'btn-danger') and contains(.,'删除')]",
    )
    DIALOG_CONFIRM_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'layui-layer-dialog')]"
        "//a[contains(@class,'layui-layer-btn0') and normalize-space()='确定']",
    )
    ROLE_TEST_CHECKBOX = (
        By.XPATH,
        "//label[contains(normalize-space(.),'Test')]//input[@name='role']",
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@onclick='submitHandler()']",
    )

    @allure.step("新增用户（仅基础信息）：登录名={login_name}")
    def add_user_UI(self, login_name: str, user_name: str, password: str) -> None:
        self.open_system()
        self.open_user()
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(self.USER_IFRAME)
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.TOOLBAR_ADD_BUTTON)
        )
        self.driver.execute_script("$.operate.add();")
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.XPATH,
                    "//iframe[contains(@src,'/system/user/add') or contains(@data-id,'/system/user/add')]",
                )
            )
        )
        user_name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "userName"))
        )
        user_name_input.clear()
        user_name_input.send_keys(user_name)
        login_name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginName"))
        )
        login_name_input.clear()
        login_name_input.send_keys(login_name)
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        ).click()
        self.driver.switch_to.default_content()

    @allure.step("获取左侧导航栏标签列表")
    def get_main_nav_labels(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "side-menu"))
        )
        labels = self.driver.find_elements(
            By.XPATH, "//ul[@id='side-menu']//span[@class='nav-label']"
        )
        return [
            label.text.strip()
            for label in labels
            if label.is_displayed() and label.text.strip()
        ]

    @allure.step("点击左侧菜单：系统管理")
    def open_system(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SYSTEM_MANAGE)
        ).click()

    @allure.step("进入系统管理-部门管理页面")
    def open_dept(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DEPT_MANAGE)
        ).click()

    @allure.step("进入系统管理-角色管理页面")
    def open_role(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ROLE_MANAGE)
        ).click()

    @allure.step("进入系统管理-用户管理页面")
    def open_user(self) -> None:
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.USER_MANAGE)
        ).click()

    @allure.step("新增部门：{name}，排序：{order}")
    def add_dept(self, name: str, order: str) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                self.DEPT_IFRAME
            )
        )

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.TOOLBAR_ADD_BUTTON
            )
        )
        self.driver.execute_script("$.operate.add(100);")

        self.driver.switch_to.default_content()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.ADD_DEPT_TITLE
            )
        )

        ImageLocator.image_click_and_write(
            "dept_name.png",
            name,
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        ImageLocator.image_click_and_write(
            "dept_sort.png",
            order,
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )

        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.ADD_CONFIRM_BUTTON
            )
        )
        confirm_button.click()

    @allure.step("新增角色：{role_name}")
    def add_role(self, role_name: str = "Test") -> None:
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                self.ROLE_IFRAME
            )
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                self.TOOLBAR_ADD_BUTTON
            )
        )
        self.driver.execute_script("$.operate.add();")
        self.driver.switch_to.default_content()
        ImageLocator.image_click_and_write(
            "role_name.png",
            role_name,
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        ImageLocator.image_click_and_write(
            "grant_word.png",
            "view",
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        ImageLocator.image_click_and_write(
            "sort.png",
            "999",
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        self.driver.execute_script(
            "var btns = document.querySelectorAll('a.layui-layer-btn0');"
            "if(btns.length){btns[btns.length-1].click();}"
        )

    @allure.step("删除部门：{name}")
    def delete_dept(self, name: str) -> None:
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                self.DEPT_IFRAME
            )
        )

        search_toggle = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.SEARCH_TOGGLE_BUTTON
            )
        )
        search_toggle.click()

        name_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.DEPT_NAME_INPUT
            )
        )
        name_input.clear()
        name_input.send_keys(name)

        search_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.DEPT_SEARCH_BUTTON
            )
        )
        search_button.click()

        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    self.ROW_BY_NAME_XPATH.format(name=name),
                )
            )
        )
        delete_button = row.find_element(
            *self.ROW_DELETE_BUTTON
        )
        delete_button.click()

        self.driver.switch_to.default_content()
        pyautogui.FAILSAFE = False
        ImageLocator.image_click(
            "confirm.png",
            confidence=0.8,
            max_attempts=3,
            wait_time=0.2,
        )

    @allure.step("给用户 {login_name} 分配部门：{dept_keyword}")
    def set_user_dept(self, login_name: str, dept_keyword: str) -> None:
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                self.USER_IFRAME
            )
        )
        row = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//tr[.//td[normalize-space()='{login_name}']]",
                )
            )
        )
        edit_button = row.find_element(
            By.XPATH,
            ".//a[contains(@class,'btn-success') and contains(.,'编辑')]",
        )
        edit_button.click()

        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.XPATH,
                    "//iframe[contains(@class,'RuoYi_iframe') and contains(@data-id,'/system/user/edit')]",
                )
            )
        )

        time.sleep(2)
        ImageLocator.image_click(
            "select_role.png",
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )

        time.sleep(2)
        self.driver.switch_to.default_content()
        ImageLocator.image_click_and_write(
            "select_dept1.png",
            dept_keyword,
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )

        time.sleep(2)
        self.driver.switch_to.default_content()
        ImageLocator.image_click_and_write(
            "select_dept2.png",
            dept_keyword,
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        time.sleep(2)
        ImageLocator.image_click(
            "dept.png",
            confidence=0.9,
            max_attempts=3,
            wait_time=0.5,
        )
        self.driver.execute_script(
            "var btns = document.querySelectorAll('a.layui-layer-btn0');"
            "if(btns.length){btns[btns.length-1].click();}"
        )

        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (
                    By.XPATH,
                    "//iframe[contains(@class,'RuoYi_iframe') and contains(@data-id,'/system/user/edit')]",
                )
            )
        )
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.SAVE_BUTTON
            )
        ).click()


class SystemMonitorPage(BasePage):
    SYSTEM_MONITOR = (
        By.XPATH,
        "//span[@class='nav-label' and normalize-space()='系统监控']/parent::a",
    )

    @allure.step("点击左侧菜单：系统监控")
    def open(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SYSTEM_MONITOR)
        ).click()


class SystemToolsPage(BasePage):
    SYSTEM_TOOLS = (
        By.XPATH,
        "//span[@class='nav-label' and normalize-space()='系统工具']/parent::a",
    )

    @allure.step("点击左侧菜单：系统工具")
    def open(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SYSTEM_TOOLS)
        ).click()
