class Cached_Computed_Attributes:
    '''mixin class with methods for managing cached computed attributes'''

    @staticmethod
    def cached_computed_attribute(attribute_name):
        def cached_computer_attribute_decorator(attribute_compute_method):

            def attribute_compute_method_with_caching(self):
                if self.is_cached(attribute_name):
                    ret = self.get_cached(attribute_name)
                    if not (ret is None): return ret

                attribute = attribute_compute_method(self)

                self.cache(attribute_name,attribute)
                return attribute

            return property(attribute_compute_method_with_caching)
        return cached_computer_attribute_decorator


    _listy_types = (list, tuple)
    def cache(self,attr,val):
        """Cache a computed attribute"""
        if (attr,str):
            setattr(self,'_'+attr,val)
            self._cached[attr]=attr
            return None

    @property
    def cached(self):
        """Get dictionary of cached computed attributes."""
        return {k:getattr(self,'_'+k) for k in self._cached.keys()}

    def list_cached(self):
        """Get names of cached computed attributes."""
        return self._cached.keys()

    def is_cached(self,attr):
        """Test if attribute or list of attribures is cached"""
        if isinstance(attr,self.__class__._listy_types):
            return [self.is_cached(a) for a in attr]

        if isinstance(attr,str):
            return attr in self._cached and hasattr(self,'_'+attr)

        #if this point is reached, something is wr

    def add_alias_to_cached(self,attr,alias):
        """Add alias or list of alias to attributes"""

        if isinstance(attr,self.__class__._listy_types) and isinstance(alias,self.__class__._listy_types) and len(attr) == len(alias):
            for a,al in zip(attr,alias): self.add_alias_to_cached(a,al)
            return None

        if isinstance(attr,str):
            if self.is_cached(attr) is None: raise KeyError(attr)
            self._cached[alias] = attr
            return None

        #if this point is reached, something is wrong.
        raise ValueError('attr should be attribute name or list of attribute names.')


    def is_alias_to_cached(self,attr):
        """Test if atrributes are aliass to other attributes."""
        if isinstance(attr,_listy_types):
            return [self.is_alias_to_cached(a) for a in attr]

        if isinstance(attr,str):
            if self.is_cached(attr) is None: raise KeyError(attr)
            return attr == self._cached[attr]

        #if this point is reached, something is wrong.
        raise ValueError('attr should be attribute be name or list of attribute names.')


    def dereference_alias(self,attr):
        """Dereference aliases to cached computed attributes. Non-aliases will deference to themselves."""
        if isinstance(attr,self.__class__._listy_types):
            return [self.dereference_alias(a) for a in attr]

        if isinstance(attr,str):
            if self.is_cached(attr) is None: raise KeyError(attr)
            return self._cached[attr]

        #if this point is reached, something is wrong.
        raise ValueError('attr should attribute name or list of attribute names.')


    def get_cached(self,attr):
        """Get cached computed attribute values"""
        if isinstance(attr,self.__class__._listy_types):
            return [self.get_cached(a) for a in attr]

        if isinstance(attr,str):
            if self.is_cached(attr) is None: raise KeyError(attr)
            return getattr(self,'_'+attr)

        #if this point is reached, something is wrong.
        raise ValueError('attr should be attribute name or list of attribute names.')


    def clear_cached(self,attr=None,all=False):
        """Clear cached computed attributes by name or list of names, or all by all=True."""
        def _safe_clear_cached(attr):
            if hasattr(self,'_'+attr): delattr(self,'_'+attr)
            if attr in self._cached: self._cached.pop(attr)

        if attr is None: return None

        if all:
            for a in attr: self.clear_cached(a)
            return None

        if isinstance(attr,self.__class__._listy_types):
            for a in attr: self.clear_cached(a)
            return None

        if isinstance(attr,str):
            if self.is_cached(attr) is None: raise KeyError(attr)
            _safe_clear_cached(attrs)
            return None

        #if this point is reached, something is wrong.
        raise ValueError('attr should be attribute name or list of attribute names, or all=True should be provided.')


