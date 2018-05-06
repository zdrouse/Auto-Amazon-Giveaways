import asyncio
from lib.giveaway import GiveAwayBot

async def main():
    ga_bot = GiveAwayBot()
    # first ga page
    ga_page = await ga_bot.login()
    # recursive function to repeat bot tasks for every ga page
    async def do_ga_workflow(page):
        last_page = await ga_bot.check_for_last_page(page)
        while last_page is False:
            await ga_bot.process_giveaways(page)
            next_page = await ga_bot.iterate_page(page)
            await do_ga_workflow(next_page)
    # call recursive function to process all bot tasks.
    await do_ga_workflow(ga_page)

asyncio.get_event_loop().run_until_complete(main())