####################################################################################################
#                                                                                                  #
#                               (Clip/Pic)Hunter Plex Channel                                      #
#                                                                                                  #
####################################################################################################
import bookmarks
from updater import Updater
from DumbTools import DumbKeyboard

# ClipHunter
CH_TITLE = L('ch_title')
CH_PREFIX = '/video/videosite'
CH_BASE_URL = 'http://www.cliphunter.com'
ICON_CH = 'icon-default-ch.png'
ICON_BM_CH = 'icon-bookmarks-ch.png'
ICON_BM_ADD_CH = 'icon-add-bookmark-ch.png'
ICON_BM_REMOVE_CH = 'icon-remove-bookmark-ch.png'
ICON_VIDEO = 'icon-video.png'
ICON_SIM = 'icon-similar.png'
ICON_CAT_CH = 'icon-tags-ch.png'
ICON_LIST = 'icon-explore.png'
ICON_TV = 'icon-tv.png'
ICON_STARS = 'icon-stars.png'
ICON_PSTARS_CH = 'icon-babe-ch.png'
ICON_PLAYLIST = 'icon-playlist.png'
ICON_UPDATE_CH = 'icon-update-ch.png'
ART_CH = 'art-default-ch.jpg'
bm_ch = bookmarks.Bookmark(CH_TITLE, CH_PREFIX, ICON_BM_ADD_CH, ICON_BM_REMOVE_CH)

#/page/sort/all/rating/uploaded/duration/hd
SORT = [
    ('date', 'Date'), ('rel', 'Relevance'), ('views', 'Views'), ('rating', 'Rating')
    ]
RATING = [
    ('all/all', 'All'), ('all/super', 'Super High'), ('all/high', 'High'), ('all/medium', 'Medium')
    ]
DURATION = [
    ('all', 'All'), ('300', 'Short'), ('900', 'Medium'), ('1800', 'Long')
    ]
UPLOADED = [
    ('all', 'Any Time'), ('today', 'Today'), ('yesterday', 'Yesterday'), ('week', 'This Week'),
    ('month', 'This Month'), ('3months', '3 Months'), ('year', 'This Year')
    ]
CHANNELS = [
    ('alphabetical', 'A-Z'), ('recently-updated', 'Recently Updated'),
    ('most-popular', 'Most Popular'), ('top-rated', 'Top Rated'), ('most-viewed', 'Most Viewed'),
    ('video-duration', 'Video Duration')
    ]
CHANNEL_OPT = [('rating', 'Best'), ('date', 'Newest'), ('views', 'Most Views')]

####################################################################################################
def Start():
    #HTTP.CacheTime = 0
    HTTP.CacheTime = CACHE_1HOUR

####################################################################################################
@handler(CH_PREFIX, CH_TITLE, thumb=ICON_CH, art=ART_CH)
def VideoMainMenu():
    """Setup Main Menu, Includes Updater"""

    oc = ObjectContainer(title2=CH_TITLE, art=R(ART_CH), no_cache=True)

    Updater(CH_PREFIX + '/updater', oc, ICON_UPDATE_CH)

    oc.add(DirectoryObject(
        key=Callback(HDOpt, title='Explore', href='/categories/All'),
        title='Explore', thumb=R(ICON_LIST), art=R(ART_CH)
        ))
    oc.add(DirectoryObject(
        key=Callback(CategoryList, title='Categories'),
        title='Categories', thumb=R(ICON_CAT_CH), art=R(ART_CH)
        ))
    oc.add(DirectoryObject(
        key=Callback(ChannelList, title='Channels', href='/channels'),
        title='Channels', thumb=R(ICON_TV), art=R(ART_CH)
        ))
    oc.add(DirectoryObject(
        key=Callback(PopularList, title='Popular', href='/popular/ratings'),
        title='Popular', thumb=R(ICON_STARS), art=R(ART_CH)
        ))
    oc.add(DirectoryObject(
        key=Callback(PornstarOpt, title='Pornstars', href='/pornstars'),
        title='Pornstars', thumb=R(ICON_PSTARS_CH), art=R(ART_CH)
        ))
    #oc.add(DirectoryObject(key=Callback(Playlists, title='Playlists'), title='Playlists', thumb=R(ICON_PLAYLIST)))
    oc.add(DirectoryObject(
        key=Callback(ClipBookmarksMain),
        title='My Bookmarks', thumb=R(ICON_BM_CH), art=R(ART_CH)
        ))
    #oc.add(PrefsObject(title='Preferences'))
    if Client.Product in DumbKeyboard.clients:
        DumbKeyboard(CH_PREFIX, oc, ClipSearch, dktitle='Search', dkthumb=R('icon-search.png'))
    else:
        oc.add(InputDirectoryObject(
            key=Callback(ClipSearch),
            title='Search', summary='Search ClipHunter', prompt='Search for...',
            thumb=R('icon-search.png'), art=R(ART_CH)
            ))

    return oc

