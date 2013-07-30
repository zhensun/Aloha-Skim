#!/usr/bin/python
# -*- coding:utf-8 -*-

# JabberBot: A simple jabber/xmpp bot framework
# Copyright (c) 2007 Thomas Perl <thp@thpinfo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Homepage: http://thpinfo.com/2007/python-jabberbot/
#


import xmpp
import inspect, re
import datetime
import os
import os.path
import sys

"""A simple jabber/xmpp bot framework

This is a simple bot framework around the "xmpppy" framework.
Copyright (c) 2007 Thomas Perl <thp@thpinfo.com>

To use, subclass the "JabberBot" class and implement "bot_" methods
(or whatever you set the command_prefix to), like this:

class StupidEchoBot(JabberBot):
    def bot_echo( self, mess, args):
        "The command description goes here"
        return 'You said: ' + args

    def bot_subscribe( self, mess, args):
        "Send the subscribe command to have me authorize your subscription to my presence"
        f = mess.getFrom()
        self.conn.Roster.Authorize( f)
        return 'Authorized.'

    def unknown_command( self, mess, cmd, args):
        "This optional method, if present, gets called if the
        command is not recognized."
        if args.split()[0].startswith( 'cheese'):
            return 'Sorry, cheesy commands not available.'
        else:
            # if we return None, the default 'unknown command' text will get printed.
            return None

username = 'jid@server.example.com'
password = 'mypassword'

bot = StupidEchoBot( username, password)
bot.serve_forever()

"""
# For top 5 user
userList = {}
timeLastSubmit = datetime.datetime.now()

class JabberBot(object):

    command_prefix = 'bot_'

    def __init__( self, jid, password, res = None):
        """Initializes the jabber bot and sets up commands."""
        self.jid = xmpp.JID( jid)
        self.password = password
        self.res = (res or self.__class__.__name__)
        self.conn = None
        self.__finished = False

        self.commands = { 'help': self.help_callback, }
        for (name, value) in inspect.getmembers( self):
            if inspect.ismethod( value) and name.startswith( self.command_prefix):
                self.commands[name[len(self.command_prefix):]] = value

        # Load modules from directory
        print("-----------------\nLoading Modules\n-----------------")
        # Get filenames of python files in modules directory
        moduleFiles = [fname[:-3] for fname in os.listdir('modules') if ((fname.endswith(".py")) and (fname[0] != '_'))]
        # Add module directory to system path
        sys.path.insert(0,'modules')
        for fname in moduleFiles:
            # Import module using __import__
            module = __import__(fname)
            for (name, value) in inspect.getmembers(module):
                if inspect.isfunction( value) and name.startswith( self.command_prefix):
                    # Add functions begin with prefix to bot's command list
                    self.commands[name[len(self.command_prefix):]] = value
                    print("Loaded " + name)
        # Delete module directory from system path
        del sys.path[0]

    def log( self, s):
        """Logging facility, can be overridden in subclasses to log to file, etc.."""
        print '%s: %s' % ( self.__class__.__name__, s, )

    def connect( self):
        if not self.conn:
            #conn = xmpp.Client( self.jid.getDomain(), debug = [])
            conn = xmpp.Client('gmail.com', debug = [])
            if not conn.connect(server=('talk.google.com',5223)):
                self.log( 'unable to connect to server.')
                return None

            if not conn.auth( self.jid.getNode(), self.password, self.res):
                self.log( 'unable to authorize with server.')
                return None

            conn.RegisterHandler( 'message', self.callback_message)
            conn.sendInitPresence()
            self.conn = conn

        return self.conn

    def quit( self):
        """Stop serving messages and exit.

        I find it is handy for development to run the
        jabberbot in a 'while true' loop in the shell, so
        whenever I make a code change to the bot, I send
        the 'reload' command, which I have mapped to call
        self.quit(), and my shell script relaunches the
        new version.
        """
        self.__finished = True

    def send( self, user, text, in_reply_to = None):
        """Sends a simple message to the specified user."""
        mess = xmpp.Message( user, text)
        if in_reply_to:
            mess.setThread( in_reply_to.getThread())
            mess.setType( in_reply_to.getType())

        self.connect().send( mess)

    def adduserlist(self, nick):
        global timeLastSubmit
        currentTime = datetime.datetime.now()
        gap = currentTime - timeLastSubmit
        """docstring for adduserlist"""
        if (userList.has_key(nick)):
            userList[nick] += 1
        else:
            userList[nick] = 1
        print userList
        if (gap.seconds > 30):
            # self.addUserDatabase(userList)
            userList.clear()
            timeLastSubmit = datetime.datetime.now()
        pass

    def callback_message( self, conn, mess):
        """Messages sent to the bot will arrive here. Command handling + routing is done in this function."""
        text = mess.getBody()
        reply = None
        # If a message format is not supported (eg. encrypted), txt will be None
        if not text:
            return

        if text.startswith("*"):
        	return

        if text.startswith('<'):
            nick = text[text.find('<')+1:text.find('>')]
            text = text[text.find('>') + 1:]
        else:
            nickText = str(mess.getFrom())
            nick = nickText[:nickText.find('/')]

        command, args = text,''

#        cmd = command.lower()
        cmd = command
        text = text.strip()
        self.adduserlist(nick)
        if text.startswith("~~"):
            if (re.match(r'^\w', text[2:])):
                text = "!d " + text[2:]
        if text.startswith("!"):
            botCmd = text.split(" ", 1)
            botCmd[0] = botCmd[0].lower()
            botCmd[0] = botCmd[0][1:]
            if self.commands.has_key(botCmd[0]):
                if (botCmd[0] == 'list'):
                    global userList
                    reply = self.bot_list(mess, nick, botCmd, userList)
                else:
                    reply = self.commands[botCmd[0]]( mess, nick, botCmd)
        else:
            unk_str = ''
            reply = self.unknown_command( mess, nick, cmd, args) or unk_str
        if reply:
            self.send( mess.getFrom(), reply, mess)

    def unknown_command( self, mess, nick, cmd, args):
        """Default handler for unknown commands

        Override this method in derived class if you
        want to trap some unrecognized commands.  If
        'cmd' is handled, you must return some non-false
        value, else some helpful text will be sent back
        to the sender.
        """
        return None

    def help_callback( self, mess, nick, botCmd):
        """Returns a help string listing available options. Automatically assigned to the "help" command."""
        usage = '\n'.join( [ '%s: %s' % ( name, command.__doc__ or '(undocumented)' ) for ( name, command ) in self.commands.items() if name != 'help' ])

        if self.__doc__:
            description = self.__doc__.strip()
        else:
            description = 'Available commands:'

        return '%s\n\n%s' % ( description, usage, )
        #return "The first rule of Fight Club is - you do not talk about Fight Club."
    def idle_proc( self):
        """This function will be called in the main loop."""
        pass

    def serve_forever( self, connect_callback = None, disconnect_callback = None):
        """Connects to the server and handles messages."""
        conn = self.connect()
        if conn:
            self.log('bot connected. serving forever.')
        else:
            self.log('could not connect to server - aborting.')
            return

        if connect_callback:
            connect_callback()

        while not self.__finished:
            try:
                conn.Process(1)
                self.idle_proc()
            except KeyboardInterrupt:
                self.log('bot stopped by user request. shutting down.')
                break

        if disconnect_callback:
            disconnect_callback()
