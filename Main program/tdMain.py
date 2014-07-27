#!/usr/bin/env python
#
# Levon Dovlatyan
# Markus Ries und Paul Goslawski
# BESSY, Berlin
# 17 July 2014
#
###############################
from tdGUI import tdGUI
from tuneDiagram import tuneDiagram

tune = tuneDiagram(3,17.85,6.75,.005);
guiMain = tdGUI(tune);

# Create a tuneDiagram object to plot everything and then create a tdGUI object to launch user interface.