####################################################################################################
@route(CH_PREFIX + '/validateprefs')
def ValidatePrefs():
    """
    Validate Prefs
    No Prefs to validate yet
    """

####################################################################################################
@route(CH_PREFIX + '/categorylist')
def CategoryList(title):
    """Setup Category List"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    url = CH_BASE_URL + '/categories/'
    html = HTML.ElementFromURL(url)
    cat_list = []
    for node in html.xpath('//div/a[contains(@href, "categories")]'):
        href = node.get('href').replace(' ', '%20')
        name = node.get('title').strip()
        img = node.xpath('./img/@src')[0]
        if (name != 'All') and ((name, href, img) not in cat_list):
            cat_list.append((name, href, img))
    for (n, h, i) in sorted(cat_list):
        oc.add(DirectoryObject(
            key=Callback(HDOpt, title='Category / %s' %n, href=h),
            title=n, thumb=i, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/hd-opt')
def HDOpt(title, href):
    """
    Default, Channels
    All, HD
    """

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    oc.add(DirectoryObject(
        key=Callback(DirectoryList, title='%s / Default' %title, href=href, page=1),
        title='Default (Site Default List)', art=R(ART_CH)
        ))
    if 'Channels' in title:
        oc.add(DirectoryObject(
            key=Callback(ChannelOpt, title='%s / All' %title, href=href, hd=0),
            title='All (SD & HD)', art=R(ART_CH)
            ))
        oc.add(DirectoryObject(
            key=Callback(ChannelOpt, title='%s / HD' %title, href=href, hd=1),
            title='HD (HD Only)', art=R(ART_CH)
            ))
    else:
        oc.add(DirectoryObject(
            key=Callback(SortBy, title='%s / All' %title, href=href, hd=0),
            title='All (SD & HD)', art=R(ART_CH)
            ))
        oc.add(DirectoryObject(
            key=Callback(SortBy, title='%s / HD' %title, href=href, hd=1),
            title='HD (HD Only)', art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/sortby')
def SortBy(title, href, hd):
    """Sort By (Date, Relevance, Views, Rating)"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in SORT:
        oc.add(DirectoryObject(
            key=Callback(Rating, title='%s / %s' %(title, s), href='%s/1/%s' %(href, h), hd=hd),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/rating')
def Rating(title, href, hd):
    """Rating (All, Super High, High, Medium)"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in RATING:
        oc.add(DirectoryObject(
            key=Callback(Uploaded, title='%s / %s' %(title, s), href='%s/%s' %(href, h), hd=hd),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/uploaded')
def Uploaded(title, href, hd):
    """Uploaded (Any Time, Today, Yesterday, This Week, This Month, 3 Months, This Year)"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in UPLOADED:
        oc.add(DirectoryObject(
            key=Callback(Duration, title='%s / %s' %(title, s), href='%s/%s' %(href, h), hd=hd),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/duration')
def Duration(title, href, hd):
    """Duration (All, Short, Medium, Long)"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in DURATION:
        oc.add(DirectoryObject(
            key=Callback(DirectoryList, title='%s / %s' %(title, s), href='%s/%s/%s' %(href, h, hd), page=1),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/channel/list')
def ChannelList(title, href):
    """Recently Updated, Most Popular, Top Rated, Most Viewed, A-Z"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in CHANNELS:
        if h != 'alphabetical':
            oc.add(DirectoryObject(
                key=Callback(Channels, title='%s / %s' %(title, s), href='%s/%s' %(href, h)),
                title=s, art=R(ART_CH)
                ))
        else:
            oc.add(DirectoryObject(
                key=Callback(Alphabetical, title='%s / A-Z' %title, href='%s/alphabetical' %href),
                title='A-Z', art=R(ART_CH)
                ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/abc')
def Alphabetical(title, href):
    """All, A-Z"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    if 'channels' in href:
        oc.add(DirectoryObject(
            key=Callback(Channels, title='%s / All' %title, href=href),
            title='All', art=R(ART_CH)
            ))
        for c in ['#'] + abc():
            oc.add(DirectoryObject(
                key=Callback(
                    Channels, title='%s / %s' %(title, c),
                    href='%s/1/%s' %(href, c.lower() if c != '#' else '1')),
                title=c, art=R(ART_CH)
                ))
    else:
        oc.add(DirectoryObject(
            key=Callback(PornstarList, title='%s / All' %title, href=href),
            title='All', art=R(ART_CH)
            ))
        for c in abc():
            oc.add(DirectoryObject(
                key=Callback(
                    PornstarList, title='%s / %s' %(title, c),
                    href='%s/%s/overview' %(href, c.lower())),
                title=c, art=R(ART_CH)
                ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/channels')
def Channels(title, href):
    """List channels"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    html = HTML.ElementFromURL(CH_BASE_URL + href)
    nextpg = nextpg_href(html)
    for node in html.xpath('//ul[@class="moviethumbs bigthumbs channelList resizable ignoreViewSwitch"]/li'):
        anode = node.xpath('./a[@class="chtl"]')[0]
        chref = anode.get('href')
        name = anode.text

        bthumb = node.xpath('./a[@class="t"]/img/@src')[0]
        athumb = node.xpath('./a[@class="chtlgx"]/img/@src')[0]

        sum_string = []
        for s in node.xpath('./a[@class="chtlgx"]/b'):
            sum_string.append(s.text)
        summary = ' | '.join([s for s in sum_string])

        oc.add(DirectoryObject(
            key=Callback(HDOpt, title='%s / %s' %(title, name), href=chref),
            title=name, thumb=athumb if athumb else bthumb, art=R(ART_CH)
            ))
    if nextpg:
        oc.add(NextPageObject(
            key=Callback(Channels, title=title, href=nextpg),
            title='Next Page>>', art=R(ART_CH)
            ))

    return oc

####################################################################################################
@route(CH_PREFIX + '/channel/opt')
def ChannelOpt(title, href, hd):
    """Best, Newest, Most Views"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    for h, s in CHANNEL_OPT:
        oc.add(DirectoryObject(
            key=Callback(DirectoryList, title='%s / %s' %(title, s), href='%s/1/%s/%s' %(href, h, hd), page=1),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/popular')
def PopularList(title, href):
    """Today, Yesterday, Week, Month, Year, Hall of Fame"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    plist = ['Today', 'Yesterday', 'Week', 'Month', 'Year', 'Hall of Fame']
    for s in plist:
        oc.add(DirectoryObject(
            key=Callback(DirectoryList,
                title='%s / %s' %(title, s),
                href='%s/%s/1' %(href, s.lower() if s != 'Hall of Fame' else 'all'), page=1),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/pornstar/opt')
def PornstarOpt(title, href):
    """Ratings, Followers, A-Z"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    pslist = [('top', 'Ratings'), ('mostfollowed', 'Followers')]
    oc.add(DirectoryObject(
        key=Callback(Alphabetical, title='%s / A-Z' %title, href=href),
        title='A-Z', art=R(ART_CH)
        ))
    for (h, s) in pslist:
        oc.add(DirectoryObject(
            key=Callback(PornstarList, title='%s / %s' %(title, s), href='%s/%s' %(href, h)),
            title=s, art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/pornstar/list')
def PornstarList(title, href):
    """List Pornstars"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    html = HTML.ElementFromURL(CH_BASE_URL + href)
    nextpg = nextpg_href(html)
    for node in html.xpath('//div[@class="paper paperSpacings xs-fullscreen photoGrid"]/a'):
        phref = node.get('href')
        thumb = node.xpath('./img/@src')[0]
        name = node.xpath('./div/span/text()')[0]

        oc.add(DirectoryObject(
            key=Callback(PornstarCH, title='%s / %s' %(title, name), href=phref, thumb=thumb),
            title=name, thumb=Resource.ContentsOfURLWithFallback(thumb, 'icon-babe-miss.png'),
            art=R(ART_CH)
            ))
    if nextpg:
        oc.add(NextPageObject(
            key=Callback(PornstarList, title=title, href=nextpg),
            title='Next Page>>', art=R(ART_CH)
            ))
    return oc

####################################################################################################
@route(CH_PREFIX + '/pornstar')
def PornstarCH(title, href, thumb):
    """Videos, Photos"""

    html = HTML.ElementFromURL(CH_BASE_URL + href)

    bm_title = title.split('/')[-1].strip()
    bm_id = bm_title.lower().replace(' ', '_')
    ps_error = html.xpath('//meta[@name="canonical"]/@content')[0]
    match = bm_ch.bookmark_exist(item_id=bm_id, category='ClipPornstar')
    header = None
    message = None

    if 'search' in ps_error:
        if match:
            header = title
            message = 'Pornstar Removed from site'
        else:
            return bm_ch.message_container('Warning', 'Pornstar Not Found')

    oc = ObjectContainer(title2=title, header=header, message=message, art=R(ART_CH), no_cache=True)

    if not 'search' in ps_error:
        oc.add(DirectoryObject(
            key=Callback(HDOpt, title='%s / Videos' %title, href='%s/movies' %href),
            title='Videos', thumb=R(ICON_VIDEO), art=R(ART_CH)
            ))
        oc.add(DirectoryObject(
            key=Callback(PhotoAlbumList,
                title='%s / Photos' %title,
                href='%s/photos/1' %href.replace('pornstars', 'models')),
            title='Photos', thumb=R(ICON_PHOTO), art=R(ART_PH)
            ))
        oc.add(DirectoryObject(
            key=Callback(PornstarCHSimilar, title='%s / Similar' %title, href=href),
            title='Similar Pornstars', thumb=R(ICON_SIM), art=R(ART_CH)
            ))

    if not thumb:
        html = HTML.ElementFromURL(CH_BASE_URL + href)
        thumb = html.xpath('//img[@id="modelpic"]/@src')[0]
    bm_ch.add_remove_bookmark(
        oc=oc, title=bm_title, thumb=thumb, url=href, item_id=bm_id,
        category='ClipPornstar', duration=None, tagline=None
        )

    return oc

####################################################################################################
@route(CH_PREFIX + '/pornstar/similar')
def PornstarCHSimilar(title, href):
    """List simialr pornstars"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    html = HTML.ElementFromURL(CH_BASE_URL + href)
    for node in html.xpath('//div[@class="links"]'):
        simnode = node.xpath('./div[@class="frontpageCatTable"]')[0]
        for node2 in simnode.xpath('.//a'):
            phref = node2.get('href')
            thumb = node2.get('data-ps-thumb')
            name = node2.text
            oc.add(DirectoryObject(
                key=Callback(PornstarCH,
                    title='%s / %s' %(title.rsplit('/', 2)[0], name),
                    href=phref, thumb=thumb),
                title=name, thumb=thumb, art=R(ART_CH)
                ))
    if len(oc) > 0:
        return oc
    else:
        return bm_ch.message_container('Similar Pornstar', 'Similar Pornstar list Empty')

####################################################################################################
@route(CH_PREFIX + '/search')
def ClipSearch(query=''):
    """Search ClipHunter"""

    href = '/search/%s' %String.Quote(query.strip(), usePlus=True)
    title = 'Search / %s' %query

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    data = JSON.ObjectFromURL(CH_BASE_URL + '/a/autocomplete?type=model&txt=%s' %String.Quote(query.strip(), usePlus=False))
    if len(data) > 0:
        oc.add(DirectoryObject(
            key=Callback(CHPSearch, query=query.strip(), data=data),
            title='Pornstars', thumb=R(ICON_PSTARS_CH), art=R(ART_CH)
            ))
        oc.add(DirectoryObject(
            key=Callback(HDOpt, title=title, href=href),
            title='Videos', thumb=R(ICON_VIDEO), art=R(ART_CH)
            ))
        return oc
    else:
        return HDOpt(title, href)

####################################################################################################
@route(CH_PREFIX + '/pornstar/search', data=list)
def CHPSearch(query, data):

    if len(data) == 1:
        t = data[0]
        h = '/pornstars/%s' %String.Quote(t, usePlus=True)
        thumb = HTTP.Request(CH_BASE_URL + '/a/modelthumb?name=%s' %String.Quote(t, usePlus=True)).content
        return PornstarCH(t, h, thumb)
    else:
        oc = ObjectContainer(title2='Search / %s' %query, art=R(ART_CH))
        for d in data:
            h = '/pornstars/%s' %String.Quote(d, usePlus=True)
            thumb = HTTP.Request(CH_BASE_URL + '/a/modelthumb?name=%s' %String.Quote(d, usePlus=True)).content
            oc.add(DirectoryObject(
                key=Callback(PornstarCH, title=d, href=h, thumb=thumb), title=d,
                thumb=thumb, art=R(ART_CH)
                ))
        return oc

####################################################################################################
@route(CH_PREFIX + '/bookmarks/main')
def ClipBookmarksMain():
    """
    Setup Bookmark Main Menu.
    Seperate by Pornstar and Video
    """

    bm = Dict['Bookmarks']
    if not bm:
        return bm_ph.message_container('Bookmarks', 'Bookmarks list Empty')

    oc = ObjectContainer(title2='My Bookmarks', art=R(ART_CH), no_cache=True)

    for key in sorted(bm.keys()):
        if len(bm[key]) == 0:
            del Dict['Bookmarks'][key]
            Dict.Save()
        else:
            if key == 'ClipPornstar':
                oc.add(DirectoryObject(
                    key=Callback(ClipBookmarksSub, category=key),
                    title='Pornstars', summary='Display Pornstar Bookmarks',
                    thumb=R(ICON_PSTARS_CH), art=R(ART_CH)
                    ))
            elif key == 'Video':
                oc.add(DirectoryObject(
                    key=Callback(ClipBookmarksSub, category=key),
                    title='Videos', summary='Display Video Bookmarks',
                    thumb=R(ICON_VIDEO), art=R(ART_CH)
                    ))

    if len(oc) > 0:
        return oc
    else:
        return bm_ch.message_container('Bookmarks', 'Bookmark list Empty')

####################################################################################################
@route(CH_PREFIX + '/bookmarks/sub')
def ClipBookmarksSub(category):
    """List Bookmarks Alphabetically"""

    bm = Dict['Bookmarks']
    if not category in bm.keys():
        return bm_ph.message_container('Error',
            '%s Bookmarks list is dirty, or no %s Bookmark list exist.' %(category, category))

    oc = ObjectContainer(title2='My Bookmarks | %s' %category, art=R(ART_CH), no_cache=True)

    for bookmark in sorted(bm[category], key=lambda k: k['title']):
        title = bookmark['title']
        thumb = bookmark['thumb']
        url = bookmark['url']
        category = bookmark['category']
        vid = bookmark['id']
        duration = bookmark['duration']
        tagline = bookmark['tagline']

        if category == 'ClipPornstar':
            oc.add(DirectoryObject(
                key=Callback(PornstarCH, title=title, href=url, thumb=thumb),
                title=title, thumb=Resource.ContentsOfURLWithFallback(thumb, 'icon-babe-miss.png'),
                art=R(ART_CH)
                ))
        elif category == 'Video':
            video_info = {
                'id': vid, 'title': title, 'duration': int(duration),
                'tagline': tagline, 'thumb': thumb, 'url': url
                }
            oc.add(DirectoryObject(
                key=Callback(VideoPage, video_info=video_info),
                title=title, thumb=thumb, art=R(ART_CH)
                ))

    if len(oc) > 0:
        return oc
    else:
        return bm_ch.message_container('Bookmarks', '%s Bookmarks list Empty' %category)

####################################################################################################
@route(CH_PREFIX + '/directorylist', page=int)
def DirectoryList(title, href, page):
    """List Videos by page"""

    url = CH_BASE_URL + href

    html = HTML.ElementFromURL(url)

    nextpg_node = html.xpath('//li/a[@rel="next"]')
    if page == 1 and not nextpg_node:
        main_title = title
    else:
        main_title = '%s | Page %i' %(title, page) if nextpg_node else '%s | Page %i | Last Page' %(title, page)

    oc = ObjectContainer(title2=main_title, art=R(ART_CH))

    for node in html.xpath('//li[@itemtype]'):
        anode = node.xpath('./a[@class="t"]')[0]
        href = anode.get('href')
        vhref = CH_BASE_URL + href
        vid = href.split('/')[2]
        thumb = anode.xpath('./img/@src')[0].strip()

        dur_node = anode.xpath('./div[@class="tr"]/text()')[0].split(':')
        duration = (int(dur_node[0])*60000) + (int(dur_node[1])*1000)

        vtitle = node.xpath('./a[starts-with(@class, "vttl")]/text()')[0].strip()
        tagline = node.xpath('./div[starts-with(@class, "info")]/text()')[0].strip()

        video_info = {
            'id': vid,
            'title': vtitle,
            'duration': duration,
            'tagline': tagline,
            'thumb': thumb,
            'url': vhref
            }

        oc.add(DirectoryObject(
            key=Callback(VideoPage, video_info=video_info),
            title=vtitle, thumb=thumb, tagline=tagline, art=R(ART_CH)
            ))

    if nextpg_node:
        href = nextpg_node[0].get('href')
        if ('popular' in href) or ('pornstars' in href):
            nextpg = int(href.split('/')[4])
        else:
            nextpg = int(href.split('/')[3])
        oc.add(NextPageObject(
            key=Callback(DirectoryList, title=title, href=href, page=nextpg),
            title='Next Page>>', art=R(ART_CH)
            ))

    if len(oc) > 0:
        return oc
    else:
        return bm_ch.message_container('Video List', 'Video List Empty')

####################################################################################################
@route(CH_PREFIX + '/video/thumbs/bin')
def CHPhotoBin(title, thumb, url):
    """Create PhotoAlbum for photos in href"""

    oc = ObjectContainer(title2=title, art=R(ART_CH))
    page = HTTP.Request(url).content
    re_count = Regex(r'var\ mov\_thumbs\ \=\ (\d+?)\;').search(page)
    count = int(re_count.group(1)) if re_count else 30
    it = Regex(r'(.*)\_(\d+)(.*)').search(thumb)
    for i in xrange(count):
        oc.add(CreatePhotoObject(title=str(i+1), url=it.group(1)+'_%i' %(i+1)+it.group(3)))
    return oc

####################################################################################################
@route(CH_PREFIX + '/videopage', video_info=dict)
def VideoPage(video_info):
    """
    Video Sub Page
    Includes Similar Videos and Bookmark Option
    """

    html = HTML.ElementFromURL(video_info['url'])
    video_removed = html.xpath('//blockquote')
    match = bm_ch.bookmark_exist(item_id=video_info['id'], category='Video')
    header = None
    message = None

    if video_removed:
        if match:
            header = video_info['title']
            message = video_removed[0].text_content().strip()
        else:
            return bm_ch.message_container('Warning', 'This video is no longer available.')

    oc = ObjectContainer(title2=video_info['title'], header=header, message=message, art=R(ART_CH), no_cache=True)

    if not video_removed:
        oc.add(VideoClipObject(
            title=video_info['title'],
            duration=video_info['duration'],
            summary=video_info['tagline'],
            thumb=video_info['thumb'],
            art=R(ART_CH),
            url=video_info['url']
            ))

        oc.add(PhotoAlbumObject(
            key=Callback(CHPhotoBin, title=video_info['title'], thumb=video_info['thumb'], url=video_info['url']),
            rating_key = video_info['url']+'/thumbs', source_title='ClipHunter',
            title='Video Thumbs', thumb=R(ICON_PHOTOALBUM), art=R(ART_CH)
            ))

        try:
            related_thumb = html.xpath('//li[@itemtype]/a[@class="t"]/img/@src')[0]
        except:
            try:
                related_thumb = html.xpath('//li/a[@class="t"]/img/@src')[0]
            except:
                related_thumb = ''

        if related_thumb != '':
            oc.add(DirectoryObject(
                key=Callback(DirectoryList, title='Related', href=video_info['url'].split(CH_BASE_URL)[1], page=1),
                title='Related Videos', thumb=related_thumb, art=R(ART_CH)
                ))

        mdl = html.xpath('//a[@class="materialButton mdl ps-popover"]')
        if mdl:
            p_name = mdl[0].text_content().strip()
            p_href = mdl[0].get('href').rsplit('/', 1)[0].replace(' ', '+')
            p_img = HTTP.Request(CH_BASE_URL + '/a/modelthumb?name=%s' %String.Quote(p_name, usePlus=True)).content
            oc.add(DirectoryObject(
                key=Callback(PornstarCH, title=p_name, href=p_href, thumb=p_img),
                title=p_name, thumb=p_img, art=R(ART_CH)
                ))
        chnl = html.xpath('//a[@class="materialButton chnl"]')
        if chnl:
            chnl_title = chnl[0].text_content().strip()
            chnl_href = chnl[0].get('href').replace(' ', '+')
            oc.add(DirectoryObject(
                key=Callback(HDOpt, title='Channels / '+chnl_title, href=chnl_href),
                title=chnl_title, thumb=R(ICON_TV), art=R(ART_CH)
                ))

    bm_ch.add_remove_bookmark(
        oc=oc, title=video_info['title'], thumb=video_info['thumb'], url=video_info['url'],
        item_id=video_info['id'], category='Video', duration=video_info['duration'],
        tagline=video_info['tagline']
        )

    return oc

####################################################################################################
def abc():
    return map(chr, range(ord('A'), ord('Z')+1))

####################################################################################################
def pichunter_list(html, relative=False):
    palist = []
    for node in html.xpath('%s//a[@class="thumb"]' %('.' if relative else '')):
        href = node.get('href')
        title = node.xpath('./img/@alt')[0]
        thumb = node.xpath('./img/@src')[0]
        palist.append((title, thumb, href))
    return palist

####################################################################################################
def nextpg_href(html):
    nextpg_node = html.xpath('//li/a[@rel="next"]')
    href = None
    if nextpg_node:
        href = nextpg_node[0].get('href')
    return href
