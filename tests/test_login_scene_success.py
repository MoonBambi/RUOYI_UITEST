import time


def test_login_success_without_captcha(logged_in):
    driver = logged_in
    assert "/index" in driver.current_url
    time.sleep(3)