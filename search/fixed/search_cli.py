#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音搜索命令行工具 (修复版)
@Date       : 2025/04/13
@Author     : Claude
@License    : MIT License
-------------------------------------------------
"""

import sys
import argparse
import os
import logging
from rich.console import Console
from search_douyin import DouyinSearcher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('search_cli')

console = Console()

def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description="抖音关键词搜索和下载工具")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-c", "--count", type=int, default=10, help="搜索数量，默认10")
    parser.add_argument("-d", "--dir", help="下载目录，默认使用配置文件中的目录")
    parser.add_argument("--cookie", help="抖音cookie")
    parser.add_argument("--auto-cookie", action="store_true", help="自动获取cookie")
    parser.add_argument("--save-only", action="store_true", help="仅保存到文件不尝试下载")
    parser.add_argument("--no-server", action="store_true", help="不使用本地签名服务器")
    parser.add_argument("--debug", action="store_true", help="启用调试模式")
    parser.add_argument("--web-mode", action="store_true", help="使用网页版模式请求")
    parser.add_argument("--mobile-mode", action="store_true", help="使用移动版模式请求")
    
    args = parser.parse_args()
    
    try:
        # 设置日志级别
        if args.debug:
            logging.getLogger('douyin_search').setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)
            logger.debug("启用调试模式")
        
        # 检查服务器状态
        if not args.no_server:
            try:
                import requests
                response = requests.get("http://localhost:8889/", timeout=3)
                if response.status_code == 200:
                    logger.info("本地签名服务器运行正常")
                else:
                    logger.warning(f"本地签名服务器响应异常: {response.status_code}")
            except Exception as e:
                logger.warning(f"无法连接本地签名服务器: {str(e)}")
                console.print("[bold yellow]提示: 如果搜索失败，请先启动本地签名服务器[/bold yellow]")
                console.print("[bold cyan]cd E:\\code_learning\\douyindownload\\TikTokDownload[/bold cyan]")
                console.print("[bold cyan]python Server\\Server.py[/bold cyan]")
                
                # 询问用户是否强制继续
                if not args.debug:  # 开发模式下不询问
                    confirm = input("签名服务器未启动，是否强制继续搜索? (y/n): ").strip().lower()
                    if confirm != 'y':
                        console.print("[bold yellow]已取消搜索，请先启动签名服务器[/bold yellow]")
                        return 0
        
        # 创建搜索器实例
        searcher = DouyinSearcher(
            cookie=args.cookie, 
            auto_cookie=args.auto_cookie,
            use_local_server=not args.no_server
        )
        
        # 设置请求模式
        if args.mobile_mode:
            logger.info("使用移动版模式请求")
            searcher.use_mobile_mode = True
        elif args.web_mode:
            logger.info("使用网页版模式请求")
            searcher.use_web_mode = True
            
        # 执行搜索
        search_results = searcher.search(args.keyword, args.count)
        
        if not search_results:
            console.print("[bold red]搜索未找到任何结果[/bold red]")
            return 1
        
        # 显示搜索结果
        console.print("[bold green]搜索结果:[/bold green]")
        for idx, video in enumerate(search_results):
            console.print(f"[{idx+1}] {video['desc'][:50]}... - 作者: {video['author']} - 点赞: {video['like_count']}")
        
        # 检查是否仅保存
        if args.save_only:
            searcher.download_videos(search_results, args.dir, save_to_file=True)
            return 0
        
        # 询问是否下载
        confirmation = input("\n是否下载这些视频? (y/n): ").strip().lower()
        if confirmation != 'y':
            console.print("[bold yellow]已取消下载[/bold yellow]")
            # 仍然保存到文件
            searcher.download_videos(search_results, args.dir, save_to_file=True)
            return 0
        
        # 下载视频
        searcher.download_videos(search_results, args.dir, save_to_file=False)
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[bold yellow]操作已取消[/bold yellow]")
        return 1
    except Exception as e:
        console.print(f"[bold red]发生错误: {str(e)}[/bold red]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
