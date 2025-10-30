# -*-Python-*-
# Created by ncrocker at 29 Oct 2023  23:25
from skimage.morphology import max_tree


class interval_timer:
    def __init__(self):
        import time as timeim

        self.timer_t0 = timeim.time()
        self.timer_t1 = self.timer_t0

    def delta_time(self):
        import time as timeim

        self.timer_t1 = timeim.time()
        dt = self.timer_t1 - self.timer_t0
        self.timer_t0 = self.timer_t1
        return dt


def label_level_from_top(image, P, S):
    # Finds levels such that all level contours for image nodes in same level contain the same peaks.
    #    Note that level values form a tree such that the parent of an image node level value is the
    #    level value of the node's 1st ancestor with a different level value.
    # OUTPUT: level,numchldcanon,Plevel
    # level: matrix of size image with level for each image node. Level value is raveled index for
    #    node image with highest value for that level.
    # numchldcanon: matrix of size image with number canonical node children for each node image.
    #    A canonical node has a different value from its parent. Non-canonical nodes have -1 children.
    # Plevel: a dictionary giving the level tree. For each key corresponding to a level value, the
    #    dictionary value is the level value of the child.
    image_rav = image.ravel()
    P_rav = P.ravel()
    numchldcanon = np.zeros(P.shape, dtype=int)
    numchldcanon_rav = numchldcanon.ravel()
    level = np.arange(len(S)).reshape(P.shape)
    level_rav = level.ravel()
    chld = np.zeros(P_rav.shape, dtype=int)
    chld[:] = -1
    Plevel = dict()
    for iS in S[::-1]:
        ipar = P_rav[iS]
        if image_rav[ipar] != image_rav[iS]:  # canoncical non-root node
            if numchldcanon_rav[ipar] == 1:
                Plevel[level_rav[chld[ipar]]] = ipar
            if numchldcanon_rav[ipar] >= 1:
                Plevel[currlevel] = ipar
            chld[ipar] = iS
            numchldcanon_rav[ipar] += 1
            iScanon = iS
        elif iS == ipar:  # root node
            iScanon = iS
        else:
            numchldcanon_rav[iS] = -1  # non-canonical node
            iScanon = ipar
        if numchldcanon_rav[iScanon] == 1:
            currlevel = level_rav[chld[iScanon]]
        else:
            currlevel = iScanon
        level_rav[iS] = currlevel
    return (level, numchldcanon, Plevel)


def label_level_from_bottom(image, P, S):
    # level value is index of lowest value node in level
    image_rav = image.ravel()
    P_rav = P.ravel()
    numchldcanon = np.zeros(P.shape, dtype=int)
    numchldcanon_rav = numchldcanon.ravel()
    brannum = np.zeros(P.shape, dtype=int)
    brannum_rav = brannum.ravel()
    level = np.arange(len(S)).reshape(P.shape)
    level_rav = level.ravel()
    for iS in S[1:]:
        ipar = P_rav[iS]
        if image_rav[ipar] != image_rav[iS]:
            numchldcanon_rav[ipar] += 1
        else:
            numchldcanon_rav[iS] = -1

    # need numcldcanon already defined here. cannot contrstuct on the fly because
    # tree traversal starting from root can only update number of children for a node
    numchldcanon_rav = numchldcanon.ravel()
    for iS in S:
        ipar = P_rav[iS]
        if image_rav[ipar] != image_rav[iS] and numchldcanon_rav[ipar] > 1:
            print(iS, ipar, brannum_rav[ipar], currlevel)
            currbrannum = brannum_rav[ipar] + 1
            currlevel = iS
        else:
            currbrannum = brannum_rav[ipar]
            currlevel = level_rav[ipar]
        brannum_rav[iS] = currbrannum
        level_rav[iS] = currlevel
    return (level, numchldcanon, brannum)


import operator


