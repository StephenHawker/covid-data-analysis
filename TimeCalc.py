"""various date time calculations"""
import logging
import datetime


class TimeCalc:

    ############################################################
    # constructor
    ############################################################
    def __init__(self):

        self.name = "Time_calc"
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr("Time Calc")

    ############################################################
    # Get EPOCH days ahead
    ############################################################
    def next_weekday(self, d, weekday):

        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        return d + datetime.timedelta(days_ahead)
