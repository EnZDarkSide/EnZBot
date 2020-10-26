from src.bot import bot


async def move_to_branch(peer_id: int, branch_name: str, **kwargs):
    await bot.branch.exit(peer_id)
    await bot.branch.add(peer_id, branch_name, **kwargs)