from guizero import App, Text
import os
import glob
import time
import RPi.GPIO as GPIO

# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28-021317bd00aa')[0]
device_file = device_folder + '/w1_slave'

#fanPin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
FAN_PIN = 7
GPIO.setup(FAN_PIN, GPIO.OUT)

def read_rom():
    name_file=device_folder+'/name'
    f = open(name_file,'r')
    return f.readline()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    if lines[0].strip()[-3:] !='YES':
        print(lines[0].strip())
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_text.value = float(temp_c)
        #return temp_c#, temp_f
    if temp_c>=30:
        GPIO.output(FAN_PIN, True)
        print('Fan On')
    elif temp_c<30:
        GPIO.output(FAN_PIN, False)
        

#     print(' rom: '+ read_rom())
# while True:
#     print('C=%3.3f  F=%3.3f'% read_temp())
#     time.sleep(1)



app = App(title="DS18B20 TEMPERATURE SENSOR", width = "750", height = "650", layout="auto")
temp_message = Text(app, text="\n\nTEMPERATURE\n", size=50, font="TH Sarabun New", color="black")
temp_text = Text(app, size = 60, font="TH Sarabun New", color="black")
cel_message = Text(app, text="C", size=50, font="TH Sarabun New", color="black")
temp_text.repeat(1, read_temp)
app.display()
#time.sleep(1)