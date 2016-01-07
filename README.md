### Installation 

1. [Install Python](https://www.python.org/downloads/)
2. Run it using python3 - `python3 trollabot.py`
    * If you want to run it constantly on a Linux server, you can use [screen](https://www.gnu.org/software/screen/)
        1. Install it, `sudo apt-get install screen`
        2. Create a new screen, `screen -S "trollabot"`
        3. Run trollabot, `python3 trollabot.py`
        4. Deattach screen by pressind `ctrl-a ctrl-d`
        5. You can reattach it by using `screen -r "Name"`, or show all screens using `screen -ls`
3. Add the bot user to your chat/friends
4. Enjoy!


### Basic commands:


#### Multi-word commands :

* `!roll d[number]` - returns a random integer from 1 to [number]
   
#### Single-word commands :

* `!kappa` - returns an ascii image of a "Kappa" emote from twitch.tv
* `!keepo` - returns an ascii image of a "Keepo" emote from twitch.tv
* `!patrick` - returns an ascii image of a "Patrick" character from Spoge Bob Square Pants
* `!doggy` - returns an ascii image of a cool dog
* `!doge` - returns an ascii image of a Shibe - the dog from "Doge" meme
* `!frankerz` - returns an ascii image of a "FrankerZ" emote from twitch.tv
* `!dansgame` - returns an ascii image of a "DansGame" emote from twitch.tv
* `!pjsalt` - returns an ascii image of a "PJSalt" emote from twitch.tv
* `!pogchamp` - returns an ascii image of a "PogChamp" emote from twitch.tv
* `!grill` - returns an ascii image of a girl
* `!squid` - returns an ascii image of a squid
   
ASCII images taken from http://twitchascii.blogspot.com


### Admin Commands


* `!stop` - stops a bot from replying to all messages
* `!start` - makes it so bot will answer messages again
* `!restart` - restarts a bot, useful for applying new settings
* `!exit` - exits a bot, and stops the program completely


### Adding new commands 


* If you want to add new one-word commands, like `!kappa`, use the settings.json file and add them in the second element of a settings array (see the example-settings.json file)
* To add multi-word commands, like `!roll d6`, modify the ifs in the `_parseMsg` method


### Progress


- [x] Add multi-word commands support
- [x] Add single-word commands support
- [x] Add single-word commands processing using JSON
- [x] Add admin commands 
- [x] Add more commands
- [x] Add logging into a file
- [ ] Add even more commands
