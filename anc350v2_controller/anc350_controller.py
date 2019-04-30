# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 17:42:33 2019

@author: Ohad Michel
"""

from Tkinter import Tk, Button, Entry, Label
from pyanc350.v2 import Positioner
import time

class ANC350_controller:
    '''A class for custon gui to control ANC350 version 2'''
    def __init__(self):
        self.root = Tk() # create interface instance
        self.root.title('ANC350 Controller') # change title
        self.root.geometry('500x300') # define window size
        self.p = Positioner() # create a positioner instance to send commands to ANC350v2
        self.pos = [self.p.getPosition(0), self.p.getPosition(1), self.p.getPosition(2)] # a position list
        
        # create text boxes to show position
        self.Xpos_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=9)
        self.Ypos_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=9)
        self.Zpos_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=9)

        # create step size boxes
        self.Xstepsize_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=3)
        self.Ystepsize_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=3)
        self.Zstepsize_ent = Entry(self.root, font = "Helvetica 16 bold", justify="center", width=3)
        self.Xstepsize_ent.insert(0, 1) # define defualt values
        self.Ystepsize_ent.insert(0, 1) # define defualt values
        self.Zstepsize_ent.insert(0, 1) # define defualt values
        # create status bar
        self.status_ent = Entry(self.root, font = "Helvetica 14 bold", justify="center", width=20, readonlybackground = "black")
        if self.p.numconnected:        
            self.status_ent.insert(0,str(self.p.posinf.id) + " Connected")
            self.status_ent.config({"fg":"green", "state":"readonly"})
        else:
            self.status_ent.insert(0, "Disconnected")
            self.status_ent.config({"fg":"red", "state":"readonly"})
        
        # create labels
        self.Xpos_lbl = Label(self.root, text = u"X (\u03BCm)", font = "Helvetica 14", justify="center")
        self.Ypos_lbl = Label(self.root, text = u"Y (\u03BCm)", font = "Helvetica 14", justify="center")
        self.Zpos_lbl = Label(self.root, text = u"Z (\u03BCm)", font = "Helvetica 14", justify="center")
        self.step_lbl = Label(self.root, text = u" Step (\u03BCm):", font = "Helvetica 12", justify="center")
        
        # create buttons
        self.read_btn = Button(self.root, text = "read", command = lambda: self.read(), font = "Helvetica 16", justify="center") 
        
        self.Xplus_btn = Button(self.root, text = "X+", command = lambda: self.move(0, 1), font = "Helvetica 16", justify="center")
        self.Xminus_btn = Button(self.root, text = "X-", command = lambda: self.move(0,-1), font = "Helvetica 16", justify="center")
        
        self.Yplus_btn = Button(self.root, text = "Y+", command = lambda: self.move(1, 1), font = "Helvetica 16", justify="center")
        self.Yminus_btn = Button(self.root, text = "Y-", command = lambda: self.move(1,-1), font = "Helvetica 16", justify="center")
        
        self.Zplus_btn = Button(self.root, text = "Z+", command = lambda: self.move(2, 1), font = "Helvetica 16", justify="center")
        self.Zminus_btn = Button(self.root, text = "Z-", command = lambda: self.move(2,-1), font = "Helvetica 16", justify="center")
        
        # place widgets on grid
        self.status_ent.grid(column = 1, row = 0, columnspan=3)
        self.Xpos_lbl.grid(column = 1, row = 1)
        self.Ypos_lbl.grid(column = 2, row = 1)
        self.Zpos_lbl.grid(column = 3, row = 1)
        self.Xpos_ent.grid(column = 1, row = 2)
        self.Ypos_ent.grid(column = 2, row = 2)
        self.Zpos_ent.grid(column = 3, row = 2)
        self.step_lbl.grid(column = 0, row = 3)
        self.Xstepsize_ent.grid(column = 1, row = 3)
        self.Ystepsize_ent.grid(column = 2, row = 3)
        self.Zstepsize_ent.grid(column = 3, row = 3)
        self.read_btn.grid(column = 2, row = 4)
        self.Yplus_btn.grid(column = 1, row = 5)
        self.Xplus_btn.grid(column = 2, row = 6)
        self.Xminus_btn.grid(column = 0, row = 6)
        self.Yminus_btn.grid(column = 1, row = 7)
        self.Zplus_btn.grid(column = 3, row = 5)
        self.Zminus_btn.grid(column = 3, row = 7)
        
        # key binding
        self.root.bind("<Next>", lambda event: self.move(0, 1)) # move +X key       
        self.root.bind("<Delete>", lambda event: self.move(0, -1)) # move -X key        
        self.root.bind("<Home>", lambda event: self.move(1, 1)) # move +Y key
        self.root.bind("<End>", lambda event: self.move(1, -1)) # move -Y key
        self.root.bind("<F2>", lambda event: self.move(2, 1)) # move +Z key
        self.root.bind("<F1>", lambda event: self.move(2, -1)) # move -Z key
        self.root.bind("<Escape>", lambda event: self.root.focus()) # focus on main window key
        self.root.bind("<Return>", lambda event: self.read()) # read key
        
    def __enter__(self):
        '''Excecutes when entering a "with" statement,  returns self'''
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Excecutes at the end of a "with" statement, closes connection to device'''
        self.p.setOutput(0,0) # deactivate axis 0
        self.p.setOutput(1,0) # deactivate axis 1
        self.p.setOutput(2,0) # deactivate axis 2        
        self.p.close()
    
    def update_pos_boxes(self):
        '''Updates values in the position boxes based on the current values stored in "self.pos" list'''
        self.Xpos_ent.delete(0, "end")
        self.Ypos_ent.delete(0, "end")
        self.Zpos_ent.delete(0, "end")
        self.Xpos_ent.insert(0, self.pos[0]/1e3)
        self.Ypos_ent.insert(0, self.pos[1]/1e3)
        self.Zpos_ent.insert(0, self.pos[2]/1e3)
    
    def read(self):
        '''Reads the positions of the 3 axes and updates the position boxes'''
        self.pos[0] = self.p.getPosition(0)
        self.pos[1] = self.p.getPosition(1)
        self.pos[2] = self.p.getPosition(2)
        self.update_pos_boxes()
        
    def move(self, axis, direct):
        '''Moves axis "axis" (0,1,2) in direction "direct" by length "stepsize" in nm'''
        # activate axis and get step size
        if axis == 0:
            self.p.setOutput(axis,1) # activate axis
            self.p.setOutput(1,0) # deactivate axis
            self.p.setOutput(2,0) # deactivate axis
            stepsize = int(float(self.Xstepsize_ent.get())*1e3) # step size in nm
        elif axis == 1:
            self.p.setOutput(axis,1) # activate axis
            self.p.setOutput(0,0) # deactivate axis
            self.p.setOutput(2,0) # deactivate axis
            stepsize = int(float(self.Ystepsize_ent.get())*1e3) # step size in nm
        elif axis == 2:
            self.p.setOutput(axis,1) # activate axis
            self.p.setOutput(0,0) # deactivate axis
            self.p.setOutput(1,0) # deactivate axis
            stepsize = int(float(self.Zstepsize_ent.get())*1e3) # step size in nm
        
        # if there is no position value stored, get one
        if not self.pos[axis]:
            self.pos[axis] = self.p.getPosition(axis)
            
        # modify position based on the step taken
        if direct>0:
            self.pos[axis] += stepsize
            
        else:
            self.pos[axis] -= stepsize
       
        self.p.moveAbsolute(axis,self.pos[axis]) # move absolute position to new value
        self.update_pos_boxes() # update new value in the position boxes
    

with ANC350_controller() as anc350:
    anc350.root.mainloop()

'''
p = Positioner()

#p.capMeasure(1)
#p.getAmplitude(1)
#p.getPosition(1)
#p.getStepwidth(1)
#p.moveAbsolute(0,p.getPosition(0)+1000)
#p.moveSingleStep(0,0)
#p.moveContinuous(0,0)
#p.setOutput(1,0)

'''