import time


class WebUI:
    def __init__(self, lampomittari, valoanturi):
        self.lampomittari = lampomittari
        self.valoanturi = valoanturi

    def kaynnista(self):
        i = 0
        while True:
            print i
            i = i + 1
            time.sleep(1)
