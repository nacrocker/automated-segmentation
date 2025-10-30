OMFIT['scratch'].setdefault('meldloc1',"")
OMFIT['scratch'].setdefault('meldloc2',"")
OMFITx.Label('Compare and merge files with Meld')
def test_existsAndIsFile_and_store(result_loc):
    def existsAndIsFile(loc):
        import os
        loc=eval(loc)
        isvalid = hasattr(loc,'filename') and os.path.isfile(loc.filename)
        setLocation(result_loc,isvalid,globals=globals(),locals=locals())
        return isvalid
    return existsAndIsFile

OMFITx.TreeLocationPicker("OMFIT['scratch']['meldloc1']",lbl='File 1:',check=test_existsAndIsFile_and_store("OMFIT['scratch']['meldloc1_valid']"),updateGUI=True)
OMFITx.TreeLocationPicker("OMFIT['scratch']['meldloc2']",lbl='File 2:',check=test_existsAndIsFile_and_store("OMFIT['scratch']['meldloc2_valid']"),updateGUI=True)
def launchMeld():
    import subprocess
    file1=eval(OMFIT['scratch']['meldloc1']).filename
    file2=eval(OMFIT['scratch']['meldloc2']).filename
    subprocess.Popen(["meld", file1,file2])

if OMFIT['scratch'].setdefault('meldloc1_valid',False) and OMFIT['scratch'].setdefault('meldloc2_valid',False):
    OMFITx.Button('Launch Meld',launchMeld,closeGUI=True)
