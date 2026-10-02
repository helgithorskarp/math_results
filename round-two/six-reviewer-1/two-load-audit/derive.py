"""Definition-level invariant frame; no author executable or fixture input."""
from algebra import ATOMS,Rat as R,POLY,Q,tvar,Dvar,avar,uvar,dot,linear,determinant,require,product,portable_digest,digest
from sympy import QQ


def construct(notify=lambda label:None, snapshot=lambda functions:None):
    q,t,D,a,u=map(R,[Q+4,tvar,Dvar,avar,uvar]);m=a+u;w=q+D-1;h=2*q+2*m-1
    loads=[D,t]
    cs=[]
    for d in loads:
        # Solve the literal mandatory singleton/spoke product=-1.
        intercept=-(w-d)/(m+1);slope=w-(q+D-d)/m
        cs.append((-1-intercept)/slope)
    gram=[[R() for _ in range(6)] for _ in range(6)]
    gram[0][0],gram[1][1]=q-1,D
    gram[2][2]=D*(q*D/a-1);gram[3][3]=D*(q*t/u-1)
    gram[2][3]=gram[3][2]=-D;gram[4][4]=(q+D)*(D-t)/(D*u)
    units=[[R(i==j) for i in range(6)] for j in range(6)]
    g=linear((1,units[0]),(-1,units[1]))
    means=[linear((1/D,units[1]),(1/D,units[2])),
           linear((1/D,units[1]),(1/D,units[3]),(1,units[4]))]
    counts=[a,u]
    K=linear((1,g),*zip(counts,means));Csum=linear(*[(c*n,v) for c,n,v in zip(cs,counts,means)])
    eta=[]
    for c,v in zip(cs,means):
        mu=linear((-1/(m+1),K),(c,v),(-1/m,Csum))
        # Each literal spoke is its type mean plus an orthogonal deviation.
        eta.append(w-dot(gram,mu,mu)-c*c*(w-dot(gram,v,v)))
    total=sum((n*e for n,e in zip(counts,eta)),R())
    zs=[m*(e-total/(m*(m-1)))/(m-2) for e in eta]
    gram[5][5]=u*(u*zs[0]+a*zs[1])/(a*m*m)
    functions={'zeta_heavy':zs[0],'zeta_light':zs[1]}
    for tag,c,z in zip(['heavy','light'],cs,zs):functions[tag+'_within_slack']=1-c*c*(q+D)/(h-q-D)-z/h
    notify('four scalar functions from mean/deviation Gram')
    snapshot(functions)
    # Full old-frame coordinate action and bilinear resolvent; two-plane
    # inverse rebuilt from its entries, not a supplied resolvent formula.
    old_action=[[q+1,D],[q-1,D]]
    block=[[h*int(i==j)-old_action[i][j] for j in range(2)] for i in range(2)]
    delta=determinant(block)
    inverse=[[block[1][1]/delta,-block[0][1]/delta],[-block[1][0]/delta,block[0][0]/delta]]
    resolvent=[[R() for _ in range(6)] for _ in range(6)]
    for i in range(2):
        for j in range(2):resolvent[i][j]=sum((gram[i][k]*inverse[k][j] for k in range(2)),R())
    for i in (2,3):
        for j in (2,3):resolvent[i][j]=gram[i][j]/(h-2*D)
    for i in (4,5):resolvent[i][i]=gram[i][i]/h
    y=linear((u*cs[0]/m,means[0]),(-u*cs[1]/m,means[1]))
    vectors=[*means,K,linear((1,y),(1,units[5]))]
    inverse_weights=[1/a,1/u,m+1,u/(a*m)]
    # Shear BEFORE dot products. Derive its coefficients from physical
    # marked coordinates; the residual must be the pure W direction.
    b=[vectors[3][2]/vectors[0][2],vectors[3][3]/vectors[1][3],R()]
    shear=[[R(i==j) for j in range(4)] for i in range(4)]
    for i in range(3):shear[i][3]=-b[i]
    require(determinant(shear)==1,'literal update shear determinant1')
    changed=[linear(*[(shear[i][j],vectors[i]) for i in range(4) if shear[i][j]!=0]) for j in range(4)]
    require(changed[3]==units[5],'all6 residual W coordinates after shear')
    budget=[[R() for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(i,4):
            weights=sum((shear[k][i]*inverse_weights[k]*shear[k][j] for k in range(4) if shear[k][i]!=0 and shear[k][j]!=0),R())
            budget[i][j]=budget[j][i]=weights-dot(resolvent,changed[i],changed[j])
        notify('sheared budget row'+str(i+1))
    require(budget[2][3]==0,'zero third sheared border')
    return functions,budget,{'q':q,'t':t,'D':D,'a':a,'u':u,'m':m,'h':h,'w':w,'cs':cs,'zs':zs,'K':K,'vectors':vectors,'resolvent':resolvent,'gram':gram,'delta':delta,'shear':shear}


def encode(z):
    return {'numerator':[(list(k),str(v)) for k,v in sorted(z.n.items())],
            'denominator':[(list(k),str(v)) for k,v in sorted(product(z.d).items())],
            'denominator_factors':[{'power':e,'terms':[(list(k),str(v)) for k,v in sorted(ATOMS[key].items())]} for key,e in sorted(z.d.items())]}


def run(notify=lambda label:None):
    functions,budget,data=construct(notify)
    for size in range(1,4):
        functions['invariant_minor_'+str(size)]=determinant([row[:size] for row in budget[:size]])
        notify('leading minor'+str(size))
    # Top-left3 is unchanged by the shear, so all four leading minors
    # correspond to the same Sylvester criterion. Generic exterior determinant.
    functions['invariant_minor_4']=determinant(budget)
    notify('generic fourth determinant')
    # Compact private interchange, coefficients are regenerated proof data;
    # author program/expected data are never an input to construction.
    return {'functions':{k:encode(v) for k,v in functions.items()},
            'budget':[[encode(z) for z in row] for row in budget]}
