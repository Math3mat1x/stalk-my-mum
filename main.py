from stalk_my_mum import following, DefaultStrategy, iphone_api, fmf_api
import asyncio

async def singular(strategy):
    """
    Infinite loop in which the chosen strategy runs.
    """
    while True:
        await strategy.alert()

async def run():
    strategies = [DefaultStrategy(iphone_api, fmf_api, email) for email in following.keys()]

    await asyncio.gather(*(singular(strategy) for strategy in strategies))

# Start
asyncio.run(run())
