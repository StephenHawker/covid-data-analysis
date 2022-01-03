"""HELPER Functions"""
import logging
import urllib.parse as urlparse
import datetime
import codecs
import configparser
import pandas as pd


class HelperFunctions:
    ############################################################
    # constructor
    ############################################################
    def __init__(self):

        self.name = "Helper Functions"
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr("Helper Functions")

    ############################################################
    # Load Config File
    ############################################################
    def load_config(self, file):
        """Load config file

        Keyword arguments:
        file -- config file path
        config -- config array
        """
        config = {}

        config = config.copy()
        cp = configparser.ConfigParser()
        cp.read(file)
        for sec in cp.sections():
            name = sec.lower()  # string.lower(sec)
            for opt in cp.options(sec):
                config[name + "." + opt.lower()] = cp.get(sec, opt).strip()
        return config

    ############################################################
    # Get query string value from link
    ############################################################
    def get_qs_value(self, url, query_string):
        """get query string from passed url query string

        Keyword arguments:
        url -- href link
        query_string -- query string key to search for
        """
        try:

            parsed = urlparse.urlparse(url)
            qs_value = urlparse.parse_qs(parsed.query)[query_string]

            for k in qs_value:
                return str(k)

        except KeyError:
            return ""
        except Exception:
            raise Exception("Error in get_qs_value - %s %s ", url, query_string)

    ############################################################
    # Get EPOCH days ahead
    ############################################################
    def next_weekday(self, d, weekday):

        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7

        return d + datetime.timedelta(days_ahead)

    ############################################################
    # untangle_utf8
    ############################################################
    def untangle_utf8(self, match):
        """unicode issues...

        Keyword arguments:
        match -- json string with unicode issues...
        """
        escaped = match.group(0)                   # '\\u00e2\\u0082\\u00ac'
        hexstr = escaped.replace(r'\u00', '')      # 'e282ac'
        buffer = codecs.decode(hexstr, "hex")      # b'\xe2\x82\xac'

        try:
            return buffer.decode('utf8')           # '€'

        except UnicodeDecodeError:
            self.LOGGER.error("Could not decode buffer: %s" % buffer)

    ############################################################
    # Flatten a nested json dataframe
    ############################################################
    def flatten_nested_json_df(self, df):

        df = df.reset_index()

        print(f"original shape: {df.shape}")
        print(f"original columns: {df.columns}")


        # search for columns to explode/flatten
        s = (df.applymap(type) == list).all()
        list_columns = s[s].index.tolist()

        s = (df.applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()

        print(f"lists: {list_columns}, dicts: {dict_columns}")
        while len(list_columns) > 0 or len(dict_columns) > 0:
            new_columns = []

            for col in dict_columns:
                print(f"flattening: {col}")
                # explode dictionaries horizontally, adding new columns
                horiz_exploded = pd.json_normalize(df[col]).add_prefix(f'{col}.')
                horiz_exploded.index = df.index
                df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
                new_columns.extend(horiz_exploded.columns) # inplace

            for col in list_columns:
                print(f"exploding: {col}")
                # explode lists vertically, adding new columns
                df = df.drop(columns=[col]).join(df[col].explode().to_frame())
                new_columns.append(col)

            # check if there are still dict o list fields to flatten
            s = (df[new_columns].applymap(type) == list).all()
            list_columns = s[s].index.tolist()

            s = (df[new_columns].applymap(type) == dict).all()
            dict_columns = s[s].index.tolist()

            print(f"lists: {list_columns}, dicts: {dict_columns}")

        print(f"final shape: {df.shape}")
        print(f"final columns: {df.columns}")
        return df