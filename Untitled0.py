# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from numpy.fft import irfft,rfft,fft,ifft,fftshift
from math import exp,sqrt,pi
import numpy as np

# <codecell>

x = linspace(-5,5,2000)

# <codecell>

def gg(x):
    return exp(-x**2/2)*1/sqrt(2*pi)
f = np.zeros(len(x))
vg = vectorize(gg)
f = vg(2*x+1)
g = vg(x)
F = fft(f)
G = fft(g)
plot(x[200:-200],G[200:-200])
plot(x[200:-200],F[200:-200])

# <codecell>

z = ifft(F*G)
fftshift(z)

# <codecell>

plot(x,z)#,'b',x,c,'r')

# <codecell>

k = np.convolve(f,g,'same')
#k=fftshift(k)
plot(x,f,x,g)

# <codecell>

c=np.exp(-(x+1)*(x+1))/sqrt(16*pi)
c=np.exp(-1./10*(2*x+1)*(2*x+1))/sqrt(10*pi)
plot(x,k/200,'r',x,c,'b')
print len(x), len(k[0:2000])
grid(True)

# <codecell>

?plot

# <codecell>


