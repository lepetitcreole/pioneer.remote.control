KODI/XBMC addon for Pioneer A/V receivers
==========================

Automatically configure your Pioneer AV receiver at KODI/XBMC booting/shutdown!

Donate :
------------
If you enjoy the add-on, donations are always welcome :)

[![PayPal]( https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5VPCDAKJJVNV8)

Installation
------------
- Download the add-on as a ZIP file from https://github.com/lepetitcreole/pioneer.remote.control from the top of this page 
- Open XBMC
 - Go to `System -> Settings -> Add-ons -> Install from zip file` and select the ZIP file previously downloaded
 - Restart XBMC and configure the add-on:
   - `System -> Settings -> Add-ons -> Enabled add-ons -> Services -> Pioneer A/V receiver remote control`
   - in NETWORK tab, click on `Start automatic discovery` (if your AV receiver is found, his IP address will be automatically set, otherwise set manually his IP address)
   - in SETTINGS tab, chose your options and enjoy!
- To set volume using a keyboard shortcut, find you KODI folder and edit your ".kodi/userdata/keymaps/keyboard.xml" file adding these lines : `<f8>RunScript(pioneer.remote.control,volumeUp)</f8>` to set volume UP pressing F8 button and `<f9>RunScript(pioneer.remote.control,volumeDown)</f9>` to set volume DOWN pressing F9 button

Features
------------
- Power ON/OFF
- Set input (BD, DVD, SAT/CBL, DVR/BDR, HDMI 4, HDMI 5/MHL, HDMI 6, HDMI 7, TV)
- Set volume at booting/shutdown
- Set volume using a keyboard/remote shortcut (Don't forget to edit your keyboard.xml file)
- Reload A/V initial status at shutdown
- Set listening mode (AUTO SURROUND, EXTENDED STEREO)

Supported devices list
------------
VSX-923-K

And maybe other Pioneer AV receiver model which supports Telnet commands

Troubleshooting
------------
- Error "Network is unreachable" :
  - connection to network has failed
     - make sure network is available when addon starts, try to delay addon starting
  - telnet session opening on the receiver has failed
     - close others applications which use telnet on the AV receiver and retry
- Error "Not connected" :
  - addon can't connect to AV receiver
     - check if AV receiver IP address is right and retry

Support 
------------
Email : lepetitcreole@live.fr