def accumulate_vs_index_along_axis_alt(P, S, value=None, weight=None, accumulate_operator=operator.add, axis=0):
    # this one attempts to process all "columns" in parallel, which is slow
    if value is None:
        value = np.ones(P.shape, dtype=np.float64)
    if weight is None:
        weight = np.ones(P.shape, dtype=np.int)
    weight_rav = weight.ravel()
    if value.ndim > 2:
        valueweighted = value * weight.reshape(weight.shape + (1,) * len(value.shape[2:]))
        valueweighted_rav = valueweighted.reshape((np.prod(P.shape), -1))
        accumulation = np.zeros(valueweighted.shape, dtype=np.result_type(valueweighted, 1.0))
        accumulation_rav = accumulation.reshape((np.prod(P.shape), -1))
    else:
        valueweighted = value * weight
        valueweighted_rav = valueweighted.ravel()
        accumulation = np.zeros(valueweighted.shape, dtype=np.result_type(valueweighted, 1.0))
        accumulation_rav = accumulation.ravel()
    accumweight = np.zeros_like(weight)
    accumweight_rav = accumweight.ravel()
    P_rav = P.ravel()
    accumweightregisters = np.zeros(P.shape[axis], dtype=weight.dtype)
    if value.ndim > 2:
        accumregisters = np.zeros((P.shape[axis],) + value.shape[2:], dtype=np.float64)
    else:
        accumregisters = np.zeros(P.shape[axis], dtype=np.float64)
    ii = np.unravel_index(np.arange(P.size), P.shape)[axis]
    hit = np.zeros(S.shape, dtype=bool)
    for iS in S[::-1]:
        if hit[iS]:
            continue
        accumregisters[:] = 0.0
        accumweightregisters[:] = 0.0
        icurr = iS
        while True:
            icurri = ii[icurr]
            if not hit[icurr]:
                accumregisters[icurri] = accumulate_operator(accumregisters[icurri], valueweighted_rav[icurr])
                accumweightregisters[icurri] += weight_rav[icurr]
            hit[icurr] = True
            if accumweightregisters[icurri]:
                accumulation_rav[icurr] = accumulate_operator(accumulation_rav[icurr], accumregisters[icurri])
                accumweight_rav[icurr] += accumweightregisters[icurri]
            if icurr == P_rav[icurr]:
                break
            icurr = P_rav[icurr]
    return (accumulation, accumweight)


import operator


def accumulate_vs_index_along_axis(P, S, value=None, weight=None, accumulate_operator=operator.add, axis=0):
    # this walks backward along P.ravel(), for each element following the tree till return to same axis index, which
    #    is the same-index-parent, and then accumulates from the value at the start to the same index-parent.
    if value is None:
        value = np.ones(P.shape, dtype=np.float64)
    if weight is None:
        weight = np.ones(P.shape, dtype=int)
    if value.ndim > 2:
        accumulation = value.astype(dtype=np.float64) * weight.reshape(weight.shape + (1,) * len(value.shape[2:]))
        accumulation_rav = accumulation.reshape((np.prod(P.shape), -1))
    else:
        accumulation = value.astype(dtype=np.float64) * weight
        accumulation_rav = accumulation.ravel()
    accumweight = weight.copy()
    accumweight_rav = accumweight.ravel()
    P_rav = P.ravel()
    ii = np.unravel_index(np.arange(P.size), P.shape)[axis]
    for iS in S[::-1]:
        iip = ii[iS]
        p = iS
        pp = P_rav[iS]
        while pp != p:
            if ii[pp] == iip:
                accumweight_rav[pp] += accumweight_rav[iS]
                accumulation_rav[pp] = accumulate_operator(accumulation_rav[iS], accumulation_rav[pp])
                break
            p = pp
            pp = P_rav[p]
    return (accumulation, accumweight)


def accumulate_other_index_vs_index_along_axis(P, S, axis=0, weight=None, accumulator=accumulate_vs_index_along_axis):
    imat = np.unravel_index(np.arange(len(S)), P.shape)[1 - axis].reshape(P.shape)
    accumulation, accumweight = accumulator(P, S, value=imat, axis=axis, weight=weight)
    return (accumulation, accumweight)


def accumulate_other_index2_vs_index_along_axis(P, S, axis=0, weight=None, accumulator=accumulate_vs_index_along_axis):
    imat = np.unravel_index(np.arange(len(S)), P.shape)[1 - axis].reshape(P.shape) ** 2
    accumulation, accumweight = accumulator(P, S, value=imat, axis=axis, weight=weight)
    return (accumulation, accumweight)


