# Jrdiver's WS2812 ZigZag Board Program
# Original Library's: Tony DiCola (tony@tonydicola.com)
# Author: Jridver
# My setup is using the 1.0 revision of this board: https://easyeda.com/sharkbytecomputer/ws2812b-try-2
# Rev 1.1 that is the current version there corrects a few of the issues I ran into.

import time

from neopixel import *

import argparse
import signal
import sys
import random

def signal_handler(signal, frame):
    colorWipe(strip, Color(0,0,0))
    sys.exit(0)

def opt_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    if args.c:
        signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_PanelWidth = 8                     #Number of LEDS Left to Right
LED_PanelHeight= 8                     #Number of LEDS Top to Bottom
LED_NumPnlWide = 3                     #Number of Panels Wide the Array is
LED_NumPnlHigh = 1                     #Number of Panels High the Array is
LED_Direction  = 1                     #1 for Horizontal, 2 for Vertical.  Top Left is assumed to be LED1
LED_PIN        = 18                    # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000                # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10                     # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 075                   # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False                 # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0                     # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP      = ws.WS2811_STRIP_RBG   # Strip type and color ordering - My PTH LED's are RBG
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and color ordering - My SMT/SMD LED's are GRB


#These can be hardcore but if you use the coordinate system or almost any of the provided patterns, you should set up with the variables above so we know the size of the array.
LED_PanelCount = LED_NumPnlWide * LED_NumPnlHigh    #Number of Panels
LED_COUNT      = LED_PanelWidth * LED_PanelHeight * LED_PanelCount     # Number of LED pixels.  Default is to generate this from the values above.


#General Functions for convenience
#--------------------------------------------------------------------------------------------------------------------
#Set all pixel's to specific color but does not display it directly.  Useful for Background Colors
def SetDisplayColor(strip, color):
    for PixelNum in range(strip.numPixels()): 
        strip.setPixelColor(PixelNum, color)

#Turn all the pixel's off but don't directly display.  Useful for clearing previous frame/design before displaying new one.
def Blank(strip):
    SetDisplayColor(strip, Color(0, 0, 0))

#Turn off all the Pixes and display it.
def BlankDisplay(strip, wait_ms):
    Blank(strip)
    strip.show()
    time.sleep(wait_ms/1000.0)
	
#Set up a coordinate system to make programing easier
#Panel size should be known.  Assuming we use a zig-zag pattern with Known direction
#Coordinates are based off upper left being (1,1)
#--------------------------------------------------------------------------------------------------------------------
def SetCordinate(strip, X, Y, color):
    if (LED_Direction == 1):    #Horizontal Pixels.  Odd Y values should be correct order, even values should be inverted order.
        PixelNum = LED_PanelWidth * (Y - 1)
        while (X > LED_PanelWidth):
            PixelNum += (LED_PanelHeight * LED_PanelWidth)
            X -= LED_PanelWidth
        if (X<=0):
            PixelNum = -100
        if (Y % 2 == 0):
            PixelNum += LED_PanelWidth - X + 1
        else:
            PixelNum += X
        PixelNum -= 1 #Subtract 1 because the LEDS use 0 as Starting point and not 1
    
    else:   #Vertical Pixels.  Almost was able to just invert x and y values.
        PixelNum = LED_PanelHeight * (X - 1)
        while (Y > LED_PanelHeight):
            PixelNum += (LED_PanelHeight * LED_PanelWidth)
            Y -= LED_PanelHeight
        if (Y<=0):
            PixelNum = -100
        if (X % 2 == 0):
            PixelNum += LED_PanelHeight - Y + 1
        else:
            PixelNum += Y
        PixelNum -= 1 #Subtract 1 because the LEDS use 0 as Starting point and not 1
        
    strip.setPixelColor(PixelNum, color)

#set entire row (all x coordinates on a single Y axis) to a specific color
def SetRow (strip, Y, color):
    for i in range(1, LED_PanelWidth+1): 
        SetCordinate(strip, i, Y, color)
    
#set entire Column (all Y coordinates on a single X axis) to a specific color    
def SetColumn (strip, X, color):
    for i in range(1, LED_PanelHeight+1): 
        SetCordinate(strip, X, i, color)
        
