from pathlib import Path

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from pages.login_page import LoginPage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"
DRIVER_DIR = PROJECT_ROOT / "drivers"


@pytest.fixture(scope="session")
def config():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_chrome_driver(options):
    driver_path = DRIVER_DIR / "chromedriver.exe"
    if not driver_path.exists():
        raise RuntimeError(f"Chrome driver not found at {driver_path}")
    service = ChromeService(executable_path=str(driver_path))
    return webdriver.Chrome(service=service, options=options)


def _build_edge_driver(options):
    driver_path = DRIVER_DIR / "msedgedriver.exe"
    if not driver_path.exists():
        raise RuntimeError(f"Edge driver not found at {driver_path}")
    service = EdgeService(executable_path=str(driver_path))
    return webdriver.Edge(service=service, options=options)


@pytest.fixture(scope="session")
def driver(config):
    browser = config.get("browser", "chrome").lower()
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        chrome_binary = config.get("chrome_binary_path")
        if chrome_binary:
            binary_path = Path(chrome_binary)
            if not binary_path.is_absolute():
                binary_path = PROJECT_ROOT / binary_path
            if not binary_path.exists():
                raise RuntimeError(f"Chrome binary not found at {binary_path}")
            options.binary_location = str(binary_path)
        driver = _build_chrome_driver(options)
    elif browser == "edge":
        options = webdriver.EdgeOptions()
        driver = _build_edge_driver(options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    driver.implicitly_wait(config.get("implicit_wait", 10))
    yield driver
    driver.quit()


@pytest.fixture
def logged_in(driver, config):
    page = LoginPage(driver)
    page.open(config["base_url"])
    page.login()
    page.dismiss_security_dialog()
    return driver


def with_login(func):
    return pytest.mark.usefixtures("logged_in")(func)
