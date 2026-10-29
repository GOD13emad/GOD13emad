#!/usr/bin/env python3
"""Robust tuned mass damper design: original deterministic synthetic 2DOF study.
Not a commissioned or physically tested absorber. Requires NumPy and SciPy.
"""
import json
import numpy as np
from scipy.optimize import differential_evolution

m1=100.;m2=6.;zeta1=0.02;f0=8.;force=100.
freq=np.linspace(5.,12.,281)
omega=2*np.pi*freq
w0=2*np.pi*f0
primary_factors=np.array([0.95,1.,1.05])
def response(ratio,damping):
 w2=w0*ratio
 k2=m2*w2*w2
 c2=2*damping*m2*w2
 results=[]
 for pf in primary_factors:
  w1=w0*pf
  k1=m1*w1*w1
  c1=2*zeta1*m1*w1
  z1=k1+k2-omega**2*m1+1j*omega*(c1+c2)
  z2=k2-omega**2*m2+1j*omega*c2
  coupling=k2+1j*omega*c2
  det=z1*z2-coupling*coupling
  primary=np.abs(force*z2/det)
  baseline=np.abs(force/(k1-omega**2*m1+1j*omega*c1))
  results.append((primary,baseline))
 return results
def score(x):
 out=response(x[0],x[1])
 return max(float(a.max()) for a,b in out)
res=differential_evolution(score,bounds=[(0.78,1.12),(0.025,0.30)],seed=20261029,
                           popsize=12,maxiter=65,polish=True,tol=0.002,workers=1)
r,z=map(float,res.x)
pairs=response(r,z)
tuned_max=max(float(a.max()) for a,b in pairs)
baseline_max=max(float(b.max()) for a,b in pairs)
reduction=(baseline_max-tuned_max)/baseline_max*100
separate=[{"natural_frequency_factor":float(f),"baseline_peak_mm":float(b.max()*1000),"tuned_peak_mm":float(a.max()*1000)}
          for f,(a,b) in zip(primary_factors,pairs)]
assert res.success or res.fun<0.008, f"optimizer did not converge: {res.message}"
assert 0.78<=r<=1.12 and .025<=z<=.30
assert tuned_max<baseline_max*.8,reduction
assert all(row["tuned_peak_mm"]<row["baseline_peak_mm"] for row in separate)
assert all(np.all(np.isfinite(a)) for a,b in pairs)
output={"scope":"INDEPENDENT_SYNTHETIC_2DOF_ABSORBER_FREQUENCY_DOMAIN",
        "model":{"primary_mass_kg":m1,"absorber_mass_kg":m2,"primary_nominal_frequency_hz":f0,
                 "primary_damping_ratio":zeta1,"harmonic_force_N":force,
                 "frequency_sweep_hz":[float(freq[0]),float(freq[-1])],"frequency_points":int(freq.size)},
        "optimization":{"method":"scipy differential_evolution","tuned_frequency_ratio":r,
                        "absorber_damping_ratio":z,"max_absolute_peak_mm":tuned_max*1000},
        "baseline_worst_peak_mm":baseline_max*1000,
        "worst_case_peak_reduction_percent":reduction,
        "uncertainty_cases":separate,"pass_checks":True,
        "limitations":"Synthetic frequency-domain linear 2DOF system, no measured primary, nonlinearities, manufacturability, control hardware, test rig, fatigue or real client data."}
print(json.dumps(output,indent=2))
print("SYNTHETIC_2DOF_TMD_ROBUST_PASS")
