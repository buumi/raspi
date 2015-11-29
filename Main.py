from LED import LED
from Valoanturi import Valoanturi
from Lampomittari import Lampomittari
from WebUI import WebUI

import RPi.GPIO as GPIO
import time
import thread
import sys


def main():
    if (len(sys.argv) < 2):
        print "Kayttoohje: sudo python Main.py Raspberryn_IP_osoite Lampomittarin_polku"
        sys.exit(0)

    ip = sys.argv[1]
    lampomittari_path = sys.argv[2]

    GPIO.setmode(GPIO.BCM)

    lampomittarin_laite = LED(17)
    valoanturin_laite = LED(27)

    lampomittari = Lampomittari(lampomittari_path, lampomittarin_laite, 24)
    valoanturi = Valoanturi(18, 23, valoanturin_laite, 6)

    web_ui = WebUI(ip, lampomittari, valoanturi)
    thread.start_new_thread(web_ui.kaynnista, ())

    while True:
        valoanturi.paivita()
        print valoanturi.anna_valoisuus()
        #print lampomittari.paivita()
        time.sleep(1)


if __name__ == "__main__":
    main()
