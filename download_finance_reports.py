# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨境卖家后台财务报表自动下载工具（精简版）
运行前：pip install selenium webdriver-manager
"""

import os
import time
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver.chrome import ChromeDriverManager

# ==================== 配置区 ====================
USERNAME = "15818779524"  # 你的账号
PASSWORD = "Amitofo202409"  # 你的密码
TARGET_MONTH = "2026-03"  # 要下载的月份
DOWNLOAD_DIR = Path.home() / "Downloads"  # 下载目录
LOGIN_URL = "https://seller.kuajingmaihuo.com/settle/site-main"


# ==================== 工具函数 ====================

def setup_driver():
    """启动 Chrome 浏览器"""
    options = Options()
    prefs = {
        "download.default_directory": str(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # 调试时注释，可以看到浏览器

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30)
    print(f"✓ 浏览器已启动，下载目录：{DOWNLOAD_DIR}")
    return driver


def wait_element(driver, xpath, timeout=10):
    """等待元素出现"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def wait_clickable(driver, xpath, timeout=10):
    """等待元素可点击"""
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))


def safe_click(driver, xpath, desc="按钮", wait=5):
    """安全点击"""
    wait_clickable(driver, xpath).click()
    print(f"✓ 已点击：{desc}")
    time.sleep(wait)


def login(driver):
    """登录"""
    print("\n=== 步骤 1: 登录 ===")

    # 切换到账号登录
    try:
        wait_clickable(driver, "//text()[contains(., '账号登录')]/..").click()
        time.sleep(2)
    except:
        pass

    # 输入手机号和密码
    wait_element(driver, "//input[@placeholder='请输入手机号']").send_keys(USERNAME)
    wait_element(driver, "//input[@placeholder='请输入密码']").send_keys(PASSWORD)
    print(f"✓ 已输入账号密码")

    # 勾选协议
    try:
        driver.find_element(By.XPATH, "//label[contains(., '我已阅读')]").click()
    except:
        pass

    # 点击获取验证码（需要手动输入）
    print("\n⚠️  请在网页上点击【获取验证码】，输入短信验证码后手动登录")
    print("   登录成功后，在下方输入 'y' 继续...")
    while input("   已完成登录？(输入 y): ").strip().lower() != 'y':
        pass
    time.sleep(3)

    # 验证登录
    if "settle/site-main" in driver.current_url:
        print("✓ 登录成功！")
        return True
    return False


def enter_seller_center(driver):
    """进入商家中心"""
    print("\n=== 步骤 2: 进入商家中心 ===")
    try:
        wait_clickable(driver, "//button[contains(., '进入') or contains(., '进入 >')]").click()
        time.sleep(10)
        print("✓ 已进入商家中心")
    except Exception as e:
        print(f"⚠️  自动进入失败，请手动点击【全球（除欧区、美国）】下的【进入 >】")
        input("   完成后按回车...")


def enter_reconciliation(driver):
    """进入对账中心"""
    print("\n=== 步骤 3: 进入对账中心 ===")
    try:
        wait_clickable(driver, "//span[contains(., '账户资金')]/..").click()
        time.sleep(3)
        wait_clickable(driver, "//span[contains(., '对账中心')]/..").click()
        time.sleep(8)
        print("✓ 已进入对账中心")
    except:
        print("⚠️  请手动点击左侧菜单【账户资金】→【对账中心】")
        input("   完成后按回车...")


def export_details(driver):
    """导出账务明细"""
    print(f"\n=== 步骤 4: 导出 {TARGET_MONTH} 账务明细 ===")

    year, month = TARGET_MONTH.split("-")
    date_range = f"{year}-{month}-01 ~ {year}-{month}-31"

    # 设置日期（如果需要）
    try:
        date_input = wait_element(driver, "//input[@type='text'][contains(@class, 'date')]")
        date_input.clear()
        date_input.send_keys(date_range)
    except:
        pass

    # 查询
    safe_click(driver, "//button[contains(., '查询')]", "【查询】", 10)

    # 导出
    safe_click(driver, "//button[contains(., '导出')]", "【导出】", 3)

    # 选择导出选项
    try:
        wait_clickable(driver, "//label[contains(., '导出列表 + 账务详情')]").click()
    except:
        pass

    # 确认
    safe_click(driver, "//button[contains(., '确认')]", "【确认】", 5)
    print("✓ 导出任务已提交")


