#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
使用保存的cookie进行抖音搜索
"""

import os
import sys
import subprocess
from rich.console import Console

console = Console()

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
    # 获取当前脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建cookie文件的绝对路径
    cookie_file = os.path.join(script_dir, "douyin_cookie.txt")
    
    # 加载cookie
    cookie = load_cookie_from_file(cookie_file)
    if not cookie:
        console.print("[bold red]无法加载cookie，请确保douyin_cookie.txt文件存在且不为空[/bold red]")
        return 1
    
    # 获取关键词参数
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = input("请输入要搜索的关键词: ").strip()
        if not keyword:
            console.print("[bold red]未提供搜索关键词[/bold red]")
            return 1
    
    # 构建搜索命令
    cmd = [
        sys.executable,  # 当前Python解释器
        "search_cli.py", 
        keyword,
        "--cookie", 
        cookie
    ]
    
    # 添加其他可选参数
    for arg in sys.argv[2:]:
        cmd.append(arg)
    
    # 执行搜索命令
    console.print(f"[bold green]开始搜索: {keyword}[/bold green]")
    
    try:
        process = subprocess.run(
            cmd,
            cwd=script_dir,
            check=True
        )
        return process.returncode
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]搜索过程出错: {str(e)}[/bold red]")
        return e.returncode
    except Exception as e:
        console.print(f"[bold red]发生错误: {str(e)}[/bold red]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
