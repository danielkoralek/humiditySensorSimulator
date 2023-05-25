from datetime import datetime, timedelta
from random import randint
from SensorUmidade import SensorUmidade

# humidity Sensor Array class
# This class simulates the humidity sensors scattered across the terrain
# Current 01 pilot + 06 active sensors
class ArraySensoresUmidade():

    # Sensors definition with the scatter across a sloping terrain
    # (the second parameter is the elevation proportion)
    listaDeSensores = [
        ('SENS-01-BAIXO', 12), 
        ('SENS-02-BAIXO', 13), 
        ('SENS-03-MEIO', 22),
        ('SENS-04-MEIO', 23), 
        ('SENS-05-ALTO', 28), 
        ('SENS-06-ALTO', 31), 
        ('SENS-00-PILOTO', 21)
    ]
    tzSP = None
    sens = []

    def __init__(self):
        rdUmidadeZero = randint(45, 55)
        controller = []
        for s, a in self.listaDeSensores:
            # Start the sensors appending them to the controller
            controller.append(SensorUmidade(
                id=s, 
                altitude=a, 
                umidadeZero=rdUmidadeZero
            ))
        self.sens = controller

    def getNumSensores(self):
        return len(self.sens)

    # Method to trigger watering event (default to 2 mm of water)
    def setRega(self, mm=2):
        for obj in self.sens:
            obj.setRega(quantidadeMM=mm)

    # Umitity reading method scanning all the sensors connected to the controller
    def getUmidade(self, agora, temperaturaMedia=23):
        dadosArray = []
        for obj in self.sens:
            idSensor = obj.getId()
            umidadeAgora = obj.getUmidadeFinal(temperaturaMedia)
            dadosSensor = {}
            dadosSensor['_id'] = "%s-%s" % (idSensor,
                                            agora.strftime('%Y%m%d%H%M%S'))
            dadosSensor['sensor'] = idSensor
            dadosSensor['horario'] = agora.strftime('%Y-%m-%d %H:%M:%S')
            dadosSensor['umidade'] = umidadeAgora
            dadosSensor['temperaturaAmbiente'] = temperaturaMedia
            dadosArray.append(dadosSensor)

        return dadosArray
