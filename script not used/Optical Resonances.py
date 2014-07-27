#
# Levon Dovlatyan
# Markus Ries und Paul Goslawski
# BESSY, Berlin
# 20 June 2014
#
###############################

import matplotlib.pyplot as plt # for plotting purposes
import numpy as np # for array operations
import Tkinter # for GUI
import tkMessageBox
from Tkinter import * 

#UI start
root = Tkinter.Tk();
root.geometry('350x300');

#UI methods
#UI stuff
def launch():    
    root.quit();
    root.destroy();
    plt.show();

#working point circle
radius = .05;
circleX = .4;
circleY = .9;

plt.plot(circleX,circleY,'ro');
circle=plt.Circle((circleX,circleY),radius,color='r',fill=False)
plt.gca().add_artist(circle)

# Integer values
order = 3;
p = np.linspace(0,50,51);

# window size
qxmin = -5;
qxmax = 5;
qymin = -5;
qymax = 5;

# Plotting formula
for i in range(1,order+1,1):
    m = np.linspace(-i,i,2*i+1);
    n1 = (i - np.abs(m));
    n2 = -(i-np.abs(m));
    for j in range(0,m.size,1):
        # check to see equation is divided by 0 or not
        if n1[j] == 0:
            plt.vlines(p/m[j],qxmin,qxmax);
        elif m[j] == 0:
            plt.hlines(p/n1[j],qymin,qymax);
            plt.hlines(p/n2[j],qymin,qymax);
        else:
            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n1[j] - np.array(m[j]*qxmin/n1[j]), p/n1[j] - np.array(m[j]*qxmax/n1[j])]);
            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n2[j] - np.array(m[j]*qxmin/n2[j]), p/n2[j] - np.array(m[j]*qxmax/n2[j])]);

#plt.axis([qxmin,qxmax,qymin,qymax]);
plt.axis([-.1,1.1,-.1,1.1]);


#User inputs
title1 = Label(root, text='Order and Integers',fg='red'); title1.grid(row=1,column=0);
# Order
order = Label(root, text='Order: '); order.grid(row=2,column=0);
orderE = Entry(root, bd=2,width=5); orderE.grid(row=2,column=1);
# m
mMin = Label(root, text='m value: '); mMin.grid(row=3,column=0);
mMinE = Entry(root, bd=2,width=5); mMinE.grid(row=3,column=1);
mMax = Label(root, text=' to '); mMax.grid(row=3,column=2);
mMaxE = Entry(root, bd=2,width=5); mMaxE.grid(row=3,column=3);
# n
nMin = Label(root, text='n value: '); nMin.grid(row=4,column=0);
nMinE = Entry(root, bd=2,width=5); nMinE.grid(row=4,column=1);
nMax = Label(root, text=' to '); nMax.grid(row=4,column=2);
nMaxE = Entry(root, bd=2,width=5); nMaxE.grid(row=4,column=3);
# Qx and Qy coordinates
title2 = Label(root, text='Coordinates for working point',fg='red'); title2.grid(row=5,column=0);
qx = Label(root, text='Qx value: '); qx.grid(row=6,column=0);
qxE = Entry(root, bd=2,width=5); qxE.grid(row=6,column=1);
qy = Label(root, text=' Qy value: '); qy.grid(row=6,column=2);
qyE = Entry(root, bd=2,width=5); qyE.grid(row=6,column=3);

launch = Tkinter.Button(root, text = "Launch", command = launch);
launch.grid(sticky=S,column=2);

root.mainloop();

