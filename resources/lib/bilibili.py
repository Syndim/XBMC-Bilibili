#coding: utf8

from config import *
from io import BytesIO
import feedparser
import xml.dom.minidom as minidom
import urllib2
import re
import gzip
import zlib
import tempfile
from niconvert import create_website

class Bili():
    def __init__(self, width=720, height=480):
        self.WIDTH = width
        self.HEIGHT = height
        self.BASE_URL = BASE_URL
        self.RSS_URLS = RSS_URLS
        self.ROOT_PATH = ROOT_PATH
        self.INTERFACE_URL = INTERFACE_URL
        self.COMMENT_URL = COMMENT_URL
        self.URL_PARAMS = re.compile('cid=(\d+)&aid=\d+')
        self.URL_PARAMS2 = re.compile("cid:'(\d+)'")
        self.PARTS = re.compile("<option value=.{1}(/video/av\d+/index_\d+\.html).*>(.*)</option>")
        for item in self.RSS_URLS:
            item['url'] = self.BASE_URL + item['url']

    def _get_rss_url(self, name):
        for item in self.RSS_URLS:
            if item['eng_name'] == name:
                return item['url']

    def _ungzip(self, content):
        bytes_buffer = BytesIO(content)
        return gzip.GzipFile(fileobj=bytes_buffer).read()

    def _get_gzip_content(self, content):
        page_content = self._ungzip(content)
        return page_content

    def _get_zlib_content(self, content):
        page_content = zlib.decompress(content)
        return page_content

    def _get_content(self, page_full_url):
        response = urllib2.urlopen(page_full_url)
        print response.headers.get('content-encoding', '')
        if response.headers.get('content-encoding', '') == 'gzip':
            return self._get_gzip_content(response.read())
        elif response.headers.get('content-encoding', '') == 'deflate':
            return self._get_zlib_content(response.read())
        else:
            return response.read()

    def _parse_urls(self, page_content):
        url_params = self.URL_PARAMS.findall(page_content)
        interface_full_url = ''
        if url_params and len(url_params) == 1 and url_params[0]:
            interface_full_url = self.INTERFACE_URL.format(str(url_params[0]))
        if not url_params:
            url_params = self.URL_PARAMS2.findall(page_content)
            if url_params and len(url_params) == 1 and url_params[0]:
                interface_full_url = self.INTERFACE_URL.format(str(url_params[0]))
        if interface_full_url:
            content = self._get_content(interface_full_url)
            doc = minidom.parseString(content)
            parts = doc.getElementsByTagName('durl')
            result = []
            for part in parts:
                urls = part.getElementsByTagName('url')
                if len(urls) > 0:
                    result.append(urls[0].firstChild.nodeValue)
            return (result, self._parse_subtitle(url_params[0]))
        print interface_full_url
        return ([], '')

    def _parse_subtitle(self, cid):
        page_full_url = self.COMMENT_URL.format(cid)
        print page_full_url
        website = create_website(page_full_url)
        if website is None:
            print page_full_url + " not supported"
            return ''
        else:
            text = website.ass_subtitles_text(
                font_name=u'黑体',
                font_size=36,
                resolution='%d:%d' % (self.WIDTH, self.HEIGHT),
                line_count=12,
                bottom_margin=0,
                tune_seconds=0
            )
            f = open(tempfile.gettempdir() + '/tmp.ass', 'w')
            f.write(text.encode('utf8'))
            return 'tmp.ass'

    def get_rss_items(self, category):
        rss_url = self._get_rss_url(category)
        parse_result = feedparser.parse(rss_url)
        return [ {
            'title': x.title,
            'link': x.link.replace(BASE_URL+'video/av', '').replace('/', ''),
            'description': x.description,
            'published': x.published
        } for x in parse_result.entries ]

    def get_index_items(self, category):
        pass

    def get_items(self, target, category=None):
        if target == 'RSS':
            if category:
                return self.get_rss_items(category)
            else:
                return self.RSS_URLS
        return []

    def get_video_list(self, av_id):
        page_full_url = self.BASE_URL + 'video/av' + str(av_id) + '/'
        page_content = self._get_content(page_full_url)
        parts = self.PARTS.findall(page_content)
        if len(parts) == 0:
            return [(u'播放', 'video/av' + str(av_id) + '/')]
        else:
            return [(part[1], part[0][1:]) for part in parts]

    def get_video_urls(self, url):
        page_full_url = self.BASE_URL + url
        print page_full_url
        page_content = self._get_content(page_full_url)
        return self._parse_urls(page_content)
