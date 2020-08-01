import tkinter as tk
import random
import sounddevice as sd

class App:
    def __init__(self, t):
        self.i0 = tk.PhotoImage(width=20,height=20)
        self.i1 = tk.PhotoImage(width=20,height=20)
        self.i2 = tk.PhotoImage(width=20,height=20)
        
        self.panel0 = tk.Label(t, image=self.i0)
        self.panel1 = tk.Label(t, image=self.i0)
        self.panel2 = tk.Label(t, image=self.i0)
        self.panel3 = tk.Label(t, image=self.i0)
        self.panel0.pack(side="top", fill="both", expand="yes")
        self.panel1.pack(side="top", fill="both", expand="yes")
        self.panel2.pack(side="top", fill="both", expand="yes")
        self.panel3.pack(side="top", fill="both", expand="yes")
        
        
    def refresh(self, i):

        self.panel3.configure(image=self.i2)
        self.panel3.image=self.i2

        self.i2 = self.i1
        self.panel2.configure(image=self.i1)
        self.panel2.image=self.i1

        self.i1 = self.i0
        self.panel1.configure(image=self.i0)
        self.panel1.image=self.i0

        self.i0 = i
        self.panel0.configure(image=i)
        self.panel0.image=i
        
        
        
        


t = tk.Tk()
a = App(t)
def task(t, app):
    data = sd.rec(400, channels=1, dtype='int32')
    
    img = tk.PhotoImage(width=20,height=20)
    row = 0
    col = 0
    for value in data:
        value = int(value[0]/128) & 0xFFFFFF
        value = "#" + hex(value)[2:].zfill(6)
        #print(value)
        
        img.put(value,(row,col))
        col += 1
        if col == 20:
            row +=1; col =0

    img = img.zoom(3)
    app.refresh(img)
    t.after(9, task, t, app)
sd.default.samplerate = 44100
task(t, a)
t.mainloop()
