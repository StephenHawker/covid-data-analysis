import os
import sys
import logging.config
import simplejson as json
import pandas
from PageScraper import PageScraper
from UKCov19 import UKCov19
from APILookup import APILookup
from DistanceCalc import DistanceCalc
from HelperFunctions import HelperFunctions
from GetNearest import GetNearest
from collections import defaultdict
"""Read Firestations web page data """
"""Project Classes"""
""" Other Imports"""


class DatabaseLoadError(Exception):
    """Database Exception

    Keyword arguments:
    Exception -- Exception
    """
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


class DataIngestError(Exception):
    """FirestationIngestError Exception

    Keyword arguments:
    Exception -- Exception
    """
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


############################################################
# Main
############################################################
def main():
    """Main process

    """
    try:

        LOGGER.info('Started run. main:')
        SCOT_VACCINE_DATA_URL = configImport["covid_data.url_scot_vaccine_supply"]
        TEMP_FILE = configImport["covid_data.temp_file"]
        TABLE_CLASS = configImport["covid_data.key_marker"] ##"ds_accordion-item__body"
        uodf_regionaldemographiccases = pandas.DataFrame
        uodf_regionalhospdata = pandas.DataFrame
        uodf_ukdata = pandas.DataFrame
        ukdf_engdata = pandas.DataFrame
        ukdf_engcasedemodata = pandas.DataFrame
        """firestation_nearest_json_with_travel = configImport["firestation.json_file_with_travel"]"""

        LOGGER.debug("scot_vaccine_data_url  : %s ", SCOT_VACCINE_DATA_URL)
        # LOGGER.debug("Postcode api URL : %s ", POSTCODE_API_URL)
        LOGGER.debug("TEMP_FILE : %s ", TEMP_FILE)
        # LOGGER.debug("csv_file : %s ", CSV_FILE)
        # LOGGER.debug("number_closest : %s ", str(NUMBER_CLOSEST))

        fs_pagescraper = PageScraper(SCOT_VACCINE_DATA_URL)
        html_data = fs_pagescraper.get_pagedata_ro('search')

        """TODO Deal with changes and updates"""

        fs_pagescraper.write_table_to_temp(TEMP_FILE)
        the_table = fs_pagescraper.get_table(TABLE_CLASS)
        the_table = fs_pagescraper.html_table

        ##fs_pagescraper.save_tab_as_list()

        ukapi = UKCov19()
        uodf_regionaldemographiccases = ukapi.get_case_demo_data('region')
        ukdf_engcasedemodata = ukapi.get_case_demo_data('nation')
        uodf_regionalhospdata = ukapi.get_region_hosp_data()
        uodf_ukdata = ukapi.get_data_uk()
        ukdf_engdata = ukapi.get_data_england()
        ukdf_regionalpositivitydata = ukapi.get_case_positivity_data('region')

        uodf_regionaldemographiccases.to_csv('uodf_regionaldemographiccases.csv')
        uodf_regionalhospdata.to_csv('uodf_regionalhospdata.csv')
        ukdf_engcasedemodata.to_csv('ukdf_engcasedemodata.csv')
        uodf_ukdata.to_csv('uodf_ukdata.csv')
        ukdf_engdata.to_csv('ukdf_engdata.csv')
        ukdf_regionalpositivitydata.to_csv('ukdf_regionalpositivitydata.csv')


        LOGGER.info('Completed run.')

    except DataIngestError as recex:
        LOGGER.error("An Exception occurred Covid Data Ingest  ")
        LOGGER.error(recex.data)
        raise DataIngestError(recex)

    except Exception:
        LOGGER.error("An Exception occurred Covid Data Ingest ")
        LOGGER.error(str(sys.exc_info()[0]))
        LOGGER.error(str(sys.exc_info()[1]))
        # print getattr(e, 'message', repr(e))
        # print(e.message)
        raise Exception("!")


############################################################
# Process the list of lookups and get the list of closest n
# firestations for each
############################################################
def process_lkp_list(df_lkp, firestations_df, top_n, json_file, b_travel):
    """Process the list of lookup addresses to get nearest n

    Keyword arguments:
    lkp_list -- base point (lat_value, lon_value)
    firestations_df -- data frame of firestation data
    """
    r_list = defaultdict(list)
    lkp_list = []

    for index, row in df_lkp.iterrows():

        nearest_list = []

        lat_value = row['latitude']
        lon_value = row['longitude']

        LOGGER.debug("process_lkp_list :lat_value: %s", str(lat_value))
        LOGGER.debug("process_lkp_list :lon_value: %s", str(lon_value))

        lkp_list = df_lkp.values[index].tolist()

        base_point = (lat_value, lon_value)  # (lat, lon)

        """Return sorted list of nearest by distance"""
        df_fs_dist_list = UO_GET_NEAREST.create_nearest_list(base_point,
                                              firestations_df=firestations_df)

        lkp_list.append(df_fs_dist_list)

        r_list["lkpaddress"].append(lkp_list)

    """save as json"""
    json.dump(r_list, open(json_file, "w"))

############################################################
# Run
############################################################

if __name__ == "__main__":

    try:

        dirname = os.path.dirname(__file__)
        filename_ini = os.path.join(dirname, 'covid_data.ini')
        UO_HELPER = HelperFunctions()

        configImport = UO_HELPER.load_config(filename_ini)

        LOG_PATH = configImport["logging.log_path"]
        LOG_FILE = configImport["logging.log_file"]
        THE_LOG = LOG_PATH + "\\" + LOG_FILE
        LOGGING_LEVEL = configImport["logging.logginglevel"]

        LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}

        # create LOGGER
        LOGGER = logging.getLogger('firestation')
        LEVEL = LEVELS.get(LOGGING_LEVEL, logging.NOTSET)
        logging.basicConfig(level=LEVEL)

        HANDLER = logging.handlers.RotatingFileHandler(THE_LOG, maxBytes=1036288, backupCount=5)
        # create FORMATTER
        FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        HANDLER.setFormatter(FORMATTER)
        LOGGER.addHandler(HANDLER)
        # UO_DISTANCE_CALC = DistanceCalc(DISTANCE_MATRIX_API_KEY)
        # UO_API_LOOKUP = APILookup(POSTCODE_API_URL)
        # UO_GET_NEAREST = GetNearest(top_n=NUMBER_CLOSEST, bln_travel_times=B_TRAVEL, api_key=DISTANCE_MATRIX_API_KEY)

        main()

    except DataIngestError as exrec:
        LOGGER.error("Error in ingest - please check:" + str(exrec.data))
        raise Exception("Covid Data ingest failed - please check")

    except Exception:
        LOGGER.error("An Exception in : MAIN :" + __name__)
        LOGGER.error(str(sys.exc_info()[0]))
        LOGGER.error(str(sys.exc_info()[1]))
        # print getattr(e, 'message', repr(e))
        # print(e.message)
        raise Exception("Covid Data ingest failed - please check")
