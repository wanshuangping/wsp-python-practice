# 视频自动裁剪与批量处理工具 (Video Auto-Cutter)

### 1. 项目背景
本项目为实习生软件工程培养计划的第一个实操项目。主要功能是读取 CSV 配置文件中的运动类型及时间戳，对原始视频进行自动化的 9:16 竖屏裁剪和片段提取。

### 2. 技术栈
- **语言**: Python 3.12
- **核心库**: MoviePy (视频处理), Pandas (数据解析)
- **版本控制**: Git (GitHub)

### 3. 项目结构说明
- `data/`: 存放原始视频素材 (`.mp4`) 和任务清单 (`.csv`)。
- `src/core/`: 存放核心剪辑逻辑，如 `batch_processor.py`。
- `src/utils/`: 存放通用的读取工具。
- `tests/`: 存放开发过程中的实验性脚本。

### 4. 快速开始
1. **安装环境依赖**:
   ```bash
   pip install -r requirements.txt