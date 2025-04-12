#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 抖音搜索功能示例
@Date       : 2025/04/13
@Author     : Claude
@License    : MIT License
-------------------------------------------------
"""

from search_douyin import DouyinSearcher

def basic_search_example():
    """基本搜索示例"""
    print("=== 基本搜索示例 ===")
    
    # 创建搜索器实例，使用自动获取cookie
    searcher = DouyinSearcher(auto_cookie=True)
    
    # 搜索关键词"科技"，获取前5个结果
    results = searcher.search("科技", max_count=5)
    
    # 打印搜索结果
    print(f"共找到 {len(results)} 个视频:")
    for idx, video in enumerate(results):
        print(f"[{idx+1}] {video['desc'][:30]}... - 作者: {video['author']} - 点赞数: {video['like_count']}")
    
    print("\n")

def search_and_download_example():
    """搜索并下载示例"""
    print("=== 搜索并下载示例 ===")
    
    # 创建搜索器实例，使用自动获取cookie
    searcher = DouyinSearcher(auto_cookie=True)
    
    # 搜索并下载视频
    search_results, download_results = searcher.search_and_download(
        keyword="美食", 
        max_count=3,
        download_dir="downloads"
    )
    
    # 检查下载结果
    success_count = sum(1 for r in download_results if r["success"])
    print(f"下载结果: {success_count}/{len(download_results)} 成功")

def search_with_manual_cookie_example():
    """使用手动提供的cookie搜索示例"""
    print("=== 使用手动提供的cookie搜索示例 ===")
    
    # 这里需要替换为真实的cookie
    cookie = "把你的cookie字符串粘贴在这里"
    
    # 创建搜索器实例，使用手动提供的cookie
    searcher = DouyinSearcher(cookie=cookie)
    
    # 搜索关键词
    results = searcher.search("旅行", max_count=5)
    
    # 打印搜索结果
    print(f"共找到 {len(results)} 个视频")

if __name__ == "__main__":
    # 运行示例
    try:
        basic_search_example()
        # 取消注释下面的行来运行更多示例
        # search_and_download_example()
        # search_with_manual_cookie_example()
    except Exception as e:
        print(f"示例运行出错: {str(e)}")
