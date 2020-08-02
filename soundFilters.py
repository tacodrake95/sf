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
blue = Color("#0000FF")
white = Color("#FFFFFF")
cRange0 = list(red.range_to(blue, 256))
cRange1 = list(blue.range_to(green, 256))
cRange2 = list(blue.range_to(white, 256))

def colorCalc(value):
    value = int((value[0]+0x7FFFFFFF))
    #print(value)
    if value < (1<<8):
        return black
    
    elif value < (1<<8):
        value = value >> 8
        return cRange0[value]
    
    elif value < (1<<16):
        value = value >> 16
        return cRange1[value]
        
    else:
        value = value >> 24
        return cRange2[value]
                       
first = 1

class App:
    def __init__(self, t):
        self.i = tk.PhotoImage(width=20,height=20)
        self.panel = tk.Label(t, image=self.i)
        self.panel.pack(side="top", fill="both", expand="yes")
        
        
    def refresh(self, i):
        self.panel.configure(image=i)
        self.panel.image=i        
        


t = tk.Tk()
a = App(t)
def task(t, app):
    data = sd.rec(1024, channels=1, dtype='int32')
    
    img = tk.PhotoImage(width=32,height=32)
    row = 0
    col = 0
    for value in data:
        color = colorCalc(value)
        value = int(value[0] >> 7) & 0xFFFFFF
        value = "#" + hex(value)[2:].zfill(6)
        #print(value)
        
        img.put(color,(row,col))
        col += 1
        if col == 32:
            row +=1; col =0

    img = img.zoom(3)
    app.refresh(img)
    t.after(25, task, t, app)
sd.default.samplerate = 40960
task(t, a)
t.mainloop()
