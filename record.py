import googlemaps
from dotenv import load_dotenv
import os


load_dotenv()

class Record:

    def __init__(self, address, city, province, zip, delivery_day):
        self.address = address
        self.city = city
        self.province = province
        self.zip = zip
        self.delivery_day = delivery_day
 

    def __get_geocode(self):
        KEY = os.environ.get("KEY")

        gmaps = googlemaps.Client(key=KEY)
        
        gcode = gmaps.geocode(f"{self.address}, {self.city}, {self.province}")
        lat_long = gcode[0]["geometry"]["location"]

        return lat_long["lat"], lat_long["lng"]

    def __hash_zip(self):
        return hash(self.zip)

    def __label_dday(self):
        return {
            'ANY DAY': 0,
            'MON': 1,
            'TUES': 2,
            'WED': 3,
            'THURS': 4,
            'FRI': 5
        }[self.delivery_day]

    def return_val(self):
        lat, lng = self.__get_geocode()
        zip_hash = self.__hash_zip()
        del_day = self.__label_dday()

        return (lat, lng, zip_hash)
