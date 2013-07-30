import random
import re

def bot_dc(mess, nick, botCmd):
    """Play DND style Dice. The default setting is 1d20 (1 20-sided dice)."""
    message = None
    if (len(botCmd) == 1):
        random.seed()
        roll = random.randint(1, 20)
        message = nick + u' rolls ' + str(roll) + u' points. (1d20)'
    elif (len(botCmd) == 2):
        if (re.match(r'[0-9]+[dD][0-9]+', botCmd[1])):
            botCmd[1] = botCmd[1].lower()
            dice = botCmd[1].split('d')
            totalRoll = 0
            rollMessage = botCmd[1] + " = "
            if (dice[0] != '0'):
                if (int(dice[0]) > 1000):
                    return u"You're holding too many dices"
                for i in range(int(dice[0])):
                    # random.seed(None)
                    if (dice[1] != '0'):
                        if (int(dice[1]) > 100000):
                            return u'Your dice has too many sides'
                        roll = random.randint(1, int(dice[1]))
                        rollMessage = rollMessage + '(' + str(roll) + ') + '
                        totalRoll = totalRoll + roll
                    else:
                        return self.optFail(u'Your dice has no side!')
                else:
                    rollMessage = rollMessage[0:len(rollMessage) - 2]
                message = nick + u' rolls ' + str(totalRoll) + u' points.' + rollMessage
            else:
                return self.optFail(u'You have no dice in your hand')
    return message
