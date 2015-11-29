import time
from bottle import route, run, template


class WebUI:
    def __init__(self, ip, lampomittari, valoanturi):
        self.ip = ip
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi


    def kaynnista(self):
        run(host=self.ip, port=8080)

    @route('/')
    def index(self):
        return "Hello World!"
