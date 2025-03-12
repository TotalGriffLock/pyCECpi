# rpi-cec-unit
Building a raspberry pi into a robust HDMI-CEC IP interface

# What?
There are some commercially available HDMI-CEC to IP interfaces for things like Control4, Crestron, etc. They cost hundreds of pounds/dollars. In the same universe, Home Assistant and Raspberry Pis exist. Surely, the expensive commercial offerings are not the only choice?

# Shopping list - Prices are UK £ sterling at the time of writing
Raspberry Pi Zero W (or Zero 2 W) - without presoldered headers £14.40 from thepihut  
SD card for Raspberry Pi OS £6.90 for a Sandisk from Amazon  
Adafruit PiOLED £14.10 from thepihut  
2x6 2.5mm pin header - a 40 pin header from the pihut is £1, you can make 6 from that, so £0.17  
3 x M2.5 20mm screws - £3.79 from eBay - cheaper in bulk  
3 x M2.5 threaded inserts - £7.99 for 100 on amazon - £0.24 for 3  
1 x Mini-HDMI solderable breakout connector like https://www.aliexpress.com/item/1005006271343149.html - £4.16 for 5 delivered from aliexpress, so £0.84 each  
1 x HDMI to HDMI (preferably female to female, no pin header) breakout board such as this https://www.aliexpress.com/item/1005006160781514.html - £5.71 delivered from aliexpress  
Some short lengths of wire, 26AWG is probably fine  
  
TOTAL SO FAR £46.15  

# Tools required
3d Printer  
Soldering Iron  
Screwdriver  

# Software required
pyCEC from https://github.com/konikvranik/pyCEC  
my updated pycec.service systemd service file from this repo  
pystats.py and pystats.service from this repo  

# Steps
Assembly is a little fiddly but it makes for what I think is a very slick form factor  
Print the .stl files from this repo (in the STL folder)  
Solder the 3x2 pin header to pins 1-6 on the Pi  
Use your soldering iron to fit 3 threaded inserts into the case  
Fit the screen in to the case first, fit the HDMI breakout onto the frame, fit the frame into the case, then fit the pi on top of the frame  
Use the Raspberry pi imager to get your OS onto the SD card with your wifi details set, and boot up the pi  
Update your OS!  
install pyCEC as per the instructions in konikvranik's repo  
install the systemd python library  
copy pycec.service from this repo into /etc/systemd/service - edit it if you want to fix the IP that pycec listens on, or change the port  
copy pystats.service from this repo into /etc/systemd/service  
systemctl enable pycec.service  
systemctl enable pystats.service  
Probably do some iptables to make sure only appropriate hosts can communicate with your pyCEC instance  
reboot!  
