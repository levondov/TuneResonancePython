import wx
import time
import threading

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as Navbar
from multiprocessing import Process
from epics import PV

import tdGUI



class tdLiveMode:
    # main screen
    size = (415, 100);
    app = 0
    frame = 0;
    panel = 0;
    live = True;
    tdMain=0;

    live=True;
    pv1 = PV('test:TuneHor');
    pv2 = PV('test:TuneVer');

    horTuneName=0;
    verTuneName=0;

    btn1=0;
    btn2=0;
    btn3=0;

    def __init__(self, tune, tdMain):
        self.app = wx.App();
        # variables
        self.tune = tune;
        self.tdMain=tdMain;

        # init frame
        frame = wx.Frame(None, -1, 'Live Mode', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER);
        self.frame = frame;
        self.frame.SetSize(self.size);
        self.frame.Centre();

        # init panel
        self.panel = wx.Panel(self.frame, -1);

        # construct everything
        self.initialize();
        self.panel.SetSizer(self.sizer);
        self.frame.Show(True);
        self.app.MainLoop()

    def initialize(self):

        self.sizer = wx.GridBagSizer(10, 5);

        hbox1 = wx.BoxSizer(wx.HORIZONTAL);

        box = wx.StaticBox(self.panel, label="EPICS tune variable names",style=wx.CENTER);
        boxsizer = wx.StaticBoxSizer(box, wx.VERTICAL);

        txt1 = wx.StaticText(self.panel, label="Horizontal freq:");
        hbox1.Add(txt1,flag=wx.ALIGN_CENTER,border=5);
        hbox1.Add((5,-1));

        self.horTuneName = wx.TextCtrl(self.panel, size=(100, -1))
        hbox1.Add(self.horTuneName,border=5);
        hbox1.Add((10,-1));

        txt2 = wx.StaticText(self.panel, label="Vertical freq:");
        hbox1.Add(txt2,flag=wx.ALIGN_CENTER,border=5);
        hbox1.Add((5,-1));

        self.verTuneName = wx.TextCtrl(self.panel, size=(100, -1))
        hbox1.Add(self.verTuneName,border=5);
        hbox1.Add((5,-1));

        boxsizer.Add(hbox1,border=5);
        self.sizer.Add(boxsizer,pos=(0,1),span=(1,5),flag=wx.ALIGN_CENTER|wx.CENTER,border=5);

        hbox2 = wx.BoxSizer(wx.HORIZONTAL);

        #buttons
        self.btn1 = wx.Button(self.panel, label='Start', size=(100, 30));
        hbox2.Add(self.btn1,border=5)
        hbox2.Add((10,-1));

        self.btn2 = wx.Button(self.panel, label='Stop', size=(100,30));
        hbox2.Add(self.btn2,border=5)
        hbox2.Add((10,-1));

        self.btn3 = wx.Button(self.panel, label='Edit Mode', size=(100,30));
        hbox2.Add(self.btn3,border=5)
        hbox2.Add((10,-1));

        self.sizer.Add(hbox2, pos=(1,1),span=(1,5),flag=wx.ALIGN_CENTER|wx.CENTER,border=5);

        line1 = wx.StaticLine(self.panel)
        self.sizer.Add(line1, pos=(2, 0), span=(1, 30), flag=wx.EXPAND|wx.BOTTOM, border=5);

        self.btn1.Bind(wx.EVT_BUTTON, self.threadLive);
        self.btn2.Bind(wx.EVT_BUTTON, self.stopLive);
        self.btn3.Bind(wx.EVT_BUTTON, self.onQuit);

    def threadLive(self, e):
        threading.Thread(target=self.refresh()).start();
        threading.Thread(target=self.goLive(e)).start();
        #procs = []
        #procs.append(Process(target=self.refresh()))
        #procs.append(Process(target=self.goLive(e), args=(e)))
        #map(lambda x: x.start(), procs)
        #map(lambda x: x.join(), procs)
    def goLive(self, e):
        if self.live:
            self.live = False;
            self.tune.on();
            self.tune.plot();
            self.tune.show();
        refFreq = 500e6 / 80;
        while self.live == False:
            qx = self.pv1.get();
            qy = self.pv2.get();
            #print(refFreq / qx, refFreq / qy, time.clock());
            self.tune.newWorkingpoint(refFreq / qx, refFreq / qy);
            self.tune.liveUpdate();
            self.tune.draw();
            time.sleep(0.1);

    def refresh(self):
        print('hello')

    def stopLive(self, e):
        print('clicked');
    def onQuit(self, e):
        self.tune.close();
        self.frame.Destroy();
        self.tdMain.show();































