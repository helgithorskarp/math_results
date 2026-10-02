"""Independent finite cases; executable author proof engines remain unused."""
from fractions import Fraction as F
from itertools import combinations,product
import json,sys
import core as c

FLOOR=F(1,1 << 40)
ETA=F(1,4096)

def base(q,k):
    sets,C,D,R,U=c.matrices(q,k);N=len(sets);non=sets[1:];s=3*q+4
    stars=[sum(p in A for A in sets) for p in range(q+3)]
    c.need(stars==[s,s-k,s-k]+[q+5]*k+[q+6]*(q-k),'every original star size')
    Sa=[F(0 in A) for A in non]
    z=[F(1-int(1 in A)-int(2 in A)+int(len(A)==3 or (len(A)==2 and A<={0,1,2}))) for A in non]
    c.need(c.mv(C,Sa)==c.mv(D,Sa)==c.mv(R,Sa)==[0]*(N-1),'all actual a-star actions')
    c.need(c.mv(C,z)==c.mv(R,z)==[0]*(N-1),'original negative-kappa separator actions')
    alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
    c.need(c.quad(D,z)==alpha>0,'whole exact separator derivative energy')
    c.need(sum(map(sum,R))==0 and max(sum(abs(v) for v in row) for row in R)==2,'whole repair margins')
    info={'q':q,'k':k,'N':N,'star_sizes':stars,'domain_sha256':c.digest([c.mask(A) for A in sets]),
          'C0_sha256':c.digest(C),'Delta_sha256':c.digest(D),'R_sha256':c.digest(R),
          'U0_sha256':c.digest(U),'negative_kappa_energy':alpha}
    return sets,C,D,R,U,Sa,info

def negative(q):
    sets,C,D,R,U,Sa,out=base(q,3);n=len(C)
    if q==4:
        v=[F(1)]*n;values={'a':c.quad(U,v),'d':c.quad(D,v),'r':c.quad(R,v)}
        c.need(values=={'a':F(-1),'d':F(179,17),'r':F(0)},'q4 actual empty-cap obstruction')
        out['dual']={'rank':1,'pairing':values}
    else:
        data=json.loads((c.ROOT/'INPUT-DUALS.json').read_text())[str(q)]
        c.need(type(data['weight']) in [str,int],'credited exact dual weight')
        weight=F(data['weight']);c.need(weight>0,'positive PSD weight')
        vectors=data['vectors'];c.need(len(vectors)==2,'two dual columns')
        c.need(all(len(v)==n and all(type(x) is int for x in v) for v in vectors),'entire integer original dual domain')
        pairs=[]
        for v in vectors:pairs.append({'a':c.quad(U,v),'d':c.quad(D,v),'r':c.quad(R,v)})
        c.need(c.canonical(pairs)==data['pairings'],'every separate original quadratic pairing')
        combo={key:pairs[0][key]+weight*pairs[1][key] for key in ['a','d','r']}
        c.need(c.canonical(combo)==data['combined'],'entire combined dual record')
        u,v=vectors;gram=sum(x*x for x in u)*sum(x*x for x in v)-sum(x*y for x,y in zip(u,v))**2
        c.need(gram>0 and combo['a']<0 and combo['d']>0 and combo['r']==0,'rank-two all-real upper separation')
        out['dual']={'rank':2,'weight':weight,'separate_pairings':pairs,'combined_pairings':combo,
                     'positive_column_Gram_determinant':gram,'vectors_sha256':c.digest(vectors)}
    # Full actual empty lift identity also holds on these infeasible domains.
    out['original_whole_control']=c.whole_controls(q,3,F(1,7),F(-2,5),sets,c.affine(c.affine(C,D,F(1,7)),R,F(-2,5)))
    return out

def continuation(q):
    k=2 if q<7 else 3
    sets,C,D,R,U,Sa,out=base(q,k);N=len(sets)
    d=max(sum(abs(v) for v in row) for row in D)
    kap=ETA/(2*d);tau=kap/24;beta=F(1,16384)
    c.need(kap<=F(1,8) and tau<=ETA/16,'entire finite interval bound')
    seed=c.affine(C,D,kap);end=c.affine(seed,R,tau)
    upper=c.affine(c.affine(U,D,-kap),R,-tau)
    out.update({'kappa':kap,'tau':tau,'derivative_absolute_row_norm':d,'new_lower_floor':FLOOR,
      'zero_cap_floor':c.psd(c.shift(U,ETA)),
      'unrepaired_positive_seed':c.psd(seed),
      'repaired_endpoint_lower_floor':c.psd(c.shift(end,FLOOR,Sa)),
      'repaired_endpoint_upper_floor':c.psd(c.shift(upper,beta)),
      'original_whole_control':c.whole_controls(q,k,kap,tau,sets,end)})
    c.need(out['unrepaired_positive_seed']['rank']==N-4,'complete finite seed kernel dimension')
    c.need(out['repaired_endpoint_lower_floor']['rank']==N-2,'endpoint exact a-star kernel')
    c.need(out['zero_cap_floor']['rank']==out['repaired_endpoint_upper_floor']['rank']==N-1,'strict finite upper forms')
    return out

