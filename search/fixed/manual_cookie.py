#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
手动获取抖音cookie工具
这个脚本提供了一种替代方法来获取抖音的cookie
"""

import os
import re
import sys
import json
import time
import platform
import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def get_chrome_data_path():
    """获取Chrome浏览器的用户数据目录路径"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
    elif system == "Darwin":  # macOS
        return os.path.join(os.environ["HOME"], "Library", "Application Support", "Google", "Chrome")
    elif system == "Linux":
        return os.path.join(os.environ["HOME"], ".config", "google-chrome")
    else:
        return None

def get_edge_data_path():
    """获取Edge浏览器的用户数据目录路径"""
    system = platform.system()
    
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data")
    elif system == "Darwin":  # macOS
        return os.path.join(os.environ["HOME"], "Library", "Application Support", "Microsoft Edge")
    elif system == "Linux":
        return os.path.join(os.environ["HOME"], ".config", "microsoft-edge")
    else:
        return None

def extract_cookies_from_sqlite(db_path, domain=".douyin.com"):
    """从SQLite Cookie数据库中提取指定域名的Cookie"""
    try:
        import sqlite3
        
        # 连接到数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询匹配域名的cookie
        cursor.execute(
            "SELECT name, value FROM cookies WHERE host_key LIKE ? OR host_key LIKE ?",
            (f"%{domain}", f"%.{domain}")
        )
        
        # 提取结果
        cookies = {}
        for name, value in cursor.fetchall():
            cookies[name] = value
        
        # 关闭连接
        conn.close()
        
        # 格式化为cookie字符串
        if cookies:
            return "; ".join([f"{name}={value}" for name, value in cookies.items()])
        return None
    except Exception as e:
        console.print(f"[red]从SQLite提取Cookie失败: {str(e)}[/red]")
        return None

def open_browser_and_guide():
    """打开浏览器并引导用户手动复制cookie"""
    system = platform.system()
    
    # 构建抖音URL
    url = "https://www.douyin.com/"
    
    # 根据操作系统选择打开方式
    try:
        if system == "Windows":
            os.system(f'start "" "{url}"')
        elif system == "Darwin":  # macOS
            os.system(f'open "{url}"')
        elif system == "Linux":
            os.system(f'xdg-open "{url}"')
        
        console.print("\n[bold yellow]请按照以下步骤手动获取Cookie:[/bold yellow]")
        console.print("1. 在打开的浏览器中登录抖音账号")
        console.print("2. 按F12或右键点击'检查'打开开发者工具")
        console.print("3. 切换到'网络(Network)'标签页")
        console.print("4. 刷新页面")
        console.print("5. 在请求列表中找到任意一个请求")
        console.print("6. 在右侧Headers中找到'Cookie:'一项")
        console.print("7. 右键点击Cookie值，选择'复制值'")
        console.print("8. 将复制的Cookie粘贴到下面的输入中")
        
        cookie = input("\n请粘贴Cookie值: ").strip()
        if cookie:
            # 验证cookie基本格式是否正确
            if "=" in cookie and ";" in cookie:
                return cookie
            else:
                console.print("[red]Cookie格式不正确，应该包含'='和';'符号[/red]")
        else:
            console.print("[red]未提供Cookie[/red]")
    except Exception as e:
        console.print(f"[red]打开浏览器失败: {str(e)}[/red]")
    
    return None

def save_cookie_to_file(cookie, filename="douyin_cookie.txt"):
    """保存Cookie到文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cookie)
        console.print(f"[green]Cookie已保存到 {filename}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]保存Cookie失败: {str(e)}[/red]")
        return False

def load_cookie_from_file(filename="douyin_cookie.txt"):
    """从文件加载Cookie"""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                cookie = f.read().strip()
            if cookie:
                console.print(f"[green]已从 {filename} 加载Cookie[/green]")
                return cookie
        console.print(f"[yellow]Cookie文件 {filename} 不存在或为空[/yellow]")
    except Exception as e:
        console.print(f"[red]加载Cookie失败: {str(e)}[/red]")
    
    return None

def main():
    console.print("[bold blue]抖音Cookie手动获取工具[/bold blue]")
    
    # 首先尝试从文件加载
    cookie = load_cookie_from_file()
    if cookie:
        # 验证cookie是否过期
        expiry_check = input("已找到保存的Cookie。是否重新获取? (y/n, 默认n): ").strip().lower()
        if expiry_check != 'y':
            return cookie
    
    # 尝试从Chrome获取
    console.print("\n[cyan]尝试从Chrome浏览器获取Cookie...[/cyan]")
    chrome_path = get_chrome_data_path()
    if chrome_path:
        console.print(f"Chrome用户数据目录: {chrome_path}")
        # 这里应该有从Chrome中提取cookie的逻辑，但由于复杂性，此处省略
        console.print("[yellow]自动从Chrome提取Cookie暂不可用[/yellow]")
    
    # 尝试从Edge获取
    console.print("\n[cyan]尝试从Edge浏览器获取Cookie...[/cyan]")
    edge_path = get_edge_data_path()
    if edge_path:
        console.print(f"Edge用户数据目录: {edge_path}")
        # 这里应该有从Edge中提取cookie的逻辑，但由于复杂性，此处省略
        console.print("[yellow]自动从Edge提取Cookie暂不可用[/yellow]")
    
    # 引导用户手动获取
    console.print("\n[cyan]尝试手动引导获取Cookie...[/cyan]")
    cookie = open_browser_and_guide()
    
    # 保存cookie
    if cookie:
        save_cookie_to_file(cookie)
    
    return cookie

if __name__ == "__main__":
    cookie = main()
    if cookie:
        console.print("[bold green]成功获取Cookie![/bold green]")
        # 显示cookie的前20个字符
        cookie_prefix = cookie[:20] if len(cookie) > 20 else cookie
        console.print(f"Cookie (前20个字符): {cookie_prefix}...")
        console.print("\n要在搜索工具中使用此Cookie，请运行:")
        console.print("[bold cyan]python search_cli.py 旅行 --cookie \"<上面获取的Cookie>\"[/bold cyan]")
    else:
        console.print("[bold red]获取Cookie失败[/bold red]")
