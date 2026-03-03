from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging


logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open(self, url: str, wait: float = 0) -> None:
        self.driver.get(url)
        if wait and wait > 0:
            WebDriverWait(self.driver, wait).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

    def find(self, by: By, value: str, wait: float = 0):
        try:
            if wait and wait > 0:
                return WebDriverWait(self.driver, wait).until(
                    EC.presence_of_element_located((by, value))
                )
            return self.driver.find_element(by, value)
        except Exception:
            logger.error(
                "find element failed: by=%s, value=%s, url=%s",
                by,
                value,
                self.driver.current_url,
                exc_info=True,
            )
            raise

    def click(self, by: By, value: str, wait: float = 0) -> None:
        try:
            if wait and wait > 0:
                WebDriverWait(self.driver, wait).until(
                    EC.element_to_be_clickable((by, value))
                ).click()
                return
            self.find(by, value).click()
        except Exception:
            logger.error(
                "click element failed: by=%s, value=%s, url=%s",
                by,
                value,
                self.driver.current_url,
                exc_info=True,
            )
            raise

    def type(self, by: By, value: str, text: str, wait: float = 0) -> None:
        try:
            element = self.find(by, value, wait=wait)
            element.clear()
            element.send_keys(text)
        except Exception:
            logger.error(
                "type into element failed: by=%s, value=%s, text=%s, url=%s",
                by,
                value,
                text,
                self.driver.current_url,
                exc_info=True,
            )
            raise
