#
# Levon Dovlatyan
# Markus Ries und Paul Goslawski
# BESSY, Berlin
# 20 June 2014
#
# ##############################

import matplotlib.pyplot as plt  # for plotting purposes
import numpy as np  # for array operations
import Tkinter  # for GUI
import tkMessageBox
import tuneDiagram
from Tkinter import *
from tuneDiagram import *

tune1 = tuneDiagram(3, .15, .16, .05);

# UI start
root = Tkinter.Tk();
root.geometry('400x300');

# UI methods
def launch():
    root.quit();
    root.destroy();
    tune1.plot();


def AdvancedValues():
    x = 4;


def advanced():
    advancedW = Toplevel();
    advancedW.geometry('300x300');
    ok = Tkinter.Button(advancedW, text='OK', command=advancedValues);
    quitAdvanced = Tkinter.Button(advanced, text='exit', command=quitAdvanced);
    ok.grid(pady=[150, 150], column=0);
    quitAdvanced.grid(pady=[150, 150], column=1);


def quitAdvanced():
    advancedW.quit();
    advancedW.destroy();


def quit():
    root.quit();
    root.destroy();

# ################# Main Menu #######################
# User inputs
title1 = Label(root, text='Order and Integers', fg='red');
title1.grid(row=1, column=0);
# Order
order = Label(root, text='Order: ');
order.grid(row=2, column=0);
orderE = Entry(root, bd=2, width=5);
orderE.grid(row=2, column=1);
# m
mMin = Label(root, text='m value: ');
mMin.grid(row=3, column=0);
mMinE = Entry(root, bd=2, width=5);
mMinE.grid(row=3, column=1);
mMax = Label(root, text=' to ');
mMax.grid(row=3, column=2);
mMaxE = Entry(root, bd=2, width=5);
mMaxE.grid(row=3, column=3);
# n
nMin = Label(root, text='n value: ');
nMin.grid(row=4, column=0);
nMinE = Entry(root, bd=2, width=5);
nMinE.grid(row=4, column=1);
nMax = Label(root, text=' to ');
nMax.grid(row=4, column=2);
nMaxE = Entry(root, bd=2, width=5);
nMaxE.grid(row=4, column=3);
# Qx and Qy coordinates
title2 = Label(root, text='Working point', fg='red');
title2.grid(row=5, column=0);
qx = Label(root, text='Qx value: ');
qx.grid(row=6, column=0);
qxE = Entry(root, bd=2, width=5);
qxE.grid(row=6, column=1);
qy = Label(root, text=' Qy value: ');
qy.grid(row=6, column=2);
qyE = Entry(root, bd=2, width=5);
qyE.grid(row=6, column=3);
# Buttons main page
launch = Tkinter.Button(root, text="Launch", command=launch);
advanced = Tkinter.Button(root, text='advanced', command=advanced);
quit = Tkinter.Button(root, text='exit', command=quit);
launch.grid(row=7, column=0, pady=[120, 10]);
advanced.grid(row=7, column=1, pady=[120, 10], padx=[30, 0]);
quit.grid(row=7, column=3, pady=[120, 10]);

root.mainloop();




