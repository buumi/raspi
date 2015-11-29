import datetime


class Lampomittari:

    def __init__(self, tiedostopolku, ohjattava, ohjaus=True, raja_arvo=20):
        """ tiedostopolku = polku anturin luomaan tiedostoon
        ohjattava = olio jolla metodit paalle ja pois_paalta
        ohjaus = onko ulkoisen laitteen ohjaus kaytossa
        raja_arvo = lampotila jonka ylapuolella ohjattava laite kaynnistyy """
        self.raja_arvo = raja_arvo
        self.ohjattava = ohjattava
        self.ohjaus = ohjaus
        self.tiedostopolku = tiedostopolku
        self.historia = {}
        self.pienin = (datetime.datetime.now(), 99999)
        self.suurin = (datetime.datetime.now(), -99999)

    def paivita(self):
        self._paivita_lampotila()

        if self.lampotila < self.pienin[1]:
            self.pienin = (datetime.datetime.now(), self.lampotila)

        if self.lampotila > self.suurin[1]:
            self.suurin = (datetime.datetime.now(), self.lampotila)

        if self.ohjaus is True:
            if self.lampotila > self.raja_arvo:
                self.ohjattava.paalle()
            else:
                self.ohjattava.pois_paalta()

        self.historia[datetime.datetime.now()] = self.lampotila

    def _paivita_lampotila(self):
        f = open(self.tiedostopolku, "r")
        rivit = f.readlines()

        if len(rivit) < 2:
            print "Lampotilan lukemisessa tapahtui virhe!"
            return

        lampotila_tuhannesosat = rivit[1][-6:]
        lampotila = float(lampotila_tuhannesosat) / 1000

        self.lampotila = lampotila

    def anna_ohjaus_tila(self):
        return self.ohjaus

    def anna_lampotila(self):
        return self.lampotila

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
