import matplotlib.pyplot as plt
def plotChldParPairs(P,x,y,*args,marker='.',linestyle=None,ls=None,**kwargs):
    if linestyle and ls:
        raise TypeError(f"Got both linestyle and ls, which are aliases of one another")
    if len(args) > 1: raise TypeError("plotChldParPairs takes up to 3 positional arguments but more were given")
    if ls: linestyle = ls
    if not linestyle: linestyle = '-'
    pts=plt.plot(x,y,*args,linestyle='none',marker=marker,**kwargs)
    col=pts[0].get_color()
    lns=plt.plot(stack([x,x[P.ravel()]],axis=1).T,stack([y,y[P.ravel()]],axis=1).T,marker=None,linestyle=linestyle,color=col)
    return pts+lns 


figure()
iS=np.argsort(S)
l=plotChldParPairs(iS[P.ravel()][S],imgav[S],var[S])