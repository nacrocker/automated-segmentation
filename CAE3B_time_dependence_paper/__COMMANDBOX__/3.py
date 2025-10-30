collectfigs_script=OMFIT['Utilities']['SCRIPTS']['Collect figures in notebook']
closefigs_script=OMFIT['Utilities']['SCRIPTS']['Close all figures']

script_hw = root['PROJECT']['SCRIPTS']['maxtree_noise_project - Haowen Sun summer 2024']['noise_histograms_v2_fixes']
script_nc = root['PROJECT']['SCRIPTS']['noise_histogram']

import pdb
import sys
debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)

kglbls = list(globals().keys())
kcmdbx = list(OMFIT['commandBox'])

kall = list(set(kglbls) - set(kcmdbx))

fighandler=collectfigs_script
#fighandler=closefigs_script

if False: 
    out_hw = script_hw.run()
    fighandler.run()
    for k in kall:
        if k in out_hw: del out_hw[k]
if True:    
    #out_nc=debugger.runcall(script_nc.run)
    out_nc = script_nc.run()
    fighandler.run()
    for k in kall:
        if k in out_nc: del out_nc[k]



#kall = [*out_hw.keys()]
#for k in kall:
#    if k in out_nc.keys():
#        try:
#            if out_hw[k] is out_nc[k]:
#                del out_nc[k]
#                del out_hw[k]
#        except:
#            pass