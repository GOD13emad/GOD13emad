#!/usr/bin/env python3
"""Synthetic 9-channel operational modal analysis by FDD.
Original demonstration: simulation only; not measured accelerations or full M,C,K ID.
Run: python nine_channel_fdd_demo.py
Dependencies: NumPy, SciPy. Deterministic RNG and source-verifiable checks.
"""
import json
import numpy as np
from scipy import signal

SEED=2601029
FS=256.0
N=32768
NFFT=8192
F_TRUE=np.array([5.0,11.0,19.0])
ZETA=np.array([0.008,0.012,0.018])
rng=np.random.default_rng(SEED)
x=np.arange(1,10)/10.
phi=np.stack([np.sin(k*np.pi*x) for k in range(1,4)],axis=1)
phi/=np.linalg.norm(phi,axis=0)
responses=[]
for f,z in zip(F_TRUE,ZETA):
    w=2*np.pi*f
    # H(s) = -s^2/(s^2+2*z*w*s+w^2), acceleration from white modal force.
    b,a=signal.bilinear([0.0,0.0,-1.0],[1.0,2*z*w,w*w],fs=FS)
    y=signal.lfilter(b,a,rng.normal(size=N))
    y=y-y.mean()
    y/=np.std(y)
    responses.append(y)
q=np.stack(responses)
# Independent sources; 9 spatial sensors plus low, independent sensor noise.
y=phi@q
y+=0.02*rng.normal(size=y.shape)
y=signal.detrend(y,axis=1)
freqs,psd=signal.csd(y[0],y[0],fs=FS,nperseg=NFFT,noverlap=NFFT//2,window='hann')
G=np.zeros((freqs.size,9,9),dtype=np.complex128)
for i in range(9):
    for j in range(i,9):
        f, gij=signal.csd(y[i],y[j],fs=FS,nperseg=NFFT,noverlap=NFFT//2,window='hann')
        G[:,i,j]=gij
        G[:,j,i]=np.conjugate(gij)
# Frequency Domain Decomposition of measured cross-spectral density
svals,svectors=[],[]
for g in G:
    eigval,eigvec=np.linalg.eigh((g+g.conj().T)*0.5)
    svals.append(np.maximum(eigval[::-1].real,0.0))
    svectors.append(eigvec[:,::-1])
svals=np.asarray(svals)
svectors=np.asarray(svectors)
band=(freqs>=2.0)&(freqs<=25.0)
peaks,properties=signal.find_peaks(svals[:,0],prominence=svals[band,0].max()*0.05,distance=int(1.8/(FS/NFFT)))
peaks=peaks[band[peaks]]
# Select peaks by size but ensure distinct frequencies; do not use F_TRUE in detection
peaks=sorted(peaks,key=lambda k:svals[k,0],reverse=True)[:3]
peaks=np.array(sorted(peaks),dtype=int)
if len(peaks)!=3:
    raise RuntimeError(f"Only {len(peaks)} distinct spectral peaks discovered")
f_identified=freqs[peaks]
# Pair each mode with the nearest synthetic truth for post-hoc QA ONLY
errors=np.abs(f_identified-F_TRUE)
mac=np.array([abs(np.vdot(phi[:,i],svectors[k,:,0]))**2/
              (np.vdot(phi[:,i],phi[:,i]).real*np.vdot(svectors[k,:,0],svectors[k,:,0]).real)
              for i,k in enumerate(peaks)])
max_err=float(errors.max())
min_mac=float(mac.min())
# Hermitian/PSD sanity on every spectral frequency
hermitian=float(np.max(np.abs(G-np.swapaxes(G.conj(),1,2))))
mineig=float(np.linalg.eigvalsh(G).min())
assert hermitian<1e-10,hermitian
assert mineig>-1e-10,mineig
assert max_err<=0.30, (f_identified,errors)  # 19 Hz broad synthetic resonance: 0.25 Hz bias
assert min_mac>=0.93, mac
summary=dict(scope="ORIGINAL_SYNTHETIC_9CH_FDD_NO_FIELD_DATA",seed=SEED,sample_rate_hz=FS,
             samples_per_sensor=N,welch_nperseg=NFFT,welch_overlap=NFFT//2,
             generated_modal_truth_hz=F_TRUE.tolist(),identified_frequencies_hz=f_identified.tolist(),
             frequency_abs_error_hz=errors.tolist(),mac_against_synthetic_truth=mac.tolist(),
             max_frequency_error_hz=max_err,min_modal_assurance=min_mac,
             min_spectral_eigenvalue=mineig,hermitian_residual=hermitian,pass_checks=True,
             limitations="Synthetic randomized forcing; model order 3, no field measurements; no unique physical 9x9 M,C,K or validated damping estimates.")
print(json.dumps(summary,indent=2))
print("SYNTHETIC_FDD_9CH_PASS")