def accumulate_other_index12_vs_index_along_axis(P, S, axis=0, weight=None, accumulator=accumulate_vs_index_along_axis):
    imat = np.unravel_index(np.arange(len(S)), P.shape)[1 - axis].reshape(P.shape)
    imat = np.stack([imat, imat**2], axis=2)
    accumulation, accumweight = accumulator(P, S, value=imat, axis=axis, weight=weight)
    return (accumulation, accumweight)


class first_at_index_accumlator:
    def __init__(self, P, axis=0):
        self.accumulation = dict()
        self.index = np.unravel_index(np.arange(np.size(P)), P.shape)[axis]

    def _keyinaccumulation(self, key):
        return builtins.any(builtins.all(kkey == kk for kkey, kk in zip(key, k)) for k in self.accumulation.keys())

    def accumulate(self, image_node, branch):
        ind = self.index[image_node]
        key = (ind,) + branch
        # print(key,image_node,self._keyinaccumulation(key))
        if not self._keyinaccumulation(key):
            self.accumulation[key] = image_node


def mark_component_recursive(image_node, image, P, S, accumulator=None):
    # this is can easily crash by recursing too deep for modest image sizes.
    image_rav = image.ravel()
    P_rav = P.ravel()
    marked = np.zeros(P.shape, dtype=bool)
    marked_rav = marked.ravel()
    if image_rav[image_node] == image_rav[P_rav[image_node]]:
        image_node = P_rav[image_node]

    def _mark(inode, image_rav, marked_rav, P_rav, S, branch=(0,)):
        if not accumulator is None and hasattr(accumulator, 'accumulate'):
            accumulator.accumulate(inode, branch)
        marked_rav[inode] = True
        iSnode = np.nonzero(S == inode)[0][0]
        chld = []
        for inodenext in S[iSnode + 1 :]:
            if P_rav[inodenext] == inode:
                chld.append(inodenext)
        for ichld, inodenext in enumerate(chld):
            brnch = branch
            if len(chld) > 1:
                brnch += (ichld,)
            _mark(inodenext, image_rav, marked_rav, P_rav, S, branch=brnch)

    _mark(image_node, image_rav, marked_rav, P_rav, S)
    return marked


def mark_component(image_node, image, P, S, accumulator=None):
    image_rav = image.ravel()
    P_rav = P.ravel()
    marked = np.zeros(P.shape, dtype=bool)
    marked_rav = marked.ravel()
    if image_rav[image_node] == image_rav[P_rav[image_node]]:
        image_node = P_rav[image_node]

    def _mark(inode, image_rav, marked_rav, P_rav, S, branch=(0,)):
        if not accumulator is None and hasattr(accumulator, 'accumulate'):
            accumulator.accumulate(inode, branch)
        marked_rav[inode] = True
        iSnode = np.nonzero(S == inode)[0][0]
        chld = []
        for inodenext in S[iSnode + 1 :]:
            if P_rav[inodenext] == inode:
                chld.append(inodenext)
        mark_eval_list = []
        for ichld, inodenext in enumerate(chld):
            brnch = branch
            if len(chld) > 1:
                brnch += (ichld,)
            mark_eval_list.insert(0, ((inodenext, image_rav, marked_rav, P_rav, S), dict(branch=brnch)))
        return mark_eval_list

    nodelist = []
    nodelist.append(((image_node, image_rav, marked_rav, P_rav, S), dict()))
    while len(nodelist) > 0:
        nextnode = nodelist.pop()
        nodelist.extend(_mark(*nextnode[0], **nextnode[1]))
    return marked


def max_tree_along_axis(P, S, axis=0):
    # this walks backward along S, for each element following the tree till return to same axis index.
    P_rav = P.ravel()
    Pa = np.zeros(P.shape, dtype=int)
    Sa = np.zeros(P.shape, dtype=int)
    Pa_rav = Pa.ravel()
    Pa_rav[:] = -1
    ui = np.unravel_index(np.arange(len(P_rav)), P.shape)
    axalt = 1 - axis
    ii = ui[axis]
    jj = ui[axalt]
    ialt = np.ones((P.shape[axalt],), dtype=np.int)
    indSa = np.zeros((2,), dtype=np.int)
    for iS in S[::-1]:
        iip = ii[iS]
        jjp = jj[iS]
        np.put(indSa, [axis, axalt], [-ialt[jjp], jjp])
        Sa[tuple(indSa)] = iip
        ialt[jjp] += 1
        pp = P_rav[iS]
        p = iS
        while pp != p and ii[pp] != iip:
            p = pp
            pp = P_rav[pp]
        Pa_rav[iS] = pp if ii[pp] == iip else iS
    return Pa, Sa


