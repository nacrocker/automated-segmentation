#-*-Python-*-
# Created by ncrocker at 25 Nov 2023  04:56

import matplotlib.pyplot as plt
import numpy as np

def cmapIDL_Standard_Gamma_II():
    # Colormap definition for "Standard Gamma-II" colormap from IDL
    import matplotlib
    from matplotlib import cm
    import numpy as np

    _r = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   4, 9, 14, 19, 23, 28, 33, 38, 42, 47, 52, 57, 61, 66, 71, 76,
                   81, 81, 81, 81, 81, 81, 81, 81, 80, 80, 80, 80, 80, 80, 80, 79,
                   84, 89, 94, 99, 104, 109, 114, 119, 124, 129, 134, 139, 144, 149, 154, 159,
                   164, 169, 174, 180, 185, 190, 196, 201, 206, 212, 217, 222, 228, 233, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 248, 240, 232, 225, 217, 209, 202, 194, 186, 179, 171, 163, 168,
                   173, 178, 183, 188, 193, 198, 203, 209, 214, 219, 224, 229, 234, 239, 244, 249,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
    _g = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 5, 10, 16, 21, 27, 32, 37, 43, 48, 54, 59, 64, 70, 75,
                   81, 85, 90, 95, 100, 105, 109, 114, 119, 124, 129, 134, 138, 143, 148, 153,
                   158, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163,
                   163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163, 163,
                   163, 169, 175, 181, 187, 193, 199, 205, 212, 218, 224, 230, 236, 242, 248, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
    _b = np.array([0, 5, 10, 15, 20, 26, 31, 36, 41, 46, 52, 57, 62, 67, 72, 78,
                   83, 88, 93, 98, 104, 109, 114, 119, 124, 130, 135, 140, 145, 150, 156, 161,
                   166, 171, 176, 182, 187, 192, 197, 202, 208, 213, 218, 223, 228, 234, 239, 244,
                   249, 255, 250, 245, 239, 234, 228, 223, 218, 212, 207, 201, 196, 190, 185, 180,
                   174, 169, 163, 158, 152, 147, 142, 136, 131, 125, 120, 114, 109, 104, 98, 93,
                   87, 82, 76, 71, 66, 60, 55, 49, 44, 38, 33, 28, 22, 17, 11, 6,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 4, 9, 14, 19, 24, 28, 33, 38, 43, 48, 53, 57, 62, 67, 72,
                   77, 82, 77, 71, 65, 59, 53, 47, 41, 36, 30, 24, 18, 12, 6, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 3, 6, 9, 12, 16, 19, 22, 25, 29, 32, 35, 38, 41, 45, 48,
                   51, 54, 58, 61, 64, 67, 71, 74, 77, 80, 83, 87, 90, 93, 96, 100,
                   103, 106, 109, 112, 116, 119, 122, 125, 129, 132, 135, 138, 142, 145, 148, 151,
                   154, 158, 161, 164, 167, 171, 174, 177, 180, 183, 187, 190, 193, 196, 200, 203,
                   206, 209, 213, 216, 219, 222, 225, 229, 232, 235, 238, 242, 245, 248, 251, 255])
    _rgb = np.column_stack((_r, _g, _b)) / 255.0
    cmstd=matplotlib.colors.ListedColormap(_rgb, name='Standard_Gamma_II')
    #cm.register_cmap(name='Standard_Gamma_II',cmap=cmstd)
    setattr(cm,'Standard_Gamma_II',cmstd)

    if not hasattr(cmstd,'_reversed_orig'):
        cmstd._reversed_orig = cmstd.reversed
    def cmstd_reversed(self,name=None):
        if name is None:
            name='Standard_Gamma_II_r'
        cmstd_rvsrd = cmstd._reversed_orig(name=name)
        setattr(cm,name,cmstd_rvsrd)
        return cmstd_rvsrd
    cmstd.reversed = cmstd_reversed.__get__(cmstd)

    return cmstd
#    return matplotlib.colors.ListedColormap(_rgb, name='hot')# name='Standard Gamma-II')

def imshowxy(x,y,img,xlabel=None,ylabel=None,title=None,ax=plt,cbkwargs=None,**kwargs):
    #extent=(np.min(x.ravel()),np.max(x.ravel()),np.min(y.ravel()),np.max(y.ravel()))
    #bnds=lambda coord: polyval(polyfit([0,len(coord)-1],[m(coord) for m in [np.min,np.max]],1),[-0.5,len(coord)-0.5])
    bnds = lambda coord: (lambda dcoord: [-dcoord/2+coord[0],+dcoord/2+coord[-1]])((coord[-1]-coord[0])/(len(coord)-1))
    extent=(*bnds(x),*bnds(y))
    im=ax.imshow(img,aspect='auto',origin='lower',extent=extent,**kwargs)
    if xlabel: plt.ylabel(ylabel)
    if ylabel: plt.xlabel(xlabel)
    if title: plt.title(title)
    if cbkwargs is None: cbkwargs = dict()
    cb=plt.colorbar(**cbkwargs)
    return im,cb

def specim(time,freq,spec,ax=plt,interpolation='none',cbkwargs=None,**kwargs):
    #im=ax.imshow(spec,aspect='auto',origin='lower',extent=(time[0],time[-1],freq[0],freq[-1]),**kwargs)
    #plt.ylabel('freq')
    #plt.xlabel('time')
    #cb=plt.colorbar()
    kwargs.setdefault('xlabel','time')
    kwargs.setdefault('ylabel','freq')
    im,cb=imshowxy(time,freq,spec,ax=ax,interpolation=interpolation,cbkwargs=cbkwargs,**kwargs)
    return im,cb


class subplot_adder:
    """allows dynamically increasing nubmer of subplots:
    fig=figure(layout='constrained')
    sbadder=subplot_adder(fig=fig,horizontal=False)
    for i in range(1,4):
        ax=sbadder.add_new_subplot()"""

    import matplotlib
    def __init__(self,fig=None,axs=None,horizontal=False):
        if not figure is None:
            if isinstance(fig,matplotlib.figure.Figure):
                self.figure=fig
            else:
                raise ValueError('fig must be matplotlib.figure.Figure object')
        else:
            self.figure=gcf()

        if not axs is None:
            if isinstance(axs,list) and all(*[isinstance(a,maptlotlib.axes.Axes) and a.figure is self.figure for a in axs]):
                self.axes=axs.copy()
            else:
                raise ValueError(f'axs must be a list of matplotlib.axes.Axes objects with figure {self.figure}')
        else:
            self.axes=[]

        self.horizontal=horizontal


    def add_new_subplot(self,**kw):
        nsb=len(self.axes)
        if self.horizontal:
            newgssh = (1,nsb+1)
        else:
            newgssh = (nsb+1,1)
        gs=GridSpec(*newgssh,figure=self.figure)
        for j,ax in enumerate(self.axes):
            #print(ax.get_subplotspec().get_geometry(),gs[j].get_geometry())
            ax.set_subplotspec(gs[j])
        self.axes.append(self.figure.add_subplot(gs[-1],**kw))
        return self.axes[-1]
