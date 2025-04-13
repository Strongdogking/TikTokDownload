#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
诊断f2库安装情况
"""

import sys
import os
import subprocess
from rich.console import Console

console = Console()

def main():
    console.print("[bold blue]开始检查f2库安装情况...[/bold blue]")
    
    # 1. 检查Python环境
    console.print(f"[cyan]Python版本:[/cyan] {sys.version}")
    console.print(f"[cyan]Python路径:[/cyan] {sys.executable}")
    console.print(f"[cyan]当前工作目录:[/cyan] {os.getcwd()}")
    
    # 2. 检查是否已安装f2
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        output = result.stdout.lower()
        if "f2 " in output:
            console.print("[bold green]已在当前Python环境中找到f2库[/bold green]")
            for line in output.splitlines():
                if "f2 " in line:
                    console.print(f"[green]安装信息: {line.strip()}[/green]")
        else:
            console.print("[bold red]当前Python环境未安装f2库[/bold red]")
    except Exception as e:
        console.print(f"[bold red]检查安装的过程中出错: {str(e)}[/bold red]")
    
    # 3. 尝试导入f2
    console.print("\n[cyan]尝试直接导入f2库...[/cyan]")
    try:
        import f2
        console.print(f"[bold green]成功导入f2库![/bold green]")
        console.print(f"[green]f2版本: {f2.__version__ if hasattr(f2, '__version__') else '未知'}[/green]")
        console.print(f"[green]f2路径: {f2.__path__ if hasattr(f2, '__path__') else '未知'}[/green]")
    except ImportError as e:
        console.print(f"[bold red]导入f2库失败: {str(e)}[/bold red]")
    
    # 4. 检查sys.path
    console.print("\n[cyan]Python导入路径:[/cyan]")
    for i, path in enumerate(sys.path):
        console.print(f"  [{i+1}] {path}")
    
    # 5. 尝试导入抖音cookie模块
    console.print("\n[cyan]尝试导入抖音cookie模块...[/cyan]")
    try:
        from f2.apps.douyin.utils.cookie import get_cookie_from_browser
        console.print("[bold green]成功导入f2.apps.douyin.utils.cookie模块![/bold green]")
    except ImportError as e:
        console.print(f"[bold red]导入cookie模块失败: {str(e)}[/bold red]")
    
    # 6. 提供解决方案
    console.print("\n[bold yellow]可能的解决方案:[/bold yellow]")
    console.print("1. 确保在正确的虚拟环境中运行 (如果使用了虚拟环境)")
    console.print("2. 重新安装f2库:")
    console.print("   [cyan]pip uninstall f2[/cyan]")
    console.print("   [cyan]pip install f2[/cyan]")
    console.print("3. 检查是否有权限问题:")
    console.print("   [cyan]pip install f2 --user[/cyan]")
    console.print("4. 如果仍然无法解决，可以使用手动提供cookie的方式:")
    console.print("   [cyan]python search_cli.py 旅行 --cookie \"你的cookie值\"[/cyan]")

if __name__ == "__main__":
    main()
