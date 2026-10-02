"""Original general-k calibrations and compact all-real five-deletion duals."""
from fractions import Fraction as F
from matrices import original,core_data,table,typ,action,quadratic,require,digest
from literal import core_data as old_original

def lower_vector(X):
    return [F(1-bool(A&2)-bool(A&4)+((A&7).bit_count()>=2)) for A in X[1:]]

def derivative(X,q):
    w=table(q)
    return [[F(0) if A==B or A&B else w[tuple(sorted((typ(A),typ(B))))][1]
             for B in X[1:]] for A in X[1:]]

def trade(X):
    n=len(X)-1;R=[[F(0)]*n for _ in range(n)];ix={A:i for i,A in enumerate(X[1:])}
    for A,B,v in ((1,2,1),(1,4,1),(2,5,-1),(4,3,-1)):
        R[ix[A]][ix[B]]=R[ix[B]][ix[A]]=F(v)
    return R

def scalars(q,k):
    N=(q*q+13*q+16)//2-k;s=3*q+4;h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h
    E=F(N-1-k*(s-k));A=F((2*k+1)*q+k)-F(2*k,q)
    T=F(q*(N-s));S=alpha-2*k*h;B=T*S-2*A*q*h
    P=q**3*(q*q+7*q+8-2*k)*(q*q+(13-6*k)*q+2*k*k-10*k+14)-4*((2*k+1)*q*q+k*q-2*k)**2
    require(P==4*q*q*(T*E-A*A),'general determinant polynomial identity')
    return N,s,h,alpha,E,A,T,S,B,P

def strengthened(q,k):
    N,s,h,alpha,E,A,T,S,B,P=scalars(q,k)
    gap=N-s;g=N-2*s;rr=F(3)+F(2,q);ww=F(s-rr,q-1)
    az=(k-1)*(ww-1);aw=1+k*(ww-1);d=g+rr
    Q=E-(k*az*az+(q-k)*aw*aw)/F(gap)-F(4*q*(1-k)**2,d)
    D=S-2*h*(A/F(gap)+F(4*q*(1-k),d))
    require(Q==E-A*A/T-F(k*(q-k)*ww*ww,q*gap)-F(4*q*(1-k)**2,d),
            'stronger general diagonal Schur identity')
    if k>=1:require(D>=B/T>0,'stronger universal derivative orientation')
    return az,aw,gap,d,Q,D

def check_identities(q,k):
    X,N,s,C,U=original(q,k=k);D=derivative(X,q);R=trade(X);n=N-1
    _,_,h,alpha,E,A,T,S,B,P=scalars(q,k)
    z=lower_vector(X);one=[F(1)]*n
    y=[F(A&7==1 and (A>>3).bit_count()==1) for A in X[1:]]
    require(not any(action(C,z)) and not any(action(R,z)) and quadratic(z,D)==alpha>0,
            'original lower kernel and orientation')
    require(quadratic(one,U)==E and sum(action(U,y))==A and quadratic(y,U)==T,
            'every original mean/pair upper identity')
    require(quadratic(one,D)==S and sum(action(D,y))==q*h and quadratic(y,D)==0,
            'every original mean/pair derivative identity')
    require(quadratic(one,R)==quadratic(y,R)==sum(action(R,y))==0,'entire mean/pair trade form zero')
    yz=[F(V&7==1 and (V>>3).bit_count()==1 and bool(V&((1<<(k+3))-8)))
        for V in X[1:]]
    yw=[y[i]-yz[i] for i in range(n)]
    extra=[F(V&7 in (2,3,4,5) and (V>>3).bit_count()==1) for V in X[1:]]
    az,aw,gap,den,Q,DD=strengthened(q,k)
    vectors=[yz,yw,extra];counts=[k,q-k,4*q]
    cross=[k*az,(q-k)*aw,4*q*(1-k)]
    blocks=[k*gap,(q-k)*gap,4*q*den]
    for i,v in enumerate(vectors):
        require(sum(v)==counts[i] and sum(action(U,v))==cross[i], 'new original count/mean identity')
        require(sum(action(D,v))==counts[i]*h and quadratic(v,D)==0,'new original derivative identity')
        require(quadratic(v,U)==blocks[i] and not any(action(R,v)),'new original diagonal and repair action')
        for wv in vectors[i+1:]:
            require(sum(a*b for a,b in zip(v,action(U,wv)))==0 and
                    sum(a*b for a,b in zip(v,action(D,wv)))==0,'entire new cross block zero')
    wd=[one[i]-az/F(gap)*yz[i]-aw/F(gap)*yw[i]-F(1-k,den)*extra[i] for i in range(n)]
    require(quadratic(wd,U)==Q and quadratic(wd,D)==DD and quadratic(wd,R)==0,
            'stronger original rational dual identities')
    bound=F(q*q*(q+1)*(3*q**3+20*q*q+49*q+24),4*(3*q+5))
    require(B>bound>0,'analytic coefficient lower bound calibration')
    return {'q':q,'k':k,'N':N,'E':str(E),'A':str(A),'T':str(T),'S':str(S),
            'B':str(B),'F0':str(T*E-A*A),'P':P,'all_original_identities_match':True,
            'stronger_Q0':str(Q),'stronger_Delta':str(DD),'all_stronger_original_identities_match':True}

