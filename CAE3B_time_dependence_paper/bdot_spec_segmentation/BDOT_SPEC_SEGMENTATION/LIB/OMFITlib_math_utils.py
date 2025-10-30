# -*-Python-*-
# Created by ncrocker at 25 Nov 2023  03:01
import numpy as np


def peaks(nx=11, ny=11, npeaks=1, cents=None, widths=None, heights=None, aspects=None, angles=None, return_parameters=False):
    rndgen = np.random.default_rng()
    if cents is None:
        cents = list(zip(nx * (rndgen.random(npeaks) - 0.5) * 0.75, ny * (rndgen.random(npeaks) - 0.5) * 0.75))
    if widths is None:
        widths = (rndgen.random(npeaks) + 0.5) * np.minimum(nx, ny) / 5 / npeaks
    if heights is None:
        heights = (rndgen.random(npeaks) + 0.25) / 1.25
    if aspects is None:
        aspects = rndgen.random(npeaks) + 1.5
    if angles is None:
        angles = (rndgen.random(npeaks) - 0.5) * np.pi / 2

    X, Y = np.meshgrid(np.arange(nx) - (nx - 1) / 2, np.arange(ny) - (ny - 1) / 2, sparse=True, indexing='xy')
    pks = np.zeros((nx, ny))
    for c, w, h, asp, ang in zip(cents, widths, heights, aspects, angles):
        Xp, Yp = np.cos(ang) * X + np.sin(ang) * Y, -np.sin(ang) * X + np.cos(ang) * Y
        pks += np.exp(-(((Xp - c[0]) / sqrt(asp)) ** 2 + ((Yp - c[1]) * sqrt(asp)) ** 2) / w**2)
    ret = (pks, X, Y)
    if return_parameters:
        ret = ret + (dict(nx=nx, ny=ny, npeaks=npeaks, cents=cents, widths=widths, heights=heights, aspects=aspects, angles=angles),)
    return ret


def HighestDensityInterval(x, a=0.6827):
    xs = np.sort(np.asarray(x).flatten())
    a = np.amin([np.amax([a, 0]), 1])
    nxs = len(xs)
    nHDI = np.amax([1, np.rint(nxs * a).astype(int)])
    print(nHDI, nxs)
    iHDI = np.argmin(xs[nHDI:] - xs[0:-nHDI])
    return (xs[iHDI], xs[iHDI + nHDI - 1]), (iHDI, iHDI + nHDI - 1, xs)


def safe_divide(a, b):
    a, b = np.broadcast_arrays(a, b)
    return np.divide(a, b, out=np.zeros(b.shape, dtype=np.result_type(a, b, 1.0)), where=b != 0)
