from LED import LED
from Valoanturi import Valoanturi
#from Lampomittari import Lampomittari
#from WebUI import WebUI

import RPi.GPIO as GPIO
import time
import thread


def main():
    GPIO.setmode(GPIO.BCM)

    #lampomittarin_laite = LED(17)
    valoanturin_laite = LED(27)

    #lampomittari = Lampomittari("/sys/bus/w1/devices/10-000802d8be47/w1_slave", lampomittarin_laite, 24)
	
    valoanturi = Valoanturi(18, 23, valoanturin_laite, 6)

    #web_ui = WebUI(lampomittari, None)
    #thread.start_new_thread(web_ui.kaynnista, ())

    while True:
        valoanturi.paivita()
        print valoanturi.anna_valoisuus()
        #print lampomittari.paivita()
        time.sleep(1)


if __name__ == "__main__":
    main()
