"""Independent inverse-map and monic-division checking, stdlib only.

Never imports generate.py, author target source, or a CAS. Fresh derivative
scatter, inverse Horner maps and full quotient multiply-back bind every
coefficient. Generated certificates remain local and are not published.
"""
import copy,json,math,sys
from core import HERE,require,input_polys,encode,decode,digest,ev

def clean(p):return {e:c for e,c in p.items() if c}
def shift_back(p,h=128):
    out={};groups={}
    for (i,j),c in p.items():groups.setdefault(j,{})[i]=c
    for j,coeff in groups.items():
        row=[]
        for i in range(max(coeff),-1,-1):
            nxt=[0]*(len(row)+1)
            for r,c in enumerate(row):nxt[r]-=h*c;nxt[r+1]+=c
            nxt[0]+=coeff.get(i,0);row=nxt
        for i,c in enumerate(row):
            if c:out[(i,j)]=c
    return out
def product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,c in enumerate(a):
        for j,cc in enumerate(b):out[i+j]+=c*cc
    return out
def sumrows(a,b):
    out=a+[0]*max(0,len(b)-len(a))
    for i,c in enumerate(b):out[i]+=c
    return out
def homography(coeff,A,B,d):
    """Full dense homogeneous Horner with an independently built B power."""
    powers=[[1]]
    for _ in range(d):powers.append(product(powers[-1],B))
    out=[0]
    for i in range(d,-1,-1):
        out=sumrows(product(out,A),[coeff.get(i,0)*c for c in powers[d-i]])
    return out
def inverse_affine(p,a,b,den):
    groups={};J=max(e[1] for e in p);out={}
    for (i,j),c in p.items():groups.setdefault(i+j,{})[j]=c
    for L,row in groups.items():
        value=homography(row,[-a,den],[b],J)
        for v,c in enumerate(value):
            if c:
                require(v<=L,'affine inverse exponent');e=(v,L-v);out[e]=out.get(e,0)+c
    return clean(out),b**J
def wronskian(P,D):
    out={}
    for (i,j),c in P.items():
        for (a,b),d in D.items():
            if i!=a:
                e=(i+a-1,j+b);out[e]=out.get(e,0)+(i-a)*c*d
    return clean(out)
def inverse_compact(p,d):
    groups={};out={}
    for (i,j),c in p.items():groups.setdefault(i,{})[j]=c
    for L,row in groups.items():
        coeff=homography(row,[-6,2],[11,-2],d)
        for v,c in enumerate(coeff):
            if c:
                require(v<=L+d,'inverse compact exponent');e=(v,L+d-v);out[e]=out.get(e,0)+c
    return clean(out)
def full_expansion(P):
    """Full multinomial q=3k-14+m composition before reduction."""
    out={};weights={}
    for (i,j),c in P.items():
        if i not in weights:
            weights[i]=[(v,r,math.comb(i,v)*math.comb(i-v,r)*3**r*(-14)**(i-v-r))
                        for v in range(i+1) for r in range(i-v+1)]
        for v,r,w in weights[i]:out[(j+r,v)]=out.get((j+r,v),0)+c*w
    return clean(out)
def monic_divide(original,norm):
    rem=dict(original);quot={}
    for v in range(max(j for i,j in rem),1,-1):
        for (i,j),c in list(rem.items()):
            if j!=v:continue
            del rem[(i,j)];quot[(i,j-2)]=quot.get((i,j-2),0)+c
            rem[(i+2,j-2)]=rem.get((i+2,j-2),0)+7*c
            rem[(i,j-2)]=rem.get((i,j-2),0)+norm*c
        rem=clean(rem)
    rebuilt=dict(rem)
    for (i,j),c in quot.items():
        for e,z in [((i,j+2),c),((i+2,j),-7*c),((i,j),-norm*c)]:rebuilt[e]=rebuilt.get(e,0)+z
    require(clean(rebuilt)==original,'entire quotient multiply back')
    require(all(j<2 for i,j in rem),'full monic remainder')
    return rem,clean(quot)
def onevariable(rows):
    out={}
    for i,c in rows:
        require(type(i) is int and i>=0 and i not in out,'unique univariate exponent')
        n=int(c);require(str(n)==c and n,'canonical univariate coefficient');out[i]=n
    return out
def radical_negative(a,b):
    """Comparison specialized to strict negativity, separately from generator."""
    if b==0:return a<0
    if a==0:return b<0
    if a<0 and b<0:return True
    if a>0 and b>0:return False
    if a<0:return a*a>7*b*b
    return a*a<7*b*b
def check_sign(p,wanted,label):
    require(p and all(wanted*c>0 for c in p.values()) and wanted*p.get((0,0),0)>0,'entire coefficient sign '+label)
