from stalk_my_mum import following, DefaultStrategy, iphone_api, fmf_api
from settings import do_not_stalk_list
import asyncio

async def singular(strategy):
    """
    Infinite loop in which the chosen strategy runs.
    """
    while True:
        await strategy.alert()

async def run():
    strategies = [DefaultStrategy(iphone_api, fmf_api, email) for email in\
            following.keys() if not email in do_not_stalk_list]

    await asyncio.gather(*(singular(strategy) for strategy in strategies))

# Start
asyncio.run(run())