def parent_tree_along_axis(P, S, axis=0):
    # this walks backward along S, for each element following the tree till return to same axis index.
    P_rav = P.ravel()
    Pa = np.zeros(P.shape, dtype=int)
    Pa_rav = Pa.ravel()
    Pa_rav[:] = -1
    ii = np.unravel_index(np.arange(len(P_rav)), P.shape)[axis]
    for iS in S[::-1]:
        pp = P_rav[iS]
        iip = ii[iS]
        p = iS
        while pp != p and ii[pp] != iip:
            p = pp
            pp = P_rav[pp]
        Pa_rav[iS] = pp if ii[pp] == iip else iS
    return Pa


def parent_tree_along_axis_alt(P, axis=0):
    # this walks backward along P.ravel(), for each element following the tree till return to same axis index.
    P_rav = P.ravel()
    Pa = np.zeros(P.shape, dtype=int)
    Pa_rav = Pa.ravel()
    Pa_rav[:] = -1
    ii = np.unravel_index(np.arange(len(P_rav)), P.shape)[axis]
    for ip, pp in enumerate(P_rav):
        iip = ii[ip]
        p = ip
        while pp != p and ii[pp] != iip:
            p = pp
            pp = P_rav[pp]
        Pa_rav[ip] = pp if ii[pp] == iip else ip
    return Pa


def parent_tree_along_axis_alt1(P, S, axis=0):
    # this walks backward along P.ravel(), following the tree to root from each value, skipping nodes whose parents have been found
    # this tries to be efficient compared to parent_tree_along_axis
    # No luck: this appears to be slower than parent_tree_along_axis
    P_rav = P.ravel()
    Pa = np.zeros(P.shape, dtype=int)
    Pa_rav = Pa.ravel()
    Pa_rav[:] = -1
    ii = np.unravel_index(np.arange(len(P_rav)), P.shape)[axis]
    ilastatind = np.zeros(P.shape[axis], dtype=int)
    for p in S[::-1]:
        if Pa_rav[p] >= 0:
            continue
        ilastatind[:] = -1
        ilastatind[ii[p]] = p
        Pa_rav[p] = p
        pp = P_rav[p]
        while pp != p:
            iip = ii[p]
            ilaaiiip = ilastatind[iip]
            if ilaaiiip >= 0:
                Pa_rav[ilaaiiip] = p
            ilastatind[iip] = p
            p = pp
            pp = P_rav[p]
        iip = ii[p]
        if ilastatind[iip] >= 0:
            Pa_rav[ilastatind[iip]] = p
    return Pa


def parent_tree_along_axis_alt2(P, S, axis=0):
    # walk along S in reverse
    # this appears to be slower than parent_tree_along_axis
    P_rav = P.ravel()
    Pa = np.zeros(P.shape, dtype=int)
    Pa_rav = Pa.ravel()
    Pa_rav[:] = -1
    axislastind = np.zeros(P.shape[axis], dtype=int)
    axislastind[:] = -1
    ii = np.unravel_index(np.arange(len(S)), image.shape)[axis]
    for iS in reversed(S):
        if Pa_rav[iS] >= 0:
            continue
        axislastind[:] = -1
        icurr = iS
        while True:
            icurri = ii[icurr]
            axli = axislastind[icurri]
            if axli >= 0:
                Pa_rav[axli] = icurr
                # hit[axli] = True
            axislastind[icurri] = icurr
            if icurr == P_rav[icurr]:
                break
            icurr = P_rav[icurr]
        axliroot = axislastind[np.nonzero(axislastind >= 0)]
        # axliroot = axliroot[np.logical_not(hit[axliroot])]
        axliroot = axliroot[Pa_rav[axliroot] < 0]
        Pa_rav[axliroot] = axliroot
        # hit[axliroot] = True
    return Pa


