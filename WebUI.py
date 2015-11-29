import time
from bottle import route, run

class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi

        self._route()

    def _route(self):
        route('/', method="GET", callback=self.index)
        route('/valoanturin_ohjaus/<tila>', method="GET", callback=self.valoanturin_ohjaus)
        route('/tiedot', method="GET", callback=self.tieto_sivu)

    def kaynnista(self):
        run(host=self.ip, port=8080)

    def index(self):
        return "Valoanturi ohjaa laitetta: " + self.valoanturi.anna_ohjaus_tila()
        return "Lampomittari ohjaa laitetta: " + self.lampomittari.anna_ohjaus_tila()

    def valoanturin_ohjaus(self, tila):
        self.valoanturi.aseta_ohjauksen_tila(tila)
        return '<script language="javascript">window.location.href = "' + self.ip + ':8080"</script>'

    def tieto_sivu(self):
        return "Tasta tulee tietosivu"
