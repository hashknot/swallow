"""
Defines quote providing classes.
"""
import requests

from bs4 import BeautifulSoup

QUOTE_BR_URL = 'http://www.bookreporter.com/features/quotes'
""" bookreporter.com's quote of the day URL """

class BaseQuote(object):
    def __init__(*args, **kwargs):
        pass

    def get(self):
        """
        Must return `(text, attribution)` 2-tuple of strs.
        """
        raise NotImplementedError

class BookReporterQuoteOTD(BaseQuote):
    """
    Gets bookreporter.com's quote of the day
    """
    def get(self):
        data = requests.get(QUOTE_BR_URL)
        html = BeautifulSoup(data.text, 'html.parser')
        main_content = html.find(attrs={'id': 'main-content'})
        quote = main_content.find(attrs={'class': 'body'}).text.strip()
        attribution = main_content.find(attrs={'class': 'field-attribution-value'}).text

        # \u2013 is the 'longdash (---)' unicode character
        attribution = attribution.replace(u'\u2013', '').strip()

        return quote, attribution
