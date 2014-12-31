import xbmc
import xbmcgui
import xbmcaddon
import time
import sys
import colorsys
import os
import datetime
import math
import telnetlib
import socket

NOSE = os.environ.get('NOSE', None)
DEBUG = False
connected = False
initialPowerStatus = False
initialVolumeStatus = "-80.0"
initialInput = ""
initialStatusIsSet = False
params = None

inputLabel = [ "BD", "DVD", "SAT/CBL", "DVR/BDR", "HDMI 4", "HDMI 5/MHL", "HDMI 6", "HDMI 7", "TV" ]
inputMapping = [ 25, 4, 6, 15, 22, 23, 24, 34, 5 ]
userInputLabel = [ "", "", "", "", "", "", "", "", "" ]
listeningMode = [ "AUTO SURROUND", "EXT. STEREO" ]
listeningModeMapping = [ "0006", "0112" ]

if not NOSE:
  import xbmc
  import xbmcaddon

__icon__       = os.path.join(xbmcaddon.Addon().getAddonInfo('path'),"icon.png")

def notify(title, msg=""):
 if not NOSE:
   global __icon__
   xbmc.executebuiltin("XBMC.Notification(%s, %s, 3, %s)" % (title, msg, __icon__))
   
def logger(log):
   if DEBUG:
      xbmc.log("[DEBUG] Pioneer A/V : " + log)
        
def start_autodisover():
  port = 1900
  ip = "239.255.255.250"
  
  address = (ip, port)
  data = ('M-SEARCH * HTTP/1.1\r\n' +
'ST: urn:schemas-upnp-org:device:MediaRenderer:1\r\n' +
'MX: 3\r\n' +
'MAN: "ssdp:discover"\r\n' +
'HOST: 239.255.255.250:1900\r\n\r\n') 
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  receiver_ip = ""
  num_retransmits = 0
  while(num_retransmits < 10) and receiver_ip == "":
      num_retransmits += 1
      try:
        client_socket.sendto(data, address)
      except socket.error:
        notify("A/V Pioneer", "Error : Network is unreachable")
        logger("Network is unreachable")
        sys.exit(0)
      else:
		notify("A/V Pioneer", "Discovery in progress...")
		recv_data, addr = client_socket.recvfrom(2048)
		if "DMP" in recv_data and "description.xml" in recv_data:
			receiver_ip = recv_data.split("LOCATION: http://")[1].split(":")[0]
			xbmcaddon.Addon().setSetting("receiver_ip", receiver_ip)
		time.sleep(1)  
  if receiver_ip == "":
     xbmc.log("[DEBUG] Pioneer A/V : Receiver IP address not found")  
     notify("A/V Pioneer", "Not found")
  else:
     xbmc.log("[DEBUG] Pioneer A/V : Receiver IP address" + receiver_ip)  
     notify("A/V Pioneer", receiver_ip)
  return receiver_ip
  