#Coordinate Range
def SetRange (strip, sX, sY, eX, eY, color):
    for X in range (sX,eX+1):
        for Y in range (sY, eY+1):
            SetCordinate(strip, X, Y, color)
   
#Letters - Most are 6 Pixels wide and all are 8 Pixels High.  There are a few Exceptions.
#--------------------------------------------------------------------------------------------------------------------
def A(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 1+yOffset, color)
    SetRange (strip, 2+xOffset, 2+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 3+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    
def B(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 6+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 6+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    
def C(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    
def D(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)

def E(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)

def F(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    
def G(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 4+xOffset, 5+yOffset, 6+xOffset, 5+yOffset, color)
    
def H(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    
def I(strip, xOffset, yOffset, color):  #4 Pixel Wide Character
    SetRange (strip, 1+xOffset, 1+yOffset, 4+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 3+xOffset, 8+yOffset, color)

def J(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 1+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 1+xOffset, 5+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)

def K(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 2+yOffset, 5+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 6+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    
def L(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)

def M(strip, xOffset, yOffset, color):  #8 Pixel Wide Character
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 7+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 2+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 3+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 6+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
 
def N(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 2+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 4+xOffset, 6+yOffset, color)    

def O(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    
def P(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)

def Q(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetCordinate(strip, 6+xOffset, 8+yOffset, color)
    SetCordinate(strip, 5+xOffset, 7+yOffset, color)
    SetCordinate(strip, 4+xOffset, 6+yOffset, color)
    
def R(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 6+yOffset, 5+xOffset, 6+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    
def S(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 4+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 5+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    
def T(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    
def U(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    
def V(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 3+xOffset, 8+yOffset, 4+xOffset, 8+yOffset, color)
    
def W(strip, xOffset, yOffset, color):  #8 Pixel Wide Character
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 7+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 3+xOffset, 7+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 6+yOffset, color)
    SetRange (strip, 6+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    
def X(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 5+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 5+xOffset, 6+yOffset, color)
    
def Y(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 8+yOffset, color)
    
def Z(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 3+yOffset, color)

def num1(strip, xOffset, yOffset, color):  #4 Pixel Wide Character
    SetRange (strip, 1+xOffset, 2+yOffset, 1+xOffset, 3+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 3+xOffset, 8+yOffset, color)
    
def num2(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    
def num3(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)

def num4(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 6+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    
def num5(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    
def num6(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 6+xOffset, 2+yOffset, color)
    
def num7(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 8+yOffset, color)
    
def num8(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    
def num9(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 1+xOffset, 7+yOffset, color)
    

def num0(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 3+xOffset, 5+yOffset, color)
    SetCordinate(strip, 4+xOffset, 4+yOffset, color)


#LED Patterns
#--------------------------------------------------------------------------------------------------------------------
def AlfaFlag(strip, xOffset, yOffset):
    SetRange(strip, 1+xOffset, 1+yOffset, 5+xOffset, 8+yOffset, Color(255, 255, 255))
    SetRange(strip, 6+xOffset, 1+yOffset, 10+xOffset, 1+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 2+yOffset, 9+xOffset, 2+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 3+yOffset, 8+xOffset, 3+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 4+yOffset, 7+xOffset, 5+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 6+yOffset, 8+xOffset, 6+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 7+yOffset, 9+xOffset, 7+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 8+yOffset, 10+xOffset, 8+yOffset, Color(0, 0, 255))


def DiveFlag(strip, xOffset, yOffset):
    SetRange(strip, 1+xOffset, 1+yOffset, 10+xOffset, 8+yOffset, Color(255, 0, 0))
    SetCordinate(strip, 1+xOffset, 1+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 2+xOffset, 1+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 2+xOffset, 2+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 3+xOffset, 2+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 3+xOffset, 3+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 4+xOffset, 3+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 4+xOffset, 4+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 5+xOffset, 4+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 6+xOffset, 4+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 5+xOffset, 5+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 6+xOffset, 5+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 7+xOffset, 5+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 7+xOffset, 6+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 8+xOffset, 6+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 8+xOffset, 7+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 9+xOffset, 7+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 9+xOffset, 8+yOffset, Color(255, 255, 255))
    SetCordinate(strip, 10+xOffset, 8+yOffset, Color(255, 255, 255))
    
def DFScrollLeft (strip, y, wait_ms):
    for lcv in range (LED_PanelWidth*LED_PanelCount - 1, (LED_PanelWidth * -1)-25, -1):
        Blank(strip)
        DiveFlag(strip, lcv, y)
        AlfaFlag(strip, lcv+11, y)
        DiveFlag(strip, lcv+22, y)
        strip.show()
        time.sleep(wait_ms/1000.0)

def MCCreeper (strip, xOffset, yOffset):
    SetRange(strip, 1+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, Color(0, 220, 25))
    SetRange(strip, 2+xOffset, 3+yOffset, 3+xOffset, 4+yOffset, Color(0, 0, 0))
    SetRange(strip, 6+xOffset, 3+yOffset, 7+xOffset, 4+yOffset, Color(0, 0, 0))
    SetRange(strip, 4+xOffset, 5+yOffset, 5+xOffset, 7+yOffset, Color(0, 0, 0))
    SetRange(strip, 3+xOffset, 6+yOffset, 3+xOffset, 8+yOffset, Color(0, 0, 0))
    SetRange(strip, 6+xOffset, 6+yOffset, 6+xOffset, 8+yOffset, Color(0, 0, 0))



def Open(strip, color, wait_ms):
    Blank(strip)
    O(strip, 0, 0, color)
    P(strip, 7, 0, color)
    E(strip, 14, 0, color)
    N(strip, 21, 0, color)
    strip.show()
    time.sleep(wait_ms/1000.0)
    
def OpenScroll(strip, color, wait_ms):
    for lcv in range (LED_PanelWidth*LED_PanelCount - 1, (LED_PanelWidth * -1)-21, -1):
        Blank(strip)
        O(strip, lcv, 0, color)
        P(strip, lcv+7, 0, color)
        E(strip, lcv+14, 0, color)
        N(strip, lcv+21, 0, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def BlargScroll(strip, color, wait_ms):
    for lcv in range (LED_PanelWidth*LED_PanelCount - 1, (LED_PanelWidth * -1)-28, -1):
        Blank(strip)
        B(strip, lcv, 0, color)
        L(strip, lcv+7, 0, color)
        A(strip, lcv+14, 0, color)
        R(strip, lcv+21, 0, color)
        G(strip, lcv+28, 0, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def Rainbow(strip):
    wait_ms=2
    for i in range(0,255):
        SetDisplayColor(strip, Color(i,255-i,0))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(0,255):
        SetDisplayColor(strip, Color(255-i,0,i))
        strip.show()
        time.sleep(wait_ms/1000.0)
    for i in range(0,255):
        SetDisplayColor(strip, Color(0,i,255-i))
        strip.show()
        time.sleep(wait_ms/1000.0)

def Random(strip):
    wait_ms=1000
    for loop in range(0,10):
        for position in range(0,LED_COUNT):
            if (random.randint(1,4)>2):
                R = random.randint(0,255)
                G = random.randint(0,255)
                B = random.randint(0,255)
            else:
                R=0
                G=0
                B=0
            strip.setPixelColor(position, Color(R, G, B))
        strip.show()
        time.sleep(wait_ms/1000.0)

def Demo(strip):
    Rainbow(strip)
    DFScrollLeft(strip, 0, 250)
    Random(strip)
    BlargScroll(strip, Color(66, 134, 244), 250)
    
def TestDisplay(strip):
    num0(strip, 0, 0, Color(66, 134, 244))
    strip.show()
    time.sleep(1) #just to slow the infinite loop down and prevent some unneeded CPU load
        
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    opt_parse()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Initialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    try:
        while True:
            #TestDisplay(strip)
            Demo(strip)
            #OpenScroll(strip, Color(66, 134, 244), 250)


        
    #Turn off the LED's on Program Exit
    except KeyboardInterrupt:
        BlankDisplay(strip, 1)
        print
        print ("BYE BYE")
