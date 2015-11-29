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

    def kaynnista(self):
        run(host=self.ip, port=8080)

    def index(self):
        return "Hello World!"
