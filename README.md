# rpi-cec-unit
Building a raspberry pi into a robust HDMI-CEC IP interface

# What?
There are some commercially available HDMI-CEC to IP interfaces for things like Control4, Crestron, etc. They cost hundreds of pounds/dollars. In the same universe, Home Assistant and Raspberry Pis exist. Surely, the expensive commercial offerings are not the only choice?

# Shopping list
Raspberry Pi Zero W (or Zero 2 W)
SD card for Raspberry Pi OS
Adafruit PiOLED
1 x M2.5 11mm standoff
3 x M2.5 18mm screws
1 x M2.5 10mm screw
4 x M2.5 threaded inserts
1 x Mini-HDMI solderable breakout connector like https://www.aliexpress.com/item/1005006271343149.html
1 x HDMI to HDMI (preferably female to female) breakout board such as this https://www.aliexpress.com/item/1005006160781514.html

# Tools required
3d Printer
Soldering Iron
Screwdriver

# Software required
pyCEC from https://github.com/konikvranik/pyCEC
my updated pycec.service systemd service file from this repo
pystats.py and pystats.service from this repo

# Steps
Print the .stl files from this repo (in the STL folder).
Use the Raspberry pi imager to get your OS onto the SD card with your wifi details set, and boot up the pi
Update your OS!
install pyCEC as per the instructions in konikvranik's repo.
copy pycec.service from this repo into /etc/systemd/service - edit it if you want to fix the IP that pycec listens on, or change the port
copy pystats.service from this repo into /etc/systemd/service
systemctl enable pycec.service
systemctl enable pystats.service
reboot!
