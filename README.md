### Linux Preset ![LINUX](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
A simple way to run premade and custom scripts on Linux. E.g. Installing your most used packages on a fresh installation. This was just something to get rid of some boredom lol.

#### Running lp
Command: ``lp``
* To run a preset: ``lp run PRESET_URL_HERE``

#### Install lp
**Make sure to replace "BRANCH" with the branch you would like to install from. E.g. main or 1.0**
* As non-root user, but with sudo: ```wget https://raw.githubusercontent.com/CyberDudeJ/linuxpreset/BRANCH/lp.py && cp lp.py lp && rm gpm.py && sudo chmod +x lp && sudo mv lp /usr/bin```
* As root user, without sudo: ```wget https://raw.githubusercontent.com/CyberDudeJ/linuxpreset/BRANCH/lp.py && cp lp.py lp && rm gpm.py && chmod +x lp && mv lp /usr/bin```
I'll add a better and faster installation script later on.

#### Creating presets
lp uses ``JSON`` to run commands. For example, command 1 would be called "1", command 2 would be called "2", etc.
**Example:** - Make sure to add ``-y`` if you're using apt.
```
{
  "1": "apt-get install btop -y",
  "2": "apt-get install htop -y"
}
```
Remember, if you're using github to host your preset file, you'll need the raw file url.
