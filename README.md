TuneResonancePython
===================

A Tune Resonance Program developed in python that can be used when working with non linear beam dynamics

----------------Current Version----------------------- <BR>

td v3.1.5 <BR>
        - added mirror tune option in settings <BR>
        - added a display of the current tune at the bottom of the page <BR>
        
td v3.1 <BR>
        - Program now shuts down follow when exited <BR>
        - Program defaults have been set the MLS values <BR>
        - Matplotlib Nav toolbar now works during live mode <BR>
        - Phase advance lines now work properly <BR>
        - added a field to get integer part <BR>

td v3.0 <BR>
        - Live mode now works perfectly 
        
td v2.5 <BR>
        - Live mode works, but instantly crashes within few seconds. The problems stems from the fact that a threading process is trying to  update the main GUI causing a fatal graphical error. GUI can only be updated within main GUI loop.  
        
td v2.0 <BR>
        - Added live mode, however the entire GUI becomes unresponsive and essentially useless. 
        
td v1.5 <BR>
        - From the advice of Andreas, switched the GUI python package from tkinter to wxpython. Added a settings page separate from main GUI 
        
td v1.0 <BR>
        - Added a few buttons to tkinter interface. Finished main tuneDiagram program to display tunes
        
----------------Default Settings---------------------- <BR>

The current default settings in the program are that of the MLS. If you would like to change the default settings to match that of another machine there are only a few variables that need to be changed.

TuneDiagram Class <BR>

Lines 18-21, variables m1,n1,m2,n2 define the axes range to display.

tdGUI Class <BR>

Line 43, variable SettingspageRange define the axes range and the integer parts of the working point <BR>
Line 50, variable pvNames defines the EPICS variable names used to grab non integer working point <BR>

Changing these will change the default startup option for the program.


----------------INFO---------------------------------- <BR>

This program is used to simulate tune resonances used in nonlinear beam dynamics. The program goes up to 10th order diagrams, but can easily be modified to go higher. A settings page provide lots of customizability for the user. There is also a 'live mode' that can connect with EPICS to get live updates of working points (x,y) and plot accordingly.

'Main Program contains the full program. 'scripts not used' is a folder containing some ideas that were not implemented.

Prerequesites needed to run Python 2.6 or higher (Has only been tested on Python 2.7+) The following python packages: 'matplotlib', 'wxpython', 'numpy', and 'pyepics'

Run/Compile 'tdMain.py' to launch the program. 'tdGUI.py' is the main GUI file for the program. 'tdGUISettings.py' contains the GUI for the settings page. 'tuneDiagram.py' is the class that does all the plotting/calculations for the program

Code comments in files should be enough to explain how everything works and how I implemented certain algorithms.

If there are any questions, feel free to ask, Levon Dovlatyan E-Mail: levondov@berkeley.edu
