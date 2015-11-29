import RPi.GPIO as GPIO


class LED:
    """Luokka kuvaamaan ledia. Ottaa muodostimessa vastaan pinnin,
        johon LED on kytketty."""

    def __init__(self, pin):
        self.pin = pin
        self.state = False
        GPIO.setup(pin, GPIO.OUT, initial=False)

    def paalle(self):
        self.state = True
        GPIO.output(self.pin, self.state)

    def pois_paalta(self):
        self.state = False
        GPIO.output(self.pin, self.state)

    def muuta_tila(self):
        self.state = not self.state
        GPIO.output(self.pin, self.state)

    def onko_paalla(self):
        return self.state
