import time
from bottle import Bottle

class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi

        self.app = Bottle()
        self._route()

    def _route(self):
        self._app.route('/', method="GET", callback=self.index)

    def kaynnista(self):
        self.app.run(host=self.ip, port=8080)

    def index(self):
        return "Hello World!"
