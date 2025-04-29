# pyCECpi - pyCEC on a pi
Building a Raspberry Pi Zero into a robust HDMI-CEC IP interface to make a non-IoT TV into a controllable TV

# What?
There are some commercially available HDMI-CEC to IP interfaces for things like Control4, Crestron, etc. They cost hundreds of pounds/dollars. In the same universe, Home Assistant and Raspberry Pis exist. Surely, the expensive commercial offerings are not the only choice? Can I build a small box to go on the back of the TV to provide this kind of functionality? Also, my TV has limited HDMI ports - I don't want to lose a whole HDMI input just to add this feature, it needs to pass HDMI through

# Requirements
* Small form factor, must hide behind TV  
* HDMI-CEC controllable over IP, for integration into automation services (e.g. Home Assistant)  
* Small display screen to see status at a glance, for troubleshooting  
* HDMI passthrough, so the device does not monopolise an HDMI input - my TV only has 3 and I use them all!  
* Cheaper than existing commercially available options

# First prototype - green board
![image](https://github.com/user-attachments/assets/cdbfc126-876a-4b8a-8f6b-64c8724e9e3b)



# Shopping list - Prices are UK £ sterling at the time of writing
Raspberry Pi Zero W (or Zero 2 W) - without presoldered headers £14.40 from thepihut + £3.90 shipping  
SD card for Raspberry Pi OS £6.90 for a 32GB Sandisk from Amazon, realistically this probably fits on a 4GB if you use Rasbian Pi OS Lite  
Adafruit PiOLED £14.10 from thepihut  
2x6 2.5mm pin header - a 40 pin header from the pihut is £1, you can make 6 from that, so £0.17  
3 x M2.5 16mm screws - £3.79 from eBay - cheaper in bulk  
1 x M2.5 6mm screw  
4 x M2.5 threaded inserts - £7.99 for 100 on amazon - £0.24 for 3  
1 x Mini-HDMI solderable breakout connector like https://www.aliexpress.com/item/1005006271343149.html - £4.16 for 5 delivered from aliexpress, so £0.84 each  
1 x HDMI to HDMI (preferably female to female, no pin header) breakout board such as one of these:  
  PURPLE BOARD https://www.aliexpress.com/item/1005006160781514.html - £5.71 delivered from aliexpress  
  GREEN BOARD https://www.amazon.co.uk/HDMI-Male-Connector-Breakout-Board/dp/B0B3792QC9  
Some short lengths of wire, 26AWG is probably fine  
According to Cura, 23g of PLA - 1kg of PLA from the Creality store at the moment is £15 delivered so the PLA is roughly £0.35  
  
TOTAL SO FAR £50.50  

# A Note on HDMI Boards
There are 2 types of HDMI breakout + passthrough boards linked here, purple and green. The dimensions are different, and the green boards tend to be a bit skewed / off centre. The STL design files accommodate for this by having quite loose tolerances around the board and where the HDMI ports sit. The green board is much easier to get, so I anticipate you'd probably use this. I think the purple board is the neater solution.  


# Tools required
3d Printer  
Soldering Iron  
Screwdriver  

# Software required
pyCEC from https://github.com/konikvranik/pyCEC  
my updated pycec.service systemd service file from this repo  
pystats.py clearoled.py and pystats.service from this repo - pystats.py is based on the Adafruit script provided with the oled screen, available at https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage  

# Steps
Assembly is a little fiddly but it makes for what I think is a very slick form factor  
Print the .stl files from this repo (in the STL folder)  
If you would like to edit the design, the Tinkercad URL is https://www.tinkercad.com/things/1sP1Ou0873z-rpi-hdmi-cec-case-v3-public?sharecode=zlmHFi9SsDDJY9WS3CIGC6sMnaif7PkTeC0AQyqL-Io   
Solder the 3x2 pin header to pins 1-6 on the Pi  
Use your soldering iron to melt 3 threaded inserts into the case and 1 into the frame  
Fit the screen in to the case first, fit the HDMI breakout onto the frame, fit the frame into the case, then fit the pi on top of the frame  
Use the Raspberry pi imager to get your OS onto the SD card with your wifi details set, and boot up the pi  
Update your OS!  
install pyCEC as per the instructions in [konikvranik's repo ](https://github.com/konikvranik/pyCEC) 
Install the systemd and psutil python library  
```
sudo apt install python3-systemd python3-psutil
```
copy pycec.service from this repo into /etc/systemd/service
```
sudo curl -JLo /etc/systemd/service/pycec.service https://raw.githubusercontent.com/TotalGriffLock/pyCECpi/refs/heads/main/etc/systemd/system/pycec.service
```
copy pystats.service from this repo into /etc/systemd/service 
```
sudo curl -JLo /etc/systemd/service/pystats.service https://raw.githubusercontent.com/TotalGriffLock/pyCECpi/refs/heads/main/etc/systemd/system/pystats.service
```
copy pystats.py and clearoled.py into /usr/local/bin and make sure they are marked executable  
```
sudo curl -JLo /usr/local/bin/pystats.py https://raw.githubusercontent.com/TotalGriffLock/pyCECpi/refs/heads/main/usr/local/bin/pystats.py
sudo curl -JLo /usr/local/bin/clearoled.py https://raw.githubusercontent.com/TotalGriffLock/pyCECpi/refs/heads/main/usr/local/bin/clearoled.py
sudo chmod +x /usr/local/bin/*.py
```
Enable the new services
```
sudo systemctl daemon-reload
sudo systemctl enable pycec.service  
sudo systemctl enable pystats.service
```
Probably do some iptables to make sure only appropriate hosts can communicate with your pyCEC instance, something like:  
```
sudo apt install iptables-persistent
sudo iptables -I INPUT 1 -m tcp -p tcp --dport 9526 -m comment --comment "Deny access to pyCEC" -j DROP
sudo iptables -I INPUT 1 --source <homeassistantip> -m tcp -p tcp --dport 9526 -m comment --comment "Permit HomeAssistant to pyCEC" -j ACCEPT
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
```
It is not well documented but you can create /etc/pycec.conf with the format:  
```
[DEFAULT]
host=1.2.3.4 # This is the IP of the pi to listen on, in case your pi has multiple network interfaces
port=9526    # This is the port to listen on
```
reboot!  

# Final Thoughts
There are loads of ways this could be smaller, cheaper, and simpler. 
* You can split HDMI-CEC directly into GPIO on the RPI, but that requires a kernel overlay, which must be maintained to stay in line with the kernel version. This route could get rid of the mini-hdmi breakout
* You don't need the oled screen, I just really like it. The case could be considerably thinner without it, reducing footprint. The screen is also 30% of the total cost.
* If I didn't require HDMI pass through, it could just be a bare RPI, and be loads smaller and simpler.
* I could just buy a new TV that supports IoT (e.g. Samsung's SmartThings), or a TV with more HDMI inputs and save all the hassle.
* It is tempting to power the pyCECpi directly from the USB port on your TV. Be wary of how long that port supplies power, after the TV has gone into standby.
