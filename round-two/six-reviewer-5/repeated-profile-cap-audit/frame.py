"""Independent written-recipe reconstruction in an orthogonal residual basis.

No target module/data access. Coordinates D=M1-M2, P=M1+M2 are used
instead of a deleted eight-row W basis.
"""
from fractions import Fraction as F

DIM = 20

def build(q):
    zero=q*0
    def vec(**kw):
        v=[zero]*DIM
        for i,a in kw.items():v[int(i)]=a
        return v
    def unit(i):
        v=[zero]*DIM;v[i]=zero+1;return v
    def add(*vs):return [sum(v[i] for v in vs) for i in range(DIM)]
    def scale(a,v):return [a*x for x in v]
    def dot(v,w):return sum(v[i]*gram[i][j]*w[j] for i in range(DIM) for j in range(DIM) if v[i] and gram[i][j] and w[j])
    s=q+6; w=q+5; rho=(q-1)/(q+2)
    E2=q/6+rho*rho*(q+3)/3
    fp=(q-8)/(10*rho*(q+3)); aa=fp/4
    cl=-2*(q-8)/(5*s); b=3*(q-11)/(5*s); a=-b/2
    ch=-9*(q-11)/(20*s)+fp*q/(8*s)
    common=(10*q-4)/100
    hl=w-common-aa*aa*E2-a*a*s/6-2*s*ch*ch/3
    hf=w-common-b*b*s/6-2*s*ch*ch/3-s*cl*cl/6
    ll=w-common-fp*fp*E2-2*s*cl*cl/3
    lf=w-common-9*fp*fp*E2
    ph=-1-common-a*b*s/6; pl=-1-common+3*fp*fp*E2
    mh=(2*ph+hf)/3; ml=(2*pl+lf)/3
    ah=2*(2*hl-ph-hf); bh=hf-mh
    al=2*(2*ll-pl-lf); bl=lf-ml; nu=2*mh-ml/2
    gram=[[zero]*DIM for _ in range(DIM)]
    diag=[q-1,6,6*(q-1),6*(q-1),s/6,s/6,
          2*s/3,2*s/3,2*s/3,2*s/3,2*s/3,2*s/3,
          2*nu,ml,ah,bh,ah,bh,al,bl]
    for i,x in enumerate(diag):gram[i][i]=x
    gram[2][3]=gram[3][2]=zero-6
    for i in (6,8,10):gram[i][i+1]=gram[i+1][i]=-s/3
    gp,h0,ax,ay,B,Y=[unit(i) for i in range(6)]
    hx=scale(F(1,6),add(h0,ax)); hy=scale(F(1,6),add(h0,ay))
    K=add(gp,scale(F(1,2),h0),ax,scale(F(1,2),ay),scale(3,Y))
    E=add(hx,scale(-rho,add(hy,Y)))
    t=[[unit(i),unit(i+1),scale(-1,add(unit(i),unit(i+1)))] for i in (6,8,10)]
    bs=[B,scale(-1,B),Y]
    marked=[add(hx if i<2 else hy,bs[i],t[i][j]) for i in range(3) for j in range(3)]
    means=[scale(F(1,2),add(unit(12),unit(13))),
           scale(F(1,2),add(scale(-1,unit(12)),unit(13))),scale(-1,unit(13))]
    residual=[]
    for i in range(3):
        wa,wf=unit(14+2*i),unit(15+2*i)
        residual += [add(means[i],scale(F(1,2),add(wa,scale(-1,wf)))),
                     add(means[i],scale(F(1,2),add(scale(-1,wa),scale(-1,wf)))),
                     add(means[i],wf)]
    base=scale(F(-1,10),K); projection=[]
    for i in range(2):
        projection += [add(base,scale(aa,E),scale(a,bs[i]),scale(ch,t[i][1])),
                       add(base,scale(aa,E),scale(a,bs[i]),scale(ch,t[i][0])),
                       add(base,scale(b,bs[i]),scale(ch,t[1-i][2]),scale(cl/2,t[2][2]))]
    projection += [add(base,scale(fp,E),scale(cl,t[2][1])),
                   add(base,scale(fp,E),scale(cl,t[2][0])),add(base,scale(-3*fp,E))]
    private=[add(p,r) for p,r in zip(projection,residual)]
    all_new=marked+private+[base]
    moment=[[zero]*DIM for _ in range(DIM)]
    moment[0][0]=q*q-1;moment[0][1]=moment[1][0]=6*(q-1);moment[1][1]=zero+36
    for i in (2,3):
        for j in (2,3):moment[i][j]=12*gram[i][j]
    for v in all_new:
        gv=[sum(gram[i][j]*v[j] for j in range(DIM) if gram[i][j] and v[j]) for i in range(DIM)]
        for i,x in enumerate(gv):
            if x:
                for j,y in enumerate(gv):
                    if y:moment[i][j]+=x*y
    ta=[add(t[i][0],scale(-1,t[i][1])) for i in range(3)]
    ts=[scale(3,add(t[i][0],t[i][1])) for i in range(3)]
    sectors=[
        [ta[0],unit(14)], [ta[1],unit(16)], [ta[2],unit(18)],
        [B,add(ts[0],scale(-1,ts[1])),unit(12),add(unit(15),scale(-1,unit(17)))],
        [gp,h0,ax,ay,add(ts[0],ts[1]),Y,ts[2],add(unit(15),unit(17)),unit(19),unit(13)]]
    identities=[]
    def check(name,d):
        if d:raise ValueError(name)
        identities.append(name)
    check('K norm',dot(K,K)-(10*q-4));check('K E orthogonal',dot(K,E));check('E norm',dot(E,E)-E2)
    for i,v in enumerate(marked+private):check('norm '+str(i),dot(v,v)-w)
    for i in range(6):
        for j in range(i):check('heavy same-mark '+str((i,j)),dot(marked[i],marked[j])+1)
    for i in range(6,9):
        for j in range(6,i):check('light same-mark '+str((i,j)),dot(marked[i],marked[j])+1)
    for facet in range(3):
        for private_mask in (1,2,3):
            for marked_mask in (1,2,3):
                if private_mask & marked_mask:
                    check('private marked '+str((facet,private_mask,marked_mask)),dot(private[3*facet+private_mask-1],marked[3*facet+marked_mask-1])+1)
        for leaf in (0,1):check('private leaf full '+str((facet,leaf)),dot(private[3*facet+leaf],private[3*facet+2])+1)
    for j,x in enumerate(add(*private)):
        check('private/empty balance '+str(j),x+9*K[j]/10)
    return dict(q=q,s=s,N=2*q+18,gram=gram,moment=moment,sectors=sectors,
                marked=marked,private=private,residual=residual,K=K,empty=base,
                scalars=[ah,bh,al,bl,nu,ml],kappa=1/(2*nu)+1/ml+4/bl,
                identities=identities,dot=dot)

def forms(model,extra_margin=0):
    gram=model['gram'];moment=model['moment'];H=model['N']-1-extra_margin
    cap=[[H*gram[i][j]-moment[i][j] for j in range(DIM)] for i in range(DIM)]
    def contract(v,w,A):
        return sum(v[i]*A[i][j]*w[j] for i in range(DIM) for j in range(DIM) if v[i] and A[i][j] and w[j])
    sectors=model['sectors'];allv=sum(sectors,[]);groups=sum(([i]*len(sec) for i,sec in enumerate(sectors)),[])
    checks=0
    for i in range(DIM):
        for j in range(DIM):
            if groups[i]!=groups[j]:
                if contract(allv[i],allv[j],gram) or contract(allv[i],allv[j],cap):raise ValueError('off-sector coupling')
                checks+=2
    blocks=[[[contract(v,w,cap) for w in sec] for v in sec] for sec in sectors]
    if blocks[0]!=blocks[1]:raise ValueError('heavy multiplicity mismatch')
    return [blocks[i] for i in (0,2,3,4)],checks
