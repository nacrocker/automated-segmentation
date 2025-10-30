import numpy as np
class AllCloseComparable(np.ndarray):
    def __new__(cls, input_array, rtol=None, atol=None, equal_nan=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.rtol = rtol
        obj.atol = atol
        obj.equal_nan = equal_nan
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.rtol = getattr(obj, 'rtol', None)
        self.atol = getattr(obj, 'atol', None)
        self.equal_nan = getattr(obj, 'equal_nan', None)

    def __eq__(self,other):
        import numpy as np
        kw = {k:v for k,v in dict(rtol=self.rtol,atol=self.atol,equal_nan=self.equal_nan).items() if not v is None}
        return np.allclose(self,other, **kw)

a=AllCloseComparable(np.arange(3),atol=1e-5)
b=AllCloseComparable(np.arange(3))+1e-4

print(a == b)
