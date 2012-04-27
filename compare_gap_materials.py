# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

import numpy as np

# <codecell>

materials = ['mylar','carbonfiber','tyvek','air']
#12 micron mylar vs 200 micron carbon fiber and 200 micron tyvek

# <codecell>

fwhms = {}
for mat in materials:
    fwhms[mat]=np.load('fwhm_%s.npy'%mat)

# <codecell>

figure(figsize(12,6))
x = range(0,90,5)
lbl= {k:k for k in materials}
lbl['mylar'] = 'mylar 12um'
lbl['tyvek'] = 'tyvek 100um'
lbl['carbonfiber'] = 'carbonfiber 100um'
lbl['air'] = 'air 0.03um'
for mat in materials:
    plot(x,fwhms[mat],'o-',label=lbl[mat])
ylim(0.5,3.0)
xlabel('Angle(deg)')
ylabel('FWHM/2.35(MeV)')
legend(loc=2)
grid(True)
title(r' Energy FWHM/2.35 from Fit to Crystalball Convoluted with Gausian for each Wrapping Material');
savefig('wrapping_mat_comparison.pdf',bbox_inches='tight')

# <codecell>


