"""Page Scraper - scrape html from a passed url"""
import logging
import urllib
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
from HelperFunctions import HelperFunctions
import io
import csv


class PageScraper:
    ############################################################
    # constructor
    ############################################################
    def __init__(self, url):

        self.html = ""
        self.site_url = url
        self.html_table = ""
        self.helper_f = HelperFunctions()
        self.table_output_rows = []
        self.LOGGER = logging.getLogger(__name__)

    ############################################################
    # str
    ############################################################
    def __str__(self):

        return repr(self.site_url)

    ############################################################
    # Get page html
    ############################################################
    def get_pagedata(self, form_value):
        """get html from page

        Keyword arguments:
        site_url -- Site URL to post to
        form_values -- form values to post
        """
        try:
            output_html = ""
            form_val = {form_value: '%', 'Submit': 'Select'}
            form_data = urllib.parse.urlencode(form_val)
            header = {"Content-type": "application/x-www-form-urlencoded",
                      "Accept": "text/plain", "Referer": self.site_url}

            header2 = {}

            header2[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                                " Chrome/41.0.2272.101 Safari/537.36"
            header2['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            header2['Content-type'] = "application/x-www-form-urlencoded"

            # body = form_data.encode(encoding='utf-8')
            s = requests.Session()
            # providers = s.post(url, params=form_data, data=form_data, timeout=15, verify=True,headers=header)

            # Open a sesssion first
            s.get(self.site_url)
            # Post form data to get
            r = s.post(self.site_url , data=form_data, headers=header2, verify=True)
            self.html = str(r.text)

            self.LOGGER.debug("Status: %s", str(r.status_code))
            self.LOGGER.debug("reason: %s", str(r.reason))

        except Exception:
            raise Exception("Error in Page_scraper - URL : %s  form value : %s ", self.site_url, self.form_value)

        finally:
            return self.html


    ############################################################
    # Get page html read only
    ############################################################
    def get_pagedata_ro(self, form_value):
        """get html from page

        Keyword arguments:
        site_url -- Site URL to post to
        form_values -- form values to post
        """
        try:
            output_html = ""
            form_val = {form_value: '%', 'Submit': 'Select'}
            form_data = urllib.parse.urlencode(form_val)
            header = {"Content-type": "application/x-www-form-urlencoded",
                      "Accept": "text/plain", "Referer": self.site_url}

            header2 = {}

            header2[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                                " Chrome/41.0.2272.101 Safari/537.36"
            header2['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            header2['Content-type'] = "application/x-www-form-urlencoded"

            fp = urllib.request.urlopen(self.site_url)
            mybytes = fp.read()

            mystr = mybytes.decode("utf8")
            fp.close()
            self.html = str(mystr)

            self.LOGGER.debug("reason: %s", str("xx"))

        except Exception:
            raise Exception("Error in Page_scraper - URL : %s  form value : %s ", self.site_url)

        finally:
            return self.html


    ############################################################
    # Get table of data
    ############################################################
    def get_table(self, table_class):
        """get table from html page

        Keyword arguments:
        html -- html
        table_class -- class of table to get
        """
        soup = BeautifulSoup(self.html, features="html.parser")
        table = soup.find('div', {'class': table_class})
        self.html_table = table


    ############################################################
    # Write Temp File of html
    ############################################################
    def write_table_to_temp(self, temp_file):
        """get table from html page

        Keyword arguments:
        self -- self
        table_class -- Table Class to get
        """
        with io.open(temp_file, "w", encoding="utf-8") as f:
            f.write(self.html)


    ############################################################
    # take table of data and convert to list
    ############################################################
    def save_tab_as_list(self):
        """get table from html page
        Keyword arguments:
        tab -- table
        csv_file - csv file to write to
        """
        try:
            row_marker = 0
            td_count = 0
            column_marker = 0

            for table_row in self.html_table.findAll('tr'):
                #row 1, store column count and append extra lat & lon cols"""
                if row_marker == 1:
                    td_count = column_marker
                    output_row.append("lat")
                    output_row.append("lon")

                column_marker = 0

                row_marker += 1

                columns = table_row.findAll('td')
                output_row = []

                for column in columns:

                    column_marker += 1

                    #Get link in detail for first column in row"""
                    if column_marker == 1:
                        fs_link = ""

                        for link in column.findAll('a', href=True):
                            """print(link['href'])"""
                            fs_link = link['href']
                            """Get latitude qs value"""
                            lat = self.helper_f.get_qs_value(fs_link, 'lat')

                            """Get longitude qs value"""
                            lon = self.helper_f.get_qs_value(fs_link, 'lon')
                            """TODO get_accuracy(row)"""

                        #Append first column header as not in data
                        if row_marker == 1:
                            output_row.append("Detail")
                        else:
                            output_row.append(column.text + " " + fs_link)

                    else:
                        output_row.append(column.text)

                     #append extra derived cols
                    if column_marker == td_count:
                        output_row.append(str(lat))
                        output_row.append(str(lon))

                self.table_output_rows.append(output_row)

            self.LOGGER.debug("cols: %s", str(td_count))

        except Exception:
            raise Exception("Error in save_tab_as_csv  : ")

    ############################################################
    # Write CSV file
    ############################################################
    def write_csv(self, csv_file):
        """get table from html page
        Keyword arguments:
        csv_file - csv file to write to
        """
        try:
            """Save to CSV"""
            with open(csv_file, 'w', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.table_output_rows)

        except Exception:
            raise Exception("Error in write_csv - csv_file : %s ", csv_file)