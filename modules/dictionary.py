import os

def bot_ec(mess, nick, botCmd):
    """Lookup in an English-Chinese dictionary. Shortcut: ~~word"""
    path = "/usr/bin/"
    """Look up word in dict via sdcv"""
    if (len(botCmd) == 1):
        message = u"/me says：“Please type in format: ‘!d word’”"
    else:
        word = botCmd[1]
        cmd = path + "sdcv --utf8-output -n '" + word + u"'| grep -E '^\-\->[A-z]|^[a-z\*【]'"
        result = os.popen(cmd.encode("UTF-8"), "r").read()
        if result:
            if result.count('-->') > 1:
                firstArrowPosition = result.find('-->')
                secondArrowPosition = result.find('-->', firstArrowPosition + 3)
                result = result[:secondArrowPosition]
            message = '/me says:\n' + result
        else:
            message = self.optFail(u"Word not found.")
    return message

def bot_ce(mess, nick, botCmd):
    """Lookup in a Chinese-English dictoinary"""
    path = "/usr/bin/"
    """Look up word in dict via sdcv"""
    if (len(botCmd) == 1):
        message = u"/me says：“Please type in format: ‘!d word’”"
    else:
        word = botCmd[1]
        cmd = path + "sdcv --utf8-output --utf8-input -n '" + word +"'"
        result = os.popen(cmd.encode("UTF-8"), "r").read()
        if result:
            if result.count('-->') > 1:
                # firstArrowPosition = result.find('-->')
                # secondArrowPosition = result.find('-->', firstArrowPosition + 3)
                # result = result[:secondArrowPosition]
                message = '/me says:\n' + result
        else:
            message = self.optFail(u"Word not found.")
    return message

def bot_d(mess, nick, botCmd):
    """Lookup in an English-Chinese dictionary. Shortcut: ~~word"""
    path = "/usr/bin/"
    """Look up word in dict via sdcv"""
    if (len(botCmd) == 1):
        message = u"/me says：“Please type in format: ‘!d word’”"
    else:
        word = botCmd[1]
        cmd = path + "sdcv --utf8-output -n '" + word + u"'| grep -E '^\-\->[A-z]|^[a-z\*【]'"
        result = os.popen(cmd.encode("UTF-8"), "r").read()
        if result:
            if result.count('-->') > 1:
                firstArrowPosition = result.find('-->')
                secondArrowPosition = result.find('-->', firstArrowPosition + 3)
                result = result[:secondArrowPosition]
            message = '/me says：\n' + result
        else:
            message = self.optFail(u"Word not found.")
    return message
