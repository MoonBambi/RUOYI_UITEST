# 若依（RuoYi）UI 自动化测试框架

这是一个基于 **Python** + **Selenium** + **Pytest** 的自动化测试框架，专为 [若依（RuoYi）官方仓库](https://github.com/yangzongzhuan/RuoYi)（传统版后台管理系统）设计。

本框架特别采用了 **场景化脚本设计** 理念，将独立的增删改查操作串联成完整的业务流程（如：员工入职 -> 分配角色 -> 权限验证 -> 离职清理），更贴近用户真实使用场景。

同时结合了 **Page Object Model (POM)** 设计模式与 **API 辅助机制**，实现“UI 验证业务，接口处理数据”，既保证了测试的真实性，又大幅提升了执行效率和稳定性。

## 核心特性

- **混合驱动**：UI 层专注于页面交互验证，繁琐的数据准备和清理（如创建/删除用户、部门、角色）通过 API 直接完成。
- **原生轻量**：API 客户端基于 Python 原生 `urllib` 封装，无需额外安装 `requests` 库即可处理登录鉴权与 Cookie 维持。
- **清晰报告**：集成 **Allure**，生成包含测试步骤、截图和日志的详细可视化报告。
- **日志管理**：测试日志自动归档到 `report/` 目录，控制台保持清爽，仅显示 Pytest 执行进度。
- **灵活配置**：支持通过 YAML 文件快速切换测试环境、浏览器类型（Chrome/Edge）及驱动路径。

## 目录结构一览

```text
RUOYI_UITEST/
├── api/                # API 接口封装（用于数据准备与清理）
│   ├── client.py       # 基础客户端（处理 Cookie 与登录）
│   └── system_manage.py # 系统管理模块接口（用户/部门/角色管理）
├── config/             # 配置文件
│   └── settings.yaml   # 环境、浏览器、等待时间等配置
├── data/               # 测试数据与接口路径定义
├── drivers/            # 浏览器驱动存放目录（chromedriver.exe 等）
├── pages/              # 页面对象（POM 层）
│   ├── base_page.py    # 封装 Selenium 常用操作
│   └── ...             # 各业务页面封装
├── report/             # 测试日志归档目录
├── tests/              # 测试用例目录
│   ├── conftest.py     # Pytest Fixtures（驱动初始化、日志配置等）
│   └── test_*.py       # 具体的业务场景用例
├── requirements.txt    # 项目依赖列表
└── run.py              # (可选) 统一运行入口
```

## 快速上手

### 1. 环境准备

**被测系统**：
确保你已经在本地（或远程）启动了若依后端服务。

- 官方仓库：[https://github.com/yangzongzhuan/RuoYi](https://github.com/yangzongzhuan/RuoYi)
- 默认登录地址：`http://localhost:80/login`
- 默认账号：`admin / admin123`

> **重要说明**：
> 本框架未包含验证码识别模块，请在若依后端配置文件（`application.yml`）中将 `shiro.user.captchaEnabled` 设置为 `false` 以关闭验证码校验，否则自动化登录将失败。

**浏览器与驱动（推荐方案）**：

本项目推荐使用 **Chrome for Testing** 以确保浏览器与驱动版本严格匹配：

1. 访问 [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) 下载 Stable 或最新版本的 ZIP 包：
   - **chrome-win64.zip**
   - **chromedriver-win64.zip**
2. 将解压后的 `chrome-win64` 和 `chromedriver-win64` 文件夹直接放置在项目根目录下。
   - 确保路径存在：`chrome-win64\chrome.exe` 和 `chromedriver-win64\chromedriver.exe`。
3. 框架已内置适配逻辑：
   - 自动识别根目录下的驱动文件。
   - 默认配置已指向该路径下的浏览器二进制文件。

*注：这两个文件夹已配置在 `.gitignore` 中，不会被提交到版本库。*

**备选方案（使用本机浏览器）**：
如果不使用独立版 Chrome，请下载与本机浏览器版本一致的 `chromedriver.exe`，放入 `drivers/` 目录，并在配置文件中清空 `chrome_binary_path` 项。

### 2. 安装依赖

建议使用虚拟环境运行：

```bash
# 创建并激活虚拟环境
python -m venv .venv
# Windows 下激活
.\.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 修改配置

打开 `config/settings.yaml`，根据实际情况调整：

```yaml
# 被测系统登录页地址
base_url: "http://localhost:80/login?redirect=%2Findex"

# 浏览器类型：chrome 或 edge
browser: "chrome"

# 隐式等待时间（秒）
implicit_wait: 10

# Chrome 二进制文件路径（如果驱动找不到浏览器，可在此指定绝对路径）
chrome_binary_path: "chrome-win64/chrome.exe"
```

### 4. 运行测试

**执行所有用例**：

```bash
pytest
```

**执行并生成 Allure 报告数据**：

```bash
pytest --alluredir=allure-results
```

### 5. 查看报告

测试完成后，使用 Allure 启动本地服务查看报告：

```bash
allure serve allure-results
```

或者生成静态 HTML 报告文件：

```bash
allure generate allure-results -o allure-report --clean
```
