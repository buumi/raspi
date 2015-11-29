import time, datetime, math
import RPi.GPIO as GPIO


class Valoanturi:

    def __init__(self, pin1, pin2, ohjattava, ohjaus=True, raja_arvo=4):
        """ pin1 = Ekan pinnin numero
        pin2 = Tokan pinnin numero 
        ohjattava = olio jolla metodit paalle ja pois_paalta
        ohjaus = onko ulkoisen laitteen ohjaus kaytossa
        raja_arvo = lampotila jonka ylapuolella ohjattava laite kaynnistyy """
        self.raja_arvo = raja_arvo
        self.ohjattava = ohjattava
        self.ohjaus = ohjaus
        self.historia = {}
        self.pienin = (datetime.datetime.now(), 99999)
        self.suurin = (datetime.datetime.now(), -99999)
        self.a_pin = pin1
        self.b_pin = pin2

    def paivita(self):
        valoisuus = self._analog_read()

        if valoisuus < self.pienin[1]:
            self.pienin = (datetime.datetime.now(), valoisuus)

        if valoisuus > self.suurin[1]:
            self.suurin = (datetime.datetime.now(), valoisuus)

        if self.ohjaus is True:
            if valoisuus > self.raja_arvo:
                self.ohjattava.paalle()
            else:
                self.ohjattava.pois_paalta()

        self.historia[datetime.datetime.now()] = valoisuus

        self.valoisuus = valoisuus
		
    def _discharge(self):
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(0.005)

    # Lue mahdollisimman usein self.b_pin
    def _charge_time(self):
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)

        count = 0

        start = datetime.datetime.now()
        GPIO.output(self.a_pin, True)

        while not GPIO.input(self.b_pin):
            count = count + 1

        stop = datetime.datetime.now()
        erotus = stop-start
        # kesto: sekuntia (float)
        kesto = erotus.seconds + erotus.microseconds/1000000.0 # sekuntia

        vastus = kesto/((220*10**(-9))*math.log(2, math.e))
        kilo_ohm = vastus/1000

        return kilo_ohm


    def _analog_read(self):
        self._discharge()
        return self._charge_time()

    def anna_ohjaus_tila(self):
        return self.ohjaus

    def anna_valoisuus(self):
        return self.valoisuus

    def anna_historia(self):
        return self.historia

    def anna_pienin(self):
        return self.pienin

    def anna_suurin(self):
        return self.suurin

    def aseta_raja_arvo(self, arvo):
        arvo = float(arvo)
        self.raja_arvo = arvo

    def aseta_ohjauksen_tila(self, paalla):
        self.ohjaus = paalla