class Pioneer:
   
  def readxml(self):
    global NOSE
    global DEBUG
    
    self.receiver_ip                      =        xbmcaddon.Addon().getSetting("receiver_ip")
    self.power_on_boot                    =        xbmcaddon.Addon().getSetting("power_on_boot") == "true"
    self.power_off_shutdown               =        xbmcaddon.Addon().getSetting("power_off_shutdown") == "true"
    self.input_boot                       =        xbmcaddon.Addon().getSetting("input_boot") == "true"
    self.input_boot_value                 =        xbmcaddon.Addon().getSetting("input_boot_value")
    self.input_shutdown                   =        xbmcaddon.Addon().getSetting("input_shutdown") == "true"
    self.input_shutdown_value             =        xbmcaddon.Addon().getSetting("input_shutdown_value")
    self.volume_boot                      =        xbmcaddon.Addon().getSetting("volume_boot") == "true"
    self.volume_boot_value                =        xbmcaddon.Addon().getSetting("volume_boot_value")
    self.volume_shutdown                  =        xbmcaddon.Addon().getSetting("volume_shutdown") == "true"
    self.volume_shutdown_value            =        xbmcaddon.Addon().getSetting("volume_shutdown_value")
    self.listening_mode_boot              =        xbmcaddon.Addon().getSetting("listening_mode_boot") == "true"
    self.listening_mode_value_boot        =        xbmcaddon.Addon().getSetting("listening_mode_value_boot")
    self.listening_mode_shutdown          =        xbmcaddon.Addon().getSetting("listening_mode_shutdown") == "true"
    self.listening_mode_value_shutdown    =        xbmcaddon.Addon().getSetting("listening_mode_value_shutdown")
    self.reload_initial_settings          =        xbmcaddon.Addon().getSetting("reload_initial_settings") == "true"
    self.starting_delay                   =        xbmcaddon.Addon().getSetting("starting_delay")
    self.disable_notifications            =        xbmcaddon.Addon().getSetting("disable_notifications") == "true"
    self.debug                            =        xbmcaddon.Addon().getSetting("debug") == "true"
    
    if self.disable_notifications:
      NOSE = True
    if self.debug:
      DEBUG = True  
      
      
  def powerOn(self):
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)
    tn.write("po\n\r")
    tn.close()
    notify("A/V Pioneer", "Power ON")
    logger("Power ON")
    xbmc.sleep(2000)

  def powerOff(self):
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)
    tn.write("pf\n\r")
    tn.close()
    notify("A/V Pioneer", "Power OFF")
    logger("Power OFF")
    xbmc.sleep(1000)

  def setVolume(self, vol):
    valueToSet = (float(vol)*2)+160+1
    str1 = '%03d%s' % (valueToSet, "vl\n\r")
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.write(str1)
    tn.close()
    str2 = '%s%d%s' % ("Vol. : ", float(vol), "dB")
    notify("A/V Pioneer", str2)
    logsStr = "Set volume to " + vol + "dB "
    logger(logsStr)
    xbmc.sleep(1000)

  def setInput(self, input):
    str1 = '%02d%s' % (inputMapping[int(input)], "fn\n\r")
    logger(str1)
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.write(str1)
    tn.close()
    str2 = "Input : " + input
    notify("A/V Pioneer", inputLabel[int(input)])
    logsStr = "Set input : " + inputLabel[int(input)]
    logger(logsStr)
    xbmc.sleep(1000)
   
  def getInputStatus(self):
    global initialInput
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.read_until("")
    tn.write("?f\n\r")
    response = tn.read_until("\n\r", 1)
    tn.close()
    rawInitialInput = str(response[2:])
    i=0
    while (int(rawInitialInput) != inputMapping[i]) and (i<=8):
        i+=1
    initialInput=str(i)
    logsStr = "Initial input status is " + inputLabel[i]
    logger(logsStr)
    xbmc.sleep(500)

  def setListeningMode(self, mode):
    str1 = '%s%s' % (listeningModeMapping[int(mode)], "sr\n\r")
    logger(str1)
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.write(str1)
    tn.close()
    notify("A/V Pioneer", listeningMode[int(mode)])
    str2 = "Listening mode : " + listeningMode[int(mode)]
    logger(str2)
    xbmc.sleep(1000)
    
  def getPowerStatus(self):
    global initialPowerStatus
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.read_until("")
    tn.write("?p\n\r")
    response = tn.read_until("\n\r", 1)
    tn.close()
    if "PWR0" in response :
      initialPowerStatus = True
    else:
      initialPowerStatus = False
    logsStr = "Initial power status is " + str(initialPowerStatus)
    logger(logsStr)
    xbmc.sleep(500)
    
  def getVolumeStatus(self):
    global initialVolumeStatus
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.read_until("")
    tn.write("?v\n\r")
    response = tn.read_until("\n\r", 1)
    tn.close()
    initialVolumeStatus = str(-80-0.5+int(response[3:])*0.5)
    logsStr = "Initial volume status is " + initialVolumeStatus
    logger(logsStr)
    xbmc.sleep(500)
    
  def getInputLabels(self):
    global inputCustomLabel
    tn = telnetlib.Telnet(self.receiver_ip, 23, 5)    
    tn.read_until("")
    for i in range(0, 8):
       request = '%s%02d%s' % ("?rgb", inputMapping[i], "\n\r")
       tn.write(request)
       response = tn.read_until("\n\r", 1)
       userInputLabel[i] = response[6:]
       logsStr = "Custom label is " + userInputLabel[i]
       logger(logsStr)
    tn.close()
    xbmc.sleep(500)
  
  def testConnection(self):
   global connected
   try:
      tn = telnetlib.Telnet(self.receiver_ip, 23, 5)
   except socket.timeout:
      notify("A/V Pioneer", "Not connected")
      connected = False
      logger("Test connection failed")
   except socket.error:
      notify("A/V Pioneer", "Network is unreachable")
      logger("Network is unreachable")
      connected = False
   else:
      tn.close()
      connected = True
      notify("A/V Pioneer", "Connected")
      logger("Test connection success")
      xbmc.sleep(1000)

if len(sys.argv) == 2:
    args = sys.argv[1]    
    if sys.argv[1] == "start_discover":
      start_autodisover()
      sys.exit(0)

pioneer = Pioneer()      
pioneer.readxml()

xbmc.sleep(int(pioneer.starting_delay)*1000)

if pioneer.receiver_ip == "":
	notify("A/V Pioneer", "Not configured yet")
	sys.exit(0)
pioneer.testConnection()
if connected:
   
   pioneer.getPowerStatus()
   if initialPowerStatus:
      pioneer.getVolumeStatus()
      pioneer.getInputStatus()
      initialStatusIsSet = True
   else:
      if pioneer.power_on_boot:
         pioneer.powerOn()
   if pioneer.volume_boot:
      pioneer.setVolume(pioneer.volume_boot_value)
   if pioneer.input_boot:
      pioneer.setInput(pioneer.input_boot_value)
   if pioneer.listening_mode_boot:
      pioneer.setListeningMode(pioneer.listening_mode_value_boot)
while not xbmc.abortRequested:
   xbmc.sleep(500)
pioneer.readxml()
pioneer.testConnection()
if connected:
   if initialPowerStatus and initialStatusIsSet and pioneer.reload_initial_settings:
         pioneer.setVolume(initialVolumeStatus)
         pioneer.setInput(initialInput)
   else:
      if pioneer.listening_mode_shutdown:
         pioneer.setListeningMode(pioneer.listening_mode_value_shutdown)
      if pioneer.volume_shutdown:
         pioneer.setVolume(pioneer.volume_shutdown_value)
      if pioneer.input_shutdown:
         pioneer.setInput(pioneer.input_shutdown_value)
      if pioneer.power_off_shutdown:
         pioneer.powerOff()