def main():
    P,D=input_polys();record=json.loads((HERE/'work/certificate.json').read_text());damage=sys.argv[1] if len(sys.argv)>1 else None
    if damage=='domain':record['domain']['k_min']=127
    elif damage=='derivative':record['derivative'][0][1]=str(int(record['derivative'][0][1])+1)
    elif damage=='denominator':record['maps']['denominator']['coefficients'].pop()
    elif damage=='compact':
        row=next(r for r in record['maps']['compact']['coefficients'] if r[0][1]!=record['maps']['compact']['q_degree'])
        row[1]=str(int(row[1])+1)
    elif damage=='endpoint':record['maps']['compact'].pop('endpoint')
    elif damage=='curve':record['curves']['32']['H'][1][1]=str(int(record['curves']['32']['H'][1][1])+1)
    elif damage=='radical':record['curves']['36']['pairs'][0][1]=str(int(record['curves']['36']['pairs'][0][1])+1)
    elif damage=='norm36':record['curves'].pop('36')
    elif damage is not None:raise ValueError('unknown semantic damage')
    require(record['domain']=={'k_min':128,'q_min':'3k'},'entire specified domain')
    require(record['P_hash']==digest(P) and record['D_hash']==digest(D),'whole credited original residual binding')
    F=wronskian(P,D);require(F==decode(record['derivative']),'entire independently scattered Wronskian')
    result={}
    for label,poly,a,b,den in [('denominator',D,3,1,1),('derivative',F,11,2,2)]:
        rec=record['maps'][label];shifted=decode(rec['coefficients']);check_sign(shifted,1,label)
        d=max(e[0] for e in poly);require(rec['scale_exponent']==d,'positive clearing scale '+label)
        inv,mult=inverse_affine(shift_back(shifted),a,b,den)
        require(inv=={e:mult*den**d*c for e,c in poly.items()},'ENTIRE inverse affine identity '+label)
        result[label]=dict(terms=len(shifted),original_hash=digest(poly),shifted_hash=digest(shifted))
        print(label,'entire inverse identity and signs pass',flush=True)
    rec=record['maps']['compact'];T=decode(rec['coefficients']);check_sign(T,-1,'compact');d=max(e[0] for e in P)
    require(rec['q_degree']==d==63,'full compact degree')
    require('endpoint' in rec,'separate closed endpoint mandatory')
    endpoint=decode(rec['endpoint']);require(endpoint=={e:c for e,c in T.items() if e[1]==d},'ENTIRE closed endpoint extraction')
    require(endpoint.get((0,d),0)<0 and all(c<0 for c in endpoint.values()),'strict closed endpoint')
    unshift=shift_back(T);inv=inverse_compact(unshift,d)
    require(inv=={(i,j+d):10**d*c for (i,j),c in P.items()},'ENTIRE inverse compact homography identity')
    endpoint_back=shift_back(endpoint)
    wanted_endpoint={}
    for (i,j),c in P.items():wanted_endpoint[(i+j,d)]=wanted_endpoint.get((i+j,d),0)+11**i*2**(d-i)*c
    require(endpoint_back==clean(wanted_endpoint),'ENTIRE direct closed endpoint polynomial')
    result['compact']=dict(terms=len(T),endpoint_terms=len(endpoint),hash=digest(T),closed_endpoint_hash=digest(endpoint))
    print('whole compact homography and closed endpoint pass',flush=True)
    require(set(record['curves'])=={'32','36'},'both required norm curves')
    expanded=full_expansion(P);result['curves']={}
    for norm,wanted in [(32,-1),(36,1)]:
        rec=record['curves'][str(norm)];A,H=onevariable(rec['A']),onevariable(rec['H']);rem,quot=monic_divide(expanded,norm)
        require(rem=={**{(j,0):c for j,c in A.items()},**{(j,1):c for j,c in H.items()}},'ENTIRE curve remainder')
        hs=onevariable(rec['H_shift']);require(shift_back({(j,0):c for j,c in hs.items()})=={(j,0):c for j,c in H.items()},'ENTIRE inverse H shift')
        require(all(wanted*c>0 for c in hs.values()) and wanted*hs.get(0,0)>0,'strict required H sign')
        aa={};bb={};seen=set()
        for j,a,b in rec['pairs']:
            require(type(j) is int and j>=0 and j not in seen,'unique radical pair');seen.add(j);a,b=int(a),int(b)
            if a:aa[(j,0)]=a
            if b:bb[(j,0)]=b
            require(radical_negative(wanted*-a,wanted*-b),'strict required radical sign')
        require(shift_back(aa)=={(j,0):c for j,c in A.items()},'ENTIRE inverse radical rational channel')
        require(shift_back(bb)=={(j+1,0):c for j,c in H.items()},'ENTIRE inverse radical irrational channel')
        require(0 in seen,'strict radical endpoint included')
        result['curves'][str(norm)]=dict(expanded_terms=len(expanded),quotient_terms=len(quot),remainder_terms=len(rem),H_terms=len(hs),radical_pairs=len(seen),remainder_hash=digest(rem))
        print('norm',norm,'complete division and radical comparisons pass',flush=True)
    require(7*64**2>167**2,'both curves lie above global monotonicity boundary')
    residues7={a*a%7 for a in range(7)};residues4={(a*a+b*b)%4 for a in range(4) for b in range(4)}
    require(33%7 not in residues7 and 34%7 not in residues7 and 35%4 not in residues4,'complete modular norm gap')
    controls=[]
    for k in (128,129,131,257,1024):
        rad=7*k*k+36;m=math.isqrt(rad);m+=int(m*m<rad);q0=3*k-14+m
        for q,wanted in ((q0-1,-1),(q0,1)):
            p,dd=ev(P,q,k),ev(D,q,k);require(dd>0 and wanted*p>0,'boundary controls, not uniform proof')
            norm=(q-3*k+14)**2-7*k*k;require(norm<=32 if wanted<0 else norm>=36,'exact integer norm boundary')
            controls.append(dict(q=q,k=k,norm=norm,P=str(p),D=str(dd)))
    require(ev(P,32,8)<0 and ev(D,32,8)>0,'known failed all-small-count extension')
    result['controls']=controls;result['counterexample_to_all_k7_extension']={'q':32,'k':8,'norm':36,'R_sign':-1}
    result['modular_coverage']={'square_residues_mod7':sorted(residues7),'sum_square_residues_mod4':sorted(residues4)}
    result['status']='all new arithmetic obligations checked; original matrix criterion remains explicit parent premise'
    result['methods']='fresh integer Wronskian scatter; inverse Horner affine/compact maps; full expanded monic division and multiply back; inverse shifts; rational squaring; no CAS or new target native source'
    (HERE/'work/check-result.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':main()
