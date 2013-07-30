from pysqlite2 import dbapi2 as sqlite
import datetime

# Path for database file
dbPath = '/home/sun/src/alohabot/spdb.db'

def bot_get(mess, nick, botCmd):
    """Get a user-defined word"""

    if (len(botCmd) == 1):
        message = u"/me says: Please use !get to get definitions."
    else:
        defWord = botCmd[1].split(" ", 1)
        sql = 'SELECT * FROM defword WHERE word like "' + defWord[0] + '"'

        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute(sql)

        result = cursor.fetchone()
        #
        if (result != None):
            message = "/me (" + result[2] + ") " + defWord[0] + ": \n" + result[1] + " --" + result[3]
            if (result[4] == 1):
                message = message + " (locked)"
        else:
            message = optFail(u"Term has not been defined yet.")
        cursor.close()
        connection.close()
    return message

def bot_set(mess, nick, botCmd):
    """Set a word's defination"""
    if (len(botCmd) == 1):
        message = u"/me says: Please use !set to define a term"
    else:
        defWord = botCmd[1].split(" ", 1)

        if (len(defWord) == 2):
            sql = 'SELECT * FROM defword WHERE word like "' + defWord[0] + '"'

            connection = sqlite.connect(dbPath)
            cursor = connection.cursor()
            cursor.execute(sql)

            result = cursor.fetchone()
            if (result == None):
                cursor.execute('INSERT INTO defword VALUES (?, ?, ?, ?, 1)',(defWord[0], defWord[1], nick, datetime.datetime.ctime(datetime.datetime.now())))
                connection.commit()
                message = optSuccess(u"Term defined.")

            else:
                if (result[4] == 0):
                    cursor.execute('UPDATE defword SET def = ? , owner = ? , locked = 1 WHERE word = ?', (defWord[1], nick, result[0]))
                    connection.commit()
                    message = optSuccess(u"Term defined.")
                elif (result[4] == 1):
                    message = optFail(u'Term has already been defined, please !unlock first')
                elif (result[4] == 2):
                    message = optFail(u'Term has been locked.')
            cursor.close()
            connection.close()
        else:
            message = u"/me says: Please use !set to define a term"
    return message

def bot_lock(mess, nick, botCmd):
    """Lock defined word"""

    if (len(botCmd) == 1):
        message = u"/me says: Please use !lock to lock a term."
    else:
        defWord = botCmd[1].split(" ", 1)
        sql = 'SELECT * FROM defword WHERE word like "' + defWord[0] + '"'

        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute(sql)

        result = cursor.fetchone()
        #
        if (result != None):
            if(result[4] != 1):
                cursor.execute('UPDATE defword SET locked = 1 WHERE word = "' + result[0] + '"')
                connection.commit()
                message = optSuccess(u'Term locked.')
            else:
                message = optFail(u'Term has already been locked.')
        else:
            message = optFail(u"Term has not been defined yet.")
        cursor.close()
        connection.close()
    return message

def bot_unlock(mess, nick, botCmd):
    """Unlock defined word"""

    if (len(botCmd) == 1):
        message = u"/me says: Please use !unlock to unlock a term."
    else:
        defWord = botCmd[1].split(" ", 1)
        sql = 'SELECT * FROM defword WHERE word like "' + defWord[0] + '"'

        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute(sql)

        result = cursor.fetchone()
        #
        if (result != None):
            if(result[4] != 0):
                cursor.execute('UPDATE defword SET locked = 0 WHERE word = "' + result[0] + '"')
                connection.commit()
                message = optSuccess(u'Term unlocked.')
            else:
                message = optFail(u'Term is not locked.')
        else:
            message = optFail(u"Term has not been defined yet.")
        cursor.close()
        connection.close()
    return message

def optSuccess(message):
    return u'/me says：“' + message + u"”"
def optFail(message):
    return u'/me says：“' + message + u"”"
