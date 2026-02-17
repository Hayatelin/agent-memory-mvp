"""
AgentMem CLI 主入口點
"""
import click
import uuid
from typing import Optional
from .config import Config
from .commands import Commands
from .formatter import print_success, print_error, print_info


@click.group()
@click.version_option("0.1.0", help="顯示版本號")
@click.pass_context
def cli(ctx):
    """AgentMem - 記憶管理工具

    使用 agentmem --help 查看幫助信息
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config()
    ctx.obj["commands"] = Commands(ctx.obj["config"])


@cli.command()
@click.pass_context
def config(ctx):
    """查看當前配置"""
    cfg = ctx.obj["config"]
    print_info("當前配置:")
    print_info(f"  API URL: {cfg.get('api_url')}")
    print_info(f"  Agent ID: {cfg.get('agent_id')}")
    print_info(f"  超時時間: {cfg.get('timeout')}s")
    print_info(f"  配置文件: {cfg.config_file}")


@cli.command()
@click.option("--api-url", help="API 服務器地址")
@click.option("--agent-id", help="Agent ID")
@click.option("--timeout", type=int, help="超時時間")
@click.pass_context
def configure(ctx, api_url, agent_id, timeout):
    """配置 AgentMem CLI"""
    cfg = ctx.obj["config"]

    if api_url:
        cfg.set("api_url", api_url)
        print_success(f"API URL 已設置: {api_url}")

    if agent_id:
        cfg.set("agent_id", agent_id)
        print_success(f"Agent ID 已設置: {agent_id}")

    if timeout:
        cfg.set("timeout", timeout)
        print_success(f"超時時間已設置: {timeout}s")

    if not any([api_url, agent_id, timeout]):
        print_error("請指定要配置的選項")


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="詳細模式")
@click.pass_context
def health(ctx, verbose):
    """檢查服務器健康狀態"""
    commands = ctx.obj["commands"]
    commands.health_check(verbose=verbose)


@cli.command()
@click.argument("content")
@click.option("--type", default="knowledge", help="記憶類型")
@click.option("--category", default="general", help="分類")
@click.option("--visibility", default="private", help="可見性")
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def create(ctx, content, type, category, visibility, output_json):
    """創建新記憶

    示例: agentmem create "Machine learning 基礎"
    """
    commands = ctx.obj["commands"]
    commands.create_memory(
        content=content,
        type=type,
        category=category,
        visibility=visibility,
        output_json=output_json,
    )


@cli.command()
@click.option("--limit", type=int, default=20, help="返回記錄數")
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def list(ctx, limit, output_json):
    """列出所有記憶

    示例: agentmem list --limit 10
    """
    commands = ctx.obj["commands"]
    commands.list_memories(limit=limit, output_json=output_json)


@cli.command()
@click.argument("memory_id")
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def get(ctx, memory_id, output_json):
    """獲取記憶詳情

    示例: agentmem get 123e4567-e89b-12d3-a456-426614174000
    """
    commands = ctx.obj["commands"]
    commands.get_memory(memory_id, output_json=output_json)


@cli.command()
@click.argument("query")
@click.option("--limit", type=int, default=10, help="返回結果數")
@click.option("--threshold", type=float, default=0.3, help="相似度閾值")
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def search(ctx, query, limit, threshold, output_json):
    """搜索記憶

    示例: agentmem search "人工智能" --limit 10
    """
    commands = ctx.obj["commands"]
    commands.search_memories(
        query=query,
        limit=limit,
        similarity_threshold=threshold,
        output_json=output_json,
    )


@cli.command()
@click.argument("memory_id")
@click.option("--content", help="新內容")
@click.option("--type", help="新類型")
@click.option("--category", help="新分類")
@click.option("--visibility", help="新可見性")
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def update(ctx, memory_id, content, type, category, visibility, output_json):
    """更新記憶

    示例: agentmem update 123e4567... --content "新內容"
    """
    commands = ctx.obj["commands"]
    commands.update_memory(
        memory_id=memory_id,
        content=content,
        type=type,
        category=category,
        visibility=visibility,
        output_json=output_json,
    )


@cli.command()
@click.argument("memory_id")
@click.pass_context
def delete(ctx, memory_id):
    """刪除記憶

    示例: agentmem delete 123e4567-e89b-12d3-a456-426614174000
    """
    commands = ctx.obj["commands"]
    if click.confirm(f"確定要刪除記憶 {memory_id[:8]}...?"):
        commands.delete_memory(memory_id)
    else:
        print_info("已取消")


@cli.command()
@click.argument("memory_id")
@click.argument("agent_id")
@click.pass_context
def share(ctx, memory_id, agent_id):
    """與另一個 Agent 共享記憶

    示例: agentmem share 123e4567... another-agent-uuid
    """
    commands = ctx.obj["commands"]
    commands.share_memory(memory_id, agent_id)


@cli.command()
@click.option("--json", "output_json", is_flag=True, help="輸出 JSON")
@click.pass_context
def stats(ctx, output_json):
    """顯示搜索統計信息

    示例: agentmem stats
    """
    commands = ctx.obj["commands"]
    commands.get_stats(output_json=output_json)


@cli.command()
@click.pass_context
def init(ctx):
    """初始化 AgentMem CLI

    生成新的 Agent ID 並配置 CLI
    """
    cfg = ctx.obj["config"]
    agent_id = str(uuid.uuid4())
    cfg.set("agent_id", agent_id)
    print_success("CLI 已初始化")
    print_success(f"Agent ID: {agent_id}")
    print_success(f"配置文件: {cfg.config_file}")


def main():
    """CLI 主函數"""
    try:
        cli()
    except Exception as e:
        print_error(f"發生錯誤: {e}")


if __name__ == "__main__":
    main()
