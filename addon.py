#coding:utf8

import xbmcplugin
import xbmcgui
import xbmc
import sys
import tempfile
from bilibili import Bili
from urllib import unquote

def get_dirs():
    dir_str = sys.argv[2]
    dir_str = dir_str.replace('?dir=', '')
    str_list =  dir_str.split('%2f%2f')
    str_list = filter(bool, str_list)
    return str_list

def gen_dir_url(dirs):
    result = 'plugin://plugin.video.bilibili/?dir=' + '//'.join(dirs)
    if result.endswith('/'):
        result = result[:-1]
    return result

def play_video(urls_info):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    i = 1
    for url in urls_info[0]:
        list_item = xbmcgui.ListItem(u'播放')
        list_item.setInfo(type='Video', infoLabels={"Title": "第"+str(i)+"/"+str(len(urls_info[0]))+" 节"})
        i += 1
        playlist.add(url, listitem=list_item)
    xbmc.Player().play(playlist)
    print tempfile.gettempprefix()
    xbmc.Player().setSubtitles(tempfile.gettempdir() + '/tmp.ass')

def main():
    handle = int(sys.argv[1])
    bili = Bili()
    dir_list = get_dirs()
    if len(dir_list) == 0:
        dir_list = [ (gen_dir_url([x]), xbmcgui.ListItem(x), True) for x in bili.ROOT_DIRS ]
        xbmcplugin.addDirectoryItems(handle, dir_list)
        xbmcplugin.endOfDirectory(handle)
    elif len(dir_list) == 1:
        dir_list = [ (gen_dir_url([dir_list[0], x['link']]), xbmcgui.ListItem(x['title']), True) for x in bili.get_items(unquote(dir_list[0])) ]
        xbmcplugin.addDirectoryItems(handle, dir_list)
        xbmcplugin.endOfDirectory(handle)
    elif len(dir_list) == 2:
        video_list = []
        for url in bili.get_video_list(dir_list[-1]):
            new_dir_list = []
            new_dir_list.extend(dir_list)
            new_dir_list.append(url[1])
            video_list.append((gen_dir_url(new_dir_list), xbmcgui.ListItem(url[0]), True))
        if video_list:
            xbmcplugin.addDirectoryItems(handle, video_list)
            xbmcplugin.endOfDirectory(handle)
    elif len(dir_list) == 3:
        video_list = bili.get_video_urls(unquote(dir_list[-1]))
        play_video(video_list)

if __name__ == '__main__':
    main()
