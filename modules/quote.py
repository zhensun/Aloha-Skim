from pysqlite2 import dbapi2 as sqlite
import random, re

# Path for database file
dbPath = '/home/sun/src/alohabot/spdb.db'

def bot_setquote(mess, nick, botCmd):
    """Insert a quote into database. A quote CANNOT be deleted."""

    message = None

    if (len(botCmd) == 1):
        message = u'What are you trying to set?'
    else:
        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO quotes VALUES (?, ?)',(botCmd[1], nick))
        connection.commit()
        message = u'Set: epic time [' + str(cursor.lastrowid) + u']'
        cursor.close()
        connection.close()
    return message

def bot_quote(mess, nick, botCmd):
    """Get quotes from database. Use !quote for a random quote, and !quote <num> for a particular quote."""
    message = None
    if (len(botCmd) == 1):
        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute("SELECT rowid, * FROM quotes ORDER BY RANDOM() LIMIT 1")
        quote = cursor.fetchone()
        message = u'Epic time [' + str(quote[0]) + u']：' + quote[1] + ' (set by ' + quote[2] + ')'
    elif (len(botCmd) == 2):
        connection = sqlite.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute("SELECT max(rowid) FROM quotes")
        maxQuote = cursor.fetchone()
        if (re.match(r'[0-9]+', botCmd[1])):
                if (int(botCmd[1]) <= maxQuote[0]):
                    roll = botCmd[1]
                    cursor.execute("SELECT * FROM quotes WHERE rowid =" + str(roll))
                    quote = cursor.fetchone()
                    message = u'Epic time[' + str(roll) + u']：' + quote[0] + ' (set by ' + quote[1] + ')'
                else:
                    message = 'Max quote: ' + str(maxQuote[0])
        else:
            message = 'Max quote: ' + str(maxQuote[0])
    return message
