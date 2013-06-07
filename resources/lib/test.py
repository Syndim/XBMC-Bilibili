#coding:utf8
from bililist import BiliList

def main():
    bili_list = BiliList()
    result = bili_list.find_all_items(r'http://www.bilibili.tv/sitemap/sitemap-34.html')

if __name__ == '__main__':
    main()
