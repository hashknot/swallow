"""
Defines 'wallpaper' providing classes.
"""
import json
import requests
import urllib2
import urlparse

WALLPAPER_BING_API_URL = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'

class BaseWallpaper(object):

    def __init__(*args, **kwargs):
        pass

    def download(self, path):
        raise NotImplementedError

    def _download_file(self, url, filename):
        """
        Utility method for downloading files.
        """
        response = urllib2.urlopen(url)
        with open(filename, 'wb') as fh:
            fh.write(response.read())


class BingWallpaperOTD(BaseWallpaper):
    """
    Gets Bing's wallpaper of the day.
    """
    def download(self, path):
        json_str = requests.get(WALLPAPER_BING_API_URL).text
        base_path = json.loads(json_str)['images'][0]['url']
        url_obj = urlparse.urlparse(WALLPAPER_BING_API_URL)
        url = '{}://{}{}'.format(url_obj.scheme, url_obj.hostname, base_path)
        self._download_file(url, path)
