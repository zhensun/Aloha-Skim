#!/usr/bin/python
# -*- coding:utf-8 -*-

from jabberbot import JabberBot
from pysqlite2 import dbapi2 as sqlite

import datetime, random, os, re, codecs

# Fill in the JID + Password of your JabberBot here...
(JID, PASSWORD) = ('alohabot@gmail.com','')

class Speaker(JabberBot):

    def bot_list(self, mess, nick, botCmd, userList):
        """List recent active users"""
        message = ''
        for key in userList:
            message = message + key + ': ' + str(userList[key]) + '\n'
        return message

    def unknown_command( self, mess, nick, cmd, args):
        "This optional method, if present, gets called if the command is not recognized."
        cmdargs = cmd + args
        import urllib
        urlregex = '(?#Protocol)(?:http(?:s?)\:\/\/|~/|/)(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?'
        source = re.search(urlregex, cmdargs)

        if (source != None):
            source = source.span()
            urlstr = cmdargs[source[0]:source[1]]
            try:
                sock = urllib.urlopen(urlstr)
            except Exception, e:
                return e[1][1]
            if ('text/html' in sock.info()['Content-type']):
                htmlSource = sock.read(1000000)
                sock.close()
                if ("<title>" in htmlSource.lower()):
                    from BeautifulSoup import BeautifulSoup
                    from BeautifulSoup import BeautifulStoneSoup
                    soup = BeautifulSoup(htmlSource)
                    if (soup.html.head.title != None):
                        titleText = str(soup.html.head.title)
                        titleText = titleText[7:len(titleText)-8]
                        titleText = BeautifulStoneSoup(titleText, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
                        return titleText.strip()
                    else:
                        return "Title of the page is empty."
                else:
                    return "No Title."
        cmdargs = cmdargs.lower().strip()
        # if(str(mess.getFrom()).startswith("chat.mozine@gmail.com")):
        #     if(holderName != "" and holderName != nick and cmdargs.find(u"独霸") == -1):
        #         self.breakUp(nick, mess)
        #     if (u"独霸" in cmdargs):
        #         previousHolderName = ""
        #         currentTime = datetime.datetime.now()
        #         global holderName
        #         global holderTime
        #         if(holderName == ""):
        #             holderName = nick
        #             holderTime = currentTime
        #         elif(holderName != nick):
        #             time = currentTime - holderTime
        #             timeStr = self.ConvertSeconds(time.seconds)
        #             msg = holderName + u"的独霸地位被" + nick + u"取代了，" + holderName + u"称霸了 " + timeStr
        #             holderName = nick
        #             holderTime = currentTime
        #             self.send(mess.getFrom(), msg, mess)
        #
        # if(str(mess.getFrom()).startswith("chat.mimijidi@gmail.com")):
        #     if(holderNameM != "" and holderNameM != nick and cmdargs.find(u"独霸") == -1):
        #         self.breakUpM(nick, mess)
        #     if (u"独霸" in cmdargs):
        #         previousHolderName = ""
        #         currentTime = datetime.datetime.now()
        #         global holderNameM
        #         global holderTimeM
        #         if(holderNameM == ""):
        #             holderNameM = nick
        #             holderTimeM = currentTime
        #         elif(holderNameM != nick):
        #             time = currentTime - holderTimeM
        #             timeStr = self.ConvertSeconds(time.seconds)
        #             msg = holderNameM + u"的独霸地位被" + nick + u"取代了，" + holderNameM + u"称霸了 " + timeStr
        #             holderNameM = nick
        #             holderTimeM = currentTime
        #             self.send(mess.getFrom(), msg, mess)

        quotes = ["blah"]

        eight = [u'以热爱祖国为荣、以危害祖国为耻',
        u'以服务人民为荣、以背离人民为耻',
        u'以崇尚科学为荣、以愚昧无知为耻',
        u'以辛勤劳动为荣、以好逸恶劳为耻',
        u'以团结互助为荣、以损人利己为耻',
        u'以诚实守信为荣、以见利忘义为耻',
        u'以遵纪守法为荣、以违法乱纪为耻',
        u'以艰苦奋斗为荣、以骄奢淫逸为耻']

        if (("os" in cmdargs or
             "Thanks" in cmdargs) and random.randint(0, 100) > 50):
            random.seed()
            return u'/me says：“' + quotes[random.randint(0, len(quotes) -1)] + u'”'
        if (u"和谐" in cmdargs or
        u"河蟹" in cmdargs):
        	random.seed()
        	return eight[random.randint(0, len(eight) -1)]
        if (u"Jesus" in cmdargs or
        u"God" in cmdargs or
        u"Bible" in cmdargs or
        u"Pray" in cmdargs or
        u"Amen" in cmdargs):
            random.seed()
            fh = codecs.open("bible.txt", "r", "utf-8")
            lineNum = random.randint(0, 31102)
            bible = ''
            for i in range (0, lineNum):
                fh.readline()
            bible = fh.readline()
            bible = bible.strip()
            fh.close()
            return u"“" + bible + u"”"
        if (u"和谐" in cmdargs or
        u"河蟹" in cmdargs):
        	random.seed()
        	return eight[random.randint(0, len(eight) -1)]
        if (u"诗篇" in cmdargs or
        "psm" in cmdargs):
            random.seed()
            fh = codecs.open("psm.txt", "r", "utf-8")
            lineNum = random.randint(0, 2461)
            bible = ''
            for i in range (0, lineNum):
                fh.readline()
            bible = fh.readline()
             bible = bible.strip()
            fh.close()
            return u"“" + bible + u"”"
        if (u"箴言" in cmdargs or
        "pro" in cmdargs):
            random.seed()
            fh = codecs.open("pro.txt", "r", "utf-8")
            lineNum = random.randint(0, 915)
            bible = ''
            for i in range (0, lineNum):
                fh.readline()
            bible = fh.readline()
            bible = bible.strip()
            fh.close()
            return u"“" + bible + u"”"
        if (cmdargs.startswith('aloha')):
            random.seed()
            fh = codecs.open("fianjmo.txt", "r", "utf-8")
            lineNum = random.randint(0, 1929)
            bible = ''
            for i in range (0, lineNum):
                fh.readline()
            fianjmo = fh.readline()
            fianjmo = fianjmo.strip()
            fh.close()
            return fianjmo


    def breakUp(self, nick, mess):
        """breakup duba"""
        global holderTime
        global holderName

        currentTime = datetime.datetime.now()
        time = currentTime - holderTime
        timeStr = self.ConvertSeconds(time.seconds)
        msg = holderName + u"称霸了 " + timeStr
        self.send( mess.getFrom(), msg, mess)
        holderName = ""
        holderTime = None

    def breakUpM(self, nick, mess):
        """breakup duba"""
        global holderTimeM
        global holderNameM

        currentTime = datetime.datetime.now()
        time = currentTime - holderTimeM
        timeStr = self.ConvertSeconds(time.seconds)
        msg = holderNameM + u"称霸了 " + timeStr
        self.send( mess.getFrom(), msg, mess)
        holderNameM = ""
        holderTimeM = None

    def ConvertSeconds(self, seconds):
        """convert seconds to hours and minutes in Chinese"""
        minutes = seconds/60
        hours = minutes/60
        days = hours/24
        seconds = seconds%60
        minutes = minutes%60
        hours = hours%24
        timeStr = ""
        if (days != 0):
            timeStr = timeStr + " " + str(days) + u" 天"
        if (hours != 0):
            timeStr = timeStr + " " + str(hours) + u" 小时"
        if (minutes != 0):
            timeStr = timeStr + " " + str(minutes) + u" 分"
        if (seconds != 0):
            timeStr = timeStr + " " + str(seconds) + u" 秒"
        return timeStr
    def optSuccess(self, message):
        return u'/me says：“' + message + u"”"
    def optFail(self, message):
        return u'/me shakes its head：“' + message + u"”"
def forever():
    """Open server forever"""
    try:
        bot = Speaker( JID, PASSWORD)
        bot.serve_forever()
    except Exception, e:
        print e
        forever()
    pass

forever()
