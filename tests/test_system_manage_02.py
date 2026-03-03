import json
import logging
import time

import allure
import pytest

from api import system_manage
from conftest import with_login
from pages.login_page import LoginPage
from pages.system_manage_page import SystemManagePage


logger = logging.getLogger(__name__)

_original_chrtype = ""
_bad_login_name = "PwdPolicyBad"
_good_login_name = "PwdPolicyGood"
_user_name = "密码测试用户"


@allure.feature("系统管理")
@allure.story("安全合规控制")
@allure.title("密码策略：设置为仅数字")
def test_prepare_password_policy(api_client):
    global _original_chrtype

    config_key = "sys.account.chrtype"
    res = system_manage.get_config_list(api_client, config_key=config_key)
    rows = res.get("rows", [])
    if not rows:
        pytest.skip(f"Config {config_key} not found")

    config_row = rows[0]
    _original_chrtype = config_row.get("configValue")
    config_id = config_row.get("configId")
    config_name = config_row.get("configName")

    if _original_chrtype == "1":
        return

    result = system_manage.edit_config(
        api_client,
        config_id=config_id,
        config_name=config_name,
        config_key=config_key,
        config_value="1",
    )
    logger.info("set sys.account.chrtype to 1 result: %s", result)
    allure.attach(
        json.dumps(result, ensure_ascii=False, indent=2),
        "设置密码策略为仅数字结果",
        allure.attachment_type.JSON,
    )
    assert result.get("code") == 0


@allure.feature("系统管理")
@allure.story("安全合规控制")
@allure.title("密码策略：校验非数字与数字密码")
@with_login
def test_password_strength_policy(api_client, driver, config):
    page = SystemManagePage(driver)

    with allure.step("策略为仅数字时，纯数字密码新增用户成功并可登录"):
        page.add_user_UI(_good_login_name, _user_name, "123456")
        time.sleep(3)
        res_good = system_manage.get_user_list_by_login_name(
            api_client, _good_login_name
        )
        allure.attach(
            json.dumps(res_good, ensure_ascii=False, indent=2),
            "纯数字密码新增结果",
            allure.attachment_type.JSON,
        )
        rows_good = res_good.get("rows") or []
        match_good = [
            row for row in rows_good if row.get("loginName") == _good_login_name
        ]
        assert len(match_good) >= 1

        login_page = LoginPage(driver)
        login_page.open(config["base_url"])
        login_page.input_username(_good_login_name)
        login_page.input_password("123456")
        login_page.login()

        labels = page.get_main_nav_labels()
        assert labels
        time.sleep(3)

@allure.feature("系统管理")
@allure.story("安全合规控制")
@allure.title("密码策略：非纯数字密码新增失败")
@with_login
def test_password_strength_policy_invalid(api_client, driver, config):
    page = SystemManagePage(driver)

    with allure.step("策略为仅数字时，非数字密码新增用户失败"):
        page.add_user_UI(_bad_login_name, _user_name, "abcde")
        time.sleep(3)
        res_bad = system_manage.get_user_list_by_login_name(api_client, _bad_login_name)
        allure.attach(
            json.dumps(res_bad, ensure_ascii=False, indent=2),
            "非数字密码新增结果",
            allure.attachment_type.JSON,
        )
        rows_bad = res_bad.get("rows") or []
        match_bad = [
            row for row in rows_bad if row.get("loginName") == _bad_login_name
        ]
        assert len(match_bad) == 0


@allure.feature("系统管理")
@allure.story("安全合规控制")
@allure.title("密码策略：恢复配置与清理数据")
def test_cleanup_password_policy(api_client):
    config_key = "sys.account.chrtype"

    if _original_chrtype != "1":
        res = system_manage.get_config_list(api_client, config_key=config_key)
        rows = res.get("rows", [])
        if rows:
            config_row = rows[0]
            config_id = config_row.get("configId")
            config_name = config_row.get("configName")
            result = system_manage.edit_config(
                api_client,
                config_id=config_id,
                config_name=config_name,
                config_key=config_key,
                config_value=_original_chrtype,
            )
            logger.info("restore sys.account.chrtype result: %s", result)
            allure.attach(
                json.dumps(result, ensure_ascii=False, indent=2),
                "恢复密码策略结果",
                allure.attachment_type.JSON,
            )

    bad_result = system_manage.delete_user_by_login_name(api_client, _bad_login_name)
    logger.info("cleanup bad user via api: %s", bad_result)
    good_result = system_manage.delete_user_by_login_name(api_client, _good_login_name)
    logger.info("cleanup good user via api: %s", good_result)
