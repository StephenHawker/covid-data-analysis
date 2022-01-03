"""various distance calculations"""
import logging
import datetime
import googlemaps
import ssl
import haversine
from haversine import haversine
import math
from collections import defaultdict
from HelperFunctions import HelperFunctions


class DistanceCalc:

    ############################################################
    # constructor
    ############################################################
    def __init__(self, api_key):

        self.api_key = api_key
        self.helper_f = HelperFunctions()
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr("Distance Calc")

    ############################################################
    # Lookup travel time based on google for specified travel
    # time
    ############################################################
    def get_travel_time(self, start_point, end_point, dept_time):
        """Do API postcode lookup for travel time

        Keyword arguments:
        api_key -- URL for the API call
        start_point -- start point (lat,lon)
        end_point -- end point (lat,lon)
        dept_time -- departure time
        """
        ssl._create_default_https_context = ssl._create_unverified_context

        try:

            gmaps = googlemaps.Client(key=self.api_key)
            directions_result = gmaps.directions(start_point,  # ("52.141366,-0.479573",
                                                 end_point,  # "52.141366,-0.489573",
                                                 mode="driving",
                                                 avoid="ferries",
                                                 departure_time=dept_time)
            directions_dic = defaultdict(list)

            self.LOGGER.debug(directions_result)

            directions_dic["distance"].append(directions_result[0]['legs'][0]['distance']['text'])
            directions_dic["duration"].append(directions_result[0]['legs'][0]['duration']['text'])
            directions_dic["time"].append(dept_time)

            return directions_dic
        except Exception as exrec:
            self.LOGGER.error("Error in get_travel_time - please check: %s", str(exrec.data), exc_info=True)
            raise Exception("Error in get_travel_time")

    ############################################################
    # Get haversine distance
    ############################################################

    def get_haversine_dist(self, start_point, end_point):
        """get haversine distance betweent 2 points

        Keyword arguments:
        start_point -- start point
        end_point -- end point
        """

        dist = haversine(start_point, end_point, unit='mi')

        if math.isnan(dist):
            rv_value = 100000000
        else:
            rv_value = dist

        return rv_value

    ############################################################
    # Get a list of travel time for the nearest stations
    # at 2 different times
    ############################################################
    def get_travel_times(self, start_point, end_point):
        travel_times = []

        # Mon 8am
        current_time = datetime.datetime.now()
        new_period1 = current_time.replace(hour=8, minute=00, second=00, microsecond=0)

        # epoch next monday
        next_monday = self.helper_f.next_weekday(new_period1, 0).timestamp()  # 0 = Monday, 1=Tuesday, 2=Wednesday...

        current_time2 = datetime.datetime.now()
        new_period2 = current_time2.replace(hour=23, minute=00, second=00, microsecond=0)

        next_thursday = self.helper_f.next_weekday(new_period2, 3).timestamp()  # 0 = Monday, 1=Tuesday, 2=Wednesday...
        if str(start_point).find("nan") == False or str(end_point).find("nan") == False:
            self.LOGGER.debug("start or end point is null %s %s", str(start_point), str(end_point))
        else:

            lst_res_mon = self.get_travel_time(start_point, end_point, next_monday)
            # Thurs 11pm
            lst_res_thur = self.get_travel_time(start_point, end_point, next_thursday)
            travel_times.append(lst_res_mon)
            travel_times.append(lst_res_thur)

        return travel_times
