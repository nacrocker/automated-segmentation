
def test_accumulate(a):
    return np.add.accumulate(a)

def test_accumulate_by_reduceat(a):
    indices = np.zeros(2 * len(a) - 1,dtype=int)
    indices[1::2] = range(1, len(a))
    return add.reduceat(a, indices)[::2]


from OMFITlib_utils import tmfun

import timeit

a=np.ones(100000)*1.0

tm_acc=tmfun(test_accumulate,a)
print('speed of accumulate: ',timeit.timeit(tm_acc,number=1))

tm_acc_redat=tmfun(test_accumulate_by_reduceat,a)
print('speed of accumulate by reduceat: ',timeit.timeit(tm_acc_redat,number=1))

print('same result: ',np.array_equiv(tm_acc.result,tm_acc_redat.result))
