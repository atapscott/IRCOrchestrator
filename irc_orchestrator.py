#! /usr/bin/env python
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>
# Extended by Alan Tapscott

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
irc.bot.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.
"""
import random
import threading
import time

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr


class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
                self.connection.get_nickname()
        ):
            self.do_command(e, a[1].strip())
        return

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        else:
            c.notice(nick, "Not understood: " + cmd)

    def say_private(self, target_nickname, msg):
        nick = target_nickname
        c = self.connection
        c.notice(nick, msg)

    def say_public(self, msg):
        c = self.connection
        c.privmsg(self.channel, msg)


class BotOrchestrator:
    BOT_AMOUNT = 10
    BOT_PULSE_INTERVAL = [1, 2]

    def __init__(self, channel, target_nickname, server, port=6667):

        self.active_bots = []
        self.channel = channel
        self.server = server
        self.port = port
        self.target_nickname = target_nickname

        self.private_sentence_buffer = self.get_file_lines('privateSentenceList.txt')
        self.public_sentence_buffer = self.get_file_lines('publicSentenceList.txt')

        self.initialize_bots()
        self.pulse_bots()

    def initialize_bots(self):
        bot_names = self.get_names(self.BOT_AMOUNT)
        for bn in range(self.BOT_AMOUNT):
            bot = IRCBot(self.channel, bot_names[bn], self.server, self.port)
            self.active_bots.append(bot)
            thread = threading.Thread(target=bot.start)
            thread.start()

    def pulse_bots(self):

        while True:
            time.sleep(random.randint(self.BOT_PULSE_INTERVAL[0], self.BOT_PULSE_INTERVAL[1] + 1))
            agent_bot = random.choice(self.active_bots)

            if random.randint(1, 3) > 1:
                self.send_private_message(agent_bot)
            else:
                self.send_public_message(agent_bot)

    def send_private_message(self, agent_bot_sayer):
        if len(self.private_sentence_buffer) == 0:
            self.private_sentence_buffer = self.get_file_lines('privateSentenceList.txt')

        private_sentence = random.choice(self.private_sentence_buffer)
        self.private_sentence_buffer.remove(private_sentence)

        agent_bot_sayer.say_private(self.target_nickname, private_sentence)

    def send_public_message(self, agent_bot_sayer):
        if len(self.public_sentence_buffer) == 0:
            self.public_sentence_buffer = self.get_file_lines('publicSentenceList.txt')

        private_sentence = random.choice(self.public_sentence_buffer)
        self.public_sentence_buffer.remove(private_sentence)

        agent_bot_sayer.say_public(private_sentence)

    def get_names(self, amount):
        return random.sample(self.get_file_lines('botNameList.txt'), amount)

    def get_private_sentences_buffer(self, amount):
        return self.get_file_lines('privateSentenceList.txt')

    def get_file_lines(self, file_url):
        try:
            with open(file_url, 'r') as lines:
                out_lines = [line.strip() for line in lines.readlines()]
                return out_lines
        except Exception as e:
            return []


def main():
    import sys

    if len(sys.argv) != 4:
        print("Usage: irc_orchestrator <server[:port]> <channel> <target_nickname>")
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print("Error: Erroneous port.")
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    target_nickname = sys.argv[3]

    bo = BotOrchestrator(channel, target_nickname, server, port)


if __name__ == "__main__":
    main()
