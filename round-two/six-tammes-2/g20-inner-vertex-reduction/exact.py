"""Whole integral identities for the inner chart; no numerical discovery."""
from fractions import Fraction as Q
from polynomials import P,dot
from frame import make,CORE,CONTACTS

def require(ok,message):
    if not ok:raise ValueError(message)

def divide(f,d):
    r={k:Q(v) for k,v in f.c.items()};q={};ld=max(d.c)
    while r:
        lm=max(r);require(all(x>=y for x,y in zip(lm,ld)), 'nonzero division remainder')
        key=tuple(x-y for x,y in zip(lm,ld));co=r[lm]/d.c[ld];q[key]=q.get(key,Q(0))+co
        for k,v in d.c.items():
            kk=tuple(x+y for x,y in zip(k,key));r[kk]=r.get(kk,Q(0))-co*v
            if not r[kk]:del r[kk]
    require(all(v.denominator==1 for v in q.values()),'integer quotient')
    ans=P({k:int(v) for k,v in q.items()});require(ans*d==f,'whole division identity');return ans

def affine(f):
    require(all(k[2]<=1 for k in f.c),'affine positive radical')
    return P({k:v for k,v in f.c.items() if k[2]==0}),P({(i,j,0):v for (i,j,k),v in f.c.items() if k==1})

def load(document):
    names={'bound0','bound1','bound2','delta','C0','C4','C6','margin','bound2_square_factor','critical_norm99','R'}
    require(set(document)=={'schema_version','variable_order','coefficient_domain','rows'} and document['schema_version']==1 and document['variable_order']==['t','z','w'] and document['coefficient_domain']=='Z','factor document domain')
    require(set(document['rows'])==names,'entire factor input')
    ans={}
    for name,rows in document['rows'].items():
        terms={};keys=[]
        for row in rows:
            require(type(row)is list and len(row)==4,'coefficient row');i,j,k,v=row
            require(all(type(x)is int and x>=0 for x in (i,j,k)) and k<=1,'nonnegative exponents, affine radical')
            require(type(v)is str and str(int(v))==v and int(v)!=0,'canonical nonzero coefficient')
            key=(i,j,k);require(key not in terms,'duplicate monomial');keys.append(key);terms[key]=int(v)
        require(bool(rows) and keys==sorted(keys),'canonical whole rows');ans[name]=P(terms)
    require(all(k[2]==0 for n in ('R','critical_norm99','bound2_square_factor') for k in ans[n].c),'bivariate derived factors')
    return ans

def bases(t,z):
    a,b,c=1+t,1-t,1+2*t;D=b*b*c;C=1+D*z*z;J=9*t**3-t*t-t+1
    q=a*D*z*z-2*D*z+2*t*t-t+1
    return {'a':a,'b':b,'c':c,'3t-1':3*t-1,'3t+1':3*t+1,'J':J,'C':C,'Q':q,'bz+1':b*z+1}

def multiplier(names,t,z):
    bs=bases(t,z);v=t*0+1
    for name in names:require(name in bs,'positive factor name');v*=bs[name]
    return v

def critical(t,z):
    # G is the physical Gram matrix of (p4,p7,n99), diagonals 1,1,621-620t.
    # Its denominator is d=(1+t)^2 C. No generic radical field is expanded.
    m=make(t,z,t*0);d=m['W_den'];W=m['W_num'];zero=t*0
    x=dot([zero,zero,zero+1],W,t);y=dot(W,[-5,-14,20],t)
    s=20-19*t;q=621-620*t
    adj=((q*d*d-y*y,d*(s*y-x*q),x*y-s*d*d),
         (d*(s*y-x*q),(q-s*s)*d*d,d*(x*s-y)),
         (x*y-s*d*d,d*(x*s-y),d*d-x*x))
    det=q*d*d-y*y-q*x*x+2*x*s*y-s*s*d*d;rr=[t,t,15]
    qn=sum((rr[i]*adj[i][j]*rr[j] for i in range(3) for j in range(3)),zero)
    return 99*det-100*qn

