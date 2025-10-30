# root = OMFIT['ModeTimeDependence']
from OMFITlib_math_utils import view_complex_as_float, view_float_as_complex, complex_multivariate_normal_noise, mode_with_random_phase
from OMFITlib_sigarraycov_utils import Vec2Cov

import numpy as np

# mimic "HN" bdot array on NSTX with comparable but made up paramenters.  Still need to look up actual paremeters.




siglocsdeg0 = (np.array([0.0, 10.0, 30.0]).reshape(1, 3) + np.arange(0, 360, 90).reshape(4, 1)).flatten()  # degrees
sigareas0 = np.array([1.0, 1.1, 1.05, 0.9, 0.98, 1.2, 1.15, 1.1, 0.95, 0.93, 1.21, 1.14])

# only using subset of array
sigusing = np.arange(10)
nsig = sigusing.size
siglocsdeg = siglocsdeg0[sigusing]
sigareas = sigareas0[sigusing]
siglocsrad = siglocsdeg * np.pi / 180.0


def tryout_mode_with_noise_covariance():
    # randnumgen = np.random.default_rng()
    # from scipy.linalg import block_diag

    imgshape = (100, 100)

    modenum = 4
    modeampl = 1.0
    # modephase = randnumgen.uniform(low=0, high=2*np.pi, size=imgshape+(1,))
    # mode0 = modeampl*np.expand_dims(np.exp(1j*modenum*siglocsrad),axis=(0,1))*np.exp(1j*modephase)
    mode0 = modeampl * mode_with_random_phase(modenum, siglocsrad, size=imgshape)

    noisesigma = 0.01
    # noisecov = noisesigma*np.eye(nsig)
    # imgnoise = view_float_as_complex(randnumgen.multivariate_normal(np.zeros((2*nsig,)), 0.5*block_diag(noisecov,noisecov), imgshape).reshape(imgshape+(nsig,2)))
    imgnoise = complex_multivariate_normal_noise(cov=noisesigma, nvars=nsig, size=imgshape)
    mode = mode0 + imgnoise

    mode0cov = np.mean(Vec2Cov(mode0), axis=(0, 1))
    modecov = np.mean(Vec2Cov(mode), axis=(0, 1))
    with np.printoptions(precision=2, linewidth=120):
        # print(abs(mode0cov))
        print(abs(modecov))
        # print(np.linalg.eigvalsh(mode0cov))
        evmc = np.linalg.eigvalsh(modecov)
        print(evmc)
        print(np.trace(modecov).real / evmc[-1])
        print(np.trace(modecov).real ** 2 / np.sum(np.abs(modecov) ** 2), np.sum(evmc) ** 2 / np.sum(evmc**2))
        # np.sum(np.abs(modecov)**2) == np.trace(modecov@np.conj(modecov.T)).real, but with fewer calculations
        # np.sum(np.abs(modecov)**2) == np.trace(modecov@np.conj(modecov.T)).real, but with fewer calculations


# tryout_mode_with_noise_covariance()

ntrials = 1000
nsamps = 100
size = (ntrials, nsamps)

# modenum=4
# modeampl = 1.0
# mode0 = modeampl*mode_with_random_phase(modenum,siglocsrad,size=size)

noisesigma = 1
noise = complex_multivariate_normal_noise(cov=noisesigma, nvars=nsig, size=size)
# mode = mode0+noise
# modecov=np.mean(Vec2Cov(mode),axis=(0,1))

noisecov = np.mean(Vec2Cov(noise), axis=1)
noisecovsigma = np.std(Vec2Cov(noise), axis=1) / np.sqrt(noise.shape[1])
with np.printoptions(precision=2, linewidth=130):
    print('abs(mean_over_trials(mean_over_samples(noise_signal_covariance))):')
    print(np.abs(np.mean(noisecov, axis=0)))
    print('std_over_trials(mean_over_samples(noise_signal_covariance)):')
    print(np.std(noisecov, axis=0))
    print('rms_over_trials(std_over_samples(noise_signal_covariance)/sqrt(nsamps)):')
    print(np.sqrt(np.mean(np.abs(noisecovsigma) ** 2, axis=0)))

evnoise = np.linalg.eigvalsh(noisecov)
import matplotlib.pyplot as plt

plt.figure(figsize=[11, 4], layout='constrained')
ax = plt.subplot(1, 2, 1)
plt.hist(np.mean(evnoise, axis=1), label='average eigenvalue', bins=np.floor(np.sqrt(ntrials)).astype(int), density=True)
plt.hist(evnoise[:, -1], label='largest eigenvalue', bins=np.floor(np.sqrt(ntrials)).astype(int), density=True)
plt.legend()
ax = plt.subplot(1, 2, 2)
iesrt = np.argsort(evnoise[:, -1])
plt.plot(evnoise[iesrt, -1], (np.arange(len(iesrt)) + 1) / len(iesrt), label='CDF of largest eigenvalue')
plt.legend()
