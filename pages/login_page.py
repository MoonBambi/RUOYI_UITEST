from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.XPATH, "//input[@name='username']")
    PASSWORD = (By.XPATH, "//input[@name='password']")
    CODE = (By.XPATH, "//input[@name='validateCode']")
    SUBMIT = (By.XPATH, "//button[@id='btnSubmit']")
    CANCEL = (
        By.XPATH,
        "//div[contains(@class,'layui-layer-dialog')]//a[contains(@class,'layui-layer-btn1') and normalize-space()='取消']",
    )

    def is_loaded(self) -> bool:
        title = self.driver.title or ""
        return "登录若依系统" in title or "若依管理系统" in title

    def input_username(self, username: str) -> None:
        self.type(*self.USERNAME, text=username)

    def input_password(self, password: str) -> None:
        self.type(*self.PASSWORD, text=password)

    def submit(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SUBMIT)
        ).click()

    def login(self) -> None:
        self.submit()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/index"))

    def dismiss_security_dialog(self, timeout: int = 5) -> None:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.CANCEL)
            ).click()
        except TimeoutException:
            pass
