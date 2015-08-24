#!/usr/bin/env python

import getpass
import sys

import click
import sleekxmpp

import logging
logger = logging.getLogger('bot')

log_datefmt = "%H:%M:%S"
log_format = "%(asctime)s:%(msecs)03d %(levelname)-8s: %(name)-20s: %(message)s"


# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class Bot(sleekxmpp.ClientXMPP):
    '''
        Very simple XMPP bot implementation derived from echobot
        
        http://sleekxmpp.com/getting_started/echobot.html
    '''

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multiuser chat

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """

        self.send_presence()
        self.get_roster()


        # Fun with chat rooms:
        # self.plugin['xep_0045'].joinMUC('room@conference.server.local',
        #                                 self.requested_jid.user,
        #                                 wait=True)
        #
        # Send a message to a chat room:
        #
        # self.send_mesage(mto=room, mbody='text here', mtype='groupchat')
        
    
    def message(self, msg):
        """
        Called when messages are received by this bot from a random user
        """
        logger.info("Received from %s: %s", msg['from'], msg['body'])
        
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()



@click.command()
@click.option("-j", "--jid", help="JID to use")
@click.option("-p", "--password", help="password to use")
@click.option("-v", "--verbose", help="Verbose logging", is_flag=True, default=False)
def main(**options):
    
    logging.basicConfig(level=logging.DEBUG if options['verbose'] else logging.INFO,
                        format=log_format, datefmt=log_datefmt)
    
    if options['jid'] is None:
        options['jid'] = raw_input("Username: ")
    if options['password'] is None:
        options['password'] = getpass.getpass("Password: ")
    
    # Start the bot up with an appropriate username/password
    xmpp = Bot(options['jid'], options['password'])
    
    if xmpp.connect():
        logger.info("Connected to server!")
        xmpp.process(block=True)
    else:
        logger.error("Error connecting to server")
    

if __name__ == '__main__':
    main()
