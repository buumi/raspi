import time
from bottle import route, run, redirect, request

class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi

        self._route()

    def _route(self):
        route('/', method="GET", callback=self.index)
        route('/<toiminto>', method="GET", callback=self.index)
        route('/tunnistautuminen/<laite>/<toiminto>', method="GET", callback=self.kayttajatunnuksen_pyynto)
        route('/<laite>/<toiminto>', method="POST", callback=self.aseta_anturin_ohjaus)
        route('/tiedot', method="GET", callback=self.tieto_sivu)

    def kaynnista(self):
        run(host=self.ip, port=8080)

    def index(self, toiminto=""):
        sivu = ""

        if toiminto == "tunnistautuminen_epaonnistui":
            sivu += "Kayttajatunnus tai salasana oli vaarin!" + "<br><br>"

        uusi_tila_valoanturi = not self.valoanturi.anna_ohjaus_tila()
        uusi_tila_lampomittari = not self.lampomittari.anna_ohjaus_tila()

        sivu += "Valoanturi ohjaa laitetta: " + str(self.valoanturi.anna_ohjaus_tila()) + " <a href='tunnistautuminen/valoanturi/" + str(uusi_tila_valoanturi) + "'>Muuta</a><br>"
        sivu += "Lampomittari ohjaa laitetta: " + str(self.lampomittari.anna_ohjaus_tila()) + " <a href='tunnistautuminen/lampomittari/" + str(uusi_tila_lampomittari) + "'>Muuta</a><br>"
        return sivu

    def kayttajatunnuksen_pyynto(self, laite, toiminto):
        return "<form action='/" + laite + "/" + toiminto + "' method='POST'>Kayttajatunnus: <input type='text' name='kayttajatunnus'><br>Salasana: <input type='password' name='salasana'><br><input type='submit' value='Jatka'>"

    def aseta_anturin_ohjaus(self, laite, toiminto):
        if laite == "lampomittari":
            laite = self.lampomittari
        elif laite == "valoanturi":
            laite = self.valoanturi
        else:
            redirect("http://" + self.ip + ":8080")

        if toiminto == "True":
            toiminto = True
        elif toiminto == "False":
            toiminto = False
        else:
            redirect("http://" + self.ip + ":8080")

        username = request.forms.get('kayttajatunnus')
        password = request.forms.get('salasana')
        if (self.onnistuuko_tunnistautuminen(username, password)):
            laite.aseta_ohjauksen_tila(toiminto)
            redirect("http://" + self.ip + ":8080")
        redirect("http://" + self.ip + ":8080/tunnistautuminen_epaonnistui")

    def tieto_sivu(self):
        return "Tasta tulee tietosivu"

    def onnistuuko_tunnistautuminen(self, kayttajatunnus, salasana):
        if (kayttajatunnus == "Admin" and salasana=="1234"):
            return True
        return False

