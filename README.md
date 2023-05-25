# humiditySensorSimulator
Simple Python code to simulate humidity sensors array scattered across a given area, under different soil conditions. In this version all the conditions are still hardcoded, but randon under a certain range. Humidity simulation (main file) also simulates human and natural watering events.

This version outputs the data into CSV format to the `/output` folder.

### Files Summary

* `SensorUmidade.py` - The sensor itself which offers a method for returning instant controlled values;
* `ArraySensoresUmidade.py` - The Array defition which will later construct the controller of a series (7) sensors scattered across a slope terrain;
* `RunSimulation.py` - This is the trigger piece which will raise the controller and make the simulation to run around the clock for 24 hours in a few seconds, producing data for one entire day, with temperature variation and random watering events. 

### How to run

Create the `/output` folder and run the main script from the command line:

```
PS C:\dev\SensorUmidade> python .\RunSimulation.py 2023-05-25
```

### Note

This was developed as part of my MBA project, and the main goal was to integrate the data in a multicloud solution. The original version of this simulator would load BigQuery DW with the daily data, combined with the OpenWeatherMap data that is being read by another script - to be linked here later. However, as I'm using this simulator to play with other pipeline resources, I've disabled the BigQuery part, and this version is outputting the data in CSV format.
