#coding: utf8

BASE_URL = r'http://www.bilibili.tv/'

INTERFACE_URL = r'http://interface.bilibili.tv/playurl?cid={0}'

COMMENT_URL = r'http://comment.bilibili.tv/{0}.xml'

ROOT_PATH = [ 'RSS', 'Index' ]

RSS_URLS = [
    {
        'name': u'动画',
        'eng_name': 'anime',
        'url': 'rss-1.xml'
    },
    {
        'name': u'音乐',
        'eng_name': 'music',
        'url': 'rss-3.xml'
    },
    {
        'name': u'游戏',
        'eng_name': 'game',
        'url': 'rss-4.xml'
    },
    {
        'name': u'娱乐',
        'eng_name': 'entertainment',
        'url': 'rss-5.xml'
    },
    {
        'name': u'专辑',
        'eng_name': 'album',
        'url': 'rss-11.xml'
    },
    {
        'name': u'新番连载',
        'eng_name': 'series',
        'url': 'rss-13.xml'
    }
]
