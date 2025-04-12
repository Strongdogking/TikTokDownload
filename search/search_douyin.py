#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音搜索实现
@Date       : 2025/04/13
@Author     : Claude
@License    : MIT License
-------------------------------------------------
"""

import re
import json
import time
import random
import logging
import requests
import subprocess
from urllib.parse import quote, urlencode
from rich.console import Console
from rich.progress import Progress

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('douyin_search')

# Rich控制台显示
console = Console()

class DouyinSearcher:
    """抖音搜索类，支持通过关键词搜索抖音视频"""
    
    def __init__(self, cookie=None, auto_cookie=False):
        """
        初始化搜索类
        
        Args:
            cookie (str, optional): 抖音cookie字符串. Defaults to None.
            auto_cookie (bool, optional): 是否自动获取cookie. Defaults to False.
        """
        self.base_url = "https://www.douyin.com"
        self.search_url = "https://www.douyin.com/search/{}"
        self.api_search_url = "https://www.douyin.com/aweme/v1/web/search/item/"
        
        # 默认请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        
        # 设置cookie
        if cookie:
            self.headers["Cookie"] = cookie
        elif auto_cookie:
            self._auto_get_cookie()
    
    def _auto_get_cookie(self):
        """尝试使用TikTokDownload的自动cookie功能"""
        try:
            import f2
            from f2.apps.douyin.utils.cookie import get_cookie_from_browser
            
            cookie = get_cookie_from_browser(domain=".douyin.com")
            if cookie:
                self.headers["Cookie"] = cookie
                logger.info("成功自动获取抖音cookie")
            else:
                logger.warning("无法自动获取抖音cookie，搜索功能可能受限")
        except ImportError:
            logger.warning("未找到f2库，无法自动获取cookie，请手动提供cookie")
    
    def _check_network_connection(self):
        """
        检查网络连接状态
        """
        try:
            # 尝试访问抖音的域名
            response = requests.get("https://www.douyin.com", headers=self.headers, timeout=5)
            if response.status_code == 200:
                logger.info("网络连接正常")
                return True
            else:
                logger.warning(f"网络连接异常，状态码: {response.status_code}")
                raise Exception(f"网络连接异常，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"网络连接失败: {str(e)}")
            raise Exception(f"网络连接失败: {str(e)}")
    
    def _generate_signature(self, keyword, cursor="0"):
        """
        生成请求签名，这是一个示例实现
        实际使用中需要根据抖音最新的签名算法进行调整
        
        Args:
            keyword (str): 搜索关键词
            cursor (str, optional): 分页游标. Defaults to "0".

        Returns:
            dict: 包含签名的参数字典
        """
        try:
            # 尝试导入f2库中的XBogus生成函数
            from f2.apps.douyin.utils.xbogus import get_xbogus
            
            params = {
                "keyword": keyword,
                "count": "10",
                "cursor": cursor,
                "type": "1",  # 1表示视频
                "aid": "6383",
                "device_platform": "webapp",
                "from_page": "search"
            }
            
            query = urlencode(params)
            xbogus = get_xbogus(query)
            params["X-Bogus"] = xbogus
            
            return params
        except ImportError:
            # 如果没有f2库，使用Server.py的服务生成签名
            logger.info("尝试使用本地Server服务生成XBogus参数")
            try:
                params_str = f"keyword={quote(keyword)}&count=10&cursor={cursor}&type=1&aid=6383&device_platform=webapp&from_page=search"
                response = requests.get(f"http://localhost:8889/xg/path/?url={quote(params_str)}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status_code") == "200":
                        result = data.get("result", [{}])[0]
                        params = result.get("params", {})
                        return params
            except:
                logger.warning("无法使用本地Server服务生成签名，搜索可能失败")
            
            # 退化方案：返回基本参数，但可能无法正常工作
            return {
                "keyword": keyword,
                "count": "10",
                "cursor": cursor,
                "type": "1",
                "aid": "6383",
                "device_platform": "webapp",
                "from_page": "search"
            }
    
    def search(self, keyword, max_count=20, max_retries=3):
        """
        搜索抖音视频
        
        Args:
            keyword (str): 搜索关键词
            max_count (int, optional): 最大获取数量. Defaults to 20.
            max_retries (int, optional): 最大重试次数. Defaults to 3.
            
        Returns:
            list: 搜索结果列表，每个元素包含视频信息
        """
        console.print(f"[bold green]开始搜索关键词:[/bold green] [bold yellow]{keyword}[/bold yellow]")
        
        results = []
        cursor = "0"
        retry_count = 0
        
        with Progress() as progress:
            search_task = progress.add_task("[cyan]搜索中...", total=max_count)
            
            while len(results) < max_count:
                try:
                    # 生成请求参数
                    params = self._generate_signature(keyword, cursor)
                    
                    # 发送请求
                    response = requests.get(
                        self.api_search_url, 
                        headers=self.headers,
                        params=params,
                        timeout=10
                    )
                    
                    # 检查响应状态
                    if response.status_code != 200:
                        logger.warning(f"搜索请求失败，状态码: {response.status_code}")
                        retry_count += 1
                        if retry_count >= max_retries:
                            break
                        time.sleep(2 + random.random() * 3)
                        continue
                    
                    # 解析响应数据
                    data = response.json()
                    
                    # 提取视频信息
                    items = data.get("data", [])
                    if not items:
                        logger.info("没有更多结果或搜索结束")
                        break
                    
                    # 处理每个视频项
                    for item in items:
                        if len(results) >= max_count:
                            break
                            
                        # 确保是视频类型
                        if item.get("type") != 1:  # 1代表视频
                            continue
                            
                        aweme = item.get("aweme_info", {})
                        if not aweme:
                            continue
                            
                        # 提取需要的信息
                        video_info = {
                            "aweme_id": aweme.get("aweme_id", ""),
                            "desc": aweme.get("desc", "无描述"),
                            "create_time": aweme.get("create_time", 0),
                            "author": aweme.get("author", {}).get("nickname", "未知作者"),
                            "like_count": aweme.get("statistics", {}).get("digg_count", 0),
                            "comment_count": aweme.get("statistics", {}).get("comment_count", 0),
                            "share_url": f"https://www.douyin.com/video/{aweme.get('aweme_id', '')}"
                        }
                        
                        # 仅添加有效ID的结果
                        if video_info["aweme_id"]:
                            results.append(video_info)
                            progress.update(search_task, advance=1)
                    
                    # 更新游标
                    cursor = str(data.get("cursor", 0))
                    if cursor == "0" or not items:
                        logger.info("搜索结束，没有更多结果")
                        break
                        
                    # 添加随机延迟，避免被反爬
                    time.sleep(1 + random.random() * 2)
                    
                except Exception as e:
                    logger.error(f"搜索过程中出错: {str(e)}")
                    retry_count += 1
                    if retry_count >= max_retries:
                        break
                    time.sleep(2 + random.random() * 3)
        
        console.print(f"[bold green]搜索完成，共找到 {len(results)} 个视频[/bold green]")
        return results
    
    def download_videos(self, video_list, download_dir=None, save_to_file=True):
        """
        使用TikTokDownload下载视频
        
        Args:
            video_list (list): 视频信息列表
            download_dir (str, optional): 下载目录. Defaults to None.
            save_to_file (bool, optional): 是否将视频信息保存到文件. Defaults to True.
            
        Returns:
            list: 下载结果列表
        """
        if not video_list:
            console.print("[bold red]没有要下载的视频[/bold red]")
            return []
            
        console.print(f"[bold green]准备处理 {len(video_list)} 个视频[/bold green]")
        
        # 始终保存到文件，便于手动下载
        output_file = "douyin_videos.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# 抖音视频搜索结果\n")
            f.write("# 可以使用TikTokTool.py手动下载这些视频\n\n")
            
            for idx, video in enumerate(video_list):
                video_id = video["aweme_id"]
                video_url = video.get("share_url", f"https://www.douyin.com/video/{video_id}")
                f.write(f"{idx+1}. ID: {video_id}\n")
                f.write(f"   描述: {video['desc'][:100]}\n")
                f.write(f"   链接: {video_url}\n")
                f.write(f"   点赞数: {video.get('like_count', 0)}\n")
                f.write(f"   作者: {video.get('author', '未知')}\n\n")
        
        console.print(f"[bold green]已将视频信息保存到 {output_file}[/bold green]")
        
        # 如果只需要保存到文件，则不尝试下载
        if save_to_file:
            console.print("[bold yellow]可以使用以下命令手动下载视频:[/bold yellow]")
            console.print("[bold cyan]# 在正确的虚拟环境中运行：[/bold cyan]")
            console.print("[bold cyan]cd E:\\code_learning\\douyindownload\\TikTokDownload[/bold cyan]")
            console.print("[bold cyan]python TikTokTool.py 1 --vid <视频ID>[/bold cyan]")
            
            # 返回所有视频为未下载状态
            return [{
                "video_id": video["aweme_id"],
                "desc": video["desc"][:30],
                "success": False,
                "message": "已保存信息到文件，请手动下载"
            } for video in video_list]
        
        # 如果需要自动下载，则尝试下载
        try:
            # 获取当前运行的Python解释器路径
            import sys
            python_executable = sys.executable
            logger.info(f"使用Python解释器: {python_executable}")
            
            # 先检查网络连接
            self._check_network_connection()
            
            results = []
            with Progress() as progress:
                download_task = progress.add_task("[cyan]下载中...", total=len(video_list))
                
                for idx, video in enumerate(video_list):
                    video_id = video["aweme_id"]
                    
                    console.print(f"[{idx+1}/{len(video_list)}] 开始下载: {video['desc'][:30]}...")
                    
                    # 构建命令
                    cmd = [python_executable, "TikTokTool.py", "1"]  # 选择抖音
                    
                    # 添加下载目录参数
                    if download_dir:
                        cmd.extend(["--dir", download_dir])
                    
                    # 添加视频ID
                    cmd.extend(["--vid", video_id])
                    
                    # 执行命令
                    try:
                        process = subprocess.run(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            cwd="E:\\code_learning\\douyindownload\\TikTokDownload"
                        )
                        
                        success = process.returncode == 0
                        results.append({
                            "video_id": video_id,
                            "desc": video["desc"][:30],
                            "success": success,
                            "message": "下载成功" if success else "下载失败"
                        })
                        
                        if success:
                            logger.info(f"视频 {video_id} 下载成功")
                        else:
                            logger.warning(f"视频 {video_id} 下载失败: {process.stderr[:500]}...")
                            
                    except Exception as e:
                        logger.error(f"下载过程中出错: {str(e)}")
                        results.append({
                            "video_id": video_id,
                            "desc": video["desc"][:30],
                            "success": False,
                            "message": f"下载异常: {str(e)}"
                        })
                    
                    # 更新进度
                    progress.update(download_task, advance=1)
                    
                    # 添加随机延迟，避免被反爬
                    time.sleep(1 + random.random() * 2)
            
            # 统计下载结果
            success_count = sum(1 for r in results if r["success"])
            console.print(f"[bold green]下载完成: {success_count}/{len(results)} 成功[/bold green]")
            
            return results
            
        except Exception as e:
            logger.error(f"自动下载失败: {str(e)}")
            console.print(f"[bold red]自动下载失败: {str(e)}[/bold red]")
            console.print("[bold yellow]请使用文件中的信息手动下载视频。[/bold yellow]")
            
            # 返回所有视频为未下载状态
            return [{
                "video_id": video["aweme_id"],
                "desc": video["desc"][:30],
                "success": False,
                "message": f"下载失败: {str(e)}"
            } for video in video_list]

    def search_and_download(self, keyword, max_count=20, download_dir=None):
        """
        一键搜索并下载视频
        
        Args:
            keyword (str): 搜索关键词
            max_count (int, optional): 最大获取数量. Defaults to 20.
            download_dir (str, optional): 下载目录. Defaults to None.
            
        Returns:
            tuple: (搜索结果列表, 下载结果列表)
        """
        # 搜索视频
        search_results = self.search(keyword, max_count)
        
        if not search_results:
            console.print("[bold red]搜索未找到任何结果[/bold red]")
            return [], []
        
        # 显示搜索结果
        console.print("[bold green]搜索结果:[/bold green]")
        for idx, video in enumerate(search_results):
            console.print(f"[{idx+1}] {video['desc'][:50]}... - 作者: {video['author']} - 点赞: {video['like_count']}")
        
        # 询问是否下载
        confirmation = input("\n是否下载这些视频? (y/n): ").strip().lower()
        if confirmation != 'y':
            console.print("[bold yellow]已取消下载[/bold yellow]")
            return search_results, []
        
        # 下载视频
        download_results = self.download_videos(search_results, download_dir)
        
        return search_results, download_results


# 命令行入口点
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="抖音关键词搜索和下载工具")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-c", "--count", type=int, default=10, help="搜索数量，默认10")
    parser.add_argument("-d", "--dir", help="下载目录，默认使用配置文件中的目录")
    parser.add_argument("--cookie", help="抖音cookie")
    parser.add_argument("--auto-cookie", action="store_true", help="自动获取cookie")
    parser.add_argument("--save-only", action="store_true", help="仅保存到文件不下载")
    
    args = parser.parse_args()
    
    # 创建搜索器实例
    searcher = DouyinSearcher(cookie=args.cookie, auto_cookie=args.auto_cookie)
    
    # 搜索并下载
    search_results = searcher.search(args.keyword, args.count)
    
    if search_results:
        # 显示搜索结果
        console.print("[bold green]搜索结果:[/bold green]")
        for idx, video in enumerate(search_results):
            console.print(f"[{idx+1}] {video['desc'][:50]}... - 作者: {video['author']} - 点赞: {video['like_count']}")
        
        # 检查是否仅保存
        if args.save_only:
            searcher.download_videos(search_results, args.dir, save_to_file=True)
        else:
            # 询问是否下载
            confirmation = input("\n是否下载这些视频? (y/n): ").strip().lower()
            if confirmation == 'y':
                searcher.download_videos(search_results, args.dir, save_to_file=False)
            else:
                console.print("[bold yellow]已取消下载[/bold yellow]")
                # 仍然保存到文件
                searcher.download_videos(search_results, args.dir, save_to_file=True)