def corner(positive,high_t):
    sets,C,D,R,U,Sa,out=base(8,3);N=len(sets)
    kap=F(1,4096) if positive else F(0);t=F(1,2) if high_t else F(3,8)
    lower=c.affine(c.affine(C,D,kap),R,t);upper=c.affine(c.affine(U,D,-kap),R,-t)
    out.update({'kappa':kap,'t':t,'lower':c.psd(lower),'upper_floor':c.psd(c.shift(upper,F(1,1 << 20))),
                'original_whole_control':c.whole_controls(8,3,kap,t,sets,lower)})
    c.need(out['lower']['rank']==N-2 if positive else out['lower']['rank']==N-3,'entire corner lower kernel')
    c.need(out['upper_floor']['rank']==N-1,'entire strict corner cap')
    if positive:
        out['new_lower_floor']=FLOOR;out['lower_floor']=c.psd(c.shift(lower,FLOOR,Sa))
        c.need(out['lower_floor']['rank']==N-2,'positive-kappa uniform lower rectangle floor')
    return out

def conventions():
    records=[];valid=0
    for entries in product([-1,0,1],repeat=6):
        a,b,d,e,f,g=entries;A=[[F(a),F(b),F(d)],[F(b),F(e),F(f)],[F(d),F(f),F(g)]]
        minors=[]
        for r in [1,2,3]:
            for ix in combinations(range(3),r):minors.append([r,c.determinant([[A[i][j] for j in ix] for i in ix])])
        expected=all(v>=0 for r,v in minors)
        try:rank=c.psd(A)['rank'];accepted=True
        except ValueError:rank=None;accepted=False
        c.need(accepted==expected,'whole ternary symmetric PSD census versus all principal minors')
        if expected:
            c.need(rank==max([r for r,v in minors if v>0]+[0]),'independent principal-minor rank')
            valid+=1
        records.append([list(entries),accepted,rank])
    damages=[]
    actions={'negative diagonal':lambda:c.psd([[F(-1)]]),
        'zero diagonal nonzero offdiagonal':lambda:c.psd([[F(0),F(1)],[F(1),F(0)]]),
        'asymmetric form':lambda:c.psd([[F(1),F(0)],[F(1),F(1)]]),
        'floated matrix entry':lambda:c.psd([[1.0]]),
        'Boolean matrix entry':lambda:c.psd([[True]]),
        'floated kappa':lambda:c.table(8,0.0),
        'wrong deleted class':lambda:c.domain(8,3,{0,3,4}),
        'missing deletion':lambda:c.domain(8,3,{3,4})}
    for name,action in actions.items():
        try:action()
        except ValueError:damages.append(name)
        else:raise ValueError('damage accepted: '+name)
    return {'whole_ternary_symmetric_forms':729,'PSD_forms':valid,'entire_census_sha256':c.digest(records),
            'rejected_damages':damages}

def scale():
    sets,C,D,R,U,Sa,out=base(4,2);small=c.psd(c.shift(U,ETA))
    sets,C,D,R,U,Sa,out=base(8,3)
    big=c.psd(c.shift(c.affine(c.affine(C,D,F(1,4096)),R,F(3,8)),FLOOR,Sa))
    return {'order40_control':small,'order89_lower_floor_control':big}

def record(name):
    if name=='conventions':return conventions()
    if name=='scale':return scale()
    if name.startswith('neg'):return negative(int(name[3:]))
    if name.startswith('continue'):return continuation(int(name[8:]))
    if name.startswith('corner'):return corner(name[6]=='1',name[7]=='b')
    raise ValueError('unknown complete case')

if __name__=='__main__':
    name=sys.argv[1];value=record(name)
    print(json.dumps(c.canonical(value),indent=2,sort_keys=True))
