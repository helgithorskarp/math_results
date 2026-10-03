"""Regenerate complete new arithmetic certificates from own parent residual."""
import json,sys
from core import *
def main():
    P,D=input_polys();F=add(mul(derivative(P),D),mul(P,derivative(D)),-1)
    maps={}
    for label,pol,a,b,den in [('denominator',D,3,1,1),('derivative',F,11,2,2)]:
        transformed,d=affine(pol,a,b,den);s=shift_first(transformed,128)
        require(all(c>0 for c in s.values()) and s.get((0,0),0)>0,'entire quadrant '+label)
        maps[label]=dict(scale_exponent=d,coefficients=encode(s))
        print(label,len(s),flush=True)
    T,d=compact(P);T=shift_first(T,128)
    require(all(c<0 for c in T.values()) and T.get((0,0),0)<0,'entire compact interval')
    endpoint={e:c for e,c in T.items() if e[1]==d}
    require(endpoint.get((0,d),0)<0,'separate closed endpoint')
    maps['compact']=dict(q_degree=d,coefficients=encode(T),endpoint=encode(endpoint))
    print('compact',len(T),'endpoint',len(endpoint),flush=True)
    curves={}
    for norm,wanted in [(32,-1),(36,1)]:
        A,H=quotient_horner(P,norm);aa=ushift(A,128);hh=ushift(H,128);bb=ushift({j+1:c for j,c in H.items()},128)
        pairs=[[j,str(aa.get(j,0)),str(bb.get(j,0))] for j in sorted(set(aa)|set(bb),reverse=True)]
        require(all(wanted*c>0 for c in hh.values()) and wanted*hh.get(0,0)>0,'whole H curve '+str(norm))
        require(all(quad_sign(int(a),int(b))==wanted for j,a,b in pairs) and quad_sign(aa.get(0,0),bb.get(0,0))==wanted,'whole radical curve '+str(norm))
        curves[str(norm)]=dict(A=[[j,str(c)] for j,c in sorted(A.items(),reverse=True)],H=[[j,str(c)] for j,c in sorted(H.items(),reverse=True)],H_shift=[[j,str(c)] for j,c in sorted(hh.items(),reverse=True)],pairs=pairs)
        print('norm',norm,'H',len(hh),'pairs',len(pairs),flush=True)
    record=dict(domain={'k_min':128,'q_min':'3k'},P_hash=digest(P),D_hash=digest(D),derivative=encode(F),maps=maps,curves=curves,trust='ordinary interpretation and parent original matrix criterion external; all new coefficients regenerated')
    (HERE/'work').mkdir(exist_ok=True);(HERE/'work/certificate.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
if __name__=='__main__':main()
