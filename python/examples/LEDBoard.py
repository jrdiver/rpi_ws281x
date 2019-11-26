# Jrdiver's WS2812 ZigZag Board Program
# Original Library's: Tony DiCola (tony@tonydicola.com)
# Author: Jridver
# My setup is using a mix of 1.0 and 2.0 revisions of this board: https://easyeda.com/sharkbytecomputer/ws2812b-try-2

import argparse
import datetime
import random
import signal
import sys
import time
from neopixel import *

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
LED_PanelWidth = 8        #Number of LEDS Left to Right
LED_PanelHeight= 8        #Number of LEDS Top to Bottom
LED_NumPnlWide = 4        #Number of Panels Wide the Array is
LED_NumPnlHigh = 2        #Number of Panels High the Array is
LED_PIN        = 18       #GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000   #LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       #DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 75       #Set to 0 for darkest and 255 for brightest
LED_INVERT     = False    #True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0        # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2812_STRIP   # Strip type and color ordering - My SMT/SMD LED's are GRB


#These can be hardcore but if you use the coordinate system or almost any of the provided patterns, you should set up with the variables above so we know the size of the array.
LED_PanelCount = LED_NumPnlWide * LED_NumPnlHigh    #Number of Panels
LED_COUNT      = LED_PanelWidth * LED_PanelHeight * LED_PanelCount  # Number of LED pixels.  Default is to generate this from the values above.
LED_TotalPanelWidth = LED_PanelWidth * LED_NumPnlWide
LED_PerPanelRow = LED_PanelWidth * LED_PanelHeight * LED_NumPnlWide


#General Functions for convenience
#--------------------------------------------------------------------------------------------------------------------
#Set all pixel's to specific color but does not display it directly.  Useful for Background Colors
def SetDisplayColor(strip, color):
    for PixelNum in range(strip.numPixels()): 
        strip.setPixelColor(PixelNum, color)

#Turn all the pixel's off but don't directly display.  Useful for clearing previous frame/design before displaying new one.
def Blank(strip):
    SetDisplayColor(strip, Color(0, 0, 0))

#Turn off all the Pixels and display it.
def BlankDisplay(strip, wait_ms):
    Blank(strip)
    strip.show()
    time.sleep(wait_ms/1000.0)
	
#Set up a coordinate system to make programing easier
#Panel size should be known.  Assuming we use a zig-zag pattern with Known direction
#Coordinates are based off upper left being (1,1)
#--------------------------------------------------------------------------------------------------------------------
def SetCordinate(strip, X, Y, color):
        PixelNum=0
        while(Y>LED_PanelHeight):
            PixelNum += LED_PerPanelRow
            Y-=LED_PanelHeight
        PixelNum += LED_PanelWidth * (Y - 1)
        if (X <= LED_TotalPanelWidth and X>0):
            #print (X)
            while (X > LED_PanelWidth):
                PixelNum += (LED_PanelHeight * LED_PanelWidth)
                X -= LED_PanelWidth
            if (Y % 2 == 0):
                PixelNum += LED_PanelWidth - X + 1
            else:
                PixelNum += X
            #print (str(X) +' '+ str(Y))
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

#region: Letters - Most charaters are 6 Pixels wide and all are 8 Pixels High.  There are a few Exceptions.
#First few functions build on the previous one.  SetText just sets the text to the led strip, DisplayText actually shows it,
#ScrollingText Makes it animated to show longer strings then would fit on the display
def ScrollingText(strip, Text, yOffset, color, wait_ms=500):
    xOffset=LED_TotalPanelWidth-1
    while(DisplayText(strip, Text, xOffset, yOffset, color, wait_ms)>0):
        xOffset-=1
def DisplayText(strip, Text, xOffset, yOffset, color, wait_ms=500):
    Blank(strip)
    Length = SetText(strip, Text, xOffset, yOffset, color)
    strip.show()
    time.sleep(wait_ms/1000.0)
    return Length
