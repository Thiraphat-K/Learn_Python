from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
import time
import RPi.GPIO as GPIO

import numpy as np
from scipy.interpolate import griddata

from colour import Color

#class thermal_cam(object):
    #low range of the sensor (this will be blue on the screen)
MINTEMP = 26

    #high range of the sensor (this will be red on the screen)
MAXTEMP = 32

    #how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()

#fanPin
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# FAN_PIN = 7
# GPIO.setup(FAN_PIN, GPIO.OUT)

#initialize the sensor
sensor = Adafruit_AMG88xx()

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

#sensor is an 8x8 grid so lets do a square
height = 1000
width = 1000

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

lcd = pygame.display.set_mode((width, height))

lcd.fill((255,0,0))

pygame.display.update()
pygame.mouse.set_visible(False)

lcd.fill((0,0,0))
pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#let the sensor initialize
time.sleep(.1)

class thermal_cam(object):
    while(1):
    #read the pixels
        sumx=0
        sumHigh = 0
        sumLow= 0
        sumMid = 0
        pixels = sensor.readPixels()
        pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    
        #perdorm interpolation
        bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
        #print(enumerate(bicubic))
        #draw everything
        for ix, row in enumerate(bicubic):
            #print(ix,row)
            for jx, pixel in enumerate(row):
                #print(displayPixelHeight*ix,jx*displayPixelWidth)
                pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))
                #sumx=sumx+int(pixel)
                if int(pixel)<450:
                    sumLow+=1
                elif int(pixel)>=450 and int(pixel) <=850:
                    sumMid+=1
                elif int(pixel)>850:
                    sumHigh+=1
        pHigh = sumHigh/10.24
        pLow = sumLow/10.24
        pMid = sumMid/10.24
        print(pHigh,pMid,pLow)
        #avg = sumx/1000
        #print(sumx,avg,end='')
        #if(avg>=800):
            #print('high')
        #elif(avg<800):
            #print('low')
        #else:
            #print('no')
        pygame.display.update()
    
#     if pHigh>26:
#         GPIO.output(FAN_PIN, True)
#         print('fan on')
#     elif pHigh<26:
#         GPIO.output(FAN_PIN, False)