class Max_Tree(Cached_Computed_Attributes):
    import numpy as np

    def __init__(self,image=None,connectivity=1):
        self._cached={}
        self._connectivity = connectivity
        if image is None:
            self._image=None
            self._connectivity=None
            self._P=None
            self._S=None
            return
        from skimage.morphology import max_tree as max_tree_ski
        self._image = image
        self._P,self._S = max_tree_ski(image, connectivity=self._connectivity)


    @property
    def image(self):
        """Get the max_tree image"""
        return self._image

    @property
    def P(self):
        """Get the max_tree parent matrix"""
        return self._P

    @property
    def S(self):
        """Get the max_tree traverser array"""
        return self._S

    @property
    def parent(self):
        """Get max_tree parent matrix"""
        return self.P

    @property
    def sorted_indices(self):
        """Get max_tree sorted_indices array"""
        return self.S

    @property
    def connectivity(self):
        """Get the max_tree connectivity."""
        return self._connectivity


    cached_computed_attribute=Cached_Computed_Attributes.cached_computed_attribute

    @cached_computed_attribute('C')
    def C(self):
        S = self.S
        P_rav = self.P.ravel()
        C_rav = [[] for _ in range(len(P_rav))]
        C = np.empty(self.image.shape,dtype=list)
        for p in S[1:]:
            q = P_rav[p]
            C_rav[q].append(p)
        C.ravel()[:]= C_rav[:]
        return C

    @cached_computed_attribute('children')
    def children(self):
        return self.C

    @cached_computed_attribute('canonicality')
    def canonicality(self):
        """Get the canonicality of each position in P, the parent matrix. i.e. whether it represens"""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        canonicality_rav = image_rav != image_rav[parent]
        p_root = sorted_indices[0]
        canonicality_rav[p_root] = True
        canonicality = np.reshape(canonicality_rav,self.P.shape)

        return canonicality



    @cached_computed_attribute('numcomponents')
    def numcomponents(self):
        """Get the number of components."""
        if self._image is None: return None

        numcomponents = np.sum(self.canonicality)
        return numcomponents



    @cached_computed_attribute('sorted_labels')
    def sorted_labels(self):
        """Get the component labels for each of the node in S, the sorted_indices array.
        Non-canonical nodes have a value equal to the negative of their canonical parent label.
        Label magnitudes increase from 0 starting at beginning of sorte_labels. """
        if self._image is None: return None

        sorted_labels=np.cumsum(self.canonicality[self.S])
        sorted_labels[~self.canonicality[self.S]] *= -1
        return sorted_labels


    @cached_computed_attribute('labels')
    def labels(self):
        """Get the component labels for each of the node in P, the parent matrix.
        Non-canonical nodes have a value equal to the negative of their canonical parent label."""
        if self._image is None: return None

        labels = self._P.copy()
        labels.ravel()[self.S] = self.sorted_labels

    @cached_computed_attribute('component_P_indices')
    def component_P_indices(self):
        """Get the indices (aka P-indices) in P, or the parent matrix, for the node correposonding to component to which the node belongs.
        For a canonical node, component_P_indices.ravel()[i] == i."""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        indices=np.reshape(np.arange(parent.size),self.P.shape)
        indices_rav=indices.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[q] == image_rav[p]: indices_rav[p]=indices_rav[q]

        return indices


    @cached_computed_attribute('order')
    def order(self):
        """Get the position within S, the sorted_indices array, of nodes in P, the parent matrix.
        In other words, for a node i in P.ravel(), S[order[i]] == i"""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        order = np.argsort(self.sorted_indices)

        return order


    @cached_computed_attribute('order_P_indices')
    def order_P_indices(self):
        """Get the order within S, the sorted_indices array, of the P-indices (component indices in P).
        For a canonical node i in P.ravel(), S[order_P_indices[i]] == i.
        For a non-canoncical node i in P.ravel(), S[order_P_indices[i]] == P.ravel[i]"""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        order = self.order

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[q] == image_rav[p]:
                order[p] = order[q]

        return order


    @cached_computed_attribute('numchildren')
    def numchildcomponents(self):
        """Get the number of child components for each comoenent node.
        Non-canonical nodes will have values which are the negative of the number of components for their parent component node."""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        numchildren = np.zeros(image.shape, dtype=int)
        numchildren_rav=numchildren.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[q] != image_rav[p]:
                numchildren_rav[q] += 1

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[q] == image_rav[p]:
                numchildren_rav[p] = -numchildren_rav[q]

        return numchildren

    @cached_computed_attribute('numchildnodes')
    def numchildnodes(self):
        """Get the number of children in the max-tree for each tree node (count includes non-canonical nodes)."""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        numchildren = np.zeros(image.shape, dtype=int)
        numchildren_rav=numchildren.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            numchildren_rav[q] += 1

        return numchildren

    @cached_computed_attribute('leaf_P_indices')
    def leaf_P_indices(self):
        """Get the P-indices of component leaf nodes. (Note that non-canonical nodes are leaf nodes but not component leave nodes.)"""
        if self._image is None: return None

        return np.flatnonzero(self.numchildnodes == 0)

    @property
    def leaves(self):
        """Alias for leaf_P_indices"""
        return self.leaf_P_indices

    @cached_computed_attribute('sorted_leaf_P_indices')
    def sorted_leaf_P_indices(self):
        """Get the P-indices ??? of component leaf nodes. (Note that non-canonical nodes are leaf nodes but not component leave nodes.)"""
        if self._image is None: return None

        return self.S[np.flatnonzero(self.numchildnodes.ravel()[self.S] == 0)]

    @cached_computed_attribute('peak')
    def peak(self):
        """Get the peak (max intensity) for each component."""
        if self._image is None: return None

        image = self._image
        parent = self._P.ravel()
        sorted_indices = self._S

        peak = image.copy()

        image_rav = image.ravel()
        peak_rav = peak.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[p] != image_rav[q]:
                peak_rav[q] = max(peak_rav[p], peak_rav[q])  # search maximum and propagate maximum to parent node
            else:
                # canonicalize value. this works because the sort_indices order will cause all
                # canonical children of q to be reached before non-canonical children
                peak_rav[p] = peak_rav[q]
        return peak


    @property
    def contrast(self):
        """Get the contrast for each component. contrast=max_over_component(intensity)/min_over_component(intensity)"""
        if self._image is None: return None

        contrast = ((self.peak).copy()).astype(np.float64)/self._image

        return contrast


    @property
    def log_contrast(self):
        """Get the log of contrast for each component. logContrast = log(max_over_component(intensity)) - log(min_over_component(intensity))."""
        if self._image is None: return None

        log_contrast = np.log(((self.peak).copy()).astype(np.float64))-np.log(self._image)

        return log_contrast


    @cached_computed_attribute('height')
    def height(self):
        """Get the height for each component.  Height = max_over_component(intensity)-min_over_component(intensity)"""
        if self._image is None: return None

        height = ((self.peak).copy()).astype(np.float64)-self._image

        return height

    @cached_computed_attribute('area')
    def area(self):
        """Get the area (number of pixels) for each component."""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        area = np.ones(image.shape, dtype=int)
        area_rav=area.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            area_rav[q] += area_rav[p]

        for p in sorted_indices[1:]:
            q = parent[p]
            if image_rav[p] == image_rav[q]:
                area_rav[p] = area_rav[q] # canonicalize value

        return area



    @cached_computed_attribute('volume')
    def volume(self):
        """Get the volume for each component. Volume = sum_over_component(intensity-min_over_parent_component(intensity))"""
        if self._image is None: return None

        image = self._image
        image_rav = image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S
        area = self.area
        area_rav=area.ravel()

        volume = np.zeros(image.shape, dtype=np.float64)
        volume_rav=volume.ravel()

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            if image_rav[p] != image_rav[q]:
                volume_rav[q] += area_rav[p]*(image_rav[p]-image_rav[q])+volume_rav[p]

        for p in sorted_indices[1:]:
            q = parent[p]
            if image_rav[p] == image_rav[q]:
                volume_rav[p] = volume_rav[q] # canonicalize value

        return volume


    @cached_computed_attribute('extents')
    def extents(self):
        """Get the extent (index ranges for each coordinate) for each component."""
        if self._image is None: return None

        image = self._image
        image_rav=image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S

        number_of_pixels = np.size(image)

        max_coord = np.array(np.unravel_index(np.arange(number_of_pixels), image.shape)).T
        min_coord = np.array(np.unravel_index(np.arange(number_of_pixels), image.shape)).T
        extents = np.ones((*image.shape,2),dtype=int)
        extents_rav = extents.reshape((number_of_pixels,2))

        for p in sorted_indices[:0:-1]:
            q = parent[p]
            max_coord[q] = np.maximum(max_coord[q], max_coord[p])
            min_coord[q] = np.minimum(min_coord[q], min_coord[p])
            extents_rav[q] = (max_coord[q] - min_coord[q]) + 1

        for p in sorted_indices[1:]:
            q = parent[p]
            if image_rav[p] == image_rav[q]:
                extents_rav[p] = extents_rav[q] # canonicalize value

        return extents

    @property
    def extension(self):
        """Get the maximum of all extents (index ranges for each coordinate) for each component."""
        if self._image is None: return None

        return np.max(self.extents,axis=2)

    @property
    def diameter(self):
        """Get diameter (alias for extension) for each component."""
        return self.extension


    def fill_components_from_markers(self,markers=None,unmarked=0,preserve_nesting=False):

        image = self._image
        if markers is None or not np.array_equal(markers.shape,image.shape):
            raise ValueError('markers should be matrix with same shape as image')

        image=self.image
        image_rav=image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S
        output = markers.copy()
        output_rav=output.ravel()

        if np.isnan(unmarked):
            for p in sorted_indices[:0:-1]:
                #if noncanonical node is marked, mark canonical parent
                q = parent[p]
                if image_rav[q] == imag_rav[p] and ~np.isnan(output_rav[p]): output_rav[q] = output_rav[p]

            for p in sorted_indices[1:]:
                q = parent[p]
                if ~np.isnan(output_rav[q]) and (not preserve_nesting or np.isnan(output_rav[p])) : output_rav[p] = output_rav[q]
        else:
            for p in sorted_indices[:0:-1]:
                #if noncanonical node is marked, mark canonical parent
                q = parent[p]
                if image_rav[q] == image_rav[p] and output_rav[p] != unmarked: output_rav[q] = output_rav[p]

            for p in sorted_indices[1:]:
                # is parent is marked, mark child.
                q = parent[p]
                if output_rav[q] != unmarked and (not preserve_nesting or output_rav[p] == unmarked): output_rav[p] = output_rav[q]

        return output


    def direct_filter(self,attribute='area',attribute_threshold=3):
        """Apply a direct filtering.

        This produces an image in which for all possible thresholds, each connected
        component has the specified attribute value greater than that threshold.
        This is the basic function called by :func:`area_opening`,
        :func:`diameter_opening`, and similar.

        For :func:`area_opening`, for instance, the attribute is the area.  In this
        case, an image is produced for which all connected components for all
        thresholds have at least an area (pixel count) of the threshold given by
        the user.

        Parameters
        ----------

        attribute : name of attribute or array of float with same shape as image
            that ontains the attributes computed for the max-tree.
        attribute_threshold : float
            The threshold to be applied to the attribute.
        """

        image = self._image

        isvalidattr = False
        if isinstance(attribute,str) and hasattr(self,attribute):
                attrtemp=getattr(self,attribute)
                if np.array_equal(attrtemp.shape,image.shape):
                    attribute=attrtemp
                    isvalidattr = True
        else:
            if np.array_equal(attribute.shape,image.shape): isvalidattr = True

        if not isvalidattr:  raise ValueError('attr should be attribute name or array with same shape as image')


        image_rav=image.ravel()
        parent = self._P.ravel()
        sorted_indices = self._S
        attribute_rav=attribute.ravel()

        output = image.copy()
        output_rav=output.reshape((size(image),*output.shape[2:]))

        p_root = sorted_indices[0]
        if attribute_rav[p_root] < attribute_threshold:
            output_rav[p_root] = 0
        else:
            output_rav[p_root] = image_rav[p_root]

        for p in sorted_indices[1:]:
            q = parent[p]

            # this means p is not canonical
            # in other words, it has a parent that has the
            # same image value.
            if image_rav[p] == image_rav[q]:
                output_rav[p] = output_rav[q]
                continue

            if attribute_rav[p] < attribute_threshold:
                # this corresponds to stopping
                # as the level of the lower parent
                # is propagated to the current level
                output_rav[p] = output_rav[q]
            else:
                # here the image reconstruction continues.
                # The level is maintained (original value).
                output_rav[p] = image_rav[p]

        return output

    def maxattrclosing(self,attr,return_nodes=False):
        """propagates maxiumum attr value along lineage from root back to leaf. For non-monotonic attributes, this fills any valley between highest value descendenent and leaf"""
        image_rav = self.image.ravel()
        S=self.S
        parent=self.P.ravel()
        maxattr = attr.copy()
        maxattr_rav=maxattr.ravel()
        if return_nodes:
            maxattrnodes = np.zeros(attr.shape,dtype=bool)
            maxattrnodes_rav = maxattrnodes.ravel()
            maxattrnodes_rav[S[0]] = True
            for p in S[1:]:
                q=parent[p]
                if image_rav[p] != image_rav[q]:
                    if maxattr_rav[p] >= maxattr_rav[q]:
                        #maxattr_rav[p] = maxattr_rav[p]
                        maxattrnodes_rav[p] = True
                        maxattrnodes_rav[q] = False
                    else:
                        maxattr_rav[p] = maxattr_rav[q]
                else:
                    maxattr_rav[p] = maxattr_rav[q] #canoicalize maxattr
            return (maxattr,maxattrnodes)
        else:
            for p in S[1:]:
                q=parent[p]
                if image_rav[p] != image_rav[q]:
                    maxattr_rav[p] = np.maximum(maxattr_rav[p],maxattr_rav[q])
                else:
                    maxattr_rav[p] = maxattr_rav[q] #canoicalize maxattr
            return maxattr

    def leafattrflatnodes(self,attr,attrthresh=None,mask=None):
        """marks nodes for components with flat attribute value around leaves (e.g. from area opening) """
        image_rav=self.image.ravel()
        S=self.S
        parent=self.P.ravel()
        flatnodes = self.numchildnodes == 0 # will only mark true leaves, not non-canonical nodes.
        if not attrthresh is None: flatnodes = flatnodes & (attr >= attrthresh)
        if not mask is None: flatnodes = flatnodes & mask
        flatnodes_rav = flatnodes.ravel()
        attr_rav=attr.ravel()
        for p in S[:0:-1]:
            q=parent[p]
            if flatnodes_rav[p] and attr_rav[q] == attr_rav[p]:
                #move flatzone node marker to parent of flatzone
                flatnodes_rav[q] = True
                flatnodes_rav[p] = False
        return flatnodes

    def leafattrflatzones(self,attr,attrthresh=None,mask=None):
        """marks zones of flat attribute value around leaves (e.g. from area opening) """
        image_rav=self.image.ravel()
        S=self.S
        parent=self.P.ravel()
        flatzones=self.numchildnodes == 0  # mark leaves
        if not attrthresh is None: flatzones = flatzones & (attr >= attrthresh)  #mark leaves with attr above threshold
        if not mask is None: flatzones = flatzones & mask  # filter markers with mask
        flatzones_rav=flatzones.ravel()
        attr_rav=attr.ravel()
        for p in S[:0:-1]:
            q=parent[p]
            if flatzones_rav[p] and attr_rav[q] == attr_rav[p]: # non-canonical node should never satify flatzones_rav[p] == True here
                flatzones_rav[q] = True # propate marker to parent with same value of attr (i.e. parent in flatzone of child)
            #if flatzones_rav[q] and image_rav[p] == image_rav[q]:
            ## noncanonical node takes on flatzone membership if canonical parent it is in flatzone.
            ## parent should already have membership established because of order of S
            #    flatzones_rav[p] = True
        for p in S[1:]:
            q = parent[p]
            if image_rav[p] == image_rav[q]:
                flatzones_rav[p] = flatzones_rav[q] # canonicalize value


        return flatzones

    def path_to_root_as_P_indices(self,P_index):
        """Get path from node to root as P-indices"""
        if self._image is None: return None
        P_rav=self.P.ravel()
        def pathfrom(q):
            p = None
            while q != p:
                yield q
                p = q
                q = P_rav[p]

        return np.fromiter(pathfrom(P_index),int)

    def isdescendent(self,node=None,of=None):
        "Tests if node is descendent of another node. If nodes are non-canonical, their canonical parents are tested."
        if self._image is None: return None

        numP=self.P.size
        if not np.issubdtype(type(node),np.integer) or not node in range(numP):
             raise ValueError(f'"node" argument should be P-index , an integer in range({numP}).')
        if not np.issubdtype(type(of),np.integer) or not of in range(numP):
             raise ValueError(f'"of" argument should be P-index label, an integer in range({numP}).')


        P_rav=self.P.ravel()
        image_rav=self.image.ravel()
        S = self.S

        qof = P_rav[of]
        if of != S[0] and image_rav[of] == image_rav[qof]: of = qof

        if of == S[0]: return node != S[0]

        qnode = P_rav[node]
        if node != S[0] and image_rav[node] == image_rav[qnode]: node = qnode


        order = self.order.ravel()

        oforder=order[of]
        ancestor = node
        oldancestor = None
        while order[ancestor] >= oforder:
            oldancestor = ancestor
            ancestor = P_rav[oldancestor]

        return order[ancestor] == oforder


    def markancestors(self,nodes):
        image_rav=self.image.ravel()
        P_rav=self.P.ravel()
        ancestors=np.zeros(self.image.shape,dtype=bool)
        ancestors_rav=ancestors.ravel()

        for n in nodes:
            qn = P_rav[n]
            if image_rav[qn] == image_rav[n]: qn = P_rav[qn]
            while not ancestors_rav[qn] and qn != n:
                ancestors_rav[qn] = True
                n = qn
                qn = P_rav[n]
        return ancestors


    def maxattrnodes(self,attr,allchildren=True):
        """Find nodes which are local maxima of attr value along lineage. A maximum passes two tests:
        (1) attr.ravel()[parent] < attr.ravel()[node]
        (2) if allchildren:
              attr.ravel()[node] >= attr.ravel[child] for all children.
            else:
              attr.ravel()[node] >= attr.ravel[child] for any child.
        """
        S=self.S
        P_rav=self.P.ravel()
        image_rav=self.image.ravel()
        attr = attr.copy()

        attr_rav=attr.ravel()
        isnoncanonical = image_rav == image_rav[P_rav]
        attr_rav[isnoncanonical] = attr_rav[P_rav[isnoncanonical]] # canonicalize attr

        maxattrnodes=np.zeros(self.image.shape,dtype=bool)
        maxattrnodes_rav = maxattrnodes.ravel()

        ##Vectorized, faster code than for-loops below:
        maxattrnodes_rav[:] = (attr_rav[P_rav] <= attr_rav) & ~isnoncanonical
        if allchildren:
            np.logical_and.at(maxattrnodes_rav,P_rav,attr_rav[P_rav]>attr_rav)
        else:
            np.logical_or.at(maxattrnodes_rav,P_rav,attr_rav[P_rav]>attr_rav)

        return maxattrnodes

        ##Equivalent to, but slower than, vecotrized code above:
        #for p in S[1:]:
        #    q = P_rav[p]
        #    maxattrnodes_rav[p] = attr_rav[q] < attr_rav[p]
        #
        #if allchildren:
        #    for p in S[1:]:
        #        q = P_rav[p]
        #        maxattrnodes_rav[q] = maxattrnodes_rav[q] and attr_rav[q] >= attr_rav[p]
        #else:
        #    for p in S[1:]:
        #        q = P_rav[p]
        #        maxattrnodes_rav[q] = maxattrnodes_rav[q] or attr_rav[q] >= attr_rav[p]
        #return maxattrnodes



    def priorityprunenodes(self,nodeinds):
        """Given a list of nodes (by P-index) in order of increasing priorty, nodes with higher priority ancestors or decendents will be pruned."""
        from collections import deque

        image_rav=self.image.ravel()
        P_rav=self.P.ravel()
        nodes = np.zeros(self.P.shape,dtype=bool)
        nodes_rav = nodes.ravel()
        nodes_rav[nodeinds] = True
        children = self.children
        children_rav=children.ravel()
        occluded_rav=np.zeros(P_rav.shape,dtype=bool)

        for p in nodeinds[::-1]:
            q = P_rav[p]
            if image_rav[q] == image_rav[p]: # only deal with canonical nodes. no effect if node is actually root.
                p,q = q,P_rav[p]
            if occluded_rav[p]: continue # this maximum was eliminated in previous iteration
            pmax = p
            while not occluded_rav[q] and q != p:
                occluded_rav[q] = True
                p = q
                q = P_rav[p]

            #childqueue=children_rav[p][:]
            childqueue=deque(children_rav[pmax])
            while childqueue:
                c = childqueue.popleft()
                occluded_rav[c] = True
                childqueue.extend(children_rav[c])

        nodes_rav[:]&=~occluded_rav

        return np.flatnonzero(nodes_rav)

    def optimummaxattrnodes(self,attr,maxattrnodes=None):
        """Given a boolean matrix (maxattrnodes) where nodes with maximum attribute value are True, eliminate suboptimum maxima,
        which have any of these propterties:
        1) an descendent maximum with higher or equal value
        2) an ancestor maximum with higher value that has no descendent maximum with even higher value
        If maxattrnodes argument is None, then calculate it."""

        from collections import deque

        image_rav=self.image.ravel()
        P_rav=self.P.ravel()
        if maxattrnodes is None:
            maxattrnodes = self.maxattrnodes(attr)
        else:
            maxattrnodes = maxattrnodes.copy()
        attr_rav=attr.ravel()
        maxattrnodes_rav = maxattrnodes.ravel()
        maxattrndinds = np.flatnonzero(maxattrnodes_rav)
        maxattrndinds = maxattrndinds[np.argsort(attr_rav[maxattrndinds])]
        children = self.children
        children_rav=children.ravel()
        occluded_rav=np.zeros(P_rav.shape,dtype=bool)

        for p in maxattrndinds[::-1]:
            q = P_rav[p]
            if image_rav[q] == image_rav[p]: # only deal with canonical nodes. no effect if node is actually root.
                p,q = q,P_rav[p]
            if occluded_rav[p]: continue # this maximum was eliminated in previous iteration
            pmax = p
            while not occluded_rav[q] and q != p:
                occluded_rav[q] = True
                p = q
                q = P_rav[p]

            #childqueue=children_rav[p][:]
            childqueue=deque(children_rav[pmax])
            while childqueue:
                c = childqueue.popleft()
                occluded_rav[c] = True
                childqueue.extend(children_rav[c])

        maxattrnodes_rav[:]&=~occluded_rav

        return maxattrnodes


    def accumulate_attribute_from_leaf_to_root(self,attr):
        """get the accumulated value of attr when walking tree from leaft to root. gives area if attr == np.ones(self.image.shape)"""
        image = self.image
        image_rav=image.ravel()
        P_rav = self.P.ravel()
        S = self.S
        acc=attr.copy()
        acc_rav = acc.reshape((np.size(image),*acc.shape[2:]))

        for p in S[:0:-1]:
            q = P_rav[p]
            acc_rav[q]+=acc_rav[p]

        for p in S[1:]:
            q = P_rav[p]
            if image_rav[p] == image_rav[q]:
                acc_rav[p] = acc_rav[q] # canonicalize value

        return acc


max_tree = Max_Tree
