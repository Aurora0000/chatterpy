# chatterpy
ChatterPy is a lightweight **IRC bot** framework based on Twisted, designed to be easy to use, with a powerful module loading system and a great amount of flexibility.

## Dependencies
* [yapsy] (http://yapsy.sourceforge.net/)
* [Twisted] (https://twistedmatrix.com)
* Python 2.7 (Twisted doesn't support Python 3)
 
## Creating a plugin
Take a look at plugins/examplePlugin and adjust that for your needs. Wiki coming soon*

*Probably never.

## Configuration File
ChatterPy requires a bot.conf file (in JSON format) with the following attributes (all are required unless specified):

"hostname" - The hostname of the IRC network to connect to (e.g. irc.freenode.net)

"port" - The port of the IRC network (e.g. 6667)

"ssl" - (`"yes"/"no"`)Toggles SSL on (required for some networks)

"nickname" - The nick of the bot

"channels" - An array of channels to join on connection

"logFile" - A location where ChatterPy can log any errors and warnings

"collision_prefix" - *Optional*. Added before nickname if the desired nickname is taken.

"collision_suffix" - *Optional*. Added after nickname if desired nickname is taken.

"enforceVersion" - `"yes"` if plugins should only be loaded if they are compatible with this version of ChatterPy. If bot.log is showing WARNINGs due to version incompatibilities, but you're sure the plugin will work anyway, set this to `"no"`.

It is advisable that at least one of the above is used, or the bot will fail to connect if the desired nick is taken.
