import logging

import cPickle
import numpy as np
from astropy import units as u

import bdmcmc.bdfit, bdmcmc.spectra, bdmcmc.get_mod

logging.basicConfig(level=logging.DEBUG)

bd = bdmcmc.spectra.BrownDwarf('U20165')
bd.get_low()

infile = open('spex_marley_backup.pkl','rb')
model = cPickle.load(infile)
infile.close()
model['wsyn'] = bd.specs['low']['wavelength']
wav_sq = model['wsyn']**2

inc = 10
start = 60

for i in range(start):
    model['fsyn'][i] = model['fsyn'][i]*3e7/wav_sq

for j in range(2,12):
    logging.debug('{} {}'.format(j,start))
    logging.debug("marley_ldwarfs{}.pkl".format(j))
    subfile = open("marley_ldwarfs{}.pkl".format(j),'rb')
    sub_grid = cPickle.load(subfile)
    subfile.close()
    logging.debug(len(sub_grid))
    logging.debug(sub_grid['teff'])
    for i in range(len(sub_grid['teff'])):
        if ((model['logg'][start+i]!=sub_grid['logg'][i]) or
            (model['teff'][start+i]!=sub_grid['teff'][i]) or
            (model['fsed'][start+i]!=sub_grid['fsed'][i])):
            logging.debug('OH NO {} {} {} {} {} {} {}'.format(i,
                model['logg'][start+i],sub_grid['logg'][i],
                model['teff'][start+i],sub_grid['teff'][i],
                model['fsed'][start+i],sub_grid['fsed'][i]))
        else:
            model['fsyn'][start+i] = sub_grid['fsyn'][i]*3e7/wav_sq
    start += inc

grav = model['logg']
bad = np.where(abs(grav-178)<1)[0]
print bad
for b in bad:
    print model['fsyn'][b]
model['logg'] = np.delete(model['logg'],bad)
model['teff'] = np.delete(model['teff'],bad)
model['fsed'] = np.delete(model['fsed'],bad)
model['fsyn'] = np.delete(model['fsyn'],bad,0)
funits = u.W / u.um / u.m / u.m 
model['fsyn'] = model['fsyn']*funits
print len(model['fsyn'])

grav = model['logg']
model['logg'][abs(grav-100)<1] = 4.0
#grav[abs(grav-178)<1] = 4.25
model['logg'][abs(grav-300)<1] = 4.5
model['logg'][abs(grav-1000)<1] = 5.0
model['logg'][abs(grav-3000)<1] = 5.5


outfile = open('SpeX_marley.pkl','wb')
cPickle.dump(model,outfile)
outfile.close()
