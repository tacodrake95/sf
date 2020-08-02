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
    data = sd.rec(1024, channels=1, dtype='int32')
    
    img = tk.PhotoImage(width=32,height=32)
    row = 0
    col = 0
    for value in data:
        value = int(value[0] << 7) & 0x7FFFFF
        value = "#" + hex(value)[2:].zfill(6)
        #print(value)
        
        img.put(value,(row,col))
        col += 1
        if col == 32:
            row +=1; col =0

    img = img.zoom(10)
    app.refresh(img)
    t.after(25, task, t, app)
sd.default.samplerate = 40960
task(t, a)
t.mainloop()
