def distance_transform_axis(inp,axis=-1,**kwargs):
    import scipy
    if 'metric' in kwargs:
        raise KeyError('invalid keyword: metric')
    if axis < 0: axis = 2+axis
    if axis < 0 or axis > 1:
        raise ValueError('invalid axis value')
    metric = np.zeros((3,3),dtype=bool)
    metric[1,:] = True
    if axis == 1: metric = metric.T
    print(axis)
    print(metric)
    out = scipy.ndimage.distance_transform_cdt(inp, metric=metric, **kwargs)
    return out



def show_a_and_distance_transform_axis(a):
    figure(figsize=(12,3))

    ax=subplot(1,3,1)
    imshow(a,origin='lower',interpolation='none')
    title('a')
    colorbar()

    ax=subplot(1,3,2)
    imshow(distance_transform_axis(a, axis=0),origin='lower',interpolation='none')
    title('distance, axis=0')
    colorbar()

    ax=subplot(1,3,3)
    imshow(distance_transform_axis(a, axis=1),origin='lower',interpolation='none')
    title('distance, axis=1')
    colorbar()
    

a=np.zeros((7,9)); a[2:5,2:7] = 1
show_a_and_distance_transform_axis(a)

xa=np.arange(-10,11).reshape((1,21))
ya=xa.T
sl=0.5
a=np.abs(ya-xa*sl) < 3
show_a_and_distance_transform_axis(a)
