"""
Temu半托管月度报表自动下载脚本 (Python + Playwright)
功能：自动登录、导航、下载并重命名报表
作者：AI Assistant
日期：2026-03-31
"""

import asyncio
import os
import shutil
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser, Download


class TemuReportDownloader:
    """Temu报表下载器"""
    
    def __init__(self):
        self.url = "https://seller.kuajingmaihuo.com/settle/site-main"
        self.download_dir = Path.home() / "Downloads"
        self.target_dir = Path.home() / "Documents" / "Temu报表"
        self.browser: Browser = None
        self.page: Page = None
        
    async def init_browser(self, headless: bool = False):
        """初始化浏览器"""
        print("🚀 启动浏览器...")
        playwright = await async_playwright().start()
        
        # 启动浏览器（非无头模式，方便观察）
        self.browser = await playwright.chromium.launch(
            headless=headless,
            slow_mo=100  # 操作间隔100ms
        )
        
        # 创建浏览器上下文，允许下载
        context = await self.browser.new_context(
            viewport={"width": 1440, "height": 900},
            accept_downloads=True
        )
        
        self.page = await context.new_page()
        print("✅ 浏览器启动成功")
        
    async def login(self):
        """登录Temu后台"""
        print(f"\n📱 访问登录页面: {self.url}")
        await self.page.goto(self.url, wait_until="domcontentloaded")
        
        # 等待用户手动登录
        print("\n" + "="*50)
        print("👉 请在浏览器中完成登录")
        print("👉 登录完成后，按回车键继续...")
        print("="*50)
        input()
        
        # 等待页面跳转
        await asyncio.sleep(2)
        print(f"✅ 登录成功，当前URL: {self.page.url}")
        
    async def navigate_to_export_history(self):
        """导航到导出历史页面"""
        print("\n📍 步骤1: 进入商家中心")
        
        # 点击全球(除欧区、美国)的进入按钮
        try:
            await self.page.click("text=全球(除欧区、美国) >> .. >> .enter-btn", timeout=5000)
        except:
            # 备用：直接导航到商家中心
            await self.page.goto("https://seller.kuajingmaihuo.com/main/main/main")
            
        await asyncio.sleep(10)  # 等待页面加载
        print("✅ 已进入商家中心")
        
        print("\n📍 步骤2: 进入对账中心")
        # 点击账户资金菜单
        await self.page.click("text=账户资金")
        await asyncio.sleep(3)
        
        # 点击对账中心子菜单
        await self.page.click("text=对账中心")
        await asyncio.sleep(8)
        print("✅ 已进入对账中心")
        
        print("\n📍 步骤3: 筛选并导出")
        # 确认日期范围
        date_input = await self.page.query_selector('input[placeholder*="日期"]')
        if date_input:
            await date_input.fill("2026-03-01 ~ 2026-03-31")
            
        # 点击查询
        await self.page.click("button:has-text('查询')")
        await asyncio.sleep(10)
        print("✅ 数据查询完成")
        
        # 点击导出按钮
        await self.page.click("button:has-text('导出')")
        await asyncio.sleep(3)
        
        # 选择导出选项
        await self.page.click("text=导出列表 + 账务详情")
        await self.page.click("button:has-text('确认')")
        await asyncio.sleep(5)
        print("✅ 导出任务已提交")
        
        # 进入导出历史页面
        await self.page.click("text=导出历史")
        await asyncio.sleep(8)
        print("✅ 已进入导出历史页面")
        
    async def download_reports(self):
        """下载报表文件"""
        print("\n📥 步骤4: 下载全球站点报表")
        
        # 设置下载监听
        async with self.page.expect_download() as download_info:
            # 点击下载按钮（第二条记录，3月份数据）
            buttons = await self.page.query_selector_all('button:has-text("下载账务明细(卖家中心)")')
            if len(buttons) >= 2:
                await buttons[1].click()  # 点击第二个（3月份那条）
            else:
                await self.page.click('button:has-text("下载账务明细(卖家中心)")')
                
        download: Download = await download_info.value
        
        # 等待下载完成
        file_path = await download.path()
        print(f"✅ 全球站点报表下载完成: {file_path}")
        
        # 重命名文件
        await self.rename_file(file_path, "财务明细.xlsx")
        
        print("\n📥 步骤5: 下载美国站点报表")
        
        async with self.page.expect_download() as download_info:
            # 点击美国站点下载按钮
            us_buttons = await self.page.query_selector_all('button:has-text("下载财务明细(美国)")')
            if len(us_buttons) >= 2:
                await us_buttons[1].click()
            else:
                await self.page.click('button:has-text("下载财务明细(美国)")')
                
        download: Download = await download_info.value
        file_path = await download.path()
        print(f"✅ 美国站点报表下载完成: {file_path}")
        
        # 重命名文件
        await self.rename_file(file_path, "财务明细 us.xlsx")
        
    async def rename_file(self, source_path: Path, new_name: str):
        """重命名并移动文件"""
        # 确保目标目录存在
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # 构建目标路径
        target_path = self.target_dir / new_name
        
        # 复制文件（保留原始下载）
        shutil.copy2(source_path, target_path)
        print(f"✅ 文件已保存: {target_path}")
        
    async def verify_files(self):
        """验证文件是否存在"""
        print("\n📋 步骤6: 验证下载结果")
        
        files = [
            self.target_dir / "财务明细.xlsx",
            self.target_dir / "财务明细 us.xlsx"
        ]
        
        all_exist = True
        for file in files:
            if file.exists():
                size = file.stat().st_size / 1024  # KB
                print(f"✅ {file.name} - {size:.1f} KB")
            else:
                print(f"❌ {file.name} - 未找到")
                all_exist = False
                
        return all_exist
        
    async def run(self):
        """运行完整的下载流程"""
        try:
            await self.init_browser(headless=False)
            await self.login()
            await self.navigate_to_export_history()
            await self.download_reports()
            
            if await self.verify_files():
                print("\n" + "="*50)
                print("🎉 任务完成！所有报表已下载并保存")
                print(f"📁 保存位置: {self.target_dir}")
                print("="*50)
            else:
                print("\n⚠️ 部分文件未找到，请检查下载状态")
                
        except Exception as e:
            print(f"\n❌ 执行出错: {str(e)}")
            raise
        finally:
            if self.browser:
                print("\n🔒 关闭浏览器...")
                await self.browser.close()
                

async def main():
    """主函数"""
    print("="*50)
    print("Temu半托管月度报表自动下载工具")
    print("="*50)
    
    downloader = TemuReportDownloader()
    await downloader.run()
    
    print("\n按回车键退出...")
    input()


if __name__ == "__main__":
    asyncio.run(main())
