# chatterpy
ChatterPy is a lightweight bot framework based on Twisted, designed to be easy to use, with a powerful module loading system and a great amount of flexibility..
## Configuration File
ChatterPy requires a bot.conf file (in JSON format) with the following attributes (all are required unless specified):
"hostname" - The hostname of the IRC network to connect to (e.g. irc.freenode.net)
"port" - The port of the IRC network (e.g. 6667)
"ssl" - Toggles SSL on (required for some networks)
"nickname" - The nick of the bot
"channels" - An array of channels to join on connection
"logFile" - A location where ChatterPy can log any errors and warnings
"collision_prefix" - *Optional*. Added before nickname if the desired nickname is taken.
"collision_suffix" - *Optional". Added after nickname if desired nickname is taken.
It is advisable that at least one of the above is used, or the bot will fail to connect if the desired nick is taken.
