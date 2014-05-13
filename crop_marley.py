
import cPickle
import numpy as np
from astropy import units as u

infile = open('SpeX_marley.pkl','rb')
model = cPickle.load(infile)
infile.close()


low_grav = np.where(model['logg']<4.45)[0]
while len(low_grav)>0:
    i = low_grav[0]
    print i
    model['logg'] = np.delete(model['logg'],i)
    model['teff'] = np.delete(model['teff'],i)
    model['fsed'] = np.delete(model['fsed'],i)
    model['fsyn'] = np.delete(model['fsyn'],i,0)
    low_grav = np.where(model['logg']<4.45)[0]

out_2 = open('SpeX_marley_nolowg.pkl','wb')
cPickle.dump(model,out_2)
out_2.close()

