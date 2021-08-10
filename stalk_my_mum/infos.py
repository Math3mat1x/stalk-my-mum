from math import radians, sin, cos, atan2, sqrt
# import requests
import aiohttp
import asyncio
import polyline
import json

class Coordinates:
    def __init__(self, a=None, b=None):
        if a and b:
            self.update(a, b)
        self.record = dict()

    def update(self, a, b):
        self.lat1, self.lng1 = a
        self.lat2, self.lng2 = b

    def find_distance(self):
        earth_radius = 6371000 # metters
        dLat = radians(self.lat2 - self.lat1)
        dLng = radians(self.lng2 - self.lng1)
        a = sin(dLat / 2) * sin(dLat / 2) + \
            cos(radians(self.lat1)) * cos(radians(self.lat2)) * \
            sin(dLng/2) * sin(dLng/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return round(earth_radius * c, ndigits=1)

    async def travel(self):
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
        return ";".join([",".join([str(i), str(j)]) for i,j in [(self.lat1, self.lng1), (self.lat2, self.lng2)]])

    @property
    async def distance(self):
        return self.find_distance()

    @property
    async def time(self):
        index = self._get_index_record()
        if not index in self.record.keys():
            self.record[index] = await self.travel()

        return self.record[index]["duration"]

    @property
    async def travel_distance(self):
        index = self._get_index_record()
        if not index in self.record.keys():
            self.record[index] = await self.travel()

        return self.record[index]["distance"]
