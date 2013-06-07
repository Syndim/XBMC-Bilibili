#coding: utf8
import utils
import re

class BiliList():
    def __init__(self):
        self.ITEMS = re.compile('<li.*?pubdate="(.*?)">.*?<a href=".*?av(\d+)/".*?>(.*?)</a></li>')

    def find_all_items(self, url):
        page_content = utils.get_page_content(url)
        results = self.ITEMS.findall(page_content)
        results_dict = dict()
        for r in results:
            if r[0] in results_dict.key():
                results_dict[r[0]].append((r[1], r[2]))
            else:
                results_dict[r[0]] = [(r[1], r[2])]
        return results_dict
