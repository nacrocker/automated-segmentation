from OMFITlib_GUI_utils import figuresNotInFigureNotebooks, inFigureNotebook

defaultVars(figs=None)

import numpy as np
if figs is None:
    figs = figuresNotInFigureNotebooks()
else:
    figs = np.asarray(figs)[inFigureNotebook(figs)]

figntbk = FigureNotebook()
add_fig_using_label = lambda fntbk,fig:fntbk.add_figure(fig=fig,label=fig.get_label())

for fnum in figs:
    fig = plt.figure(fnum)
    add_fig_using_label(figntbk,fig)
    plt.close(fig)
