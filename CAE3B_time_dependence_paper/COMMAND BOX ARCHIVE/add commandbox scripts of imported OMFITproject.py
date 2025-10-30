def finish_OMFITproject_import(proj):
    if isinstance(proj,OMFITproject):
        if '__GUISAVE__' in proj:
            guisaveind = proj.index('__GUISAVE__')
            tmp = proj.pop('__GUISAVE__')
            proj.insert(guisaveind, 'GUISAVE__', tmp)

        if '__COMMANDBOX__' in proj:
            print('whoo')
            cmdboxind = proj.index('__COMMANDBOX__')
            oldcmdbox=proj.pop('__COMMANDBOX__')
            proj.insert(cmdboxind,'COMMANDBOX__',OMFITtree(''))
            cmdbox=proj['COMMANDBOX__']
            for k in oldcmdbox.keys():
                knew=k.split('.py')[0]
                print(knew)
                print(oldcmdbox[k].filename)
                cmdbox[knew]=OMFITpythonTask(oldcmdbox[k].filename)



finish_OMFITproject_import(OMFIT['bdot_spec_segmentation'])
