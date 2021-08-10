from .infos import Coordinates
from . import following
from .alert import alert
import time
import asyncio

class DefaultStrategy():
    """
    Default Strategy.
    """

    def __init__(self, iphone_api, fmf_api, friend):
        print(f"Creating {friend}...")
        self.iphone_api = iphone_api
        self.fmf_api = fmf_api
        self.friend_email = friend
        self.friend_id = following[friend]
        self.coordinates = Coordinates()
        self.near_friend = False
        self.time_refresh = 0 # time of last refresh

    async def _refresh(self):
        loop = asyncio.get_event_loop()
        iphone = await loop.run_in_executor(None, self.iphone_api.iphone.location)
        # iphone = self.iphone_api.iphone.location()
        self.iphone = (iphone["longitude"], iphone["latitude"])

        await loop.run_in_executor(None, self.fmf_api.refresh_client)
        friend = self.fmf_api.location_of(self.friend_id)
        if friend:
            self.friend = (friend["longitude"], friend["latitude"])
            
            self.coordinates.update(self.iphone, self.friend)
        else:
            print(self.friend_email)
            await asyncio.sleep(5)

    async def alert(self):
        # If you're near the friend, wait 30 minutes before the next refresh
        if self.near_friend:
            print(f"You're near {self.friend_email}, sleeping for 30 minutes.")
            await asyncio.sleep(30 * 60)

        start_time = time.time()
        await self._refresh()

        self.time_refresh = time.time()

        # If the friend is located at less than 2 km from you
        try:
            await self.coordinates.distance
        except AttributeError:
            return None

        if await self.coordinates.distance <= 2000:
            # If you are already near him, do not alert
            if self.near_friend:
                return False
            # If you weren't, do alert
            else:
                await alert(self.friend_email)
                self.near_friend = True
                return True
        # If you were near a friend but now he’s located at more than 2 km, reset
        elif self.near_friend:
            print(f"{self.friend_email} has moved away from you.")
            self.near_friend = False
            return False
        # Else wait
        else:
            duration = await self.coordinates.time
            duration = (duration - 4*60) / 2

            to_wait = duration - (time.time() - start_time)
            if to_wait < 0:
                return False

            print(f"{self.friend_email}: wait {to_wait} seconds.")
            await asyncio.sleep(to_wait)
            return False
