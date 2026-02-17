"""
CLI 輸出格式化
"""
import json
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax


console = Console()


def print_success(message: str) -> None:
    """打印成功消息"""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """打印錯誤消息"""
    console.print(f"[red]✗[/red] {message}")


def print_info(message: str) -> None:
    """打印信息消息"""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_warning(message: str) -> None:
    """打印警告消息"""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_table(
    data: List[Dict[str, Any]],
    title: str = "",
    headers: List[str] = None,
) -> None:
    """打印表格"""
    if not data:
        print_warning("沒有數據")
        return

    if headers is None:
        headers = list(data[0].keys())

    table = Table(title=title)

    for header in headers:
        table.add_column(header, style="cyan")

    for row in data:
        table.add_row(*[str(row.get(h, "")) for h in headers])

    console.print(table)


def print_json(data: Dict[str, Any] | List[Any]) -> None:
    """打印 JSON 數據"""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=False)
    console.print(syntax)


def print_memory(memory: Dict[str, Any]) -> None:
    """打印記憶詳情"""
    panel_content = f"""
[bold]ID:[/bold] {memory.get('id', 'N/A')}
[bold]類型:[/bold] {memory.get('type', 'N/A')}
[bold]分類:[/bold] {memory.get('category', 'N/A')}
[bold]可見性:[/bold] {memory.get('visibility', 'N/A')}
[bold]內容:[/bold]
{memory.get('content', 'N/A')[:200]}...
[bold]創建時間:[/bold] {memory.get('created_at', 'N/A')}
"""
    panel = Panel(panel_content, title="記憶詳情")
    console.print(panel)


def print_search_results(results: Dict[str, Any]) -> None:
    """打印搜索結果"""
    search_results = results.get("results", [])

    if not search_results:
        print_warning("未找到相關記憶")
        return

    console.print(f"\n[bold]搜索結果 ({len(search_results)} 條)[/bold]\n")

    for i, result in enumerate(search_results, 1):
        score = result.get("similarity_score", 0)
        content = result.get("content", "")[:80]
        console.print(f"{i}. [{score:.1%}] {content}...")

    stats = {
        "查詢嵌入時間": f"{results.get('query_embedding_time_ms', 0)}ms",
        "搜索時間": f"{results.get('search_time_ms', 0)}ms",
    }

    table = Table(title="性能統計")
    table.add_column("指標", style="cyan")
    table.add_column("值", style="green")

    for key, value in stats.items():
        table.add_row(key, value)

    console.print(table)
