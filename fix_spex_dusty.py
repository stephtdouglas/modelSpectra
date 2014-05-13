
import cPickle
import numpy as np
from astropy import units as u

import bdmcmc.bdfit, bdmcmc.spectra, bdmcmc.get_mod


bd = bdmcmc.spectra.BrownDwarf('U20165')
bd.get_low()

infile = open('SpeX_dusty_old.pkl','rb')
model = cPickle.load(infile)
infile.close()
model['wsyn'] = bd.specs['low']['wavelength']

out_1 = open('SpeX_dusty.pkl','wb')
cPickle.dump(model,out_1)
out_1.close()

high_grav = np.where(model['logg']>5.55)[0]
while len(high_grav)>0:
    i = high_grav[0]
    model['logg'] = np.delete(model['logg'],i)
    model['teff'] = np.delete(model['teff'],i)
    model['fsyn'] = np.delete(model['fsyn'],i,0)
    high_grav = np.where(model['logg']>5.55)[0]

out_2 = open('SpeX_dusty_cut.pkl','wb')
cPickle.dump(model,out_2)
out_2.close()
