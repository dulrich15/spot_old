
from __future__ import division

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

# matplotlib.rcParams['xtick.direction'] = 'out'
# matplotlib.rcParams['ytick.direction'] = 'out'

    xmax = 2.0
    xmin = -xmax
    NX = 20
    ymax = 2.0
    ymin = -ymax
    NY = 20

    x = np.linspace(xmin, xmax, NX)
    y = np.linspace(ymin, ymax, NY)
    X, Y = np.meshgrid(x, y)

    S2 = X**2 + Y**2  # This is the radius squared
    Bx = -Y/S2
    By = +X/S2
    B2 = Bx**2 + By**2  # This is the mag field squared

    plt.figure()

    co = B2/B2.max()
    lw = 2
    # plt.streamplot(X, Y, Bx, By, color=co, linewidth=lw, cmap=plt.cm.binary)
    # plt.colorbar()

plt.savefig('temp.png')
