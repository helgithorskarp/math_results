"""PRIVATE candidate constant-size sectors for h triangles plus one triangle.

Fractions or the credited exact QQ(h,q) engine; full original bridges need
separate verification. Sector signs are not presumed positive.
"""
from fractions import Fraction as F
from model import recipe,construct
from exact import require,zero,unit,vecadd,scale,matvec,dot,gram,psd_rank

def outer_add(S,G,row,multiplicity=1):
    x=matvec(G,row)
    for i in range(len(S)):
        for j in range(len(S)):S[i][j]+=multiplicity*x[i]*x[j]

def sectors(h,q):
    if type(h) is int:h=F(h)
    if type(q) is int:q=F(q)
    require(not isinstance(h,float) and not isinstance(q,float),'exact parameter types')
    p=recipe(h,q);s,N=[p[z] for z in ['s','N']];H=N-1
    grams={};frames={};caps={}
    for suffix in ['H','L']:
        c=p['c'+suffix];a=p['alpha'+suffix]
        G=[[2*s,F(0)],[F(0),a]]
        S=[[2*s*s*(1+c*c),-s*c*a],[-s*c*a,a*a/2]]
        grams['anti'+suffix]=G;frames['anti'+suffix]=S
    G=zero(4,4)
    for i,z in enumerate([2*s/3,12*s,2*p['nu'],2*p['betaH']]):G[i][i]=z
    S=zero(4,4)
    # A facet contrast with coefficients (1,-1), squared length2.
    # Use pairings directly here, so no hidden metric normalization.
    rows=[([s/3,s,0,0],4),([s/3,-2*s,0,0],2),
          ([p['a']*s/3,p['cH']*s,p['nu'],-p['betaH']/2],4),
          ([p['b']*s/3,2*s*p['cH']/(h-1),p['nu'],p['betaH']],2)]
    for x,m in rows:
        for i in range(4):
            for j in range(4):S[i][j]+=m*x[i]*x[j]
    grams['standard']=G;frames['standard']=S
    G=zero(10,10)
    G[0][0]=q-1;G[1][1]=3*h;G[2][2]=G[3][3]=3*h*(q-1);G[2][3]=G[3][2]=-3*h
    for i,z in zip(range(4,10),[6*h*s,s*(h-1)/(3*h),6*s,h*p['betaH'],p['betaL'],p['muL']]):G[i][i]=z
    e=lambda i:unit(10,i)
    hx=scale(1/(3*h),vecadd(e(1),e(2)));hy=scale(1/(3*h),vecadd(e(1),e(3)))
    VL=vecadd(hy,e(5));E=vecadd(hx,scale(-p['rho'],VL))
    K=vecadd(e(0),scale(-1,e(1)),scale(3*h,hx),scale(3,hy),scale(3,e(5)))
    common=scale(-1/(3*h+4),K)
    VHl=vecadd(hx,scale(1/(6*h),e(4)));VHf=vecadd(hx,scale(-1/(3*h),e(4)))
    VLl=vecadd(VL,scale(F(1,6),e(6)));VLf=vecadd(VL,scale(F(-1,3),e(6)))
    UHl=vecadd(common,scale(p['A'],E),scale(p['cH']/(6*h),e(4)),scale(-1/(2*h),e(7)),scale(1/h,e(9)))
    UHf=vecadd(common,scale(-p['cH']/(3*h),e(4)),scale(-p['cL']/(3*h),e(6)),scale(1/h,e(7)),scale(1/h,e(9)))
    ULl=vecadd(common,scale(p['FF'],E),scale(p['cL']/6,e(6)),scale(F(-1,2),e(8)),scale(-1,e(9)))
    ULf=vecadd(common,scale(p['G'],E),e(8),scale(-1,e(9)))
    S=zero(10,10);S[0][0]=q*q-1;S[1][1]=9*h*h;S[0][1]=S[1][0]=3*h*(q-1)
    for i in [2,3]:
        for j in [2,3]:S[i][j]=6*h*G[i][j]
    for row,m in [(VHl,2*h),(VHf,h),(VLl,2),(VLf,1),(UHl,2*h),(UHf,h),(ULl,2),(ULf,1),(common,1)]:outer_add(S,G,row,m)
    grams['fixed']=G;frames['fixed']=S
    for name,G in grams.items():caps[name]=[[H*G[i][j]-frames[name][i][j] for j in range(len(G))] for i in range(len(G))]
    return p,grams,frames,caps

