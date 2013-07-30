# Get random number betwen 1 and 100

import random

def bot_roll(mess, nick, botCmd):
    """Get a random number between 1 and 100 (WoW style)"""
    random.seed()
    roll = random.randint(1, 100)
    if (len(botCmd) > 1):
        event = botCmd[1]
        message = nick + u' Rolled on ' + event + u' , gets ' + str(roll) + u' points.'
    else:
        message = nick + u' gets ' + str(roll) + u' points.'
    return message
    pass
