#coding: utf8

BASE_URL = r'http://www.bilibili.tv/'

INTERFACE_URL = r'http://interface.bilibili.tv/playurl?cid={0}'

COMMENT_URL = r'http://comment.bilibili.tv/{0}.xml'

RSS_URLS = [
    {
        'name': u'动画',
        'url': 'rss-1.xml'
    },
    {
        'name': u'音乐',
        'url': 'rss-3.xml'
    },
    {
        'name': u'游戏',
        'url': 'rss-4.xml'
    },
    {
        'name': u'娱乐',
        'url': 'rss-5.xml'
    },
    {
        'name': u'专辑',
        'url': 'rss-11.xml'
    },
    {
        'name': u'新番连载',
        'url': 'rss-13.xml'
    }
]
