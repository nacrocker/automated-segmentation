#this demo shows how defaultVars can be build up in increments.
#defaultVarsPartial can be used by mulitiple contributing code blocks to extend defaultVars interface for their own purposes
#defaultVars GUI is triggered, if appropriate, by call to defaultVarsFinal
#defaultVars function can be overriden by defaultVarsFinal to allow minimal modification of existing OMFITpython scripts when code blocks added that extend defaultVars GUI
from OMFITlib_SCRIPT_utils import defaultVarsPartial, defaultVarsFinal as defaultVars
defaultVarsPartial(b=2)
defaultVars(a=3)
print(a,b)
