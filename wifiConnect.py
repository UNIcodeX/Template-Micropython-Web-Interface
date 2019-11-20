import network
from time import sleep

import config

wlan = network.WLAN(network.STA_IF)


def clearLine():
  print(" "*40, end="\r")


def connect():
  ssid     = ""
  password = ""
  known    = config.known_networks
  
  if not wlan.isconnected():
    wlan.active(True)
    
    print("\nScanning for and attempting to connect to known networks.")

    avail = wlan.scan()
    avail = [a[0].decode() for a in avail]
    print("Found networks...")
    for a in avail:
      print(a)
    print("\n")

    for k in known.keys():
      if k in avail:
        ssid = k
        password = known[k]['p']
        break

    if not ssid:
      print("No known networks found.")
      return False

    conMsg = "Connecting to {}".format(ssid)

    print(conMsg)
    wlan.connect(ssid, password)
    extra = ""
    while not wlan.isconnected():
      if extra == "":
        extra = "."
      elif extra == ".":
        extra = ".."
      elif extra == "..":
        extra = "..."
      else:
        extra = "."
      clearLine()
      print(conMsg+extra, end="\r")
      sleep(.5)

    clearLine()

    print("Connection successful")
    print("IP: {}".format(wlan.ifconfig()[0]))
  
  else:
    print("Already connected.")
  
  # cleanup
  del ssid
  del password
  del conMsg
  del extra
  del known
  del avail  
  
  return True

