#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音搜索命令行工具
@Date       : 2025/04/13
@Author     : Claude
@License    : MIT License
-------------------------------------------------
"""

import sys
import argparse
from rich.console import Console
from search_douyin import DouyinSearcher

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
    
    args = parser.parse_args()
    
    try:
        # 创建搜索器实例
        searcher = DouyinSearcher(cookie=args.cookie, auto_cookie=args.auto_cookie)
        
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
