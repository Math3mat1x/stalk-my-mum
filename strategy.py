from infos import Coordinates
import time

class Default():
    """
    Default Strategy.
    """

    def __init__(self, iphone_api, fmf_api, friend_id):
        self.iphone_api = iphone_api
        self.fmf_api = fmf_api
        self.friend_id = friend_id
        self.coordinates = Coordinates()
        self.near_friend = False
        self.time_refresh = 0 # time of last refresh

    def _refresh(self):
        iphone = self.iphone_api.iphone.location()
        self.iphone = (iphone["longitude"], iphone["latitude"])

        self.fmf_api.refresh_client()
        friend = self.fmf_api.location_of(self.friend_id)
        self.friend =  (friend["longitude"], friend["latitude"])
        
        self.coordinates.update(self.iphone, self.friend)

    def alert(self):
        # If you're near the friend, wait 30 minutes before the next refresh
        if self.near_friend:
            time.sleep(30 * 60)

        start_time = time.time()
        self._refresh()
        self.time_refresh = time.time()

        # If the friend is located at less than 2 km from you
        if self.coordinates.distance <= 2000:
            # If you are already near him, do not alert
            if self.near_friend:
                return False
            # If you weren't, do alert
            else:
                self.near_friend = True
                return True
        # If you were near a friend but now he’s located at more than 2 km, reset
        elif self.near_friend:
            self.near_friend = False
        # Else wait
        else:
            duration = self.coordinates.time
            duration = (duration - 4*60) / 2

            to_wait = duration - (time.time() - start_time)
            if to_wait < 0:
                return None

            time.sleep(to_wait)
            return False
