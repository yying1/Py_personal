# sensorApp.py
# Driver for the sensor - alarm program
# Frank Yue Ying
# yying2

from sensor import Sensor
from alarm import Alarm

# Display the sensor-alarm menu, get valid choice
def menu():
    print('1. Display sensors')
    print('2. Display alarms')
    print('3. Add sensor')
    print('4. Add alarm')
    print('5. Change sensor')
    print('0. Quit')
    choice = int(input('Enter your choice: '))
    if choice < 0 or choice > 5:
         choice = 0 # Quit if the user is stupid
    return choice

# Sound all alarms
def soundAlarms(alarms):
    for index,alarm in enumerate(alarms): 
        print("Alarm #"+str(index),end = ", ")
        alarm.soundAlarm()
    

# Initialize the sensors and alarms
# Get a menu choice
# Perform that choice
# Repeat until done
def main():
    # Empty sensor and alarm list
    sensorList = []
    alarmList = []

    print('*** Sensor App ***\n')

    choice = menu()
    while choice != 0:
        # Display the sensors
        if choice == 1:
            print()
            print('Sensor list:')
            count = 0
            for s in sensorList:
                print(str(count) + ': ' + s.__str__())
                count += 1
            print()

        # Display the alarms
        elif choice == 2:
            print()
            print('Alarm list:')
            count = 0
            for a in alarmList:
                print(str(count) + ': ' + a.__str__())
                count += 1
            print()

        # Add a new sensor
        elif choice == 3:
            location = input('Enter the sensor location: ')
            tripValue = float(input('Enter the sensor tripValue: '))
            s = Sensor(location, tripValue)
            sensorList.append(s)

        # Add a new alarm
        elif choice == 4:
            location = input('Enter the alarm location: ')
            message = input('Enter the alarm message: ')
            a = Alarm(location, message)
            alarmList.append(a)

        # Test by changing one sensor and see if the
        #   sensor trips; if so, sound all alarms
        elif choice == 5:
            sensorNumber = int(input('Enter the sensor number: '))
            if sensorNumber < 0 or sensorNumber > len(sensorList):
                print('Error, bad sensor number')
            else:
                print('Current value = ' + str(sensorList[sensorNumber].getValue()) )
                value = float(input('Enter new value: '))
                sensorList[sensorNumber].setValue(value)
                if sensorList[sensorNumber].getValue() > sensorList[sensorNumber].getTripValue():
                    print('Sensor #' + str(sensorNumber)+", "+sensorList[sensorNumber].getLocation()+", is tripped.")
                    soundAlarms(alarmList)
                    sensorList[sensorNumber].reset()

        choice = menu()

    print('\n*** Thanks for using the Sensor App ***')

if __name__ == '__main__':
    main()
