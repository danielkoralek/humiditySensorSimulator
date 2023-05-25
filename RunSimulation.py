from datetime import datetime, timedelta
from random import randint
import sys 
import pandas as pd
from ArraySensoresUmidade import ArraySensoresUmidade
import uuid

#
# Clients In-line config
# Geo data to be combined with the second part of the project, which is
# reading weather forecast from the OpenWeatherMap source.
# 
clientes = [
    {
        "client_id"     : "92a71676-6b94-456d-88f5-c307ac8ef8f0",
        "client_name"   : "Abulafia",
        "geo"           : "-23.63999471182137,-46.97577444283879"
    },
    {
        "client_id"     : "2bbabb97-20eb-40b5-a096-5de13142002a",
        "client_name"   : "Daniel",
        "geo"           : "-23.6149357659427,-46.52902717213119"        
    }
]

#
# Defines different watering styles for the two clients
# 
perfilRega = {
    "92a71676-6b94-456d-88f5-c307ac8ef8f0" : 2,
    "2bbabb97-20eb-40b5-a096-5de13142002a" : 1
}


#
# Sensors reading simulation 
# Simulates messages for 24 hours every day, seeding of 00:01:15
#
def simulaLeitura(data, idCliente, geoPos, horariosRega):

    arr = ArraySensoresUmidade()
    records = []
    irrigacao = []
    
    # Momento da Leitura (variar 23 horas do dia, iniciando à 00:01:15)
    dataLeitura = datetime.strptime(data, '%Y-%m-%d').date()
    momentoLeitura = datetime(dataLeitura.year, 
                              dataLeitura.month,
                              dataLeitura.day,
                              0,1,15
                              )

    #
    # Execution controllers
    rangeHoras = 7 * 24
    contadorRodadas = 0 

    for clockMachine in range(rangeHoras):

        readId = str(uuid.uuid4())

        # Atribui uma rega de 2mm
        horaDia = int(momentoLeitura.strftime('%H'))
        if horaDia in horariosRega:
            quantidade = perfilRega[idCliente]
            arr.setRega(mm=quantidade)
            print('Rega')
            recordRega = {
                "client_id"     : idCliente,
                "geo"           : geoPos,
                "horario"       : momentoLeitura,
                "tipo_irrigacao": "rega",
                "volume_mm"     : quantidade
            }
            irrigacao.append(recordRega)

        # Simulates hardcoded temperature variation
        # TODO: connect this with the temperature captured from the OpenWeather API
        temperaturaAmbiente = 19
        if horaDia >= 0 and horaDia < 8: temperaturaAmbiente = 19
        elif horaDia >= 8 and horaDia < 11: temperaturaAmbiente = 22
        elif horaDia >= 11 and horaDia < 16: temperaturaAmbiente = 27
        elif horaDia >= 16 and horaDia < 20: temperaturaAmbiente = 25
        elif horaDia >= 20 and horaDia <= 24: temperaturaAmbiente = 20

        # Random NATURAL WATERING / Rain
        # using the watering method to pour some more water
        contadorRodadas += 1
        if contadorRodadas >= 10:
            contadorRodadas=0
            dice = randint(1,14)
            if dice in [1,4,7]:
                arr.setRega(mm=dice)
                print('Choveu %smm' % dice) # echoes the rain volume
                recordChuva = {
                    "client_id"     : idCliente,
                    "geo"           : geoPos,
                    "horario"       : momentoLeitura,
                    "tipo_irrigacao": "chuva",
                    "volume_mm"     : dice
                }
                irrigacao.append(recordChuva)

        #
        # Reads all the sensors in the Array!
        # 
        listaDados = arr.getUmidade(momentoLeitura, temperaturaAmbiente)
        for dado in listaDados:

            sensorCliente = str(idCliente +dado['sensor']).lower()
            sensorRecord = {
                "client_id"     : idCliente,
                "read_id"       : readId,
                "sensor_id"     : sensorCliente,
                "geo"           : geoPos,
                "horario"       : momentoLeitura,
                "umidade"       : dado['umidade']
            }

            records.append(sensorRecord)

        #
        # Accelerates time in 1 hour
        #
        momentoLeitura = momentoLeitura + timedelta(hours=1)

    #
    # Insere dados de todas as leituras de  1 cliente no BigQuery
    #
    dfhumidity = pd.DataFrame(
        records,
        columns=[
            "client_id",
            "read_id",
            "sensor_id",
            "geo",
            "horario",
            "umidade"
        ]
    )

    saveId = str(uuid.uuid4())

    humidityPath = 'output/humidity-%s.csv' % saveId
    dfhumidity.to_csv(humidityPath, header=True)

    #
    # Load watering data to BigQuery
    #
    dfWatering = pd.DataFrame(
       irrigacao,
       columns=[
            "client_id",
            "geo",
            "horario",
            "tipo_irrigacao",
            "volume_mm"
       ] 
    )

    wateringPath = 'output/watering-%s.csv' % saveId
    dfWatering.to_csv(wateringPath, header=True)

    print('Done farmer %s' % idCliente)

if __name__ == "__main__":
    seedData = sys.argv[1]
    for cli in clientes:
        print("Coletando sensores de %s" % cli['client_name'])

        # Assigns different watering times for each person
        if cli['client_name'] == 'Abulafia':
            horariosRega = [9,18]
        elif cli['client_name'] == 'Daniel' :
            horariosRega = [8,14]
        
        # Triggers simulation
        simulaLeitura(
            data=seedData, 
            idCliente=cli['client_id'], 
            geoPos=cli['geo'], 
            horariosRega=horariosRega
        )

    sys.exit(0)