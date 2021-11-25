# Frank Yue Ying
# yying2
# TBD
# Needs:
# - constructor with location and message parameters (with default values)
# - getters and setters
# - soundAlarm, simulates the alarm going off by printing the message and location
# - __str__, returns the message and location as one string
class Alarm:
    def __init__(self,location = "Kitchen",message = "Warning! Warning!"):
        self._location = location
        self._message = message
    def __str__(self):
        return self._location+", Message: "+self._message
    def setLocation(self,location):
        self._location = location
    def setMessage(self,message):
        self._message = message
    def getLocation(self):
        return self._location
    def getMessage(self):
        return self._message
    def soundAlarm(self):
        print(self._location+", "+self._message)