def derive(document,system):
    f=load(document);t,z,w=[P.var(i) for i in range(3)];m=make(t,z,w);Y=m['points'];R=m['root_squared'];a,b,c=1+t,1-t,1+2*t;bs=bases(t,z)
    require(f['R']==R,'entire radical square')
    require(m['C']-m['S']==b*c*(b*z+1)**2 and m['C']+m['S']==bs['Q'],'positive E factorization')
    require(a*bs['Q']==m['D']*(a*z-1)**2+4*t*t,'positive quadratic identity')
    F=a**5*c*(3*t-1)*(b*z+1)
    for j in range(3):require(-(Y[0][j]+2*Y[11][j])==F*f['bound'+str(j)],'entire boundedness coordinate identity')
    F0=a**6*c*(3*t-1)*(b*z+1);F6=a**4*c*(3*t-1)*(3*t+1)*(b*z+1)
    u0=[divide(v,F0) for v in Y[0]];u6=[divide(v,F6) for v in Y[6]]
    L0=divide(m['Omega'],F0);L6=divide(m['Omega'],F6)
    delta=u0[1]*u6[0]-u0[0]*u6[1];alpha=-2*u6[0]+13*u6[1];beta=2*u0[0]-13*u0[1]
    C0=L0*alpha;C6=L6*beta;C4=15*delta-alpha*u0[2]-beta*u6[2]
    raw={'delta':delta,'C0':C0,'C4':C4,'C6':C6,'margin':24*delta-t*(C0+C4+C6)}
    for name,p in raw.items():require(p.reduced(R)==multiplier(system['Farkas_positive_factors'][name],t,z)*f[name],'entire positive-factor Farkas identity: '+name)
    for j in range(3):require(([-13,-2,15][j]*delta-alpha*u0[j]-beta*u6[j]-(C4 if j==2 else P.cv(0))).reduced(R)==0,'entire Cramer vector identity')
    A,B=affine(f['bound2']);H=B*B*R-A*A
    require(H==-8*bs['J']*c*c*b**4*a**4*bs['Q']*f['bound2_square_factor'],'entire alternate boundedness square factor')
    circuits=[(0,9,5,11),(5,6,0,11),(11,7,0,5),(1,8,2,4),(4,10,1,2),(2,12,1,10)]
    for i,j,k,l in circuits:
        require(all(a*(Y[i][v]+Y[j][v])==2*t*(Y[k][v]+Y[l][v]) for v in range(3)),'entire contact circuit')
    require(all(a*a*(Y[8][v]+Y[12][v])==(5*t*t-1)*(Y[1][v]+Y[2][v]) for v in range(3)),'entire longer B circuit')
    require(all(m['h']*Y[0][v]==a*(2*t*Y[6][v]+2*t*Y[7][v]+b*Y[9][v]) for v in range(3)),'entire all-low-A circuit')
    require(f['critical_norm99']==critical(t,z),'entire critical norm identity')
    return f,{'whole_boundedness_identities':3,'positive_coordinate_divisions':8,'whole_Farkas_factor_identities':5,'whole_Cramer_components':3,'whole_contact_circuits':8,'critical_w_free_identity':True,'alternate_square_factor_identity':True,'positive_E_and_Q_identities':3}

def obligations(f):
    out=[]
    for name,parts in [('bound0',[('B',1),('H',1)]),('bound1',[('A',1),('B',1)]),('bound2',[('A',1),('H',-1)]),('delta',[('A',1),('B',1)]),('C0',[('A',1),('H',-1)]),('C4',[('A',1),('H',-1)]),('C6',[('A',1),('B',1)]),('margin',[('B',1),('H',1)])]:
        A,B=affine(f[name]);ps={'A':A,'B':B,'H':B*B*f['R']-A*A}
        out.extend((name+'-'+part,ps[part],sign) for part,sign in parts)
    return out+[('critical-norm99',f['critical_norm99'],1)]
