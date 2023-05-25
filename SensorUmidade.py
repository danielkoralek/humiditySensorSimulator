from datetime import datetime, timedelta
from random import randint

# humidity sensor simulator with a random / range variance
class SensorUmidade():

    # Class initialization - takes external parameters such as 
    # height and initial umitity level
    def __init__(self, id, altitude, umidadeZero):
        self.id = id
        self.umidadeZero = umidadeZero
        self.umidadeFinal = umidadeZero
        self.altitudeRelativa = altitude

    def getId(self):
        return self.id

    def getUmidadeZero(self):
        return self.umidadeZero

    # Random watering simulator (in mm volume)
    def setRega(self, quantidadeMM):
        self.umidadeFinal += 14*quantidadeMM

    # Defines the output humidity based on a set of influencing parameters 
    def getUmidadeFinal(self, temperaturaAtual=25):
        fator = self.determinaFatorReducao(temperaturaAtual, 
                                           self.altitudeRelativa)
        refer = self.umidadeFinal

        self.umidadeFinal = refer - (int(refer * fator)) # + self.variacaoSensor
        if self.umidadeFinal < 10: self.umidadeFinal = 10
        elif self.umidadeFinal > 80: self.umidadeFinal = 80
        return self.umidadeFinal

    # Defines the soil humidity decreasing factor, based on some 
    # influencing paramters.
    def determinaFatorReducao(self, temperatura, altitude, tipoSolo="normal"):
        fator = 0

        # Fator Temperatura
        if temperatura <= 0: fator = 0.003
        elif temperatura > 50: fator = 0.49
        else:
            fator = temperatura/360

        # Fator altitude Relativa
        fator += altitude/480
        return fator

