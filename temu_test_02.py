async def init_browser_with_profile(self, headless: bool = False):
    """使用本地 Chrome 用户数据目录（保留登录）"""
    print("🚀 尝试启动本地 Chrome 并加载用户数据...")

    # 自动检测常见路径（优先）
    possible_paths = [
        Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data",  # Windows
        Path.home() / "Library" / "Application Support" / "Google" / "Chrome",  # macOS
        Path.home() / ".config" / "google-chrome",  # Linux
    ]
    user_data_dir = None
    for p in possible_paths:
        if p.exists():
            user_data_dir = p
            break

    if not user_data_dir:
        print("❌ 未找到 Chrome 用户数据目录，请手动指定路径")
        return False

    print(f"📁 使用用户数据目录: {user_data_dir}")

    # 检查是否被占用
    lock_file = user_data_dir / "SingletonLock"
    if lock_file.exists():
        print("⚠️ 检测到 Chrome 可能正在运行，请关闭所有 Chrome 窗口后再试")
        input("按回车键继续尝试启动（确保已关闭 Chrome）...")

    self.playwright = await async_playwright().start()

    try:
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            channel="chrome",
            headless=headless,
            slow_mo=100,
            viewport={"width": 1440, "height": 900},
            accept_downloads=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-automation"
            ]
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        print("✅ 浏览器启动成功，保留登录状态")
        return True
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False