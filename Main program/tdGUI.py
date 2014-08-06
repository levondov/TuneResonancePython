import wx
import sys
import threading
import time
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as Navbar
from epics import PV
#from tdLiveMode import tdLiveMode
from tdGUISettings import tdGUISettings

myEVT_PLOT = wx.NewEventType();
EVT_PLOT = wx.PyEventBinder(myEVT_PLOT, 1);

class tdGUI:
    # main screen
    size = (640, 560);
    app = 0
    frame = 0;
    panel = 0;

    # box sizers
    hbox1 = 0;
    hbox2 = 0;
    vbox = 0;

    #buttons
    btn1=0; #start live
    btn15=0; # stop live
    btn2=0; # settings

    # display tune
    txt = '';
    horTune = 0;
    verTune = 0;

    # matplotlib stuff
    tune = 0; #tuneDiagram object
    canvas = 0; #matplotlib canvas object. In matlab this would be the figure object
    toolbar = 0; # toolbar object provided by matplotlib

    # settings stuff
    settingspage = 0; # settingspage object. When this is created, settingspage opens
    settingspageRange = [2, 3, 3, 4, 3, 2]; # first 4 values define axis range, i.e. m=1 -> m=2 & n=2-> to n=3, last 2 values are working point integer parts
    settingspageCheckbox = [True, True, True, True, False, False, True, False, False]; #determines whether a checkbox has been selected or not on the settings page
    settingspageOrderbox = [True, True, True, False, False, False, False, False, False, False]; # same as above checkbox, but this is used for the order #

    #live mode
    worker = 0; # this will be the thread object created to run the live updating
    livemode = False; # if true, continue grabbing data from epics and updating. if false, then stop
    pvNames = ['TUNEZRP:measX','TUNEZRP:measY','MCLKHGP:rdFrq',unicode(80)]; #holds epics variable names (default MLS values)
    pv1 = pvNames[0];#PV('test:TuneHor'); #create a PV object for each epics variable so you can then call PVobject.get() and PVobject.put()
    pv2 = pvNames[1];#PV('test:TuneVer'); # same as above, NOTE: PV object is created later in initialization(); this is just to define variables
    rfFreq = pvNames[2]; # same as above
    harNum = pvNames[3]; # harmonic number
    pvWarning = False; # a warning that checks whether the epics variable names are inputted correctly

    def __init__(self, tune):
        # start wx GUI
        self.app = wx.App();
        # variables
        self.tune = tune;

        # init frame
        frame = wx.Frame(None, -1, 'td GUI v3.0', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER);
        self.frame = frame;
        self.frame.SetSize(self.size);
        self.frame.Centre(); # frame in the center of the screen
        self.livemode = livemode(); # separate class made for livemode for easier use. Set current livemode to false
        # init panel
        self.panel = wx.Panel(self.frame, -1);

        # create canvas and toolbar objects
        fig = self.tune.getfig(); # get matplotlib figure
        self.canvas = FigureCanvas(self.panel, -1, fig); #use matplotlib backend to grab canvas
        self.toolbar = Navbar(self.canvas); #use matplotlib backend to grab toolbar

        # create horizontal & vertical boxes
        self.vbox = wx.BoxSizer(wx.VERTICAL);
        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL);
        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL);

        # construct everything
        self.initialize();
        self.frame.Show(True); #show the GUI on the screen

        # main loop for wx GUI
        self.app.MainLoop()

    def initialize(self):

        # add buttons
        self.hbox1.Add(self.toolbar, border=5); # add toolbar
        self.hbox1.Add((5, -1)); # add some spacing
        # create and add button 1
        self.btn1 = wx.Button(self.panel, label='Start Live', size=(80, 30));
        self.hbox1.Add(self.btn1, flag=wx.CENTER); #wx.CENTER aligns the buttons in the center
        self.hbox1.Add((5, -1));
        # create and add button 2
        self.btn15 = wx.Button(self.panel, label='Stop Live', size=(80,30));
        self.hbox1.Add(self.btn15, flag=wx.CENTER);
        self.hbox1.Add((5, -1));
        # create and add button 3
        self.btn2 = wx.Button(self.panel, label='Settings', size=(80, 30));
        self.hbox1.Add(self.btn2, flag=wx.CENTER);
        # add exti door image
        exitImage = wx.Image('exit.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap();
        btn3 = wx.BitmapButton(self.panel, id=-1, bitmap=exitImage);
        self.hbox1.Add((25, -1));
        self.hbox1.Add(btn3, flag=wx.CENTER);

        self.txt = wx.StaticText(self.panel, label='Horizontal Tune: '+str(self.horTune)+' , Vertical Tune: '+str(self.verTune));
        self.hbox2.Add(self.txt,flag=wx.CENTER|wx.EXPAND);

        # add horzinal boxes to vertical box
        self.vbox.Add(self.hbox1, flag=wx.LEFT | wx.TOP, border=5);
        self.vbox.Add((-1, 10));
        self.vbox.Add(self.canvas, flag=wx.EXPAND, border=5)
        self.vbox.Add(self.hbox2,flag=wx.ALIGN_CENTER,border=5)

        self.panel.SetSizer(self.vbox);

        # events binded to buttons. e.g. if btn1 is pressed, call the method startLive()
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow);
        self.btn1.Bind(wx.EVT_BUTTON, self.startLive);
        self.btn15.Bind(wx.EVT_BUTTON, self.stopLive);
        self.btn2.Bind(wx.EVT_BUTTON, self.settingsPage);
        btn3.Bind(wx.EVT_BUTTON, self.OnCloseWindow);
        self.panel.Bind(EVT_PLOT, self.continueLive)

        # disable stop live button initially
        self.btn15.Disable();

    # Update the graph. Executed when hitting 'ok' on settings page
    def update(self, e):
        # plot everything according to what options were selected in settings page
        self.tune.plot();
        # draw all the new plotting and update the graph (essentially the same as plt.show())
        self.canvas.draw();

    # when start button is pressed
    def startLive(self, e):
        #first check epics values
        if self.pv1 == '' or self.pv2 == '':
            wx.MessageBox('Warning! No EPICS variables detected, check settings.', 'Warning', wx.OK | wx.ICON_WARNING);
        elif self.pvWarning:
            wx.MessageBox('Warning! No EPICS variables found with that name, please check to see if spelling is correct', 'Warning', wx.OK | wx.ICON_WARNING);
        elif type(self.pvNames[3]) == type(''): #harmonic number should be an int not string
            wx.MessageBox('Warning! The harmonic number has been inputted in correctly', 'Warning', wx.OK | wx.ICON_WARNING);
        else:
            # first create the PV objects
            self.setPV(self.pvNames[0],self.pvNames[1],self.pvNames[2],self.pvNames[3]);
            # live mode on, disable and enable some buttons
            self.livemode.change(True);
            self.btn1.Disable();
            self.btn2.Disable();
            self.btn15.Enable();
            # get integer part of the tune
            integerHor = self.settingspageRange[4];
            integerVer = self.settingspageRange[5];
            # check for mirror tune
            if self.settingspageCheckbox[8]:
                integerHor+=0.5
                integerVer+=0.5
            # start separate thread to process event so the GUI does not freeze up
            self.worker = CountingThread(self.panel,self, self.tune,self.canvas,self.livemode, self.pv1, self.pv2, self.rfFreq, self.pvNames[3], [integerHor, integerVer]);
            self.worker.daemon = True;
            self.worker.start();

    # when stop button is pressed, stop live mode
    def stopLive(self, evt):
        # stop livemode and enable some buttons
        self.livemode.change(False);
        self.btn1.Enable();
        self.btn2.Enable();
        self.btn15.Disable();

    # will continue updating and drawing as long as we are in live mode
    def continueLive(self, evt):
        if self.livemode.get():
            # update canvas
            self.canvas.draw();
            # update text
            self.updateTuneText()
            # after drawing, start over from startLive()
            self.startLive(evt);

    def updateTuneText(self):
        self.horTune,self.verTune = self.livemode.getTune()
        txt2 = wx.StaticText(self.panel, label='Horizontal Tune: '+str(self.horTune)+' , Vertical Tune: '+str(self.verTune));
        self.hbox2.Remove(self.txt);
        self.txt.Destroy()
        txt2.SetForegroundColour((255,0,0)) # set text color
        self.hbox2.Add(txt2);
        self.hbox2.Layout();
        self.vbox.Layout();
        self.txt = txt2;

    # Opens a settings page/window
    def settingsPage(self, e):
        self.settingspage = tdGUISettings(self, self.tune, self.tune.getorder(), self.settingspageRange, self.settingspageCheckbox, self.settingspageOrderbox);

