def inFigureNotebook(figs=None):
    import numpy as np
    import matplotlib.pyplot as plt
    from omfit_plot import _active_FigureNotebooks as active_FigureNotebooks
    figs = np.asarray(figs)
    isin = np.zeros(figs.shape,dtype=bool)
    isinrav = isin.ravel()
    for ifig,fig in enumerate(figs):
        if isinstance(fig,{int,str,np.integer}): fig = plt.figure(fig)
        for fnb in active_FigureNotebooks.keys():
            if fig in active_FigureNotebooks[fnb].figures.values():
                isinrav[ifig] = True
                break
    return isin

def figuresNotInFigureNotebooks():
    import matplotlib.pyplot as plt
    import numpy as np
    fignums =  np.asarray(plt.get_fignums())
    return(fignums[~inFigureNotebook(fignums)])


def figuresInFigureNotebooks():
    import matplotlib.pyplot as plt
    import numpy as np
    fignums =  np.asarray(plt.get_fignums())
    return(fignums[inFigureNotebook(fignums)])