def SetText(strip, Text, xOffset, yOffset, color):
    Blank(strip)
    Position = 0
    Text = Text.upper()
    while(len(Text)>0):
        Letter = Text[0]
        if (Letter == "A"):
            Position += A(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "B"):
            Position += B(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "C"):
            Position += C(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "D"):
            Position += D(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "E"):
            Position += E(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "F"):
            Position += F(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "G"):
            Position += G(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "H"):
            Position += H(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "I"):
            Position += I(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "J"):
            Position += J(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "K"):
            Position += K(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "L"):
            Position += L(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "M"):
            Position += M(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "N"):
            Position += N(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "O"):
            Position += O(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "P"):
            Position += P(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "Q"):
            Position += Q(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "R"):
            Position += R(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "S"):
            Position += S(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "T"):
            Position += T(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "U"):
            Position += U(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "V"):
            Position += V(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "W"):
            Position += W(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "X"):
            Position += X(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "Y"):
            Position += Y(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "Z"):
            Position += Z(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "1"):
            Position += num1(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "2"):
            Position += num2(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "3"):
            Position += num3(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "4"):
            Position += num4(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "5"):
            Position += num5(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "6"):
            Position += num6(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "7"):
            Position += num7(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "8"):
            Position += num8(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "9"):
            Position += num9(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "0"):
            Position += num0(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == ":"):
            Position += colon(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "."):
            Position += period(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "!"):
            Position += exclamation(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == ","):
            Position += comma(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == ";"):
            Position += semicolin(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "\\"):
            Position += backslash(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "/"):
            Position += forwardslash(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "*"):
            Position += star(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "-"):
            Position += dash(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "+"):
            Position += plus(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "?"):
            Position += questionmark(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == "$"):
            Position += dollarsign(strip, xOffset + Position, yOffset, color) + 1
        elif (Letter == " "):
            Position += 3
        Text = Text[1: :]
    return Position+xOffset