# The next 4 methods are mainly used to save user settings. e.g. if the user turns off a checkbox, it should stay turned off next time the settings page is opened
    # used by the settingspage to update axis settings
    def setRange(self, newrange):
        self.settingspageRange = newrange;

    # used by the settingspage to update all checkboxes
    def setCheckbox(self, newcheckboxValues):
        self.settingspageCheckbox = newcheckboxValues;

    # used by the settings page to update order boxes
    def setOrderbox(self, newValues):
        self.settingspageOrderbox = newValues;

    # set the epics variable names
    def setPV(self, horName, verName, rfFreq, harNum):
        # will throw an exception if something goes wrong assigning the epics variable names
        try:
            self.pvNames = [horName, verName, rfFreq, harNum];
            self.pv1 = PV(horName);
            self.pv2 = PV(verName);
            self.rfFreq = PV(rfFreq);
            self.pv1.get();
            self.pv2.get();
            self.rfFreq.get();
            self.pvWarning = False;
        except:
            self.pvWarning = True;

    # returns current epics variable names. Used by settings page to keep fields updated
    def getpvNames(self):
        return self.pvNames;

    # gives a warning window when exiting program
    def OnCloseWindow(self, e):

        dial = wx.MessageDialog(None, 'Are you sure you want to quit?', 'Warning',wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION);
        ret = dial.ShowModal();

        if ret == wx.ID_YES:
            self.frame.Destroy();
            sys.exit();

