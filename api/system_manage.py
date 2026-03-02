from urllib.parse import urlencode, urljoin
from urllib.request import Request
from pathlib import Path
import json
import yaml

from api.client import ApiClient


BASE_DIR = Path(__file__).resolve().parent.parent
API_URL_FILE = BASE_DIR / "data" / "api_url.yaml"
with API_URL_FILE.open("r", encoding="utf-8") as f:
    API_URLS = yaml.safe_load(f) or {}

#在api/system_manage.py中添加系统管理模块的API函数

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

