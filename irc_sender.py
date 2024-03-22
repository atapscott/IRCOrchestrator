#! /usr/bin/env python
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>
# Extended by Alan Tapscott

import irc.client
import sys
import random


class IRCSenderBot(irc.client.SimpleIRCClient):
    def __init__(self, target, out_file_URL):
        irc.client.SimpleIRCClient.__init__(self)
        self.target = target
        self.out_file_URL = out_file_URL

    def on_welcome(self, connection, event):
        connection.join(self.target)

    def on_join(self, c, e):
        out_message = self.get_file_output(self.out_file_URL)
        out_message = out_message.replace('\n', ' ')
        c.privmsg(self.target, out_message)
        c.disconnect()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def get_file_output(self, file_url):
        with open(file_url, 'r') as in_file:
            return in_file.read()

    def get_random_nickname(selfs):
        with open('botNameList.txt', 'r') as name_lines:
            names = [line.strip() for line in name_lines.readlines()]
            return random.choice(names)


def main():
    if len(sys.argv) != 4:
        print("Usage: irccat2 <server[:port]> <ouputFileURL> <target>")
        print("\ntarget is a nickname or a channel.")
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

    target = sys.argv[2]
    out_file_url = sys.argv[3]

    c = IRCSenderBot(target, out_file_url)
    try:
        nickname = c.get_random_nickname()
        c.connect(server, port, nickname)
    except irc.client.ServerConnectionError as x:
        print(x)
        sys.exit(1)
    c.start()


if __name__ == "__main__":
    main()