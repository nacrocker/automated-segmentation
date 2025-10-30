import numpy as np
from skimage.morphology import max_tree

#image = np.array([[15, 13, 16], [12, 12, 10], [16, 12, 14]])
image = np.array([[40, 40, 39, 39, 38],
                  [40, 41, 39, 39, 39],
                  [30, 30, 30, 32, 32],
                  [33, 33, 30, 32, 35],
                  [30, 30, 30, 33, 36]], dtype=np.uint8)

P, S = max_tree(image, connectivity=1)
P_rav=P.ravel()
image_rav = image.ravel()
#a canonical node has a different value from its parent.

print()
print('####')
print()

####

from OMFITlib_max_tree_utils import label_level_from_top

level,numchldcanon,Plevel=label_level_from_top(image,P,S)
print(image)
print(P)
print(S)
print(numchldcanon)
print(level)
print(Plevel)

print()
print('####')
print()

####

from OMFITlib_max_tree_utils import label_level_from_bottom

level,numchldcanon,brannum=label_level_from_bottom(image,P,S)
print(image)
print(P)
print(S)
print(numchldcanon)
print(brannum)
print(level)

print()
print('####')
print()
####

from OMFITlib_max_tree_utils import accumulate_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index2_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index12_vs_index_along_axis

axis=1
accum,accumc = accumulate_other_index_vs_index_along_axis(P,S,axis=axis)
accumav = np.divide(accum,accumc, where=accumc!=0,out=np.zeros_like(accum))
accum2,accumc = accumulate_other_index2_vs_index_along_axis(P,S,axis=axis)
accum2av = np.divide(accum2,accumc, where=accumc!=0,out=np.zeros_like(accum2))
accumvar=accum2av-accumav**2

print(image)
print(P)
print(S)
print(level)
print(accumc)
print(accum)
print(accum2)
print(accumav)
print(accum2av)
print(accumvar)

print()
print('####')
print()

####
from OMFITlib_max_tree_utils import first_at_index_accumlator
from OMFITlib_max_tree_utils import mark_component


faiacc=first_at_index_accumlator(P,axis=1)
mk=mark_component(4,image,P,S,accumulator=faiacc)
print(image)
print(P)
print(S)
print(mk)
#print(acc.accumulation)

firstind=np.full_like(image,fill_value=-1,dtype=int)
firstind_rav=firstind.ravel()
firstind_rav[list(faiacc.accumulation.values())] = [k[0] for k in faiacc.accumulation.keys()]
print(firstind)

branchfirstind=np.full_like(image,fill_value=(-1,),dtype=tuple)
branchfirstind_rav=branchfirstind.ravel()
branchfirstind_rav[list(faiacc.accumulation.values())] = [k[1:] for k in faiacc.accumulation.keys()]
print(branchfirstind)

print()
print('####')
print()

####

axis=1
#accumoiviaa,accumoiviaa_count = accumulate_other_index_vs_index_along_axis(P,S,axis=axis)
#accumoi2viaa,_ = accumulate_other_index2_vs_index_along_axis(P,S,axis=axis)
accumoi12viaa,accumoiviaa_count = accumulate_other_index12_vs_index_along_axis(P,S,axis=axis)
accumoiviaa = accumoi12viaa[:,:,0]
accumoi2viaa = accumoi12viaa[:,:,1]
faiacc=first_at_index_accumlator(image,axis=axis)

icomp=0
mk=mark_component(icomp,image,P,S,accumulator=faiacc)

nacc=image.shape[axis]
acccomp=np.zeros(nacc)
acccomp2=np.zeros(nacc)
acccomp_count=np.zeros(nacc)
accumoiviaa_rav=accumoiviaa.ravel()
accumoi2viaa_rav=accumoi2viaa.ravel()
accumoiviaa_count_rav=accumoiviaa_count.ravel()

np.add.at(acccomp,[k[0] for k in faiacc.accumulation.keys()],accumoiviaa_rav[list(faiacc.accumulation.values())])
np.add.at(acccomp2,[k[0] for k in faiacc.accumulation.keys()],accumoi2viaa_rav[list(faiacc.accumulation.values())])
np.add.at(acccomp_count,[k[0] for k in faiacc.accumulation.keys()],accumoiviaa_count_rav[list(faiacc.accumulation.values())])

acccompav = np.divide(acccomp,acccomp_count, where=acccomp_count!=0,out=np.zeros_like(acccomp))
acccomp2av = np.divide(acccomp2,acccomp_count, where=acccomp_count!=0,out=np.zeros_like(acccomp))
acccompvar=acccomp2av-acccompav**2

print(image)
print(mk)

print(acccompav)
print(acccomp2av)
print(acccompvar)