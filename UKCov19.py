"""UK Covid 19 API interface """
import logging
import csv
from uk_covid19 import Cov19API
from HelperFunctions import HelperFunctions

class UKCov19:
    ############################################################
    # constructor
    ############################################################
    def __init__(self):

        self.name = "UKCov19"
        self.html = ""
        self.helper_f = HelperFunctions()
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr(self.name)

    ############################################################
    # Get Data
    ############################################################
    def get_data_england(self):

        """Get the Covid data via the API"""
        try:
            ## areaType=nation, areaName=England
            area_name = 'England'
            area_type = 'nation'

            # The location for which we want data.
            location_filter = [f'areaType={area_type}',
                               f'areaName={area_name}']

            # The metric(s) to request. NOTE: More than in
            # the previous example, for variety.
            req_structure = {
                "date": "date",
                "areaCode": "areaCode",
                "areaName": "areaName",
                "newCasesByPublishDate":
                    "newCasesByPublishDate",
                "newCasesBySpecimenDate":
                    "newCasesBySpecimenDate",
                "newDeaths28DaysByDeathDate":
                    "newDeaths28DaysByDeathDate",
                "hospitalCases":
                    "hospitalCases",
                "newAdmissions":
                    "newAdmissions"
            }

            # Request the data.
            # This gets all pages and we don't need to care how.
            # , latest_by="newCasesBySpecimenDateAgeDemographics"
            api = Cov19API(filters=location_filter, structure=req_structure)
            # Get the data.
            # NOTE3: If a 204 (Success - no data) occurs can we tell?
            data = api.get_dataframe()
            return(data)
        except Exception as ex:  # pylint: disable=broad-except
            print(f'Exception [{ex}]')

    ############################################################
    # Get Data
    ############################################################
    def get_data_uk(self):

        """Get the Covid data via the API"""
        try:
            ## areaType=nation, areaName=England
            area_type = 'overview'

            # The location for which we want data.
            location_filter = [f'areaType={area_type}']

            # The metric(s) to request. NOTE: More than in
            # the previous example, for variety.
            req_structure = {
                "areaCode": "areaCode",
                "areaName": "areaName",
                "areaType": "areaType",
                "date": "date",
                "newCasesByPublishDate":
                    "newCasesByPublishDate",
                "newCasesBySpecimenDate":
                    "newCasesBySpecimenDate",
                "newDeaths28DaysByDeathDate":
                    "newDeaths28DaysByDeathDate",
                "hospitalCases":
                    "hospitalCases",
                "newAdmissions":
                    "newAdmissions"
            }

            # Request the data.
            # This gets all pages and we don't need to care how.
            # , latest_by="newCasesBySpecimenDateAgeDemographics"
            api = Cov19API(filters=location_filter, structure=req_structure)
            # Get the data.
            # NOTE3: If a 204 (Success - no data) occurs can we tell?
            data = api.get_dataframe()
            return(data)
        except Exception as ex:  # pylint: disable=broad-except
            print(f'Exception [{ex}]')


    ############################################################
    # Get Data for regional case demographics
    ############################################################
    def get_case_demo_data(self,area_type):

        """Get the Covid data via the API"""
        try:
            ## areaType=nation, areaName=England
            v_area_type = area_type

            # The location for which we want data.
            location_filter = [f'areaType={v_area_type}']
            # The metric(s) to request. NOTE: More than in
            # the previous example, for variety.
            req_structure = {
                "date": "date",
                "areaCode": "areaCode",
                "areaName": "areaName",
                "areaType": "areaType",
                "newCasesBySpecimenDateAgeDemographics": "newCasesBySpecimenDateAgeDemographics"
            }

            # Request the data.
            # This gets all pages and we don't need to care how.
            # , latest_by="newCasesBySpecimenDateAgeDemographics"
            api = Cov19API(filters=location_filter, structure=req_structure)
            # Get the data.
            # NOTE3: If a 204 (Success - no data) occurs can we tell?
            data = api.get_dataframe()
            data2 = self.helper_f.flatten_nested_json_df(data)
            return(data2)
        except Exception as ex:  # pylint: disable=broad-except
            print(f'Exception [{ex}]')


    ############################################################
    # Get Data for regional case demographics
    ############################################################
    def get_region_hosp_data(self):

        """Get the Covid data via the API"""
        try:
            ## areaType=nation, areaName=England
            area_type = 'nhsRegion'

            # The location for which we want data.
            location_filter = [f'areaType={area_type}']
            # The metric(s) to request. NOTE: More than in
            # the previous example, for variety.
            req_structure = {
                "areaCode": "areaCode",
                "areaName": "areaName",
                "areaType": "areaType",
                "date": "date",
                "covidOccupiedMVBeds": "covidOccupiedMVBeds",
                "hospitalCases": "hospitalCases",
                "newAdmissions": "newAdmissions"
            }

            # Request the data.
            # This gets all pages and we don't need to care how.
            # , latest_by="newCasesBySpecimenDateAgeDemographics"
            api = Cov19API(filters=location_filter, structure=req_structure)
            # Get the data.
            # NOTE3: If a 204 (Success - no data) occurs can we tell?
            data = api.get_dataframe()
            return(data)
        except Exception as ex:  # pylint: disable=broad-except
            print(f'Exception [{ex}]')



    ############################################################
    # Get Data for regional case demographics
    ############################################################
    def get_case_positivity_data(self,area_type):

        """Get the Covid data via the API"""
        try:
            ## areaType=nation, areaName=England
            v_area_type = area_type

            # The location for which we want data.
            location_filter = [f'areaType={v_area_type}']
            # The metric(s) to request. NOTE: More than in
            # the previous example, for variety.
            req_structure = {
                "date": "date",
                "areaCode": "areaCode",
                "areaName": "areaName",
                "areaType": "areaType",
                "uniqueCasePositivityBySpecimenDateRollingSum": "uniqueCasePositivityBySpecimenDateRollingSum"
            }

            # Request the data.
            # This gets all pages and we don't need to care how.
            # , latest_by="newCasesBySpecimenDateAgeDemographics"
            api = Cov19API(filters=location_filter, structure=req_structure)
            # Get the data.
            # NOTE3: If a 204 (Success - no data) occurs can we tell?
            data = api.get_dataframe()
            data2 = self.helper_f.flatten_nested_json_df(data)
            return(data2)
        except Exception as ex:  # pylint: disable=broad-except
            print(f'Exception [{ex}]')