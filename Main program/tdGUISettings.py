import wx
import wx.lib.agw.floatspin as FS
import tdGUI
import tuneDiagram


class tdGUISettings:

    # main window
    size = (450,450);
    window = 0;
    parent = 0;
    frame = 0;
    panel = 0;
    tune = 0;
    sizer=0;

    # settings values
    rangeValues=0;

    # lists
    list1=0;
    list2=0;
    list3=0;
    list4=0;
    nlist=0;
    integerM=0;
    integerN=0;

    # checkboxes
    checkboxValues=0;
    checkbox1=0;
    checkbox2=0;
    checkbox3=0;
    checkbox4=0;
    checkbox5=0;
    checkbox6=0;
    checkbox7=0;
    checkbox8=0;

    # order checkboxes
    orderboxValues=0;
    orderbox1=0;
    orderbox2=0;
    orderbox3=0;
    orderbox4=0;
    orderbox5=0;
    orderbox6=0;
    orderbox7=0;
    orderbox8=0;
    orderbox9=0;
    orderbox10=0;

    # buttons
    btn1=0;
    btn2=0;

    # tune names
    horTuneName='';
    verTuneName='';
    rfFreqName='';
    harNumName='';

    def __init__(self, parent, tune, order, rangeValues=[2,3,3,4,3,2],checkboxValues=[True,True,True,True,True,False,False,False],
                 orderboxValues=[True,True,True,False,False,False,False,False,False,False]):
        self.window=wx.App();

        # variables
        self.tune = tune;
        self.parent = parent;
        self.rangeValues=rangeValues;
        self.checkboxValues=checkboxValues;
        self.orderboxValues=orderboxValues;

        # init frame
        frame = wx.Frame(None, -1, 'Settings', style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER);
        self.frame = frame;


        # init panel
        self.panel = wx.Panel(self.frame, -1);

        #construct everything
        self.initialize();
        self.frame.Show(True);
        self.frame.SetSize(self.size);
        self.frame.Centre();
        self.panel.SetSizer(self.sizer);
        # close window
        self.frame.Bind(wx.EVT_CLOSE, self.onClose);

        self.window.MainLoop()

    def initialize(self):

        # init sizer
        self.sizer = wx.GridBagSizer(10, 5);

        # adding live mode box
        box0 = wx.StaticBox(self.panel, label="Live Mode options");
        boxsizer0 = wx.StaticBoxSizer(box0, wx.VERTICAL);

        hbox1 = wx.BoxSizer(wx.HORIZONTAL);

        txt1 = wx.StaticText(self.panel, label="Horizontal freq:");
        hbox1.Add(txt1,flag=wx.ALIGN_CENTER,border=5);
        hbox1.Add((5,-1));

        pvNames = self.parent.getpvNames();

        self.horTuneName = wx.TextCtrl(self.panel, size=(120, -1));
        self.horTuneName.SetValue(pvNames[0]);
        hbox1.Add(self.horTuneName,border=5);
        hbox1.Add((10,-1));

        txt2 = wx.StaticText(self.panel, label="Vertical freq:");
        hbox1.Add(txt2,flag=wx.ALIGN_CENTER,border=5);
        hbox1.Add((5,-1));

        self.verTuneName = wx.TextCtrl(self.panel, size=(120, -1));
        self.verTuneName.SetValue(pvNames[1]);
        hbox1.Add(self.verTuneName,border=5);
        hbox1.Add((5,-1));

        boxsizer0.Add(hbox1,border=5);

        hbox2 = wx.BoxSizer(wx.HORIZONTAL);

        txt1 = wx.StaticText(self.panel, label='RF Freq:               ');
        hbox2.Add(txt1, flag=wx.ALIGN_CENTER,border=5);
        hbox2.Add((5,-1));

        self.rfFreqName = wx.TextCtrl(self.panel, size=(120, -1));
        self.rfFreqName.SetValue(pvNames[2]);
        hbox2.Add(self.rfFreqName,border=5);
        hbox2.Add((10,-1));

        txt2 = wx.StaticText(self.panel, label="Harmonic #: ");
        hbox2.Add(txt2,flag=wx.ALIGN_CENTER,border=5);
        hbox2.Add((5,-1));

        self.harNumName = wx.TextCtrl(self.panel, size=(120, -1));
        self.harNumName.SetValue(pvNames[3]);
        hbox2.Add(self.harNumName,border=5);
        hbox2.Add((5,-1));

        boxsizer0.Add(hbox2,border=5);
        self.sizer.Add(boxsizer0,pos=(0,1),span=(3,6),flag=wx.ALIGN_CENTER|wx.CENTER,border=5);

        # Adding graphical options box
        box1 = wx.StaticBox(self.panel, label="Graphical options");
        boxsizer1 = wx.StaticBoxSizer(box1, wx.VERTICAL);

        self.checkbox1 = wx.CheckBox(self.panel, label="Horizontal resonances");
        boxsizer1.Add(self.checkbox1, flag=wx.LEFT|wx.TOP,border=5);
        if self.checkboxValues[0]:
            self.checkbox1.Set3StateValue(wx.CHK_CHECKED);

        self.checkbox2 = wx.CheckBox(self.panel, label='Vertical resonances');
        boxsizer1.Add(self.checkbox2, flag=wx.LEFT,border=5);
        if self.checkboxValues[1]:
            self.checkbox2.Set3StateValue(wx.CHK_CHECKED);

        self.checkbox3 = wx.CheckBox(self.panel, label='Summing resonances');
        boxsizer1.Add(self.checkbox3, flag=wx.LEFT,border=5);
        if self.checkboxValues[2]:
            self.checkbox3.Set3StateValue(wx.CHK_CHECKED);

        self.checkbox4 = wx.CheckBox(self.panel, label='DIfference resonances');
        boxsizer1.Add(self.checkbox4, flag=wx.LEFT|wx.BOTTOM,border=5);
        if self.checkboxValues[3]:
            self.checkbox4.Set3StateValue(wx.CHK_CHECKED);

        self.sizer.Add(boxsizer1, pos=(3,1), span=(1,3),flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,border=10);

        # Adding color scheme box
        box2 = wx.StaticBox(self.panel, label="Color scheme");
        boxsizer2 = wx.StaticBoxSizer(box2, wx.VERTICAL);

        self.checkbox5 = wx.CheckBox(self.panel, label='Random');
        boxsizer2.Add(self.checkbox5, flag=wx.LEFT|wx.TOP,border=5);
        if self.checkboxValues[4]:
            self.checkbox5.Set3StateValue(wx.CHK_CHECKED);

        self.checkbox6 = wx.CheckBox(self.panel, label='Black');
        boxsizer2.Add(self.checkbox6, flag=wx.LEFT,border=5);
        if self.checkboxValues[5]:
            self.checkbox6.Set3StateValue(wx.CHK_CHECKED);

        self.checkbox7 = wx.CheckBox(self.panel, label='By order');
        boxsizer2.Add(self.checkbox7, flag=wx.LEFT|wx.BOTTOM,border=5);
        if self.checkboxValues[6]:
            self.checkbox7.Set3StateValue(wx.CHK_CHECKED);

        self.sizer.Add(boxsizer2, pos=(3,4), span=(1,2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,border=10);

        # Adding order box
        box3 = wx.StaticBox(self.panel, label="Order",style=wx.CENTER);
        boxsizer3 = wx.StaticBoxSizer(box3, wx.HORIZONTAL);

        hbox = wx.BoxSizer(wx.HORIZONTAL);

        self.orderbox1 = wx.CheckBox(self.panel, label='1');
        hbox.Add(self.orderbox1,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[0]:
            self.orderbox1.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox2 = wx.CheckBox(self.panel, label='2');
        hbox.Add(self.orderbox2,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[1]:
            self.orderbox2.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox3 = wx.CheckBox(self.panel, label='3');
        hbox.Add(self.orderbox3,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[2]:
            self.orderbox3.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox4 = wx.CheckBox(self.panel, label='4');
        hbox.Add(self.orderbox4,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[3]:
            self.orderbox4.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox5 = wx.CheckBox(self.panel, label='5');
        hbox.Add(self.orderbox5,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[4]:
            self.orderbox5.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox6 = wx.CheckBox(self.panel, label='6');
        hbox.Add(self.orderbox6,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[5]:
            self.orderbox6.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox7 = wx.CheckBox(self.panel, label='7');
        hbox.Add(self.orderbox7,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[6]:
            self.orderbox7.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox8 = wx.CheckBox(self.panel, label='8');
        hbox.Add(self.orderbox8,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[7]:
            self.orderbox8.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox9 = wx.CheckBox(self.panel, label='9');
        hbox.Add(self.orderbox9,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[8]:
            self.orderbox9.Set3StateValue(wx.CHK_CHECKED);

        self.orderbox10 = wx.CheckBox(self.panel, label='10');
        hbox.Add(self.orderbox10,flag=wx.LEFT);
        hbox.Add((5,-1));
        if self.orderboxValues[9]:
            self.orderbox10.Set3StateValue(wx.CHK_CHECKED);

        boxsizer3.Add(hbox,border=5);
        self.sizer.Add(boxsizer3,pos=(4,1),span=(1,5), flag=wx.CENTER|wx.ALIGN_CENTER,border=10);

       # Adding m,n value ranges

        boxAxis = wx.StaticBox(self.panel, label='Axes settings');
        boxsizerAxis = wx.StaticBoxSizer(boxAxis, wx.VERTICAL);

        hboxAxis1 = wx.BoxSizer(wx.HORIZONTAL);

        txt1 = wx.StaticText(self.panel,label='Vertical:\t');
        hboxAxis1.Add(txt1, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis1.Add((5,-1));

        self.list1 = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS, min=0, max=20, initial=self.rangeValues[0]);
        hboxAxis1.Add(self.list1, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis1.Add((5,-1));

        txt2 = wx.StaticText(self.panel, label='to');
        hboxAxis1.Add(txt2, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis1.Add((5,-1));

        self.list2 = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS, min=0, max=20, initial=self.rangeValues[1]);
        hboxAxis1.Add(self.list2, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis1.Add((5,-1));

        boxsizerAxis.Add(hboxAxis1,border=5);
        hboxAxis2 = wx.BoxSizer(wx.HORIZONTAL);

        txt3 = wx.StaticText(self.panel,label='Horizontal:  ');
        hboxAxis2.Add(txt3, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis2.Add((5,-1));

        self.list3 = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS, min=0, max=20, initial=self.rangeValues[2]);
        hboxAxis2.Add(self.list3, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis2.Add((5,-1));

        txt4 = wx.StaticText(self.panel, label='to');
        hboxAxis2.Add(txt4, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis2.Add((5,-1));

        self.list4 = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS, min=0, max=20, initial=self.rangeValues[3]);
        hboxAxis2.Add(self.list4, flag=wx.ALIGN_CENTER,border=5);
        hboxAxis2.Add((5,-1));

        boxsizerAxis.Add(hboxAxis2,border = 5);
        hboxMain = wx.BoxSizer(wx.HORIZONTAL);
        hboxMain.Add(boxsizerAxis);
        hboxMain.Add((5,-1));

        boxInteger = wx.StaticBox(self.panel, label='Integer Values');
        boxsizerInteger = wx.StaticBoxSizer(boxInteger, wx.VERTICAL);

        hboxInteger1 = wx.BoxSizer(wx.HORIZONTAL);

        txt1 = wx.StaticText(self.panel, label='m:\t\t');
        hboxInteger1.Add(txt1, flag=wx.ALIGN_CENTER, border=5);
        self.integerM = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS,min=0,max=20,initial=self.rangeValues[5]);
        hboxInteger1.Add(self.integerM, flag=wx.ALIGN_CENTER,border=5);
        hboxInteger1.Add((5,-1));
        boxsizerInteger.Add(hboxInteger1,border=5);

        hboxInteger2 = wx.BoxSizer(wx.HORIZONTAL);

        txt1 = wx.StaticText(self.panel, label='n:\t\t');
        hboxInteger2.Add(txt1, flag=wx.ALIGN_CENTER, border=5);
        self.integerN = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS,min=0,max=20,initial=self.rangeValues[4]);
        hboxInteger2.Add(self.integerN, flag=wx.ALIGN_CENTER,border=5);
        hboxInteger2.Add((5,-1));
        boxsizerInteger.Add(hboxInteger2,flag=wx.EXPAND,border=5);

        hboxMain.Add(boxsizerInteger);
        hboxMain.Add((5,-1));
        self.sizer.Add(hboxMain,pos=(5,1),span=(2,6),flag=wx.ALIGN_CENTER|wx.CENTER,border=5);


        self.checkbox8 = wx.CheckBox(self.panel, label='Display phase advance resonance lines');

        self.sizer.Add(self.checkbox8,pos=(7,1),span=(1,4),flag=wx.LEFT|wx.ALIGN_LEFT);

        ntxt = wx.StaticText(self.panel, label='N (# units):');
        self.nlist = wx.SpinCtrl(self.panel,size=((50,-1)),style=wx.SP_ARROW_KEYS, min=0, max=20, initial=1);
        self.sizer.Add(ntxt,pos=(8,1),span=(1,1),flag=wx.ALIGN_CENTER);
        self.sizer.Add(self.nlist,pos=(8,2),span=(1,1),flag=wx.ALIGN_CENTER);
        self.nlist.Disable();

        if self.checkboxValues[7]:
            self.checkbox8.Set3StateValue(wx.CHK_CHECKED);
            self.nlist.SetValue(self.tune.getN());
            self.updateUnitTune(-1);
            self.updateUnitN(-1);

        # Add last 2 buttons
        self.btn1 = wx.Button(self.panel, label='Ok', size=(100, 30));
        self.sizer.Add(self.btn1,pos=(8,5),flag=wx.ALIGN_CENTER|wx.CENTER, border=5);

        #self.btn2 = wx.Button(self.panel, label='Cancel', size=(100,30));
        #self.sizer.Add(self.btn2,pos=(8,5),flag=wx.ALIGN_CENTER|wx.CENTER,border=5);

        # binding events
        self.btn1.Bind(wx.EVT_BUTTON, self.update);
        #self.btn2.Bind(wx.EVT_BUTTON, self.onClose);
        self.list1.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.list2.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.list3.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.list4.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.nlist.Bind(wx.EVT_SPINCTRL, self.updateUnitN);
        self.integerM.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.integerN.Bind(wx.EVT_SPINCTRL, self.updateAxis);
        self.checkbox1.Bind(wx.EVT_CHECKBOX, self.updateLines);
        self.checkbox2.Bind(wx.EVT_CHECKBOX, self.updateLines);
        self.checkbox3.Bind(wx.EVT_CHECKBOX, self.updateLines);
        self.checkbox4.Bind(wx.EVT_CHECKBOX, self.updateLines);
        self.checkbox5.Bind(wx.EVT_CHECKBOX, self.updateColor5);
        self.checkbox6.Bind(wx.EVT_CHECKBOX, self.updateColor6);
        self.checkbox7.Bind(wx.EVT_CHECKBOX, self.updateColor7);
        self.checkbox8.Bind(wx.EVT_CHECKBOX, self.updateUnitTune);
        self.orderbox1.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox2.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox3.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox4.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox5.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox6.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox7.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox8.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox9.Bind(wx.EVT_CHECKBOX, self.updateOrder);
        self.orderbox10.Bind(wx.EVT_CHECKBOX, self.updateOrder);


    # executes when user hits 'ok' button
    def update(self, e):
        # update settings
        self.parent.update(e);
        self.updateliveSettings(e);

        #close page
        self.onClose(e);

    def updateOrder(self,e):
        checkboxObjects = [self.orderbox1,self.orderbox2,self.orderbox3,self.orderbox4,self.orderbox5,self.orderbox6,self.orderbox7,self.orderbox8,self.orderbox9,self.orderbox10];
        for i in range(0,10,1):
            if checkboxObjects[i].IsChecked():
                self.orderboxValues[i] = True;
            else:
                self.orderboxValues[i] = False;
        self.parent.setOrderbox(self.orderboxValues);
        self.tune.newOrder(self.orderboxValues);
        #self.parent.update(e);

    def updateliveSettings(self, e):
        self.parent.setPV(self.horTuneName.GetValue(),self.verTuneName.GetValue(),self.rfFreqName.GetValue(),self.harNumName.GetValue());

    # update axis range
    def updateAxis(self, e):
        m1 = self.list1.GetValue();
        self.list1.SetValue(m1);
        m2 = self.list2.GetValue();
        self.list2.SetValue(m2);
        n1 = self.list3.GetValue();
        self.list3.SetValue(n1);
        n2 = self.list4.GetValue();
        self.list4.SetValue(n2);
        integerM = self.integerM.GetValue();
        self.integerM.SetValue(integerM);
        integerN = self.integerN.GetValue();
        self.integerN.SetValue(integerN);
        self.tune.newAxis(m1,m2,n1,n2);
        self.rangeValues = [m1, m2, n1, n2, integerN, integerM];
        self.parent.setRange(self.rangeValues);

    def updateUnitTune(self, e):
        # if unit tune is checked, disable all color options
        if self.checkbox8.IsChecked():
            self.checkbox5.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkbox6.Set3StateValue(wx.CHK_CHECKED);
            self.checkbox7.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkbox5.Disable();
            self.checkbox6.Disable();
            self.checkbox7.Disable();
            self.tune.newUnitTune(True);
            self.checkboxValues[7] = True;
            self.nlist.Enable();
        else:
            self.checkbox5.Enable();
            self.checkbox6.Enable();
            self.checkbox7.Enable();
            self.tune.newUnitTune(False);
            self.checkboxValues[7] = False;
            self.nlist.Disable();
        # update gui and tune diagram
        self.checkboxValues[5] = True;
        self.checkboxValues[4] = False;
        self.checkboxValues[6] = False;
        self.parent.setCheckbox(self.checkboxValues);
        self.tune.newColor([self.checkboxValues[4],self.checkboxValues[5],self.checkboxValues[6]]);

    def updateUnitN(self, e):
        mlsX = 0.18;
        mlsY = 0.22;
        bessyX = 0.85;
        bessyY = 0.75;
        self.tune.newWorkingpoint(self.integerN.GetValue() + mlsX, self.integerM.GetValue() + mlsY);
        self.tune.newUnitTune(True,self.nlist.GetValue());

    # update the selections for color scheme
    # first two lines deselect other 2 checkboxes
    # next 3 lines update the checkbox array
    # final line sends updated array back to main gui
    def updateColor5(self, e):
        if self.checkbox5.IsChecked():
            self.checkbox6.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkbox7.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkboxValues[4] = True;
            self.checkboxValues[5] = False;
            self.checkboxValues[6] = False;
            self.parent.setCheckbox(self.checkboxValues);
            self.tune.newColor([self.checkboxValues[4],self.checkboxValues[5],self.checkboxValues[6]]);
    def updateColor6(self, e):
        if self.checkbox6.IsChecked():
            self.checkbox5.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkbox7.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkboxValues[5] = True;
            self.checkboxValues[4] = False;
            self.checkboxValues[6] = False;
            self.parent.setCheckbox(self.checkboxValues);
            self.tune.newColor([self.checkboxValues[4],self.checkboxValues[5],self.checkboxValues[6]]);
    def updateColor7(self, e):
        if self.checkbox7.IsChecked():
            self.checkbox5.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkbox6.Set3StateValue(wx.CHK_UNCHECKED);
            self.checkboxValues[6] = True;
            self.checkboxValues[4] = False;
            self.checkboxValues[5] = False;
            self.parent.setCheckbox(self.checkboxValues);
            self.tune.newColor([self.checkboxValues[4],self.checkboxValues[5],self.checkboxValues[6]]);

    # update lines in graph
    def updateLines(self, e):
        checklist = [self.checkbox1, self.checkbox2, self.checkbox3, self.checkbox4];
        # check settings page to see what has been checked on/off and update checkbox
        for i in range(0,4):
            if checklist[i].IsChecked():
                self.checkboxValues[i] = True;
            else:
                self.checkboxValues[i] = False;
        # send new settings of checkbox back to main gui to stay updated
        self.parent.setCheckbox(self.checkboxValues);
        # apply new checkbox settings to tune diagram
        self.tune.newLines([self.checkboxValues[0],self.checkboxValues[1],self.checkboxValues[2],self.checkboxValues[3]]);

    # destroy frame when exiting
    def onClose(self, e):
        self.frame.Destroy();
