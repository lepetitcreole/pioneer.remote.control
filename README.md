XBMC addon for Pioneer A/V receivers
==========================

Automatically configure your Pioneer AV receiver at booting/shutdown XBMC!

Donate :
------------
If you enjoy the add-on, donations are always welcome :)

[![PayPal]( https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5VPCDAKJJVNV8)

Installation
------------
- Download the add-on as a ZIP file from https://github.com/lepetitcreole/pioneer.remote.control from the top of this page 
- Open XBMC
 - Go to `System -> Settings -> Add-ons -> Install from zip file` and select the ZIP file previously downloaded
 -  Restart XBMC and configure the add-on:
   - `System -> Settings -> Add-ons -> Enabled add-ons -> Services -> Pioneer A/V receiver remote control`
   - in NETWORK tab, click on `Start automatic discovery` (if your AV receiver is found, his IP address will be automatically set, otherwise set manually his IP address)
   - in SETTINGS tab, chose your options and enjoy!

Features
------------
- Power ON/OFF
- Set input (BD, DVD, SAT/CBL, DVR/BDR, HDMI 4, HDMI 5/MHL, HDMI 6, HDMI 7, TV)
- Set volume
- Reload A/V initial status at shutdown

Supported devices list
------------
VSX-923-K

And maybe other Pioneer AV receiver model which supports Telnet commands

Troubleshooting
------------
- Error "Network is unreachable" :
  - connection to network has failed
   - make sure network is available when addon starts
  - only one telnet session can be opened on the receiver
   - close others applications which use telnet on the AV receiver and retry
- Error "Not connected" :
  - addon can't connect to AV receiver
   - check if AV receiver IP address is right and retry

Support 
------------
Email : lepetitcreole@live.fr