def calibration():
    X,N,s,C,U=original(8,k=3);D=derivative(X,8);R=trade(X)
    old=old_original(8,3,scan=True)
    require((X,N,s,C,D,R,U)==old,'every published q8,k3 original entry')
    records=[check_identities(q,k) for q in range(4,9) for k in range(q+1)]
    # Universal sign identity uses coefficient equality, not a sampled fit.
    a=[8,5,1];b=[5,3];product=[sum(a[i]*b[j] for i in range(3) for j in range(2) if i+j==d) for d in range(4)]
    product[0]-=16
    require(product==[24,49,20,3],'universal positive coefficient identity')
    rec={'agent':'six-downset-3','role':'researcher','baseline':{'q':8,'k':3,'N':89,
         'all_original_entries_match':True,'status':'credited reproduction, not new research'},
         'calibrations':records,'calibration_count':35,'coefficient_lower_bound_polynomial':product,
         'universal_scope':'ordinary written derivation q>=4,1<=k<=q; finite samples are calibration only'}
    rec['record_sha256']=digest(rec);return rec

def exceptional_vector(X):
    values=[]
    for A in X[1:]:
        core=A&7;out=(A>>3).bit_count();z=(A&248).bit_count()
        value=32
        if core==1 and out==1:value-=1 if z else 2
        if core in (2,3,4,5) and out==1:value+=1
        values.append(F(value))
    return values

def run():
    records=[]
    for q in range(5,19):
        X,N,s,C,D,R,U=core_data(q);n=N-1;z=lower_vector(X)
        _,_,h,alpha,E,A,T,S,B,P=scalars(q,5)
        require(not any(action(C,z)) and not any(action(R,z)) and quadratic(z,D)==alpha>0,
                'original lower dual for all real negative kappa')
        if q<18:
            w=[F(17 if V&7==1 and (V>>3).bit_count()==1 else 18) for V in X[1:]]
            p=F(q**4+331*q**3-6302*q*q+4176*q+720,2*q)
            d=162*q*(q+1)+F(936*q-2268,3*q+5)
            label='18*one-indicator(all pairs ax)'
        else:
            w=exceptional_vector(X);p=F(-8368,51);d=F(10381888,59)
            label='32*one-2*y_outside_Z-y_Z+indicator(bx,cx,abx,acx)'
            require(T*E-A*A==F(1905788,81)>0,'q18 separates general necessary determinant from full feasibility')
            rec18=check_identities(18,5)
            require(rec18['stronger_Q0']=='-126891185/110844216','new universal dual excludes exceptional q18')
        require(quadratic(w,U)==p<0 and quadratic(w,D)==d>0 and quadratic(w,R)==0,
                'original all-real upper dual and orientation')
        records.append({'q':q,'k':5,'N':N,'s':s,'dual':label,'U0':str(p),'Delta':str(d),'R':'0',
                        'lower_z_Delta':str(alpha),'all_original_pairings_match':True})
    rec={'agent':'six-downset-3','role':'researcher','all_real_ansatz_exclusions':records,
         'exceptional_general_reduction':rec18,
         'parameters':'all real kappa,t by written original PSD-dual bridge',
         'trust_boundary':'pinned affine entries, written universal kernel identities, exact arithmetic; no formalization'}
    rec['record_sha256']=digest(rec);return rec
