rt=root # rt=OMFIT['ModeTimeDependence']

defParams=SortedDict(dict(
    xlimv = None,
    ylimv = None,
    saveFIG=True,
    savePDF=False,
    saveLocation=None,
    saveTag=None,
    ))

from OMFITlib_SCRIPT_utils import this_is_WORKFLOW_script
if this_is_WORKFLOW_script() and parent and not 'parameters' in parent: parent['parameters'] = SortedDict()
if parent and 'parameters' in parent: defParams.update(parent['parameters'])

#with namespace_environment(OMFIT['Utilities']):
#    from OMFITlib_SCRIPT_utils import forceDefaultVarsGUI
#    forceDefaultVarsGUI()

defaultVars(**defParams)


if saveTag is None:
    saveTag=''
if saveTag != '': saveTag='_'+saveTag


from OMFITlib_max_tree_class import max_tree as max_tree_cl

sproot=rt['OUTPUTS']['synth1']['sp']

sp=sproot['sp']
fsp=sproot['freq']
tsp=sproot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr



from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()
cmap=cmstd
CSS4 = matplotlib.colors.CSS4_COLORS

#bgcolor = CSS4['aliceblue']
#bgcolor = CSS4['cyan']
#bgcolor = CSS4['cadetblue']
bgcolor = CSS4['paleturquoise']


axs,ims,cbs=[],[],[]
def save_handles(ax,im,cb):
    axs.append(ax)
    ims.append(im)
    cbs.append(cb)

figs_to_save=[]
def add_figure_to_save(fig=None,name=None):
    if not fig is None:
        figs_to_save.append(dict(fig=fig,name=name))

def apply_lims_and_labels(ax=None):
    if ax is None: ax=gca()
    if not xlimv is None: ax.set_xlim(xlimv)
    if not ylimv is None: ax.set_ylim(ylimv)
    ax.set_xlabel('time [msec]')
    ax.set_ylabel('freq [kHz]')

def attribute_panel_maker(fig,gsit,kwprep=None):
    def make_attribute_panel(attr,tit,norm=None,cmap='viridis',**kwextra):
        if not kwprep is None:
            kwextra['norm'],kwextra['cmap'] = norm,cmap
            kwprep(kwextra)
            norm = kwextra.pop('norm',None)
            cmap = kwextra.pop('cmap',None)
        gsc=next(gsit)
        ax = fig.add_subplot(gsc)
        im,cb=specim(tsp,fsp,attr,cmap=cmap,norm=norm,**kwextra)
        apply_lims_and_labels(ax)
        save_handles(ax,im,cb)
        title(tit)
        ax.set_facecolor(bgcolor)
        if len(axs) > 0 and axs[0] != ax:
            ax.sharex(axs[0])
            ax.sharey(axs[0])
    return make_attribute_panel

def override_norm_key_with_log(kwextra):
    if 'vlimdict' in kwextra:
        normLog=matplotlib.colors.LogNorm(**kwextra['vlimdict'])
    else:
        normLog=matplotlib.colors.LogNorm()
    kwextra['norm'] = normLog

def make_gridspec_iterator(fig,gridshape):
    gs = GridSpec(*gridshape, figure=fig)
    gsrav = lambda i: gs[np.unravel_index(i, gs.get_geometry())]
    gsit = (gsrav(i) for i in range(np.product(gs.get_geometry())))
    return gsit

def prep_figure(gridshape,panelsize,name):
    fgsz=(panelsize[0]*gridshape[1],panelsize[1]*gridshape[0])
    #figtreeatrib = plt.figure(figsize=fgsz,layout='constrained')
    fig= plt.figure(figsize=fgsz,layout='tight')
    add_figure_to_save(fig=fig,name=name)
    gsit = make_gridspec_iterator(fig,gridshape)
    return fig,gsit

fgsz0=(6,4.5) #single panel (horiz,vert)

fig,gsit = prep_figure((2,1),fgsz0,'figure_spcgsynth_tree_attributes'+saveTag)
make_lin_attribute_panel = attribute_panel_maker(fig,gsit)
make_log_attribute_panel =  attribute_panel_maker(fig,gsit,kwprep=override_norm_key_with_log)          

make_lin_attribute_panel(self.area,'area')
#make_log_attribute_panel(self.area/self.image.size,'area fraction')
#make_lin_attribute_panel(self.area/self.extents[...,1]/self.image.shape[0],'average vertical extent fraction')
#make_lin_attribute_panel(self.extents[...,1]/self.image.shape[1],'horizontal extent fraction')

make_log_attribute_panel(self.contrast,'contrast')
#make_lin_attribute_panel(self.height,'height')
#make_lin_attribute_panel(self.volume,'volume')

fig,gsit = prep_figure((2,1),fgsz0,'figure_spcgsynth_tree_gain'+saveTag)
make_lin_attribute_panel = attribute_panel_maker(fig,gsit)
make_log_attribute_panel =  attribute_panel_maker(fig,gsit,kwprep=override_norm_key_with_log)          

#make_lin_attribute_panel(self.volume/self.area,'average height')
make_lin_attribute_panel(self.volume*self.extents[...,1]/self.area,'average spectral density')
make_lin_attribute_panel(self.volume/(self.area*self.image),'signal-to-noise')

from OMFITlib_utils import saveFigToTree
for ftsdict in figs_to_save:
    figtosave,nametosave = ftsdict['fig'],ftsdict['name']
    saveFigToTree(figtosave,saveLocation=saveLocation,saveName=nametosave,saveFIG=saveFIG,savePDF=savePDF)