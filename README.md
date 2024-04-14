# IRC Bot Orchestrator

Based on code by [Jason R. Coombs ](https://github.com/jaraco) and [Joel Rosdahl](https://github.com/jrosdahl).
## Sender

Simple bot that sends the content of a text file to the target IRC server and channel.
```
# With the requirements file loaded and any desired virtualenv
# Escape the # if needed (perhaps use \ or surround with quotes the channel name)
python irc_sender.py [target.irc.url] [#channel name] [output_file_url]

```

## Orchestrator
Simple program to have IRC bots enter a channel and message publicly and a specific nickname using plain text lists.


## Usage
```
# With the requirements file loaded and any desired virtualenv
# Escape the # if needed (perhaps use \ or surround with quotes the channel name)
python irc_orchestrator.py [target.irc.url] [#channel name] [target_nickname]
```
* Edit the constants **BOT_AMOUNT** and **BOT_PULSE_INTERVAL** to establish the amount of bots to join and how often they speak (in seconds).
* Edit the txt files to define what they should say. 