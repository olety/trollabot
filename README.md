### Installation 

1. [Install Python](https://www.python.org/downloads/)
2. Compile it in python3 - `python3 trollabot.py`
    * If you want to run it constantly on a Linux server, you can use [screen](https://www.gnu.org/software/screen/)
        1. Install it, `sudo apt-get install screen`
        2. Create a new screen, `screen -S "trollabot"`
        3. Run trollabot, `python3 trollabot.py`
        4. Deattach screen by pressind `ctrl-a ctrl-d`
        5. You can reattach it by using `screen -r "Name"`, or show all screens using `screen -ls`
3. Enjoy!

### Basic commands:

* `!roll d[number]` - returns a random integer from 1 to [number]
* `!kappa` - returns an ascii image of a "Kappa" emote from twitch.tv

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
- [ ] Add logging into a file
- [ ] Add more commands