def boundary_sectors(h):
    p,g,s,c=sectors(h,F(2))
    radical=vecadd(unit(10,2),unit(10,3))
    for forms in (g,s,c):
        require(not any(matvec(forms['fixed'],radical)),'q2 full fixed10 radical identity')
        keep=[i for i in range(10) if i!=3]
        forms['fixed']=[[forms['fixed'][i][j] for j in keep] for i in keep]
    return p,g,s,c

def literal_blocks(h,q):
    p,G,S,cap,v=construct(h,q);size=len(G);e=lambda i:unit(size,i)
    Ws=v['Wrows'];Ms=[scale(F(1,3),vecadd(*Ws[3*i:3*i+3])) for i in range(h+1)]
    WA=[vecadd(Ws[3*i],scale(-1,Ws[3*i+1])) for i in range(h+1)]
    WF=[scale(F(1,3),vecadd(scale(2,Ws[3*i+2]),scale(-1,Ws[3*i]),scale(-1,Ws[3*i+1]))) for i in range(h+1)]
    TA=[vecadd(t[0],scale(-1,t[1])) for t in v['Ts']]
    TS=[vecadd(t[0],t[1],scale(-2,t[2])) for t in v['Ts']]
    groups=[('antiH',F(1),[TA[i],WA[i]]) for i in range(h)]+[('antiL',F(1),[TA[h],WA[h]])]
    for k in range(1,h):
        weights=[F(i<k)-k*F(i==k) for i in range(h)]
        comb=lambda rows:vecadd(*(scale(a,z) for a,z in zip(weights,rows)))
        groups.append(('standard',F(k*(k+1),2),[comb(v['B']),comb(TS[:h]),comb(Ms[:h]),comb(WF[:h])]))
    old_keep=[0,1,2] if q==2 else list(range(4))
    groups.append(('fixed',F(1),[e(i) for i in old_keep]+[vecadd(*TS[:h]),v['Y'],TS[h],vecadd(*WF[:h]),WF[h],vecadd(*Ms[:h])]))
    basis=[z for name,m,vs in groups for z in vs];dim=size-1 if q==2 else size
    require(len(basis)==dim,'ENTIRE changed quotient space count')
    GB=gram(G,basis,zero(size,size));SB=gram(S,basis,zero(size,size));CB=gram(cap,basis,zero(size,size))
    require(psd_rank(gram([[F(i==j) for j in range(size)] for i in range(size)],basis,zero(size,size)))==dim,'complete literal sector representatives independent')
    if q==2:
        radical=vecadd(e(2),e(3))
        require(all(not any(matvec(A,radical)) for A in (G,S,cap)),'q2 complete ambient forms share the radical')
        require(psd_rank(G)==psd_rank(GB)==dim,'q2 sector representatives cover the entire physical quotient')
    _,g,s,c=boundary_sectors(F(h)) if q==2 else sectors(F(h),F(q));offset=0;cross=0;labels=[]
    for gid,(name,m,vs) in enumerate(groups):
        k=len(vs);labels.extend([gid]*k)
        for original,reduced,tag in [(GB,g,'Gram'),(SB,s,'full frame'),(CB,c,'cap')]:
            block=[row[offset:offset+k] for row in original[offset:offset+k]]
            require(block==[[m*z for z in row] for row in reduced[name]],'ENTIRE sector '+tag+' identity '+name)
        offset+=k
    for i in range(dim):
        for j in range(dim):
            if labels[i]!=labels[j]:
                require(GB[i][j]==SB[i][j]==CB[i][j]==0,'EVERY cross-sector position');cross+=1
    return dict(h=h,q=str(q),ambient_coordinate_dimension=size,changed_dimension=dim,complete_change_rank=dim,fixed_sector_dimension=len(c['fixed']),cross_sector_positions=cross,all_Gram_frame_cap_sector_positions=sum(3*len(vs)**2 for _,_,vs in groups),all_reduced_sectors_PD=all(psd_rank(a)==len(a) for a in c.values()))

if __name__=='__main__':
    import signal,json,time
    from pathlib import Path
    def alarm(signum,frame):raise TimeoutError('unchanged60s sector guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    out=[literal_blocks(h,q) for h,q in [(2,F(4)),(3,F(4)),(4,F(4)),(3,F(9,2)),(4,F(8))]]
    signal.alarm(0);record=dict(agent='six-downset-1',role='researcher',status='PRIVATE exact complete sector correspondences at literal h/q only',controls=out)
    Path('work/sectors-controls.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
