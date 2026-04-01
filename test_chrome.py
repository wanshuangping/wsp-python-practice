import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome", headless=False)
        page = await browser.new_page()
        await page.goto("https://www.baidu.com")
        print("浏览器已打开，5秒后关闭...")
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())