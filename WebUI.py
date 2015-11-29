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
        route('/hallintasivu', method="GET", callback=self.hallinta_sivu)
        route('/tiedot', method="GET", callback=self.tieto_sivu)

    def kaynnista(self):
        run(host=self.ip, port=8080)

    def index(self):
        return "Hello World!"

    def hallinta_sivu(self):
        return "Tasta tulee hallintasivu"

    def tieto_sivu(self):
        return "Tasta tulee tietosivu"
