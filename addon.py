#coding: utf8
import tempfile
from xbmcswift2 import Plugin, xbmc, xbmcgui
from resources.lib.bilibili import Bili

plugin = Plugin()
bili = Bili()

def _play_video(urls_info, show_comments='1'):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    i = 1
    for url in urls_info[0]:
        list_item = xbmcgui.ListItem(u'播放')
        list_item.setInfo(type='video', infoLabels={"Title": "第"+str(i)+"/"+str(len(urls_info[0]))+" 节"})
        i += 1
        playlist.add(url, listitem=list_item)
    xbmc.Player().play(playlist)
    if show_comments == '1':
        xbmc.Player().setSubtitles(tempfile.gettempdir() + '/tmp.ass')

@plugin.route('/')
def index():
    dir_list = [
        {
            'label': name,
            'path': plugin.url_for('show_target_items', target=name)
        } for name in bili.ROOT_PATH ]
    return dir_list

@plugin.route('/items/<target>/')
def show_target_items(target):
    dir_list = [
        {
            'label': item['name'],
            'path': plugin.url_for('show_category_items', target=target, category=item['eng_name'])
        } for item in bili.get_items(target) ]
    return dir_list

@plugin.route('/items/<target>/<category>/')
def show_category_items(target, category):
    if target == 'RSS':
        dir_list = [ {
            'label': item['title'],
            'path': plugin.url_for('show_video_list', url=item['link'])
        } for item in bili.get_items(target, category) ]
    elif target == 'Index':
        dir_list = [ {
            'label': item['title'],
            'path': plugin.url_for('show_monthly_items', target=target, category=category, month=item['link'])
        } for item in bili.get_items(target, category) ]
    else:
        dir_list = []
    return dir_list

@plugin.route('/items/<target>/<category>/<month>/')
def show_monthly_items(target, category, month):
    dir_list = [ {
        'label': item['title'],
        'path': plugin.url_for('show_video_list', url=item['link'])
    } for item in bili.get_video_by_month(category, month)]
    return dir_list

@plugin.route('/videos/<url>/')
def show_video_list(url):
    dir_list = []
    for item in bili.get_video_list(url):
        dir_list.append({
            'label': item[0],
            'path': plugin.url_for('play_video', url=item[1], show_comments=1),
        })
        dir_list.append({
            'label': item[0] + u'(无弹幕)',
            'path': plugin.url_for('play_video', url=item[1], show_comments=0),
        })
    return dir_list

@plugin.route('/video/<url>/<show_comments>/')
def play_video(url, show_comments):
    playlist = bili.get_video_urls(url)
    _play_video(playlist, show_comments)

if __name__ == '__main__':
    plugin.run()
