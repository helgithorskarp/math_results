from pathlib import Path
import json,time
import numpy as np
import cvxpy as cp
P=Path(__file__).resolve().parent
z=np.load(P/'M10_sevendeck.npz');z2=np.load(P/'M10_integer_moments.npz');A=np.concatenate([z['A'],z2['A']]);Q=[z[f'Q{i}'] for i in range(5)]+[z2[f'Q{i}'] for i in range(16)];z3=np.load(P/'M10_full_squares.npz');Q += [z3[f'Q{i}'] for i in range(35)];r,c=A.shape
rs=np.maximum(1,np.max(np.abs(A),axis=1));qs=[max(1,int(np.max(np.abs(q)))) for q in Q]
y=cp.Variable(r,nonneg=True);Z=[cp.Variable(q.shape[1:],PSD=True) for q in Q];t=cp.Variable();co=(A/rs[:,None]).T@y
for q,scale,v in zip(Q,qs,Z):co+=q.reshape(c,-1)/scale@cp.reshape(v,(v.shape[0]**2,),order='C')
prob=cp.Problem(cp.Minimize(t),[co<=t,cp.sum(y)+sum(cp.trace(v) for v in Z)==1])
print('model',r,c,[q.shape[1] for q in Q],qs,flush=True);start=time.monotonic()
value=prob.solve(solver='CLARABEL',verbose=True,max_iter=300)
out={'status':prob.status,'value':float(value),'seconds':time.monotonic()-start,'rows':r,'variables':c,'row_scales':rs.tolist(),'matrix_scales':qs,'y':None if y.value is None else y.value.tolist(),'matrices':[None if v.value is None else v.value.tolist() for v in Z],'solver':prob.solver_stats.solver_name,'solver_iterations':prob.solver_stats.num_iters,'density':None if prob.constraints[0].dual_value is None else prob.constraints[0].dual_value.tolist(),'claim':'Discovery only; requires exact certificate check.'}
(P/'discovery.json').write_text(json.dumps(out)+'\n');print('RESULT',out['status'],out['value'],out['seconds'],flush=True)
