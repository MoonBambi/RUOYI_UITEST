from pathlib import Path
from datetime import datetime
import logging
import time

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

from pages.login_page import LoginPage
from api.client import create_logged_in_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"
DRIVER_DIR = PROJECT_ROOT / "drivers"
REPORT_DIR = PROJECT_ROOT / "report"

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _build_chrome_driver(options):
    driver_path = DRIVER_DIR / "chromedriver.exe"
    if not driver_path.exists():
        raise RuntimeError(f"Chrome driver not found at {driver_path}")
    service = ChromeService(executable_path=str(driver_path))
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    time.sleep(3)
    return driver


def _build_edge_driver(options):
    driver_path = DRIVER_DIR / "msedgedriver.exe"
    if not driver_path.exists():
        raise RuntimeError(f"Edge driver not found at {driver_path}")
    service = EdgeService(executable_path=str(driver_path))
    driver = webdriver.Edge(service=service, options=options)
    driver.maximize_window()
    time.sleep(3)
    return driver


def pytest_configure(config):
    REPORT_DIR.mkdir(exist_ok=True)
    log_file = REPORT_DIR / f"test_{datetime.now():%Y%m%d_%H%M%S}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    logging.getLogger().info("Pytest session started")


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    root_logger = logging.getLogger()
    if report.failed:
        root_logger.error(f"Test {report.nodeid} FAILED")
    elif report.skipped:
        root_logger.warning(f"Test {report.nodeid} SKIPPED")
    else:
        root_logger.info(f"Test {report.nodeid} PASSED")


@pytest.fixture(scope="session")
def driver(config):
    browser = config.get("browser", "chrome").lower()
    logger.info(f"Creating WebDriver for browser: {browser}")
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        chrome_binary = config.get("chrome_binary_path")
        options.add_argument("password-store=basic")
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            },
        )
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
    try:
        yield driver
    finally:
        logger.info("Quitting WebDriver")
        driver.quit()


@pytest.fixture(scope="session")
def api_client(config):
    return create_logged_in_client(config["base_url"])


@pytest.fixture
def logged_in(driver, config):
    logger.info("Logging in with default account")
    page = LoginPage(driver)
    page.open(config["base_url"])
    page.login()
    page.dismiss_security_dialog()
    logger.info("Login finished")
    return driver


def with_login(func):
    return pytest.mark.usefixtures("logged_in")(func)
