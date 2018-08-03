# SmileToOpen
DeepLearning pretrained network to handle face identification for garage door opening/closing.

## Install
1. Edit crontab
You have to modify the crontab in order to launch the script every time your raspberry starts :
``` sudo crontab -e```
``` @reboot /your_path/recognize.sh```
2. Electrical connections
* GPIO pin 6 is used as a GROUND.
* GPIO pin 7 is used as a positive output (+1.5V).
Figure 1, Raspberry pin board: ![alt text](https://i.stack.imgur.com/gaU6t.png "Raspberry pin board")


