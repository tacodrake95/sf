import tkinter as tk
import random
import sounddevice as sd

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
    data = sd.rec(4096, channels=1, dtype='int16')
    
    img = tk.PhotoImage(width=64,height=64)
    row = 0
    col = 0
    for value in data:
        value = int(value[0] << 7) & 0xFFFFFF
        value = "#" + hex(value)[2:].zfill(6)
        #print(value)
        
        img.put(value,(row,col))
        col += 1
        if col == 64:
            row +=1; col =0

    img = img.zoom(3)
    app.refresh(img)
    t.after(100, task, t, app)
sd.default.samplerate = 40960
task(t, a)
t.mainloop()
