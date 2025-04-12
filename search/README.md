# 抖音关键词搜索模块

这个模块为TikTokDownload项目提供了通过关键词搜索抖音视频并批量下载的功能。

## 功能特点

- 通过关键词搜索抖音视频
- 批量下载搜索结果中的视频
- 支持自动获取cookie或手动提供cookie
- 可配置搜索结果数量和下载目录
- 提供命令行工具和Python API

## 使用方法

### 命令行使用

```bash
# 基本使用 - 搜索并下载关键词"旅行"的前10个视频
python search_cli.py 旅行

# 指定搜索数量和下载目录
python search_cli.py 美食 --count 20 --dir "./downloads/food"

# 仅搜索不下载
python search_cli.py 科技 --search-only

# 使用自动获取cookie
python search_cli.py 舞蹈 --auto-cookie

# 使用手动提供的cookie
python search_cli.py 游戏 --cookie "your_cookie_string_here"
```

### Python API使用

```python
from search.search_douyin import DouyinSearcher

# 创建搜索器实例
searcher = DouyinSearcher(auto_cookie=True)

# 搜索视频
results = searcher.search("旅行", max_count=10)

# 仅下载搜索到的视频
searcher.download_videos(results, download_dir="./downloads")

# 一键搜索并下载
search_results, download_results = searcher.search_and_download(
    keyword="美食",
    max_count=5,
    download_dir="./downloads"
)
```

## 参数说明

### DouyinSearcher类

- `cookie` (str, optional): 抖音cookie字符串
- `auto_cookie` (bool, optional): 是否自动获取cookie

### search方法

- `keyword` (str): 搜索关键词
- `max_count` (int, optional): 最大获取数量，默认20
- `max_retries` (int, optional): 最大重试次数，默认3

### download_videos方法

- `video_list` (list): 视频信息列表
- `download_dir` (str, optional): 下载目录

### search_and_download方法

- `keyword` (str): 搜索关键词
- `max_count` (int, optional): 最大获取数量，默认20
- `download_dir` (str, optional): 下载目录

## 注意事项

1. 需要有效的cookie才能正常搜索，可以使用`--auto-cookie`自动获取或手动提供
2. 抖音有反爬虫机制，频繁请求可能导致IP被限制
3. 下载视频需要保证TikTokDownload项目正常工作
4. 使用此工具下载视频时，请遵守相关法律法规和平台规定

## 示例

参考`example.py`文件了解更多使用示例。

## 依赖

- requests
- rich
- 以及TikTokDownload项目的依赖
