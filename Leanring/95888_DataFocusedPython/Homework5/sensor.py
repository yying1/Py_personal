# class Sensor
# 
# Models a simple heat sensor that can be tripped
#    if the current temperature value rises above tripValue
#
# Private data:
#   __location, str: where the sensor is located
#   __value, float: current sensor temperature reading
#   __tripValue, float: threshold temperature
#
# Methods:
#   __init__(): sets __value to factory preset; sets __location and __tripValue
#   getLocation(): returns __location
#   setValue(value): sets new __value
#   getValue(): returns __value
#   getTripValue(): returns __tripValue
#   trip(): has the sensor been tripped, T/F
#   reset(): set __value back to factory preset
#   __str__(): returns str of this Sensor
class Sensor:

    # Set all data
    def __init__(self, location, tripValue):
        self.__location = location
        self.__value = 70.0
        self.__tripValue = tripValue

    # __location getter
    def getLocation(self):
        return self.__location

    # __value setter
    def setValue(self, value):
        self.__value = value

    # __value getter
    def getValue(self):
        return self.__value

    # __tripValue getter
    def getTripValue(self):
        return self.__tripValue

    # Did the sensor trip?
    def trip(self):
        if self.__value >= self.__tripValue:
            return True
        else:
            return False

    # Return __value to factory setting
    def reset(self):
        self.__value = 70.0

    # stringify Sensor
    def __str__(self):
        return self.__location + ', Value: ' + str(self.__value) + ', Trip Value: ' + str(self.__tripValue)

