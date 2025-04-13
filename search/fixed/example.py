#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音搜索示例
@Date       : 2025/04/13
@Author     : Claude
@License    : MIT License
-------------------------------------------------
"""

from search_douyin import DouyinSearcher
from rich.console import Console

console = Console()

def main():
    # 创建搜索器实例
    searcher = DouyinSearcher(auto_cookie=True)
    
    # 查询关键词
    keyword = input("请输入要搜索的关键词: ")
    count = int(input("要搜索多少个视频 (默认10): ") or "10")
    
    # 搜索视频
    console.print(f"[cyan]开始搜索关键词: [bold]{keyword}[/bold][/cyan]")
    results = searcher.search(keyword, count)
    
    if not results:
        console.print("[bold red]没有找到相关视频[/bold red]")
        return
    
    # 显示搜索结果
    console.print(f"[bold green]搜索结果 (共{len(results)}个):[/bold green]")
    for idx, video in enumerate(results, 1):
        console.print(f"[{idx}] {video['desc'][:50]}... - 作者: {video['author']} - 点赞数: {video['like_count']}")
    
    # 询问是否下载
    download = input("\n是否下载这些视频? (y/n): ").lower() == 'y'
    if download:
        # 指定下载目录
        download_dir = input("下载目录 (留空使用默认): ")
        if not download_dir:
            download_dir = None
            
        # 下载视频
        searcher.download_videos(results, download_dir, save_to_file=not download)
    else:
        console.print("[yellow]将视频信息保存到文件中[/yellow]")
        searcher.download_videos(results, save_to_file=True)
    
    console.print("[bold green]操作完成[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]操作已取消[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]发生错误: {str(e)}[/bold red]")
