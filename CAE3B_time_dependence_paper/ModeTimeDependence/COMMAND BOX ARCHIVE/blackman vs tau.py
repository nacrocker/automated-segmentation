def blkmnt(M):
    n = arange(1-M, M, 2)
    tau = n/(M-1)/2 + 0.5
    return 0.42 + 0.5*cos(2*np.pi*(tau-0.5)) + 0.08*cos(4.0*np.pi*(tau-0.5))

def blkmn(M):
    n = arange(1-M, M, 2)
    return 0.42 + 0.5*cos(pi*n/(M-1)) + 0.08*cos(2.0*pi*n/(M-1))

print(np.array_equiv(blkmn(10),np.blackman(10)))
#True
print(np.array_equiv(blkmn(11),np.blackman(11)))
#True

#envlf = lambda tau: 0.42 + 0.5*cos(2*np.pi*(tau-0.5)) + 0.08*cos(4*np.pi*(tau-0.5)) #0 <= tau <= 1
#Mtaus = lambda M: (np.arange(1-M, M, 2)/(M-1)/2) + 0.5
#allclosefortype = lambda a,b,safety_factor=2.0: np.allclose(a,b,1+np.finfo(b[0]).resolution*safety_factor,np.finfo(b[0]).resolution*safety_factor)
from  OMFITlib_math_utils import allclosefortype, taus_for_Mpoint_blackman, blackman_vs_tau
envlf = blackman_vs_tau
Mtaus = taus_for_Mpoint_blackman

print(np.array_equiv(blkmn(10),blkmnt(10)))
#False
print(np.array_equiv(envlf(Mtaus(10)),blkmnt(10)))
#True
print(allclosefortype(blkmn(10),blkmnt(10)))
#True
print(allclosefortype(envlf(Mtaus(10)),np.blackman(10)))
#True
print(allclosefortype(envlf(Mtaus(10)),blkmn(10)))
#True


print(allclosefortype(envlf(Mtaus(10.1)),np.blackman(10.1)))
#True
