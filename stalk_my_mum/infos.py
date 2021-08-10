from math import radians, sin, cos, atan2, sqrt
import aiohttp
import asyncio
import polyline
import json

class Coordinates:
    """
    Gives distance or travel distance between two given coordinates.
    """

    def __init__(self, a=None, b=None):
        """
        Initilize the object.
        Input:
            a (opt, iter): first coordinates
            b (opt, iter): second coordinates
        """

        if a and b:
            self.update(a, b)
        self.record = dict()

    def update(self, a, b):
        """
        Updates the coordinates.
        Input:
            a (iter): first coordinates
            b (iter): second coordinates
        """
        self.lat1, self.lng1 = a
        self.lat2, self.lng2 = b

    def find_distance(self):
        """
        Computes the as the birds fly distance between the two coordinates.
        Returns:
            distance (float): distance between the two coordinates in metters.
        """

        earth_radius = 6371000 # metters
        dLat = radians(self.lat2 - self.lat1)
        dLng = radians(self.lng2 - self.lng1)
        a = sin(dLat / 2) * sin(dLat / 2) + \
            cos(radians(self.lat1)) * cos(radians(self.lat2)) * \
            sin(dLng/2) * sin(dLng/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return round(earth_radius * c, ndigits=1)

    async def travel(self):
        """
        Uses OSRM's test server to compute the travel distance and time between
        the two coordinates.
        Returns:
            infos (dict): duration and distance
        """

        a = (self.lng1, self.lat1)
        b = (self.lng2, self.lat2)

        url = "http://router.project-osrm.org/table/v1/driving/polyline(" + \
                polyline.encode([b, a]) + ")"

        payload = {"sources": 0, "destinations": 1, "annotations": "duration,distance"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as response:
                response = await response.text()

        response = json.loads(response)
    
        return {"duration": response["durations"][0][0],\
                "distance": response["distances"][0][0]}
    
    def _get_index_record(self):
        """
        Formats the coordinates to create a dict index for self.record.
        Returns:
            str : lat1,lng2;lat2,lng2
        """

        return ";".join([",".join([str(i), str(j)]) for i,j in [(self.lat1, self.lng1), (self.lat2, self.lng2)]])

    @property
    async def distance(self):
        """
        Returns the as the birds fly distance.
        """
        return self.find_distance()

    @property
    async def time(self):
        """
        Returns the time that the shortest route would take.
        """

        index = self._get_index_record()
        if not index in self.record.keys():
            self.record[index] = await self.travel()

        return self.record[index]["duration"]

    @property
    async def travel_distance(self):
        """
        Returns the distance that the shortest route would take.
        """

        index = self._get_index_record()
        if not index in self.record.keys():
            self.record[index] = await self.travel()

        return self.record[index]["distance"]
