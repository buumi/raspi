import time
from bottle import route, run, redirect

class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi

        self._route()

    def _route(self):
        route('/', method="GET", callback=self.index)
        route('/tunnistautuminen/<kohdesivu>', method="GET", callback=self.kayttajatunnuksen_pyynto)
        route('/valoanturin_ohjaus_True', method="GET", callback=self.valoanturin_ohjaus_paalle)
        route('/valoanturin_ohjaus_False', method="GET", callback=self.valoanturin_ohjaus_pois_paalta)
        route('/tiedot', method="GET", callback=self.tieto_sivu)

    def kaynnista(self):
        run(host=self.ip, port=8080)

    def index(self):
        uusi_tila_valoanturi = not self.valoanturi.anna_ohjaus_tila()
        sivu = "Valoanturi ohjaa laitetta: " + str(self.valoanturi.anna_ohjaus_tila()) + " <a href='tunnistautuminen/valoanturin_ohjaus_" + str(uusi_tila_valoanturi) + "'>Muuta</a><br>"
        sivu += "Lampomittari ohjaa laitetta: " + str(self.lampomittari.anna_ohjaus_tila()) + "<br>"
        return sivu

    def kayttajatunnuksen_pyynto(self, kohdeosoite):
        return "<form action='" + kohdeosoite + "' method='POST'>Kayttajatunnus: <input type='text' name='kayttajatunnus'><br>Salasana: <input type='password'> name='salasana'><br><input type='submit' value='Jatka'>"

    def valoanturin_ohjaus_paalle(self):
        self.valoanturi.aseta_ohjauksen_tila(True)
        redirect("http://" + self.ip + ":8080")

    def valoanturin_ohjaus_pois_paalta(self):
        self.valoanturi.aseta_ohjauksen_tila(False)
        redirect("http://" + self.ip + ":8080")

    def tieto_sivu(self):
        return "Tasta tulee tietosivu"
