"""Optional bounded NumPy discovery for the closed RID receiving triangle.

Six receiving and ten source Bernstein coefficients per quadratic cut.
No floating positivity is accepted as a theorem; exact replay is required.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    if os.environ.get(key)!='1':raise RuntimeError('all numerical threads must be one')
from pathlib import Path
from time import monotonic
import argparse,hashlib,json,platform,resource
import numpy as np
from geometry import build,OUT
from domain import make_domain
from forest import write_certificate


def approximate(x):return float(x.a)+float(x.b)*((1+5**0.5)/2)
def vec(v):return np.array([approximate(x) for x in v])


def receiving_cut_matrices(data,domain):
    R=np.array([vec(x) for x in domain['R']]);pairs=[(i,j) for i in range(3) for j in range(i,3)]
    result=[]
    for cut in data['cuts']:
        block=[]
        if cut['kind']=='support':
            support=domain['supports'][cut['support']];E=vec(support['E']);v=vec(cut['v'])
            raw=[np.cross(E,r) for r in R];H=np.array([approximate(x) for x in support['H']])
            for i,j in pairs:
                L=(raw[i]+raw[j])/2;h=(H[i]+H[j])/2;a=np.dot(L,v);f=np.cross(v,L)
                M=np.zeros((4,4));M[0,0]=a-h;M[0,1:]=M[1:,0]=f
                M[1:,1:]=np.outer(L,v)+np.outer(v,L)-(a+h)*np.eye(3);block.append(M)
        else:
            k=vec(cut['k']);lines=[np.concatenate(([np.dot(r,k[1:])],k[0]*r+np.cross(k[1:],r))) for r in R]
            for i,j in pairs:
                M=(np.outer(lines[i],lines[j])+np.outer(lines[j],lines[i]))/2
                M[0,0]-=np.dot(R[i],R[j]);block.append(M)
        result.append(block)
    return np.array(result)


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,required=True);args=parser.parse_args()
    if args.output.resolve().parent==OUT.resolve():raise ValueError("discovery output belongs outside the public source directory")
    start=monotonic();data=build();domain=make_domain(data);geometry_seconds=monotonic()-start
    matrices=receiving_cut_matrices(data,domain);flat=matrices.reshape(540*6,16)
    roots=[np.array([vec(v) for v in T]) for T in domain['roots']]
    pairs=[(i,j) for i in range(4) for j in range(i,4)];edges=[(i,j) for i in range(4) for j in range(i+1,4)]
    queue=[(ri,'',T) for ri,T in reversed(list(enumerate(roots)))]
    nodes=[];leaves=[];visited=0;max_depth=0;reason=None;minimum_margin=float('inf')
    while queue:
        if visited>=10000:reason='node cap';break
        if monotonic()-start>=12:reason='soft wall-time guard';break
        ri,path,T=queue.pop();visited+=1;max_depth=max(max_depth,len(path))
        if float(np.max(np.einsum('ij,ij->i',T,T)))<1/625-1e-12:
            leaves.append({'root':ri,'path':path,'kind':'local'});continue
        q=np.concatenate([np.ones((4,1)),T],axis=1)
        features=np.array([np.outer(q[i],q[j]).reshape(16) for i,j in pairs]).T
        coeff=(flat@features).reshape(540,6,10);minima=np.min(coeff,axis=(1,2))
        cut=int(np.argmax(minima));margin=float(minima[cut])
        if margin>1e-9:
            leaves.append({'root':ri,'path':path,'kind':data['cuts'][cut]['kind'],'cut':cut})
            minimum_margin=min(minimum_margin,margin);continue
        if len(path)>=40:queue.append((ri,path,T));reason='depth cap';break
        i,j=max(edges,key=lambda e:(float(np.dot(T[e[0]]-T[e[1]],T[e[0]]-T[e[1]])),-edges.index(e)))
        mid=(T[i]+T[j])/2;left=T.copy();right=T.copy();left[j]=mid;right[i]=mid
        nodes.append({'root':ri,'path':path,'edge':[i,j]})
        queue.append((ri,path+'1',right));queue.append((ri,path+'0',left))
    state={'schema':'private-rid-triangle-source-forest-v1','agent':'six-rupert-3','role':'researcher',
           'status':'complete floating proposal; exact verification required' if not queue else 'INCOMPLETE floating proposal',
           'termination_reason':reason,'exact_receiving_domain':domain['record'],
           'proposal_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'model_source_sha256':hashlib.sha256((OUT/'geometry.py').read_bytes()).hexdigest(),
           'domain_source_sha256':hashlib.sha256((OUT/'domain.py').read_bytes()).hexdigest(),
           'python':platform.python_version(),'numpy':np.__version__,
           'thread_count':1,'limits':{'node_cap':10000,'soft_seconds':12,'max_depth':40,'external_seconds':20},
           'visited':visited,'internal_nodes':nodes,'leaves':leaves,
           'pending':[{'root':ri,'path':path,'approximate_vertices':T.tolist()} for ri,path,T in queue],
           'maximum_depth':max_depth,'minimum_proposed_tensor_coefficient':None if minimum_margin==float('inf') else minimum_margin,
           'geometry_seconds':round(geometry_seconds,3),'seconds':round(monotonic()-start,3),
           'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'no_mathematical_nonexistence_claim':True}
    if queue:
        args.output.with_suffix('.incomplete.json').write_text(json.dumps(state,separators=(',',':'))+'\n')
    else:
        args.output.write_text(write_certificate(state))
    print(json.dumps({k:state[k] for k in ['status','termination_reason','visited','maximum_depth','minimum_proposed_tensor_coefficient','geometry_seconds','seconds','peak_kib']}|{
        'internal_nodes':len(nodes),'leaves':len(leaves),'pending':len(queue),
        'certificate_sha256':None if queue else hashlib.sha256(args.output.read_bytes()).hexdigest(),
        'certificate_bytes':None if queue else args.output.stat().st_size}))


if __name__=='__main__':main()
