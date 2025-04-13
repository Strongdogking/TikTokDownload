# 抖音视频搜索工具 (修复版)

这是对原版搜索工具的修复版本，解决了编码问题和一些异常处理问题。

## 主要修复

1. 修复了 `UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 8360: illegal multibyte sequence` 错误
   - 改用 `subprocess.Popen` 并使用 UTF-8 编码处理子进程输出
   - 添加了错误容忍处理，避免编码问题导致程序崩溃

2. 修复了 `'NoneType' object is not subscriptable` 错误
   - 改进异常处理流程
   - 添加了更多数据验证

## 使用方法

### 作为命令行工具使用

```bash
# 基本用法
python search_cli.py 旅行

# 高级用法：指定搜索数量和下载目录
python search_cli.py 旅行 -c 20 -d ./downloads

# 仅保存视频信息到文件，不尝试下载
python search_cli.py 旅行 --save-only

# 使用自动获取cookie（需要安装f2库）
python search_cli.py 旅行 --auto-cookie

# 手动指定cookie
python search_cli.py 旅行 --cookie "your_cookie_here"
```

### 在代码中使用

```python
from search_douyin import DouyinSearcher

# 创建搜索器实例
searcher = DouyinSearcher()

# 搜索视频
results = searcher.search("旅行", max_count=10)

# 下载视频
searcher.download_videos(results, download_dir="./downloads")

# 或者仅保存信息
searcher.download_videos(results, save_to_file=True)
```

### 示例程序

可以运行示例程序来体验完整功能：

```bash
python example.py
```

## 注意事项

1. 首次搜索时可能会自动尝试使用本地服务生成签名参数，如果出现错误，请先确保已正确配置并启动本地服务：
   ```bash
   cd E:\code_learning\douyindownload\TikTokDownload
   python Server\Server.py
   ```

2. 下载功能依赖TikTokTool.py主程序，请确保工作目录中存在该文件。

3. 如果使用F2下载功能，需要正确配置F2。

## 依赖项

- requests
- rich
- f2 (可选，用于自动获取cookie)
