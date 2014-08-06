
import matplotlib.pyplot as plt # for plotting purposes
import numpy as np # for array operations
import time

class tuneDiagram:

    #working point
    circle=0;
    radius = 0;
    qX = 0;
    qY = 0;
    N = 1;
    firstDraw=True; # this is used for efficiency

    # integers
    order = [False,False,False,False,False,False,False,False,False,False];
    m1 = 2;
    n1 = 3;
    m2 = 3;
    n2 = 4;
    p = 0;

    # window
    qxmin = 0;
    qxmax = 0;
    qymin = 0;
    qymax = 0;
    fig = 0;

    #settings page stuff
    lines = [True,True,True,True]; #[hor lines, ver lines, sum, diff], 1 = true, 0 = false
    color = [False, False, True]; # [random, black, order]
    unitTune = False;

    # line color
    # The way this works is as follows. TuneDiagram will plot according to the currentColor and currentOrder. Through the
    # settings page, one can change these settings. e.g. change color settings to random. currentColor = colorRandom and
    # currentOrder = randomOrder.
    currentColor=0;
    currentOrder=0;
    colorRandom=['#000080','#008000','#FF0000','#800080','#FFFF00','#FF9900','#000000','#75BBBB','#FF00FF','#00FF00'];
    colorBlack=['#000000']*10;
    randomOrder=np.random.randint(7,size=1000);
    fixedOrder=[0,1,2,3,4,5,6,7,8,9]; # used for displaying order #s by color. e.g. order 1 lines = blue, order 2 lines = red etc

    def __init__(self, order, qx, qy, radius, p=50, qxmin=-20, qxmax=20, qymin=-20, qymax=20):
        # update settings page to reflect current order
        for i in range(0,order,1):
            self.order[i] = True;
        self.qX = qx; self.qY = qy;
        self.radius = radius;
        self.p = p;
        self.qxmin = qxmin; self.qxmax = qxmax;
        self.qymin = qymin; self.qymax = qymax;
        self.findColor(); # set default color settings (by order)

    def plot(self):

        # creating figure
        plt.figure(self.fig);
        plt.cla();
        self.axisSize();
        plt.axis([self.n1-0.1,self.n2+0.1,self.m1-0.1,self.m2+0.1]);
        #plt.title('Tune Resonance Program v3.0');
        plt.xlabel('Qx'); plt.ylabel('Qy');

        # add working point
        self.addWorkingPoint();

        self.plotMain();

        if self.unitTune:
            self.plotUnit();

    def plotMain(self):

        # Integer value array
        p = np.linspace(0,self.p,self.p + 1);

        # Easier to define variables for window
        qxmin = self.qxmin; qxmax = self.qxmax;
        qymin = self.qymin; qymax = self.qymax;
        k = 0;
        # Plotting formula
        for l in range(len(self.order)-1,-1,-1):
            if self.order[l]:
                i = l+1;
            else:
                i = 0;
            m = np.linspace(-i,i,2*i+1);
            n1 = (i - np.abs(m));
            n2 = -(i-np.abs(m));
            for j in range(0,m.size,1):
                # check to see equation is divided by 0 or not
                # ver & hor res lines
                if ((n1[j] == 0 and self.lines[1]) or (m[j] == 0 and self.lines[0])) and i != 0 :
                    # vertical lines
                    if n1[j] == 0 and self.lines[1]:
                        plt.vlines(p/m[j],qxmin,qxmax,colors=self.currentColor[self.currentOrder[k]]);
                    # horizontal lines
                    if m[j] == 0 and self.lines[0]:
                        plt.hlines(p/n1[j],qymin,qymax,colors=self.currentColor[self.currentOrder[k]]);
                        plt.hlines(p/n2[j],qymin,qymax,colors=self.currentColor[self.currentOrder[k]]);
                # sum and dif res lines
                elif not(n1[j] == 0) and not(m[j] == 0):
                    # resonance sum lines
                    if self.lines[2]:
                        if np.sign(m[j]) > 0:
                            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n2[j] - np.array(m[j]*qxmin/n2[j]), p/n2[j] - np.array(m[j]*qxmax/n2[j])],color=self.currentColor[self.currentOrder[k]]);
                        else:
                            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n1[j] - np.array(m[j]*qxmin/n1[j]), p/n1[j] - np.array(m[j]*qxmax/n1[j])],color=self.currentColor[self.currentOrder[k]]);
                    # resonance dif lines
                    if self.lines[3]:
                        if np.sign(m[j]) > 0:
                            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n1[j] - np.array(m[j]*qxmin/n1[j]), p/n1[j] - np.array(m[j]*qxmax/n1[j])],color=self.currentColor[self.currentOrder[k]]);
                        else:
                            plt.plot([[qxmin]*p.size,[qxmax]*p.size],[p/n2[j] - np.array(m[j]*qxmin/n2[j]), p/n2[j] - np.array(m[j]*qxmax/n2[j])],color=self.currentColor[self.currentOrder[k]]);
                # update color settings
                if self.color[2] == False:
                    k+=1;
            if self.color[2] == True:
                k+=1;

    def plotUnit(self):

        # Add relative working point
        self.plotUnitCircle();
        print(self.qX, self.qY)
        # Easier to define variables for window
        qxmin = np.floor(self.qX / self.N); qxmax = qxmin+1;
        qymin = np.floor(self.qY / self.N); qymax = qymin+1;
        # Plotting formula
        for l in range(len(self.order)-1,-1,-1):
            if self.order[l]:
                i = l+1;
            else:
                i = 0;
            m = np.linspace(-i,i,2*i+1);
            n1 = (i - np.abs(m));
            n2 = -(i-np.abs(m));
            for j in range(0,m.size,1):
                # check to see equation is divided by 0 or not
                # ver & hor res lines
                if ((n1[j] == 0 and self.lines[1]) or (m[j] == 0 and self.lines[0])) and i != 0:
                    # vertical lines
                    if n1[j] == 0 and self.lines[1]:
                        plt.vlines((self.N/m[j]),0,20,colors='r');
                    # horizontal lines
                    if m[j] == 0 and self.lines[0]:
                        plt.hlines((self.N/n1[j]),0,20,colors='r');
                        plt.hlines((self.N/n2[j]),0,20,colors='r');
                # sum and dif res lines
                elif not(n1[j] == 0) and not(m[j] == 0):
                    # resonance sum lines
                    for p in range(0,5,1):
                        if self.lines[2]:
                            if np.sign(m[j]) > 0 and ((p/n2[j] - np.array(m[j]*qxmax/n2[j]) >= qymin) or (p/n2[j] - np.array(m[j]*qxmin/n2[j]) >= qymin)) \
                                    and ((p/n2[j] - np.array(m[j]*qxmax/n2[j]) <= qymax) or (p/n2[j] - np.array(m[j]*qxmin/n2[j]) <= qymax)):
                                plt.plot([[qxmin*self.N],[qxmax*self.N]],[(p/n2[j] - np.array(m[j]*qxmin/n2[j]))*self.N, (p/n2[j] - np.array(m[j]*qxmax/n2[j]))*self.N],color='r');
                            elif ((p/n1[j] - np.array(m[j]*qxmax/n1[j]) >= qymin) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) >= qymin)) \
                                    and ((p/n1[j] - np.array(m[j]*qxmax/n1[j]) <= qymax) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) <=qymax)):
                                plt.plot([[qxmin*self.N],[qxmax*self.N]],[(p/n1[j] - np.array(m[j]*qxmin/n1[j]))*self.N, (p/n1[j] - np.array(m[j]*qxmax/n1[j]))*self.N],color='r');
                    # resonance dif lines
                        if self.lines[3]:
                            if np.sign(m[j]) > 0 and ((p/n1[j] - np.array(m[j]*qxmax/n1[j]) >= qymin) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) >= qymin)) \
                                    and ((p/n1[j] - np.array(m[j]*qxmax/n1[j]) <= qymax) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) <= qymax)):
                                plt.plot([[qxmin*self.N],[qxmax*self.N]],[(p/n1[j] - np.array(m[j]*qxmin/n1[j]))*self.N, (p/n1[j] - np.array(m[j]*qxmax/n1[j]))*self.N],color='r');
                            elif ((p/n2[j] - np.array(m[j]*qxmax/n2[j]) >= qymin) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) >= qymin)) \
                                    and ((p/n2[j] - np.array(m[j]*qxmax/n2[j]) <= qymax) or (p/n1[j] - np.array(m[j]*qxmin/n1[j]) <= qymax)):
                                plt.plot([[qxmin*self.N],[qxmax*self.N]],[(p/n2[j] - np.array(m[j]*qxmin/n2[j]))*self.N, (p/n2[j] - np.array(m[j]*qxmax/n2[j]))*self.N],color='r');

    def plotUnitCircle(self):
        qX2 = np.floor(self.qX) + self.qX/self.N - np.floor(self.qX/self.N);
        qY2 = np.floor(self.qY) + self.qY/self.N - np.floor(self.qY/self.N);
        circle1=plt.Circle((qX2,qY2),self.radius,color='r',fill=True);
        plt.gca().add_artist(circle1);

    def getfig(self):
        self.plot();
        plt.figure(self.fig);
        return plt.gcf();

    def getorder(self):
        return self.order;

    def getN(self):
        return self.N;

    def axisSize(self):
        ax = plt.axes(xlim=(self.qxmin, self.qxmax), ylim=(self.qymin, self.qymax));
        return ax;

    # sets current color & color order based on the 'color' array
    def findColor(self):
        if self.color[0]:
            self.currentColor = self.colorRandom;
            self.currentOrder = self.randomOrder;
        elif self.color[1]:
            self.currentColor = self.colorBlack;
            self.currentOrder = self.randomOrder;
        else: # color by order
            self.currentColor = self.colorRandom;
            self.currentOrder = self.fixedOrder;

    def addWorkingPoint(self):
        plt.figure(self.fig);
        if self.firstDraw:
            self.circle=plt.Circle((self.qX,self.qY),self.radius,color='k',fill=True);
            self.firstDraw = False;
        self.circle.center = self.qX,self.qY;
        plt.gca().add_artist(self.circle);

    def liveUpdate(self):
        #plt.axis([self.n1-0.1,self.n2+0.1,self.m1-0.1,self.m2+0.1]);
        self.addWorkingPoint();

    def newOrder(self,order):
        self.order = order;

    def newWorkingpoint(self,x,y,n=1):
        self.qX = x;
        self.qY = y;
        self.N = n;
        # set axis to automatically change so working point is always in view. WARNING: this will disable the matplotlib toolbar buttons
        #self.newAxis(np.floor(y),np.ceil(y),np.floor(x),np.ceil(x));

    def newAxis(self, m1, m2, n1, n2):
        self.m1 = m1;
        self.m2 = m2;
        self.n1 = n1;
        self.n2 = n2;

    def newLines(self,lines):
        self.lines = lines;

    def newColor(self,color):
        self.color = color;
        self.randomOrder = np.random.randint(7,size=1000);
        self.findColor();

    def newUnitTune(self,unitTune, n = 1):
        self.unitTune = unitTune;
        self.N = n;

    def show(self):
        plt.figure(self.fig);
        plt.show();

    def draw(self):
        plt.figure(self.fig);
        plt.draw();

    def on(self):
        plt.figure(self.fig);
        plt.ion();

    def close(self):
        plt.close();
