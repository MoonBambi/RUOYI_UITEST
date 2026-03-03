from urllib.parse import urlencode, urljoin
from urllib.request import Request
from pathlib import Path
import json
import yaml
import allure

from api.client import ApiClient


BASE_DIR = Path(__file__).resolve().parent.parent
API_URL_FILE = BASE_DIR / "data" / "api_url.yaml"
with API_URL_FILE.open("r", encoding="utf-8") as f:
    API_URLS = yaml.safe_load(f) or {}


@allure.step("查询用户列表（根据登录名）")
def get_user_list_by_login_name(
    client: ApiClient,
    login_name: str,
    page_num: int = 1,
    page_size: int = 10,
) -> dict:
    form = {
        "pageSize": str(page_size),
        "pageNum": str(page_num),
        "orderByColumn": "createTime",
        "isAsc": "desc",
        "deptId": "",
        "parentId": "",
        "loginName": login_name,
        "phonenumber": "",
        "status": "",
        "params[beginTime]": "",
        "params[endTime]": "",
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["user"]["list_by_login_name"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("新增用户：loginName={login_name}")
def add_user(
    client: ApiClient,
    login_name: str,
    user_name: str,
    password: str = "123456",
    dept_id: str = "",
    dept_name: str = "",
    phonenumber: str = "",
    email: str = "",
    sex: str = "0",
    remark: str = "",
    status: str = "0",
    role_ids: str = "",
    post_ids: str = "",
) -> dict:
    form = {
        "deptId": dept_id,
        "userName": user_name,
        "deptName": dept_name,
        "phonenumber": phonenumber,
        "email": email,
        "loginName": login_name,
        "password": password,
        "sex": sex,
        "remark": remark,
        "status": status,
        "roleIds": role_ids,
        "postIds": post_ids,
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["user"]["add"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("删除用户：ids={ids}")
def delete_user(
    client: ApiClient,
    ids: str,
) -> dict:
    form = {
        "ids": ids,
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["user"]["delete"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("根据登录名删除用户：loginName={login_name}")
def delete_user_by_login_name(
    client: ApiClient,
    login_name: str,
) -> dict:
    result = get_user_list_by_login_name(client, login_name)
    if result.get("code") != 0:
        return result
    total = result.get("total", 0)
    if total == 0:
        return {"code": 0, "msg": "no user to delete"}
    rows = result.get("rows") or []
    ids_list = [str(row.get("userId")) for row in rows if row.get("userId")]
    if not ids_list:
        return {"code": 0, "msg": "no userId to delete"}
    ids = ",".join(ids_list)
    return delete_user(client, ids)


@allure.step("查询部门列表（根据名称）：deptName={dept_name}")
def get_dept_list_by_name(
    client: ApiClient,
    dept_name: str,
    status: str = "",
) -> dict:
    form = {
        "deptName": dept_name,
        "status": status,
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["dept"]["list_by_name"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("查询角色列表（根据名称）：roleName={role_name}")
def get_role_list_by_name(
    client: ApiClient,
    role_name: str,
    page_num: int = 1,
    page_size: int = 10,
    role_key: str = "",
    status: str = "",
) -> dict:
    form = {
        "pageSize": str(page_size),
        "pageNum": str(page_num),
        "orderByColumn": "roleSort",
        "isAsc": "asc",
        "roleName": role_name,
        "roleKey": role_key,
        "status": status,
        "params[beginTime]": "",
        "params[endTime]": "",
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["role"]["list_by_name"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("删除角色：ids={ids}")
def delete_role(
    client: ApiClient,
    ids: str,
) -> dict:
    form = {
        "ids": ids,
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["role"]["delete"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("根据角色名称删除角色：roleName={role_name}")
def delete_role_by_name(
    client: ApiClient,
    role_name: str,
    role_key: str = "",
    status: str = "",
) -> dict:
    result = get_role_list_by_name(
        client,
        role_name,
        role_key=role_key,
        status=status,
    )
    if isinstance(result, dict) and result.get("code") is not None:
        rows = result.get("rows") or []
    else:
        rows = result or []
    if not rows:
        return {"code": 0, "msg": "no role to delete"}
    ids_list = [str(row.get("roleId")) for row in rows if row.get("roleId")]
    if not ids_list:
        return {"code": 0, "msg": "no roleId to delete"}
    ids = ",".join(ids_list)
    return delete_role(client, ids)


@allure.step("根据部门ID删除部门：deptId={dept_id}")
def delete_dept_by_id(
    client: ApiClient,
    dept_id: int,
) -> dict:
    path = API_URLS["system_manage"]["dept"]["delete_prefix"]
    url = urljoin(client.server_root, f"{path}/{dept_id}")
    req = Request(
        url,
        method="GET",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("根据部门名称删除部门：deptName={dept_name}")
def delete_dept_by_name(
    client: ApiClient,
    dept_name: str,
    status: str = "",
) -> dict:
    result = get_dept_list_by_name(client, dept_name, status)
    if isinstance(result, dict) and result.get("code") is not None:
        rows = result.get("rows") or []
    else:
        rows = result or []
    if not rows:
        return {"code": 0, "msg": "no dept to delete"}
    last_response = None
    for row in rows:
        dept_id = row.get("deptId")
        if not dept_id:
            continue
        last_response = delete_dept_by_id(client, int(dept_id))
        if last_response.get("code") != 0:
            return last_response
    if last_response is None:
        return {"code": 0, "msg": "no valid deptId to delete"}
    return last_response


@allure.step("查询参数配置：configKey={config_key}")
def get_config_list(
    client: ApiClient,
    config_key: str = "",
    config_name: str = "",
    config_type: str = "",
    page_num: int = 1,
    page_size: int = 10,
) -> dict:
    form = {
        "pageSize": str(page_size),
        "pageNum": str(page_num),
        "orderByColumn": "createTime",
        "isAsc": "desc",
        "configName": config_name,
        "configKey": config_key,
        "configType": config_type,
        "params[beginTime]": "",
        "params[endTime]": "",
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["config"]["list"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))


@allure.step("修改参数配置：configName={config_name}, configKey={config_key}")
def edit_config(
    client: ApiClient,
    config_id: int,
    config_name: str,
    config_key: str,
    config_value: str,
    config_type: str = "Y",
    remark: str = "",
) -> dict:
    form = {
        "configId": str(config_id),
        "configName": config_name,
        "configKey": config_key,
        "configValue": config_value,
        "configType": config_type,
        "remark": remark,
    }
    encoded = urlencode(form).encode("utf-8")
    path = API_URLS["system_manage"]["config"]["edit"]
    req = Request(
        urljoin(client.server_root, path),
        data=encoded,
        method="POST",
    )
    req.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded; charset=UTF-8",
    )
    with client.opener.open(req) as resp:
        body_bytes = resp.read()
    return json.loads(body_bytes.decode("utf-8"))
