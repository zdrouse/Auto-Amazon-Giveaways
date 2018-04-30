import asyncio
from lib.giveaway import GiveAwayBot

async def main():
    ga_bot = GiveAwayBot()
    ga_page = await ga_bot.login()
    await ga_bot.process_giveaways(ga_page)

asyncio.get_event_loop().run_until_complete(main())