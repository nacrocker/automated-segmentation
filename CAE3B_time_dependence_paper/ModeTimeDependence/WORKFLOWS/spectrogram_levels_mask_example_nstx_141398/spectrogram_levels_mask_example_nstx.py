#root=OMFIT['ModeTimeDependence']

defParams=SortedDict(dict(
    bdotarray = 'HN',
    shot=141398,
    plotcoilind=7,
    timekey = (0.4, 0.7),
    freqrange=[350e3, 875e3],
    levels=[5e-7],
    cmap='Standard_Gamma_II',
    colors=None,
    spquantrange = [.03,1],
    saveFIG=True,
    savePDF=False,
    saveLocation=None,
    saveTag=None
    ))

if parent and 'parameters' in parent: defParams.update(parent['parameters'])

#with namespace_environment(OMFIT['Utilities']):
#    from OMFITlib_SCRIPT_utils import forceDefaultVarsGUI
#    forceDefaultVarsGUI()

defaultVars(**defParams)

stftroot = root['OUTPUTS'][shot]['bdot'][bdotarray]['stft'][timekey]

bdotnames = stftroot['bdotnames']
bdotshortnames=stftroot['bdotshortnames']

ibdot = 0
if bdotarray+str(plotcoilind) in bdotshortnames: ibdot = bdotshortnames.index(bdotarray+str(plotcoilind))



tsp0,fsp0,sp0 = stftroot['time'],stftroot['freq'],np.abs(stftroot[ibdot])**2


infreqrange=(lambda x,r:(x >= r[0]) & (x < r[1]))(fsp0,freqrange)
tsp,fsp,sp = tsp0,fsp0[infreqrange],sp0[infreqrange,...]

#spquantrange = [.03,1]

vlim=None
if not spquantrange is None: vlim=np.quantile(sp,spquantrange)
if not vlim is None:
    vlimdict=dict(vmin=vlim[0],vmax=vlim[1])
else:
    vlimdict={}


normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)

fig=plt.figure(figsize=(4, 3),layout='constrained')
levels=np.atleast_1d(levels)
#levelscf=np.append(levels,vlim[1])
#levelscf=np.append(levels,[vlim[1],vlim[1]+1])
#levelscf=np.append(levels,vlim[1]*1.01)
levelscf=np.append(levels,np.maximum(np.max(sp),np.max(levels))*1.00001)

if isinstance(cmap,str) and cmap == 'Standard_Gamma_II':
    from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
    cmstd=cmapIDL_Standard_Gamma_II()
    cmap=cmstd
cdict=dict()
if colors is None:
    if isinstance(cmap,str): cmap=matplotlib.cm.get_cmap(cmap)
    #if isinstance(cmap,str): cmap=matplotlib.colormaps[cmap]
    colors=cmap(norm(levels))
    colors=[c[0:3] for c in colors]
    cdict['colors'] = colors
else:
    if isinstance(colors,np.ndarray):
        colors=[c for c in colors]
    cdict['colors'] = colors

#formatter=matplotlib.ticker.ScalarFormatter()
#formatter=matplotlib.ticker.ScalarFormatter().set_scientific(True)
#formatter=matplotlib.ticker.LogFormatter()
#formatter=matplotlib.ticker.LogFormatter(labelOnlyBase=False)
#formatter=matplotlib.ticker.LogFormatterSciNotation()
formatter=matplotlib.ticker.FormatStrFormatter('%0.2e')

cf=plt.contourf(tsp,fsp/1e6,sp,levelscf,norm=norm,**cdict,extend='max')
cf.cmap.name='OMFIT_'+cf.cmap.name
setattr(matplotlib.cm,cf.cmap.name,cf.cmap)
plt.xlabel('time [sec]')
plt.ylabel('freq [MHz]')

cb=matplotlib.figure.Figure.colorbar(fig,cf,norm=norm,format=formatter,extend='max')
#cb=plt.colorbar(cf,norm=norm,format=formatter,extend='max')
if len(levelscf) > len(levels): plt.setp(cb.ax.yaxis.get_ticklabels()[len(levels)-len(levelscf):],visible=False)


intr=lambda x:np.int(np.round(x))
if saveTag is None:
    saveTag=f'{bdotshortnames[ibdot]}_{shot}_t{intr(timekey[0]*1e3):d}_{intr(timekey[1]*1e3):d}_f{intr(freqrange[0]/1e3):d}_{intr(freqrange[1]/1e3):d}'

from OMFITlib_utils import saveFigToTree
saveFigToTree(fig,saveLocation=saveLocation,saveName='figure_spcg_levels_mask_'+saveTag,saveFIG=saveFIG,savePDF=savePDF)
