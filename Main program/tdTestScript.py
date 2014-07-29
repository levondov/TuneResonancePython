import epics
from epics import caget, caput
from epics import PV
import time
import numpy as np

# small test script which can be used to see how the program works.
# generates default values from the MLS and applies a 5% noise to them


# Can change these to whatever your epics variables are called
pv1 = PV('TUNEZRP:measX');
pv2 = PV('TUNEZRP:measY');
pv3 = PV('MCLKHGP:rdFrq');

refFreq = 500e6;
horFreq = 1.115e6;
verFreq = 1.45e6;

pv1.put(horFreq);
pv2.put(verFreq);
pv3.put(refFreq);

def noise():
    while True:
        noiseX = (2*np.random.rand()-1)*0.05*horFreq;
        noiseY = (2*np.random.rand()-1)*0.05*verFreq;
        noiseRF =(2*np.random.rand()-1)*0.0005*refFreq;

        pv1.put(pv1.get() + noiseX);
        pv2.put(pv2.get() + noiseY);
        pv3.put(pv3.get() + noiseRF);

        print 'Hor tune = {0}, and Ver tune =  {1}, and RF = {2}'.format(pv1.get()/refFreq,pv2.get()/refFreq,pv3.get());
        time.sleep(0.05)

noise();