# custon event class created for updating live mode
class CountEvent(wx.PyCommandEvent):
    def __init__(self, etype, eid):
        wx.PyCommandEvent.__init__(self, etype, eid)

# threading class used in live mode
class CountingThread(threading.Thread):
    def __init__(self, parent, tdGUI, tune, canvas, livemode, pv1, pv2, rfFreq, pvNames, integers):
        threading.Thread.__init__(self)
        self._parent = parent;
        self._GUI = tdGUI;
        self._tune = tune;
        self._canvas = canvas;
        self._livemode = livemode;
        self._pv1 = pv1;
        self._pv2 = pv2;
        self._rfFreq = rfFreq;
        self._pvNames = pvNames;
        self._intHor = integers[0];
        self._intVer = integers[1];
        try:
            self._pvNames = int(self._pvNames);
        except:
            print('WARNING: The harmonic number has to be a number');
            self._livemode.change(False);
    # run will get executed when calling threadobject.start()
    def run(self):
        # get RF freq
        refFreq = self._rfFreq.get() / int(self._pvNames);
        # print current tune, this can be disabled
        self._livemode.changeTune(self._intHor + self._pv1.get()/refFreq,self._intVer + self._pv2.get()/refFreq)
        # update the tune working point qX and qY values
        self._tune.newWorkingpoint(self._intHor + (self._pv1.get() / refFreq), self._intVer + (self._pv2.get() / refFreq));
        # plot the working point as a circle using the new qX and qY coordinates
        self._tune.liveUpdate();
        # execute an event telling the GUI that this thread is done
        time.sleep(0.5)
        evt = CountEvent(myEVT_PLOT, -1);
        wx.PostEvent(self._parent, evt);

# a class to be used by everything to check the current status of livemode (True or False)
class livemode:
    livemode=False;
    currentHorTune=0;
    currentVerTune=0;

    def __init__(self):
        self.livemode = False;

    def change(self, livemode):
        self.livemode = livemode;

    def changeTune(self,hor,ver):
        self.currentHorTune=hor;
        self.currentVerTune=ver;

    def getTune(self):
        return self.currentHorTune,self.currentVerTune;

    def get(self):
        return self.livemode;