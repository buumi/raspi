import time
from bottle import route, run, redirect, request, template, static_file
import os

class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi
        self._route()

    def _route(self):
        route('/', method="GET", callback=self.index)
        route("tyylit.css", callback=self.tyylit)
        route('/<toiminto>', method="GET", callback=self.index)
        route('/tunnistautuminen/<laite>/<toiminto>', method="GET", callback=self.tunnistautuminen)
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
        return template("index", content=sivu)

    def tyylit(self):
        return static_file("tyylit.css", root=".")

    def tunnistautuminen(self, laite, toiminto):
        return "<form action='/" + laite + "/" + toiminto + "' method='POST'>Kayttajatunnus: <input type='text' name='kayttajatunnus'><br>Salasana: <input type='password' name='salasana'><br><input type='submit' value='Jatka'>"


    '''
        Menemalla osoitteeseen RASPBERRYN_IP/<LAITE>/<TOIMINTO> voi ohjata Raspberryn toimintaa
        <LAITE> mahdolliset arvot ovat lampomittari ja valoanturi
        <TOIMINTO> mahdolliset arvot ovat True, False tai Float-arvo
        True arvolla <LAITE> alkaa ohjaamaan siihen liitettya laitetta
        False arvolla <LAITE> lopettaa siihen liitetyn laitteen ohjaamisen
        Float arvolla asetetaan ohjattavan laitteen kaynnistymisen raja-arvo

        HUOM: Metodi tarkistaa, etta POST-taulukko sisaltaa oikean kayttajatunnuksen ja salasanan.
        Tanne metodiin onkin tarkoitus tulla metodin kayttajatunnuksen pyynto kautta!
    '''
    def aseta_anturin_ohjaus(self, laite, toiminto):
        username = request.forms.get('kayttajatunnus')
        password = request.forms.get('salasana')
        if (self.onnistuuko_tunnistautuminen(username, password)):
            if laite == "lampomittari":
                laite = self.lampomittari
            elif laite == "valoanturi":
                laite = self.valoanturi
            else:
                # Jos tuntematon laite, ohjaa etusivulle
                redirect("http://" + self.ip + ":8080")

            if toiminto == "True":
                laite.aseta_ohjauksen_tila(True)
            elif toiminto == "False":
                laite.aseta_ohjauksen_tila(False)
            elif self.is_number(toiminto):
                laite.aseta_raja_arvo(float(toiminto))

            redirect("http://" + self.ip + ":8080")
        else:
            redirect("http://" + self.ip + ":8080/tunnistautuminen_epaonnistui")

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def tieto_sivu(self):
        return template("index", "Tasta tulee tietosivu")

    def onnistuuko_tunnistautuminen(self, kayttajatunnus, salasana):
        if (kayttajatunnus == "Admin" and salasana=="1234"):
            return True
        return False

