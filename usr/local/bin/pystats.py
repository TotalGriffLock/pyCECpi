#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT
# Additions for the pyCECpi project, see https://github.com/TotalGriffLock/pyCECpi

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import select
import textwrap
import re
import psutil
from systemd import journal
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)


# systemd bits
j = journal.Reader()
j.seek_tail()
j.add_match(_SYSTEMD_UNIT='pycec.service')
j.get_previous()

# paging, start on page 1
showpage = 1

while True:
    journalstr1 = ""
    journalstr2 = ""
    wraptext = list()
    # See if we have a new journal message to display
    event = j.wait(1)
    if event == journal.APPEND:
      # We do, we should display this instead
      for entry in j:
        if not "poll" in entry['MESSAGE']:
          draw.rectangle((0, 0, width, height), outline=0, fill=0)
          # First split off the timestamp, this will be the 1st line to display
          split1 = entry['MESSAGE'].split(',',1)
          # Then split the message up by dashes - pyCEC outputs logs using a dash delimiter
          if len(split1) > 1:
            split2 = split1[1].split('- ',2)
            # Now wordwrap it so that it fits nicely on the screen
            wraptext = textwrap.fill(split2[2],20).split('\n', 3)
          else:
            wraptext.append("")
          # Draw the text on the oled screen
          # If it's longer than 3 lines it will get truncated
          # Check the lines exist before trying to display them
          draw.text((x, top + 0), split1[0], font=font, fill=255)
          draw.text((x, top + 8), wraptext[0], font=font, fill=255)
          if len(wraptext) > 1:
            draw.text((x, top + 16), wraptext[1], font=font, fill=255)
          if len(wraptext) > 2:
            draw.text((x, top + 24), wraptext[2], font=font, fill=255)
          disp.image(image)
          disp.show()
          time.sleep(0.3)
    elif showpage == 2:
      cmd = "iwgetid -r"
      ssid = subprocess.check_output(cmd, shell=True).decode("utf-8")
      cmd = "hostname -I | cut -d' ' -f1"
      IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
      for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "/usr/local/bin/pycec" in cmdline:
          cmd = "journalctl --boot -u pycec | grep Serv | tail -n1"
          journalstr = subprocess.check_output(cmd, shell=True).decode("utf-8")
          split1 = journalstr.split('- ',2)
          split2 = re.search("'(.+)', (\d+)", split1[2])
          journalstr1 = "pyCEC is listening on"
          journalstr2 = split2.group(1) + ":" + split2.group(2)
      if len(journalstr1) == 0:
        journalstr1 = ""
        journalstr2 = "pyCEC is NOT running!"
      # Blank the screen and write four lines of text.
      draw.rectangle((0, 0, width, height), outline=0, fill=0)
      draw.text((x, top + 0), "SSID: " + ssid, font=font, fill=255)
      draw.text((x, top + 8), "IP: " + IP, font=font, fill=255)
      draw.text((x, top + 16), journalstr1, font=font, fill=255)
      draw.text((x, top + 24), journalstr2, font=font, fill=255)

      # Display image.
      disp.image(image)
      disp.show()
      time.sleep(5)
      showpage = 1

    else:
      # Shell scripts for system monitoring from here:
      # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
      cmd = 'cut -f 1 -d " " /proc/loadavg'
      CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
      cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB %.2f%%\", $3,$2,$3*100/$2 }'"
      MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
      cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
      Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
      for process in psutil.process_iter():
        cmdline = process.cmdline()
        if "/usr/local/bin/pycec" in cmdline:
          journalstr2 = "pyCEC PID: " + str(process.pid)
      if len(journalstr2) == 0:
        journalstr2 = "pyCEC is NOT running!"

      # Blank the screen and write four lines of text.
      draw.rectangle((0, 0, width, height), outline=0, fill=0)
      draw.text((x, top + 0), "CPU load: " + CPU, font=font, fill=255)
      draw.text((x, top + 8), MemUsage, font=font, fill=255)
      draw.text((x, top + 16), Disk, font=font, fill=255)
      draw.text((x, top + 24), journalstr2, font=font, fill=255)

      # Display image.
      disp.image(image)
      disp.show()
      time.sleep(5)
      showpage = 2
