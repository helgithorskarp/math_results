"""Fresh exact original-matrix affine audit of signed declarative input."""
import json
from pathlib import Path
from fractions import Fraction as Q
from affine import C,add,scale,dimensions,labels,table,numeric_table,energy_ordered,energy_unordered,det,sigma


def require(test,reason):
    if not test:raise ValueError(reason)


def audit(inp,old):
    require(inp['n']==26 and old['n']==24,'original ground sizes')
    names,pairs=labels();require(inp['names']==names and len(pairs)==30,'complete declared real face')
    require(inp['active']==[8,9,10,11,12],'declared active transport labels')
    B,e,ell=table();N,s,h=dimensions(26);const=lambda c:[c]+[0]*36
    require((N,s,h)==(67108837,33554406,33554431),'original dimensions')
    for a in range(25):
        for b in range(25):require(B[a][b]==B[b][a],'all original symmetry coefficients')
    for j in range(37):
        x=[0]*36
        if j:x[j-1]=1
        BB,ee,ll=numeric_table(x)
        for a in range(25):
            for b in range(25):
                require(BB[a][b]==B[a][b][0]+(B[a][b][j] if j else 0),'two full class recoveries')
        for a in range(25):require(ee[a]==e[a][0]+(e[a][j] if j else 0),'all actual empty entries')
        require(ll==ell[0]+(ell[j] if j else 0),'actual empty loop')
    for a in range(1,25):
        row=add(e[a],const(s));star=[0]*37
        for b in range(1,25):
            row=add(row,scale(C(26-a,b),B[a][b]))
            star=add(star,scale(C(25-a,b-1),B[a][b]))
        require(row==const(N),'all original nonempty rows')
        require(star==const(s),'all outside-point stars')
    erow=ell[:];estar=[0]*37
    for a in range(1,25):
        erow=add(erow,scale(C(26,a),e[a]));estar=add(estar,scale(C(25,a-1),e[a]))
    require(erow==const(N) and estar==const(s),'empty row AND empty point-stars')
    u=inp['integer_layer_direction'];v=inp['old_integer_layer_direction']
    require(len(u)==len(v)==24 and all(type(z)is int for z in u+v),'two full integral layer profiles')
    eu=energy_ordered(B,u);ev=energy_ordered(B,v)
    require(eu==energy_unordered(B,u) and ev==energy_unordered(B,v),'ordered versus factorial unordered energies')
    mu=inp['old_direction_weight'];w=inp['empty_direction_weight'];lam=inp['deficit_difference_weights']
    require(type(mu)is int and type(w)is int and len(lam)==6 and all(type(t)is int and t>0 for t in [mu,w]+lam),'positive integral PSD weights')
    cut=add(add(eu,scale(mu,ev)),scale(w,ell))
    for j in range(6):cut[j+1]+=2*lam[j]
    expected=[Q(inp['full36_affine_cut_intercept'])]+list(map(Q,inp['full36_affine_cut_coefficients']))
    require(cut==expected and cut[1:7]==[0]*6,'complete exact proper-only cut, all six cancellations')
    full=(1<<26)-1;AA=[(1<<i)-1 for i in range(8,14)];TT=[full^a for a in AA]
    rows=[0,1,1+sum(1<<j for j in range(2,9))]+AA
    def f(mask,z):return 0 if not mask else z[mask.bit_count()-1]*((1 if mask&1 else 0)-(1 if mask&2 else 0))
    minor=[[f(a,u),f(a,v),int(a==0)]+[int(a==aa)-int(a==tt) for aa,tt in zip(AA,TT)] for a in rows]
    require(det(minor)==-1575,'original nine-column nonzero minor')
    require(len(set(rows))==9 and all(a.bit_count()<=24 for a in rows+AA+TT),'all rank and difference vertices are original')
    for j,a in enumerate(range(8,14)):
        require(add(const(2*s),scale(-2,B[a][26-a]))==[0]+[2*int(k==j) for k in range(36)],'six literal complement differences')
    oldpairs=[tuple(map(int,t[1:].split('_'))) for t in old['names'][6:]]
    require(old['names'][:6]==['d'+str(i)for i in range(7,13)] and len(old['values'])==36,'credited n24 input census')
    require([(a+1,b+1)for a,b in oldpairs]==pairs,'all thirty shifted proper labels')
    transported=[Q(value)*sigma(26,a+1,b+1)/sigma(24,a,b) for value,(a,b) in zip(old['values'][6:],oldpairs)]
    require(transported==list(map(Q,inp['fixed_transported_proper_values'])),'all exact normalized transport values')
    P0=cut[0]+sum(k*t for k,t in zip(cut[7:],transported))
    require(P0==Q(inp['strict_negative_fixed_slice_pairing']) and P0<0,'whole exact strict-negative slice pairing')
    norms=[2*sum(C(24,a-1)*z[a-1]**2 for a in range(1,25))for z in (u,v)]+[1]+[2]*6
    weights=[1,mu,w]+lam; tau=sum(a*b for a,b in zip(weights,norms))
    W=sum(abs(k)*sigma(26,a,b)for k,(a,b)in zip(cut[7:],pairs))
    require(tau>0 and W>0,'quantitative denominators')
    rho=-P0/tau;Gamma=-P0/W
    require(rho>0 and Gamma>0,'quantitative original negative eigenvalue and normalized repair distance')
    return {'schema':'six-reviewer-1/original-n26-affine-audit-v1','agent':'six-reviewer-1','role':'independent mathematical reviewer','N':N,'s':s,'h':h,'names':names,'B':B,'empty_entries':e,'empty_loop':ell,'energy_u':eu,'energy_v':ev,'cut':cut,'rank_minor_rows':rows,'rank_minor':minor,'rank_minor_determinant':str(det(minor)),'rank_Y':9,'transported_values':list(map(str,transported)),'P0':str(P0),'nine_squared_original_norms':norms,'nine_positive_weights':weights,'trace_Y':tau,'normalized_coefficient_l1':str(W),'negative_eigenvalue_gap_rho':str(rho),'necessary_normalized_proper_motion_Gamma':str(Gamma),'all_full_affine_identities_verified':True,'basis_count':37,'original_class_coefficient_count':25*25*37,'mathematical_scope':'All 36 REAL parameters on this declared original n26 face; fixed slice excludes all real six-deficit repairs. Ordinary counting proof; no harmonic decoding.'}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('INPUT.json'));p.add_argument('--old-input',type=Path,default=Path(__file__).with_name('N24_INPUT.json'));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    out=audit(json.loads(a.input.read_text()),json.loads(a.old_input.read_text()))
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:out[k]for k in ['P0','trace_Y','normalized_coefficient_l1','negative_eigenvalue_gap_rho','necessary_normalized_proper_motion_Gamma','rank_Y','basis_count']}))
