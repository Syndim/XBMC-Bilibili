#coding: utf8

from config import *
import feedparser
import xml.dom.minidom as minidom
import re
import os
import tempfile
import utils
import pickle
from niconvert import create_website

class Bili():
    def __init__(self, width=720, height=480):
        self.WIDTH = width
        self.HEIGHT = height
        self.BASE_URL = BASE_URL
        self.RSS_URLS = RSS_URLS
        self.INDEX_URLS = INDEX_URLS
        self.ROOT_PATH = ROOT_PATH
        self.INTERFACE_URL = INTERFACE_URL
        self.COMMENT_URL = COMMENT_URL
        self.URL_PARAMS = re.compile('cid=(\d+)&aid=\d+')
        self.URL_PARAMS2 = re.compile("cid:'(\d+)'")
        self.PARTS = re.compile("<option value=.{1}(/video/av\d+/index_\d+\.html).*>(.*)</option>")
        self.ITEMS = re.compile('<li.*?pubdate="(.*?)">.*?<a href=".*?av(\d+)/".*?>(.*?)</a></li>')
        for item in self.RSS_URLS:
            item['url'] = self.BASE_URL + item['url']
        for item in self.INDEX_URLS:
            item['url'] = self.BASE_URL + item['url']

    def _get_url(self, dict_obj, name):
        for item in dict_obj:
            if item['eng_name'] == name:
                return item['url']

    def _get_rss_url(self, name):
        return self._get_url(self.RSS_URLS, name)

    def _get_index_url(self, name):
        return self._get_url(self.INDEX_URLS, name)

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
            content = utils.get_page_content(interface_full_url)
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

    def _get_index_items(self, url):
        pickle_file = tempfile.gettempdir() + '/' + url.split('/')[-1].strip() + '_tmp.pickle'
        if os.path.exists(pickle_file):
            return pickle.load(open(pickle_file, 'rb'))
        else:
            page_content = utils.get_page_content(url)
            results = self.ITEMS.findall(page_content)
            results_dict = dict()
            for r in results:
                if r[0] in results_dict.keys():
                    results_dict[r[0]].append((r[1], r[2]))
                else:
                    results_dict[r[0]] = [(r[1], r[2])]
            f = open(pickle_file, 'wb')
            pickle.dump(results_dict, f)
            return results_dict

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
        index_url = self._get_index_url(category)
        parse_result = self._get_index_items(index_url)
        return [ {
            'title': x,
            'link': x,
            'description': x,
            'published': x
        } for x in sorted(parse_result.keys())]

    def get_video_by_month(self, category, month):
        index_url = self._get_index_url(category)
        parse_result = self._get_index_items(index_url)
        return [ {
            'title': x[1],
            'link': x[0],
            'description': x[1],
            'published': month
        } for x in parse_result[month] ]

    def get_items(self, target, category=None):
        if target == 'RSS':
            if category:
                return self.get_rss_items(category)
            else:
                return self.RSS_URLS
        elif target == 'Index':
            if category:
                return self.get_index_items(category)
            else:
                return self.INDEX_URLS
        return []

    def get_video_list(self, av_id):
        page_full_url = self.BASE_URL + 'video/av' + str(av_id) + '/'
        page_content = utils.get_page_content(page_full_url)
        parts = self.PARTS.findall(page_content)
        if len(parts) == 0:
            return [(u'播放', 'video/av' + str(av_id) + '/')]
        else:
            return [(part[1], part[0][1:]) for part in parts]

    def get_video_urls(self, url):
        page_full_url = self.BASE_URL + url
        print page_full_url
        page_content = utils.get_page_content(page_full_url)
        return self._parse_urls(page_content)

