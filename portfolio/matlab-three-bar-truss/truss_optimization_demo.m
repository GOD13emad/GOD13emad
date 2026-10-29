function truss_optimization_demo()
% Independent, self-authored portfolio demonstration (NOT customer work).
% Three-bar pin-jointed planar truss; SI units and linear-elastic steel.
% Free joint C=(0,1) m is connected to three fully fixed support nodes:
% S1=(-1,0), S2=(1,0), S3=(0,2). The free joint has 2 DOF.
% Minimize member mass under displacement, axial-stress and area limits.
% MATLAB base functions only (fminsearch); no Optimization Toolbox.
% Verified output must be checked by a fresh run before any public claim.
% This tiny toy model does NOT validate client geometry or algorithms.
 E=210e9; rho=7850; P=[10000;-30000];
 supports=[-1,0;1,0;0,2]; free=[0,1];
 vec=free-supports;
 L=sqrt(sum(vec.^2,2));
 n=vec./L;
 maxDisp=0.12e-3; maxStress=120e6;
 minArea=100e-6; maxArea=4000e-6;
 baseline=[1200;1200;1200]*1e-6;
 [baseMass,baseU,baseStress,baseResidual]=analyse(baseline,E,rho,L,n,P);
 seeds=[1200,1200,1200;1000,1600,1000;1600,1000,1000;900,900,1900]';
 options=optimset('Display','off','MaxFunEvals',3500,'MaxIter',2200,...
                 'TolX',1e-10,'TolFun',1e-10);
 bestMass=inf; bestArea=[];
 for k=1:size(seeds,2)
   z0=log(seeds(:,k)*1e-6);
   fun=@(z) objective(z,E,rho,L,n,P,baseMass,maxDisp,maxStress,minArea,maxArea);
   [z,~,~]=fminsearch(fun,z0,options);
   A=min(max(exp(z),minArea),maxArea);
   [~,u,s,~]=analyse(A,E,rho,L,n,P);
   ratio=max([max(abs(u))/maxDisp;max(abs(s))/maxStress;1]);
   A=A*ratio*(1+2e-7);
   if any(A>maxArea) || any(A<minArea)
      continue
   end
   [mass,u,s,~]=analyse(A,E,rho,L,n,P);
   if max(abs(u))<=maxDisp*(1+1e-6) && ...
      max(abs(s))<=maxStress*(1+1e-6) && mass<bestMass
      bestMass=mass; bestArea=A;
   end
 end
 if isempty(bestArea)
   error('PORTFOLIO_DEMO:NoFeasibleSolution','No feasible optimum identified');
 end
 [optMass,optU,optStress,optResidual]=analyse(bestArea,E,rho,L,n,P);
 improved=100*(baseMass-optMass)/baseMass;
 assert(optResidual<1e-10 && baseResidual<1e-10,'Equilibrium failed');
 assert(max(abs(optU))<=maxDisp*(1+1e-6),'Displacement limit failed');
 assert(max(abs(optStress))<=maxStress*(1+1e-6),'Stress limit failed');
 assert(all(bestArea>=minArea) && all(bestArea<=maxArea),'Area bounds failed');
 assert(improved>1 && improved<100,'No meaningful mass improvement');
 fprintf('INDEPENDENT_TOY_DEMO PASS\n');
 fprintf('Model: three-bar 2D steel truss, free joint with 2 DOF\n');
 fprintf('Input load N: Fx=%g Fy=%g\n',P(1),P(2));
 fprintf('Baseline mass kg: %.6f\n',baseMass);
 fprintf('Optimized mass kg: %.6f\n',optMass);
 fprintf('Mass reduction percent: %.3f\n',improved);
 fprintf('Optimal areas mm2: %.3f %.3f %.3f\n',bestArea*1e6);
 fprintf('Max abs displacement mm: %.6f (limit %.6f)\n',...
    max(abs(optU))*1e3,maxDisp*1e3);
 fprintf('Max abs axial stress MPa: %.6f (limit %.6f)\n',...
    max(abs(optStress))/1e6,maxStress/1e6);
 fprintf('Relative equilibrium residual: %.3e\n',optResidual);
 fprintf('Scope: original synthetic demonstration only; not a client deliverable.\n');
end

function value=objective(z,E,rho,L,n,P,baselineMass,maxDisp,maxStress,Amin,Amax)
 A=exp(z);
 if any(~isfinite(A)) || any(A<1e-12) || any(A>1)
   value=1e12;return
 end
 try
   [mass,u,s,~]=analyse(A,E,rho,L,n,P);
   penalty=sum(max(0,abs(u)/maxDisp-1).^2)+...
           sum(max(0,abs(s)/maxStress-1).^2)+...
           sum(max(0,A/Amax-1).^2)+sum(max(0,Amin./A-1).^2);
   value=mass/baselineMass+1e5*penalty;
 catch
   value=1e12;
 end
end

function [mass,u,sigma,residual]=analyse(A,E,rho,L,n,P)
 K=zeros(2,2);
 for i=1:3
   K=K+(E*A(i)/L(i))*(n(i,:)'*n(i,:));
 end
 if ~all(isfinite(K(:))) || rcond(K)<1e-12
   error('PORTFOLIO_DEMO:SingularStiffness','Stiffness is invalid');
 end
 u=K\P;
 sigma=E*(n*u)./L;
 mass=rho*sum(A.*L);
 residual=norm(K*u-P)/max(norm(P),1);
end
