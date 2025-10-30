with namespace_environment(OMFIT['Utilities']):
    from OMFITlib_GUI_utils import run_or_plot_treeLocation, select_treeLocation
 

loc="OMFIT['commandBox']['out_nc']['area']"
run_or_plot_treeLocation(loc)
gca().set_title("out_nc['area']")
scratch=OMFIT['scratch']
scratch['_']=out_hw['area'].reshape(out_hw['P'].shape)
loc="OMFIT['scratch']['_']"
print(loc)
run_or_plot_treeLocation(loc)
gca().set_title("out_hw['area'].reshape(out_hw['P'].shape)")