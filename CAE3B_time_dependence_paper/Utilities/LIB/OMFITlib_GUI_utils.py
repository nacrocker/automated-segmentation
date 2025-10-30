from omfit_plot import _active_FigureNotebooks as active_FigureNotebooks

def inFigureNotebook(figs=None):
    import numpy as np
    import matplotlib.pyplot as plt
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
    return fignums[~inFigureNotebook(fignums)]


def figuresInFigureNotebooks():
    import matplotlib.pyplot as plt
    import numpy as np
    fignums =  np.asarray(plt.get_fignums())
    return fignums[inFigureNotebook(fignums)]


def select_treeLocation(loc):
    """Select location in tree browser.
    loc: string location, eg \"OMFIT['Module']\""""
    locnodes=parseLocation(loc)
    for ilnd in range(1,len(locnodes)-1):
        locanc = buildLocation(['']+locnodes[1:ilnd+1])
        try:
            #OMFITaux['treeGUI'].focus(locanc)
            OMFITaux['treeGUI'].force_selection(locanc)
            OMFITaux['GUI'].TreeviewOpen()
        except Exception as exc:
            print(exc)
            break
    
    locshort=buildLocation(['']+locnodes[1:])
    OMFITaux['treeGUI'].force_selection(locshort)

def run_or_plot_treeLocation(loc):
    """Select location in tree browser and run or plot.
    loc: string location, eg \"OMFIT['Module']\""""
    select_treeLocation(loc)
    result=OMFITaux['GUI'].run_or_plot()
    return result


 

