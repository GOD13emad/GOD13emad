#!/usr/bin/env python3
"""Original reproducible synthetic benchmark: LQR vibration suppression.
One mechanical SDOF, sampled disturbance pulse, 27-parameter robustness check.
Not a commissioned controller or tested real hardware. Requires NumPy/SciPy.
"""
import json
import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.integrate import solve_ivp

mass=10.0; damping=12.0; stiffness=150.0
A=np.array([[0.,1.],[-stiffness/mass,-damping/mass]])
B=np.array([[0.],[1./mass]])
Q=np.diag([800000.,800.])
R=np.array([[0.1]])
S=solve_continuous_are(A,B,Q,R)
K=np.linalg.solve(R,B.T@S).reshape(-1)
assert np.min(np.linalg.eigvalsh(S))>0
assert np.all(np.real(np.linalg.eigvals(A-B@K[None,:]))<0)

t_eval=np.linspace(0,8,2001)
def run(m,c,k,controller):
    AA=np.array([[0.,1.],[-k/m,-c/m]])
    BB=np.array([0.,1./m])
    gain=K if controller else np.zeros_like(K)
    def ode(t,x,force):
        return AA@x+BB*(force-np.dot(gain,x))
    cut=np.searchsorted(t_eval,0.25,side="right")
    t1=t_eval[:cut];t2=t_eval[cut:]
    a=solve_ivp(lambda t,x:ode(t,x,100.),(0.,0.25),[0.,0.],rtol=1e-9,atol=1e-11,dense_output=True)
    b=solve_ivp(lambda t,x:ode(t,x,0.),(0.25,8.),a.sol(0.25),rtol=1e-9,atol=1e-11,dense_output=True)
    x=np.column_stack((a.sol(t1),b.sol(t2)))
    return x
p=run(mass,damping,stiffness,False)
c=run(mass,damping,stiffness,True)
base_peak=float(np.max(np.abs(p[0])))
controlled_peak=float(np.max(np.abs(c[0])))
reduction=float(100*(base_peak-controlled_peak)/base_peak)
max_ctrl=float(np.max(np.abs(K@c)))
assert controlled_peak<base_peak
assert max_ctrl<500.
assert reduction>5.
max_real_pole=-np.inf
for m in (8.,10.,12.):
  for d in (8.,12.,18.):
    for k in (120.,150.,180.):
      Ap=np.array([[0.,1.],[-k/m,-d/m]])
      Bp=np.array([[0.],[1./m]])
      max_real_pole=max(max_real_pole,float(np.max(np.real(np.linalg.eigvals(Ap-Bp@K[None,:])))))
assert max_real_pole<-0.05
out={"scope":"ORIGINAL_SYNTHETIC_MASS_SPRING_DAMPER_CONTROL_ONLY",
     "plant":{"mass_kg":mass,"damping_Ns_per_m":damping,"stiffness_N_per_m":stiffness,
              "disturbance_N":100,"pulse_seconds":0.25},
     "lqr_state_feedback_gain":K.tolist(),
     "open_loop_peak_displacement_mm":base_peak*1000,
     "controlled_peak_displacement_mm":controlled_peak*1000,
     "peak_displacement_reduction_percent":reduction,
     "peak_control_effort_N":max_ctrl,
     "robust_parameter_grid_cases":27,
     "worst_closed_loop_real_part":max_real_pole,
     "pass_checks":True,
     "limitations":"Linear SDOF synthetic simulation only; no actuator dynamics, saturation, sensor noise, sampling/latency, nonlinear plant or experimental validation."}
print(json.dumps(out,indent=2))
print("SYNTHETIC_LQR_ROBUST_GRID_PASS")