def calculate_area(image, P, S):
    area = np.ones(image.size, dtype=np.int)
    P_rav = P.ravel()
    for p in S[:0:-1]:
        pp = P_rav[p]
        area[pp] = area[pp] + area[p]
    return area


def calculate_volume(image, P, S):
    image_rav = image.ravel()
    vol = image_rav.copy()
    P_rav = P.ravel()
    for p in S[:0:-1]:
        pp = P_rav[p]
        vol[pp] = vol[pp] + vol[p]
    return vol


def calculate_height(image, P, S):
    image_rav = image.ravel()
    height = np.zeros(image.size, dtype=np.float64)
    P_rav = P.ravel()
    for p in S[:0:-1]:
        pp = P_rav[p]
        height[pp] = maximum(height[pp], height[p] + image_rav[p] - image_rav[pp])
    return height


def propagate_max_to_leaves(val, P, S):
    P_rav = P.ravel()
    mxval = val.copy()
    mxval_rav = mxval.ravel()
    for p in S[1:]:
        pp = P_rav[p]
        if mxval_rav[pp] > mxval_rav[p]:
            mxval_rav[p] = mxval_rav[pp]
    return mxval


def ancestry(P, S, iS=-1):
    P_rav = P.ravel()
    p = S[iS]
    while True:
        yield p
        pp = P_rav[p]
        if pp == p:
            break
        p = pp


# old and broken
def calculate_index_moment_along_axis(P, S, Pa=None, axis=0, order=1, weight=None):
    if weight is None:
        weight = np.ones(P.shape)
    weight_rav = weight.ravel()
    ij = np.unravel_index(np.arange(S.size), P.shape)
    ii = ij[axis]
    jj = ij[1 - axis] * 1.0
    if Pa is None:
        Pa = parent_tree_along_axis(P, S, axis=axis)
    Pa_rav = Pa.ravel()
    jsum = (jj**order) * weight_rav
    jwght = weight_rav.copy()
    # for ip,p in enumerate(S[:0:-1]):
    for p in S[:0:-1]:
        ppa = Pa_rav[p]
        if ppa != p:
            jwght[ppa] += jwght[p]
            jsum[ppa] += jsum[p]
    jav = jsum / jwght
    return jav.reshape(P.shape), jwght.reshape(P.shape), Pa


# old and broken
def calculate_moment_along_axis_alt(P, S, Pa=None, axis=0, order=1, weight=None):
    if weight is None:
        weight = np.ones(P.shape)
    weight_rav = weight.ravel()
    ij = np.unravel_index(np.arange(S.size), P.shape)
    ii = ij[axis]
    jj = ij[1 - axis] * 1.0
    if Pa is None:
        Pa = parent_tree_along_axis(P, S, axis=axis)
    Pa_rav = Pa.ravel()
    jav = jj**order
    jwght = weight_rav.copy()
    # for ip,p in enumerate(S[:0:-1]):
    for p in S[:0:-1]:
        ppa = Pa_rav[p]
        if ppa != p:
            jav[ppa] = jav[ppa] * jwght[ppa] + jav[p] * jwght[p]
            jwght[ppa] += jwght[p]
            jav[ppa] /= jwght[ppa]
    return jav.reshape(P.shape), jwght.reshape(P.shape), Pa


def accumulate_on_tree(value, P, S):
    value_rav = value.ravel()
    accum = value_rav.copy()
    P_rav = P.ravel()
    for p in S[:0:-1]:
        pp = P_rav[p]
        accum[pp] += accum[p]
    return accum.reshape(P.shape)


# old and broken
# the following is wrong
def calculate_average_component_variance_along_axis(P, S, Pa=None, axis=0, weight=None):
    if weight is None:
        weight = np.ones(P.shape)
    weight_rav = weight.ravel()
    ij = np.unravel_index(np.arange(S.size), P.shape)
    ii = ij[axis]
    jj = ij[1 - axis] * 1.0
    if Pa is None:
        Pa = parent_tree_along_axis(P, S, axis=axis)
    iav, iwght, _ = calculate_moment_along_axis(P, S, Pa=Pa, axis=axis, weight=weight)
    iav = accumulate_on_tree(((jj - iav.ravel()) ** 2).reshape(P.shape) * weight, P, S)
    iav = iav / iwght
    return iav