def A(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 1+yOffset, color)
    SetRange (strip, 2+xOffset, 2+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 3+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    return 6
def B(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 6+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 6+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    return 6  
def C(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    return 6   
def D(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    return 6
def E(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def F(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    return 6
def G(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 4+xOffset, 5+yOffset, 6+xOffset, 5+yOffset, color)
    return 6
def H(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    return 6
def I(strip, xOffset, yOffset, color): 
    SetRange (strip, 1+xOffset, 1+yOffset, 4+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 3+xOffset, 8+yOffset, color)
    return 4
def J(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 1+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 1+xOffset, 5+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    return 6
def K(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 2+yOffset, 5+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 6+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def L(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def M(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 7+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 2+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 3+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 6+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
    return 8
def N(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 2+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 4+xOffset, 6+yOffset, color)    
    return 6
def O(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    return 6
def P(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    return 6
def Q(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetCordinate(strip, 6+xOffset, 8+yOffset, color)
    SetCordinate(strip, 5+xOffset, 7+yOffset, color)
    SetCordinate(strip, 4+xOffset, 6+yOffset, color)
    return 6
def R(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 6+yOffset, 5+xOffset, 6+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def S(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 4+yOffset, 3+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 5+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 6+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    return 6
def T(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    return 6
def U(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    return 6
def V(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 5+xOffset, 7+yOffset, color)
    SetRange (strip, 3+xOffset, 8+yOffset, 4+xOffset, 8+yOffset, color)
    return 6
def W(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 7+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 3+xOffset, 7+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 6+yOffset, color)
    SetRange (strip, 6+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    return 8
def X(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 2+xOffset, 8+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 5+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 5+xOffset, 6+yOffset, color)
    return 6
def Y(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 8+yOffset, color)
    return 6
def Z(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 3+yOffset, color)
    return 6
def num1(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 1+xOffset, 3+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 4+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 3+xOffset, 8+yOffset, color)
    return 4
def num2(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def num3(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    return 6
def num4(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 4+yOffset, 6+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 1+yOffset, 6+xOffset, 8+yOffset, color)
    return 6
def num5(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    return 6
def num6(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 6+xOffset, 2+yOffset, color)
    return 6
def num7(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 6+xOffset, 2+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 3+yOffset, color)
    SetRange (strip, 4+xOffset, 4+yOffset, 5+xOffset, 4+yOffset, color)
    SetRange (strip, 3+xOffset, 5+yOffset, 4+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 6+yOffset, 3+xOffset, 8+yOffset, color)
    return 6
def num8(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 3+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    return 6
def num9(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 2+xOffset, 4+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 1+xOffset, 7+yOffset, color)
    return 6
def num0(strip, xOffset, yOffset, color):
    SetRange (strip, 2+xOffset, 1+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 2+xOffset, 7+yOffset, color)
    SetRange (strip, 5+xOffset, 2+yOffset, 6+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 5+xOffset, 8+yOffset, color)
    SetCordinate(strip, 3+xOffset, 5+yOffset, color)
    SetCordinate(strip, 4+xOffset, 4+yOffset, color)
    return 6
def colon(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 3+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    return 2
def exclamation(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 5+yOffset, color)
    SetRange (strip, 1+xOffset, 7+yOffset, 2+xOffset, 8+yOffset, color)
    return 2
def period(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 7+yOffset, 2+xOffset, 8+yOffset, color)
    return 2
def comma(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetCordinate(strip, 1+xOffset, 8+yOffset, color)
    return 2
def semicolin(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 3+yOffset, 2+xOffset, 4+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 7+yOffset, color)
    SetCordinate(strip, 1+xOffset, 8+yOffset, color)
    return 2
def backslash(strip, xOffset, yOffset, color):
    SetRange (strip, 1+xOffset, 1+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 3+xOffset, 6+yOffset, 4+xOffset, 8+yOffset, color)
    return 4
def forwardslash(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 3+yOffset, 3+xOffset, 6+yOffset, color)
    SetRange (strip, 1+xOffset, 6+yOffset, 2+xOffset, 8+yOffset, color)
    return 4
def star(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 3+yOffset, 3+xOffset, 7+yOffset, color)
    SetRange (strip, 2+xOffset, 5+yOffset, 4+xOffset, 5+yOffset, color)
    SetCordinate(strip, 1+xOffset, 4+yOffset, color)
    SetCordinate(strip, 1+xOffset, 6+yOffset, color)
    SetCordinate(strip, 5+xOffset, 4+yOffset, color)
    SetCordinate(strip, 5+xOffset, 6+yOffset, color)
    return 5
def dash(strip, xOffset, yOffset, color):  
    SetRange (strip, 1+xOffset, 4+yOffset, 6+xOffset, 5+yOffset, color)
    return 6
def plus(strip, xOffset, yOffset, color): 
    SetRange (strip, 1+xOffset, 4+yOffset, 6+xOffset, 5+yOffset, color)
    SetRange (strip, 3+xOffset, 2+yOffset, 4+xOffset, 7+yOffset, color)
    return 6
def questionmark(strip, xOffset, yOffset, color): 
    SetRange (strip, 3+xOffset, 1+yOffset, 4+xOffset, 1+yOffset, color)
    SetRange (strip, 1+xOffset, 2+yOffset, 5+xOffset, 2+yOffset, color)
    SetRange (strip, 1+xOffset, 3+yOffset, 2+xOffset, 3+yOffset, color)
    SetRange (strip, 5+xOffset, 3+yOffset, 6+xOffset, 4+yOffset, color)
    SetRange (strip, 4+xOffset, 5+yOffset, 5+xOffset, 5+yOffset, color)
    SetRange (strip, 3+xOffset, 6+yOffset, 4+xOffset, 6+yOffset, color)
    SetRange (strip, 3+xOffset, 8+yOffset, 4+xOffset, 8+yOffset, color)
    return 6
def dollarsign(strip, xOffset, yOffset, color):
    SetRange (strip, 3+xOffset, 1+yOffset, 3+xOffset, 8+yOffset, color)
    SetRange (strip, 2+xOffset, 2+yOffset, 4+xOffset, 2+yOffset, color)
    SetCordinate(strip, 1+xOffset, 3+yOffset, color)
    SetRange (strip, 2+xOffset, 4+yOffset, 4+xOffset, 4+yOffset, color)
    SetRange (strip, 5+xOffset, 5+yOffset, 5+xOffset, 6+yOffset, color)
    SetCordinate(strip, 1+xOffset, 6+yOffset, color)
    SetRange (strip, 2+xOffset, 7+yOffset, 4+xOffset, 7+yOffset, color)
    return 5
#endregion
#region LED Patterns
def AlfaFlag(strip, xOffset, yOffset):
    SetRange(strip, 1+xOffset, 1+yOffset, 5+xOffset, 8+yOffset, Color(255, 255, 255))
    SetRange(strip, 6+xOffset, 1+yOffset, 10+xOffset, 1+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 2+yOffset, 9+xOffset, 2+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 3+yOffset, 8+xOffset, 3+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 4+yOffset, 7+xOffset, 5+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 6+yOffset, 8+xOffset, 6+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 7+yOffset, 9+xOffset, 7+yOffset, Color(0, 0, 255))
    SetRange(strip, 6+xOffset, 8+yOffset, 10+xOffset, 8+yOffset, Color(0, 0, 255))
    return 10    
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
    return 10
def MCCreeper(strip, xOffset, yOffset):
    SetRange(strip, 1+xOffset, 1+yOffset, 8+xOffset, 8+yOffset, Color(0, 220, 25))
    SetRange(strip, 2+xOffset, 3+yOffset, 3+xOffset, 4+yOffset, Color(0, 0, 0))
    SetRange(strip, 6+xOffset, 3+yOffset, 7+xOffset, 4+yOffset, Color(0, 0, 0))
    SetRange(strip, 4+xOffset, 5+yOffset, 5+xOffset, 7+yOffset, Color(0, 0, 0))
    SetRange(strip, 3+xOffset, 6+yOffset, 3+xOffset, 8+yOffset, Color(0, 0, 0))
    SetRange(strip, 6+xOffset, 6+yOffset, 6+xOffset, 8+yOffset, Color(0, 0, 0))
    return 8
#endregion
def DFScrollLeft(strip, y, wait_ms):
    for lcv in range(LED_PanelWidth*LED_NumPnlWide - 1, (LED_PanelWidth * -1)-25, -1):
        Blank(strip)
        Position = DiveFlag(strip, lcv, y)
        Position += AlfaFlag(strip, lcv+Position+1, y)+1
        DiveFlag(strip, lcv+Position+1, y)
        strip.show()
        time.sleep(wait_ms/1000.0)

def Open(strip, x, y, color, wait_ms):
    DisplayText(strip, "Open", x, y, color, wait_ms)
    
def OpenScroll(strip, y, color, wait_ms):
    ScrollingText(strip, "Open", y, color, wait_ms)

def BlargScroll(strip, y, color, wait_ms):
    ScrollingText(strip, "Blarg", y, color, wait_ms)

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

#Reads time off of pi and displays it...needs at least 30 or so pixels wide to display properly in 24 hour format, 37 for 12 hour.
def Clock(strip, color, wait_ms = 1000, hrformat = 24, xOffset = 0, yOffset = 0):
    now = datetime.datetime.now()
    Time = ""
    if (hrformat == 12):
        Time = now.strftime("%-I:%M%p")
    else:
        Time = now.strftime("%-H:%M")
    ScrollingText(strip, Time, yOffset, color, wait_ms)
       
def Random(strip):
    wait_ms=1000
    for loop in range(0,10):
        for position in range(0,LED_COUNT):
            if (random.randint(1,4)>2):
                R = random.randint(0,150)
                G = random.randint(0,150)
                B = random.randint(0,150)
            else:
                R=0
                G=0
                B=0
            strip.setPixelColor(position, Color(R, G, B))
        strip.show()
        time.sleep(wait_ms/1000.0)

def Demo(strip):
    #Rainbow(strip)
    DFScrollLeft(strip, 4, 100)
    #Random(strip)
    #BlargScroll(strip, 4, Color(66, 134, 244), 100)
    
def TestDisplay(strip):
    Blank(strip)
    colon(strip, 0, 0, Color(66, 134, 244))
    strip.show()
    time.sleep(1) #Just to slow the infinite loop down and prevent some unneeded CPU load and give you second to look at it if its not the only thing you have active.
        
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
            MCCreeper(strip, 12, 4)
            strip.show()
            time.sleep(2000/1000.0)
            #Clock(strip, Color(15, 252, 3), 150, 12, 0,4)
            #ScrollingText(strip, "abcdefghijklmnopqrstuvwxyz 1234567890 :?.!,;-+*/\\", 0, Color(15, 252, 3), 100)
            ScrollingText(strip, "Only $499.95!", 0, Color(15, 252, 3), 100)
            #DFScrollLeft(strip, 4, 100)
            #TestDisplay(strip)
            Demo(strip)
            Open(strip, 0, 4, Color(66, 134, 244), 1000)

    #Turn off the LED's on Program Exit
    except KeyboardInterrupt:
        BlankDisplay(strip, 1)
        print
        print ("BYE BYE")