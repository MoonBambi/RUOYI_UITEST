import os

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .base_page import BasePage


class SystemManagePage(BasePage):
    SYSTEM_MANAGE = (
        By.XPATH,
        "//span[@class='nav-label' and normalize-space()='系统管理']/parent::a",
    )
    DEPT_MANAGE = (
        By.XPATH,
        "//a[contains(@class,'menuItem') and contains(@href,'/system/dept')]",
    )
    DEPT_IFRAME = (
        By.XPATH,
        "//iframe[contains(@class,'RuoYi_iframe') and @data-id='/system/dept']",
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

    def open_system_manage(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SYSTEM_MANAGE)
        ).click()

    def open_dept_manage(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.DEPT_MANAGE)
        ).click()

    def add_dept_with_keyboard(self, name: str, order: str) -> None:
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

        body = self.driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(self.driver)
        actions.click(body)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(name)
        actions.send_keys(Keys.TAB)
        actions.send_keys(order)
        actions.perform()

        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.ADD_CONFIRM_BUTTON
            )
        )
        confirm_button.click()

    def search_and_delete_dept_by_name(self, name: str) -> None:
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
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    self.DIALOG_CONFIRM_BUTTON
                )
            )
        except TimeoutException:
            pass

        used_image = False
        try:
            import pyautogui  # type: ignore

            pyautogui.FAILSAFE = False
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "imgs", "confirm.png")
            location = pyautogui.locateCenterOnScreen(
                image_path, confidence=0.8
            )
            if location is not None:
                pyautogui.click(location.x, location.y)
                used_image = True
        except Exception:
            used_image = False

        if not used_image:
            self.driver.execute_script(
                "var btns = document.querySelectorAll('a.layui-layer-btn0');"
                "if(btns.length){btns[btns.length-1].click();}"
            )
