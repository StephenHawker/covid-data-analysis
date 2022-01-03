"""various distance calculations"""
import logging
from HelperFunctions import HelperFunctions
from DistanceCalc import DistanceCalc
import re
import pandas


class GetNearest:
    ############################################################
    # constructor
    ############################################################
    def __init__(self, top_n, bln_travel_times, api_key):
        self.name = "Get Nearest"
        self.top_n = top_n
        self.LOGGER = logging.getLogger(__name__)
        self.helper_f = HelperFunctions()
        self.dist_calc = DistanceCalc(api_key=api_key)
        self.bln_travel_times = bln_travel_times
        self.api_key = api_key

    ############################################################
    # str
    ############################################################
    def __str__(self):
        return repr("Get Nearest")

    ############################################################
    # Read firestations into a data frame, take a vector point passed
    # and return an ordered list from nearest ASC distance
    ############################################################
    def create_nearest_list(self, base_point, firestations_df):
        """Create ordered list of

        Keyword arguments:
        base_point -- base point (lat_value, lon_value)
        firestations_df -- data frame of firestation data
        """

        distance_list = []

        for index, row in firestations_df.iterrows():
            lat = row['lat']
            lon = row['lon']
            point = (lat, lon)

            """Get as the crow files haversine distance"""
            dist = self.dist_calc.get_haversine_dist(base_point, point)

            distance_list.append(dist)

        df_fs_dist = firestations_df
        df_fs_dist['distance'] = distance_list

        """sort by distance ascending"""
        df_fs_dist.sort_values(by=['distance'], inplace=True)

        """Get top n"""
        df_fs_dist_ret = df_fs_dist[:int(self.top_n)]

        lst_json = []
        lc = 0

        for ix, rw in df_fs_dist_ret.iterrows():

            lst_travel = []

            a_json_str = df_fs_dist_ret.iloc[lc].to_json()
            a_a = re.sub(r"(?i)(?:\\u00[0-9a-f]{2})+", self.helper_f.untangle_utf8, a_json_str)

            lst_travel.append(a_a)
            lat = rw['lat']
            lon = rw['lon']
            point = (lat, lon)

            """Get travel time if required"""
            if self.bln_travel_times:
                lst_travel_times = self.dist_calc.get_travel_times(base_point, point)
                lst_travel.append(lst_travel_times)

            lst_json.append(lst_travel)
            lc += 1

        return lst_json
