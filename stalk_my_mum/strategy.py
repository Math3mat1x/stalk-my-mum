from .infos import Coordinates
from . import following, lookup_dict, iphone
from .alert import alert
import time
import asyncio

# class iPhone():
#     def __init__(self,iphone_api):
#         self.locations = list()
#         self.iphone_api = iphone_api

#     async def update(self):
#         refresh = False

#         if len(self.locations) >= 2:
#             timestamp1, a1, b1 = self.location[0], self.location[-1]
#             timestamp2, a2, b2 = self.location[0], self.location[-2]

#             if timestamp2 - timestamp1 <= 60:
#                 distance = Coordinates((a1, b1), (a2, b2))
#                 if distance <= 30:
#                     return None

#         loop = asyncio.get_event_loop()
#         iphone = await loop.run_in_executor(None, self.iphone_api.iphone.location)
#         self.locations.append((time.time(), iphone[0], iphone[1]))

#         return iphone

class DefaultStrategy():
    """
    Default Strategy.
    """

    def __init__(self, iphone_api, fmf_api, friend):
        """
        Initialize the object.
        Input:
            iphone_api: PyiCloud object
            fmf_api: Find My Friend Object
            friend: email or phone_number of friend
        """

        self.friend_email = lookup_dict[friend] if friend in lookup_dict.keys() else friend
        print(f"Creating {self.friend_email}...")
        self.iphone_api = iphone_api
        self.fmf_api = fmf_api
        self.friend_id = following[friend]
        self.coordinates = Coordinates()
        self.near_friend = False
        self.count = int()

    async def _refresh(self):
        """
        If your friend is within 2 km of you, call the alert() function.

        Returns:
            bool: was alert() called?
        """

        # loop.run_in_excutor makes PyiCloud asynchronous, right??
        loop = asyncio.get_event_loop()
        phone = await iphone.update()
        # iphone = await loop.run_in_executor(None, self.iphone_api.iphone.location)
        self.iphone = (phone["longitude"], phone["latitude"])

        await loop.run_in_executor(None, self.fmf_api.refresh_client)
        friend = self.fmf_api.location_of(self.friend_id)

        # If able to receive the location of the friend
        if friend:
            self.count = int()
            self.friend = (friend["longitude"], friend["latitude"])
            
            self.coordinates.update(self.iphone, self.friend)
        # Otherwise, wait
        else:
            if self.count == 4:
                print(f"Unable to find {self.friend_email}")
            await asyncio.sleep(5)
            self.count += 1
            await self._refresh()

    async def alert(self):
        # If you're near the friend, wait 30 minutes before the next refresh
        if self.near_friend:
            print(f"You're near {self.friend_email}, sleeping for 30 minutes.")
            await asyncio.sleep(30 * 60)

        start_time = time.time()
        await self._refresh()

        # Check if you have coordinates
        try:
            await self.coordinates.distance
        except AttributeError:
            return None

        # If the friend is located at less than 2 km from you
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
