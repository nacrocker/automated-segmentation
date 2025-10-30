def this_is_WORKFLOW_script():
    lineage=parseLocation(thisName)
    return len(lineage) >= 3 and lineage[-3] == 'WORKFLOWS'


#this demo allows defaultVars to be built up in increments.
#defaultVarsPartial can be used by mulitiple contributing code blocks to extend defaultVars interface for their own purposes
#defaultVars GUI is triggered, if appropriate, by call to defaultVarsFinal
#defaultVars function can be overriden by defaultVarsFinal to allow minimal modification of existing OMFITpython scripts when code blocks added that extend defaultVars GUI


def defaultVarsDicts():
    defaultVarsClosure=dict(zip(defaultVars.__code__.co_freevars, defaultVars.__closure__))
    inputDict=defaultVarsClosure['inputDict'].cell_contents
    userDict=defaultVarsClosure['userDict'].cell_contents
    return inputDict,userDict

def forceDefaultVarsGUI():
    inputDict,_ = defaultVarsDicts()
    inputDict['defaultVarsGUI'] = True

def defaultVarsPartial(**kw):
    """Build up temporary dict to become defaultVars dict"""
    if not hasattr(this,'_defaultVarsTemp'):
        this._defaultVarsTemp = dict()
    this._defaultVarsTemp.update(kw)
    return this._defaultVarsTemp

#clearing the way to for users of this module to override defaultVars with defaultVarsFinal
_defaultVars=defaultVars

def defaultVarsFinal(**kw):
    """Add vars of temporary defaultVars dict to defaultVars dict"""
    kw = defaultVarsPartial(**kw)
    if hasattr(this,'_defaultVarsTemp'):
        delattr(this,'_defaultVarsTemp')
    kw = _defaultVars(**kw)
    return kw


##def defaultVarsPartial(**kw):
##    """Add vars to defaultVars dict without triggring defaultVars GUI"""
##    inputDict,_ = defaultVarsDicts()
##    if 'defaultVarsPartial' not in inputDict:
##        inputDict['defaultVarsPartial'] = dict()
##    inputDict['defaultVarsPartial'].update(kw)
##    return inputDict['defaultVarsPartial']
##
##def defaultVarsFinal(**kw):
##    """Add vars to defaultVars dict, allowing defaultVars GUI to be triggered"""
##    kw = **defaultVarsPartial(**kw)
##    inputDict,_ = defaultVarsDicts()
##    del inputDict['defaultVarsPartial']:
##    defaultVars(**kw)

##def defaultVarsPartial(**kw):
##    """Add vars to defaultVars dict without triggring defaultVars GUI"""
##    inputDict,userDict = defaultVarsDicts()
##    _defaultVarsGUI = inputDict['defaultVarsGUI']
##    inputDict['defaultVarsGUI']=False
##    try:
##        defaultVars(**userDict,**kw)
##    except Exception as e:
##        print(e)
##    finally:
##        inputDict['defaultVarsGUI']=_defaultVarsGUI
##
##def defaultVarsFinal(**kw):
##    """Add vars to defaultVars dict, allowing defaultVars GUI to be triggered"""
##    inputDict,userDict = defaultVarsDicts()
##    defaultVars(**userDict,**kw)

#def defaultVarsPartial_nochecking(**kw):
#    """Add vars to defaultVars dict without triggring defaultVars GUI"""
#    inputDict,userDict = defaultVarsDicts()
#    _defaultVarsGUI = inputDict['defaultVarsGUI']
#    inputDict['defaultVarsGUI']=False
#    import os
#    from omfit_classes.utils_base import _streams
#    _streams.backup()
#    try:
#        with open(os.devnull, 'w') as f:
#            _streams['WARNING'] = f
#            defaultVars(**kw,strict_defaultVars=False)
#    except Exception as e:
#        print(e)
#    finally:
#        _streams.restore()
#        inputDict['defaultVarsGUI']=_defaultVarsGUI

#def defaultVarsFinal_nochecking(**kw):
#    """Add vars to defaultVars dict, allowing defaultVars GUI to be triggered"""
#    import os
#    from omfit_classes.utils_base import _streams
#    _streams.backup()
#    try:
#        with open(os.devnull, 'w') as f:
#            _streams['WARNING'] = f
#            defaultVars(**kw,strict_defaultVars=False)
#    except Exception as e:
#       print(e)
#    finally:
#        _streams.restore()
#        inputDict['defaultVarsGUI']=_defaultVarsGUI


from contextlib import contextmanager

@contextmanager
def overriddenSeqVals(seq,indices,values):
    """
    #examples:

    #code:
    a=[1]
    with overriddenSeqVals(a,[0],[2]):
        print(a)
    print(a)
    #output:
    [2]
    [1]

    #code:
    a=[1]
    with overriddenSeqVals(a,['a'],[2]):
        print(a)
    print(a)
    #output:
    {'a': 2}
    {'a': 1}
    """

    olditems = {i:seq[i] for i in indices}
    for i,v in zip(indices,values):
        seq[i] = v
    try:
        yield seq
    finally:
        for i,v in olditems.items():
            seq[i] = v
