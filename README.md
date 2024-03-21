# Bot Orchestrator

Simple program to have IRC bots enter a channel and message publicly and a specific nickname using plain text lists.
Based on code by[Jason R. Coombs ](https://github.com/jaraco) and [Joel Rosdahl](joel@rosdahl.net).

## Usage
```
# With the requirements file loaded
python irc_orchestrator.py [targer.irc.url] [#channel name] [target_nickname]
```
* Edit the constants **BOT_AMOUNT** and **BOT_PULSE_INTERVAL** to establish the ammount of bots to join and how often they speak (in seconds).
* Edit the txt files to define what they should say. 