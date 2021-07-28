from math import radians, sin, cos, atan2, sqrt
import requests
import polyline
import json

class Coordinates:
    def __init__(self, a, b):
        self.update(a, b)

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

    def travel(self):
        a = (self.lat1, self.lng1)
        b = (self.lat2, self.lng2)

        url = "http://router.project-osrm.org/table/v1/driving/polyline(" + \
                polyline.encode([b, a]) + ")"

        response = requests.get(url, {"sources": 0, "destinations": 1, \
                "annotations": "duration,distance"})

        response = json.loads(response.text)
    
        return {"duration": response["durations"][0][0],\
                "distance": response["distances"][0][0]}

    @property
    def distance(self):
        return self.find_distance()

    @property
    def time(self):
        return self.travel()["duration"]

    @property
    def travel_distance(self):
        return self.travel()["distance"]
