#-*-Python-*-
# Created by ncrocker at 25 Nov 2023  04:56

def timestamp(date=None):
    if date is None: date=datetime.datetime.now().timestamp()
    return convertDateFormat(date,format_out="%Y-%m-%d_%H_%M_%S_%f")

def saveFigToTree(fig,saveLocation=None,saveName=None,saveFIG=True,savePDF=False,FIGsuffix='',PDFsuffix='_pdf'):
    if saveFIG or savePDF:
        if not saveLocation:
            if parent and parent is not root:
                saveLocation=parent
            else:
                saveLocation="root['FIGURES']"
        if isinstance(saveLocation,str):
            sLp = parseLocation(saveLocation)
            rt=sLp[0]
            if len(rt) == 0:
                rt = 'root'
            sLp[0] = ''
            saveLocation = (lambda ap: ap[0][ap[1]])(eval(rt).addBranchPath(buildLocation(sLp))[-1])

    if saveName is None: saveName = 'figure_'+timestamp()
    if saveFIG: saveLocation[saveName+FIGsuffix] = savedFigure(fig)
    if savePDF:
        fig.savefig(saveName+'.pdf')
        saveLocation[saveName+PDFsuffix] = OMFITpath(saveName+'.pdf')

class savedFigureFixed(savedFigure):
    def __init__(self, fig):
        for k, ax in enumerate(fig.axes):
            if ax.get_legend() is not None:
                ax.get_legend().set_draggable(False)
        self.figurePickle = pickle.dumps(fig)
        for k, ax in enumerate(fig.axes):
            if ax.get_legend() is not None:
                ax.get_legend().set_draggable(True)




#should probably put the following in some utility module
def assigntoarr(arr,ind,vals):
    import numpy as np
    np.put(arr,ind,vals)
    return arr

def boolindices(shape,ind,raveled_indices=False):
    import numpy as np
    bi = np.zeros(shape,dtype=bool)
    if raveled_indices:
        bi.ravel()[ind] = True
    else:
        bi[ind]=True

    return bi

class cache:
    def __init__(self):
        self._value=None

    def __call__(self,value=None):
        if value is None:
            return self._value
        else:
            self._value=value
            return value


class tmfun:
    def __init__(self,fun,*params,**kw):
        self.params = params
        self.kw = kw
        self.fun = fun
        self.result = None
    def __call__(self):
        self.result=self.fun(*self.params,**self.kw)
