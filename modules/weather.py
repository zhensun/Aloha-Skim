import re
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup

def bot_w(mess, nick, botCmd):
    """Weather forecast"""
    if (len(botCmd) == 1):
        message = u"Usage: !weather + City Name or zip code"
    else:
        cityname = botCmd[1]
        url = 'http://search.weather.com.cn/static/url.php'
        values = {'cityinfo': cityname.encode('utf8')}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        url = the_page[the_page.find('URL=')+4:len(the_page)-3]
        request = urllib2.Request(url)
        page = urllib2.urlopen(request).read()
        message = 'Cannot find such a city'
        if page.find('<div class="box_contenttodayinwea" id="c_1_1">') != -1:
            soup = BeautifulSoup(page)
            message = str(soup.head.title)
            message = message[7:message.find('-')] + ', '
            page = page[page.find('<div class="box_contenttodayinwea" id="c_1_1">'):]
            page = page[:page.find('</div>') + 6]
            soup = BeautifulSoup(page)
            ems = soup.fetch('em')

            for i in range(0, 3):
                message = message + re.sub('<(.|\n)+?>', '', str(ems[i]))
                if i < 2:
                    message = message + ', '
    return message