def download_files(driver):
    """下载并重命名文件"""
    print("\n=== 步骤 5: 下载文件 ===")

    # 打开导出历史
    safe_click(driver, "//button[contains(., '导出历史')]", "【导出历史】", 8)

    # 下载全球站点
    print("\n--- 下载全球站点 ---")
    try:
        wait_clickable(driver,
                       "//button[contains(., '下载账务明细 (卖家中心)') or contains(., '下载账务明细')]").click()
        time.sleep(10)
        try:
            wait_clickable(driver, "//button[contains(., '我知道了')]").click()
        except:
            pass
        time.sleep(2)
        rename_file("财务明细")
    except Exception as e:
        print(f"⚠️  全球站点下载失败：{e}")

    # 下载美国站点
    print("\n--- 下载美国站点 ---")
    try:
        wait_clickable(driver, "//button[contains(., '下载财务明细 (美国)') or contains(., '下载 (美国)')]").click()
        time.sleep(5)

        # 处理授权
        try:
            for cb in driver.find_elements(By.XPATH, "//input[@type='checkbox']"):
                if not cb.is_selected():
                    cb.click()
            wait_clickable(driver, "//button[contains(., '确认授权') or contains(., '确认切换')]").click()
        except:
            pass

        time.sleep(15)
        try:
            wait_clickable(driver, "//button[contains(., '我知道了')]").click()
        except:
            pass
        time.sleep(10)
        rename_file("财务明细 us")
    except Exception as e:
        print(f"⚠️  美国站点下载失败：{e}")


def rename_file(base_name):
    """重命名最新下载的文件"""
    time.sleep(2)
    exts = ['.xlsx', '.xls', '.csv']
    files = [f for f in DOWNLOAD_DIR.iterdir() if f.suffix.lower() in exts]

    if not files:
        print("⚠️  未找到新文件")
        return

    latest = max(files, key=lambda f: f.stat().st_mtime)
    new_name = f"{base_name}_{TARGET_MONTH}{latest.suffix}"
    new_path = DOWNLOAD_DIR / new_name

    # 避免重名
    counter = 1
    while new_path.exists():
        new_name = f"{base_name}_{TARGET_MONTH}_{counter}{latest.suffix}"
        new_path = DOWNLOAD_DIR / new_name
        counter += 1

    shutil.move(str(latest), str(new_path))
    print(f"✓ 已重命名：{new_name}")


# ==================== 主函数 ====================

def main():
    print("=" * 50)
    print("跨境卖家后台财务报表自动下载工具")
    print("=" * 50)
    print(f"账号：{USERNAME}")
    print(f"月份：{TARGET_MONTH}")
    print(f"下载目录：{DOWNLOAD_DIR}")
    print("=" * 50)

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    driver = None

    try:
        driver = setup_driver()
        driver.get(LOGIN_URL)
        time.sleep(3)

        if not login(driver):
            print("❌ 登录失败")
            return

        enter_seller_center(driver)
        enter_reconciliation(driver)
        export_details(driver)
        download_files(driver)

        print("\n" + "=" * 50)
        print("✅ 完成！文件已下载到：")
        print(f"   {DOWNLOAD_DIR}")
        print("=" * 50)

    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
### 2. 安装依赖（在 PyCharm 的 Terminal 里）
# ```bash
# pip install selenium webdriver - manager
# ### 3. 修改配置（如果需要）
# 代码顶部的配置区可以改：
# ```python
# USERNAME = "15818779524"  # 改成你的账号
# PASSWORD = "Amitofo202409"  # 改成你的密码
# TARGET_MONTH = "2026-03"  # 改成你要的月份
# ### 4. 运行
# - 右键代码区 → Run
# 'download_finance_reports'
# - 或点顶部绿色三角形 ▶️
# ### 5. 流程说明
# 1.浏览器自动打开 → 输入账号密码
# 2. ** 暂停等你手动输入短信验证码 **
# 3.你在网页登录成功后，在PyCharm 底部输入# `y`回车
# 4.# 脚本自动完成后续所有步骤
# 5.# 文件下载到你的~ / Downloads`# 文件夹
