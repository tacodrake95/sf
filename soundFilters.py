import tkinter as tk
import random
import sounddevice as sd
from colour import Color


def lerp(lo, hi, pc):
    return lo + (hi - lo) * pc

def vecLerp(lo, hi, pc):
    return (lerp(lo[0], hi[0], pc), lerp(lo[1], hi[1], pc), lerp(lo[2], hi[2], pc))

black = Color("#000000")
red = Color("#FF0000")
green = Color("#00FF00")
yellow = Color("#FFFF00")
blue = Color("#0000FF")
white = Color("#FFFFFF")
cRange0 = list(black.range_to(red, 256))
cRange1 = list(red.range_to(blue, 256))
cRange2 = list(blue.range_to(green, 256))
cRange3 = list(green.range_to(yellow, 256))
def colorCalc(value):
    
    if value < (1<<8):
        #print(value)
        return cRange0[value]
    
    elif value < (1<<16):
        value = value >> 8
        return cRange1[value]
    
    elif value < (1<<24):
        value = value >> 16
        return cRange2[value]
        
    else:
        value = value >> 24
        return cRange3[value]
                       
first = 1

class App:
    def __init__(self, t):
        self.i = tk.PhotoImage(width=20,height=20)
        self.panel = tk.Label(t, image=self.i)
        self.panel.pack(side="top", fill="both", expand="yes")
        
        
    def refresh(self, i):
        self.panel.configure(image=i)
        self.panel.image=i        
        

res = 64
sRate = 44100

spf = (res * res)
tsf = 1/res


t = tk.Tk()
a = App(t)
def task(t, app):
    data = sd.rec(spf, channels=1, dtype='int32')
    
    img = tk.PhotoImage(width=res,height=res)
    row = 0
    col = 0
    sam = 0
    for value in data:
        value = abs(value[0]) & 0xFFFFFFFF
        color = colorCalc(value)
        img.put(color,(row,col))
        col += 1
        if col == res:
            row +=1; col =0

    img = img.zoom(10)
    app.refresh(img)
    t.after(int(tsf*((spf/sRate) * 1000)), task, t, app)
sd.default.samplerate = sRate
task(t, a)
t.mainloop()
