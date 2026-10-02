"""Literal finite full-frame checks; uniform coverage is in PROOF.md.

Includes actual empty, all cross/internal/untouched sectors, forced star,
raw repair and full endpoint/gap checks. No floating point is used.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,importlib.util,json,resource,signal,time
HELPER=Path(__file__).resolve().parent.parent/'two-load-types'/'verify_full.py'
spec=importlib.util.spec_from_file_location('two_load_type_full',HELPER)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
base,two=prior.base,prior.two
vecadd,scale,dot,unit,nullspace=prior.vecadd,prior.scale,prior.dot,prior.unit,prior.nullspace
require=base.require
def alarm(signum,frame):raise TimeoutError('three-distinct stage60s guard reached')
signal.signal(signal.SIGALRM,alarm)
def build(n,loads):
    base.require(type(n) is int and 3<=n<=6 and 3<=len(loads)<=n,'literal marks/cube guard')
    base.require(all(type(t) is int and t>=1 for t in loads),'positive integer loads')
    base.require(len(set(loads)) in (2,3) and loads==sorted(loads,reverse=True),'two or three decreasing types (two types only for the credited baseline)')
    q=1<<(n-1);D=max(loads);M=sum(loads);N=2*q+2*M;s=q+D;w=F(s-1);k=loads.count(D)
    base.require(M>=3 and N<=80,'residual and literal guards')
    oldN=2*q-1;full=oldN;old=list(range(1,2*q));marks=[i for i,t in enumerate(loads) for _ in range(t)]
    c0=[[F((q+D)*int(a==b)+(q-D)*int(a^b==full)-1) for b in old] for a in old]
    hs=[[F(-bool(a&(1<<mark))) for a in old] for mark in range(len(loads))]
    oldco=[[F(i==j) for j in range(oldN)] for i in range(oldN)]+[[x/D for x in hs[mark]] for mark in marks]
    ti=[[F(q+D)*(int(u==v)-F(1,D)) if marks[u]==marks[v] else F(0) for v in range(M)] for u in range(M)]
    residual=[[F(0)]*(oldN+M) for _ in range(oldN+M)]
    for u in range(M):
        for v in range(M):residual[oldN+u][oldN+v]=ti[u][v]
    b=two.gram(c0,oldco,residual)
    cs=[F(M*(w-loads[mark]-M-1),M+1)/((M-1)*w-1+loads[mark]) for mark in marks]
    csum=[F(0)]*oldN+cs
    leafco=[[-F(1,M+1)+cs[u]*int(j==oldN+u)-csum[j]/M for j in range(oldN+M)] for u in range(M)]
    lg=two.gram(b,leafco,[[F(0)]*M for _ in range(M)]);eta=[w-lg[u][u] for u in range(M)]
    totaleta=sum(eta);zeta=[F(M,M-2)*(x-totaleta/(M*(M-1))) for x in eta]
    W=[[zeta[u]*int(u==v)-(zeta[u]+zeta[v])/M+sum(zeta)/(M*M) for v in range(M)] for u in range(M)]
    base.require(all(sum(row)==0 for row in W),'row-zero general residual')
    base.require([W[u][u] for u in range(M)]==eta,'exact general residual diagonals')
    base.require(base.psd_rank(W)==M-1,'positive full residual simplex')
    family=list(range(2*q));coeff=[[F(i==j) for j in range(oldN+M)] for i in range(oldN)]
    for u in range(M):
        fresh=1<<(n+u);family.extend([fresh,fresh|(1<<marks[u])]);coeff.extend([leafco[u],[F(j==oldN+u) for j in range(oldN+M)]])
    residual=[[F(0)]*(N-1) for _ in range(N-1)]
    for u in range(M):
        for v in range(M):residual[oldN+2*u][oldN+2*v]=W[u][v]
    seed=two.gram(b,coeff,residual)
    A2=sum(t*t for t in loads);B=w+M*(q+D)-A2-2*M
    base.require(sum(map(sum,seed))==B/(M+1)**2,'general centered empty energy')
    rawcoeff=[[F(i==j) for j in range(oldN+M)] for i in range(oldN)]
    rawres=[[F(0)]*(N-1) for _ in range(N-1)]
    for u in range(M):
        rawcoeff.extend([[-F(j==oldN+u)/w for j in range(oldN+M)],[F(j==oldN+u) for j in range(oldN+M)]])
        rawres[oldN+2*u][oldN+2*u]=w-1/w
    raw=two.gram(b,rawcoeff,rawres)
    raw_B=w+(1-1/w)**2*(M*(q+D)-A2)-2*M*(1-1/w)+M*(w-1/w)
    base.require(sum(map(sum,raw))==raw_B,'actual raw empty energy')
    Traw=(N-1)*w+raw_B
    return family,s,seed,raw,Traw,{'n':n,'q':q,'loads':loads,'N':N,'s':s,'k':k,'minimum_eta':str(min(eta)),'minimum_zeta':str(min(zeta)),'minimum_c':str(min(cs)),'maximum_c':str(max(cs)),'seed_empty_energy':str(B/(M+1)**2)}

def mm(A,B):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def transpose(A):return list(map(list,zip(*A)))
def zero(n,m=None):return [[F(0)]*(n if m is None else m) for _ in range(n)]
def determinant(A):
    # Exact rational elimination, separate from cofactor reconstruction.
    B=[r[:] for r in A];answer=F(1)
    for j in range(len(B)):
        pivot=next((i for i in range(j,len(B)) if B[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:B[j],B[pivot]=B[pivot],B[j];answer=-answer
        d=B[j][j];answer*=d
        for i in range(j+1,len(B)):
            factor=B[i][j]/d
            for k in range(j+1,len(B)):B[i][k]-=factor*B[j][k]
    return answer
def scalars(q,loads):
    D,t,v=loads;m=sum(loads);w=F(q+D-1);h=F(2*q+2*m-1)
    ci=[F(m*(w-d-m-1),m+1)/((m-1)*w-1+d) for d in loads]
    normK=w+m*(q+D)-sum(d*d for d in loads)-2*m
    csquare=sum(c*c*d*(q+D-d) for c,d in zip(ci,loads))
    kc=sum(c*d*(w-d) for c,d in zip(ci,loads))
    eta=[w-normK/(m+1)**2-c*c*w+2*c*c*(q+D-d)/m-csquare/m**2+2*c*(w-d)/(m+1)-2*kc/(m*(m+1)) for c,d in zip(ci,loads)]
    total=sum(d*e for d,e in zip(loads,eta))
    zeta=[F(m,m-2)*(e-total/(m*(m-1))) for e in eta]
    W=[[zeta[i]/loads[i]*int(i==j)-(zeta[i]+zeta[j])/m+sum(d*z for d,z in zip(loads,zeta))/m**2 for j in range(3)] for i in range(3)]
    G=zero(9);G[0][0]=q-1;G[1][1]=D
    for i in range(3):
        for j in range(3):G[2+i][2+j]=D*(q*int(i==j)-1)
    G[5][5]=F(q+D)*(F(1,t)-F(1,D));G[6][6]=F(q+D)*(F(1,v)-F(1,D))
    for i in range(2):
        for j in range(2):G[7+i][7+j]=W[i][j]
    F0=zero(9);F0[0][0]=(q+1)*(q-1);F0[0][1]=F0[1][0]=D*(q-1);F0[1][1]=D*D
    for i in range(3):
        for j in range(3):F0[2+i][2+j]=2*D*G[2+i][2+j]
    R=zero(9);delta=(h-q-1)*(h-D)-D*(q-1)
    R[0][0]=F(q-1)*(h-D)/delta;R[0][1]=R[1][0]=F(D*(q-1))/delta;R[1][1]=F(D)*(h-q-1)/delta
    for i in range(3):
        for j in range(3):R[2+i][2+j]=G[2+i][2+j]/(h-2*D)
    for i in range(5,9):
        for j in range(5,9):R[i][j]=G[i][j]/h
    action=zero(9);action[0][0]=q+1;action[1][0]=q-1;action[0][1]=action[1][1]=D
    for i in range(2,5):action[i][i]=2*D
    require(mm(R,[[h*int(i==j)-action[i][j] for j in range(9)] for i in range(9)])==G,'complete resolvent/old-frame identity')
    L=[]
    for i in range(3):
        a=[F(0)]*9;a[1]=a[2+i]=F(1,D)
        if i>0:a[4+i]=F(1)
        L.append(a)
    K=vecadd(unit(9,0),scale(-1,unit(9,1)),*(scale(d,l) for d,l in zip(loads,L)))
    Csum=vecadd(*(scale(d*c,l) for d,c,l in zip(loads,ci,L)))
    contrasts=[vecadd(scale(ci[i],L[i]),scale(F(-1,m),Csum),unit(9,7+i)) for i in range(2)]
    updates=L+[K]+contrasts
    inv=zero(6)
    for i,d in enumerate(loads):inv[i][i]=F(1,d)
    inv[3][3]=m+1
    for i in range(2):
        for j in range(2):inv[4+i][4+j]=F(i==j,loads[i])-F(1,m)
    Wc=[[F(loads[i])*int(i==j)+F(loads[i]*loads[j],loads[2]) for j in range(2)] for i in range(2)]
    require(mm(Wc,[row[4:] for row in inv[4:]])==[[F(i==j) for j in range(2)] for i in range(2)],'exact two-contrast inverse weights')
    products=mm(mm(updates,R),transpose(updates))
    budget=[[inv[i][j]-products[i][j] for j in range(6)] for i in range(6)]
    # Remove the old part of both contrasts by a determinant-one congruence.
    B=zero(4,2)
    for i in range(3):
        for j in range(2):B[i][j]=ci[i]*int(i==j)-F(loads[i],m)*ci[i]
    transform=[[F(i==j) for j in range(6)] for i in range(6)]
    for i in range(4):
        for j in range(2):transform[i][4+j]=-B[i][j]
    changed=mm(mm(transpose(transform),budget),transform)
    expected=zero(6)
    for i in range(4):
        for j in range(4):expected[i][j]=budget[i][j]
    for i in range(4):
        for j in range(2):expected[i][4+j]=expected[4+j][i]=-inv[i][i]*B[i][j]
    for i in range(2):
        for j in range(2):expected[4+i][4+j]=inv[4+i][4+j]-W[i][j]/h+sum(inv[l][l]*B[l][i]*B[l][j] for l in range(4))
    require(changed==expected,'all six-by-six two-contrast congruence entries')
    leading=[determinant([row[:size] for row in changed[:size]]) for size in range(1,7)]
    within=[1-c*c*(q+D)/(h-q-D)-z/h for c,z in zip(ci,zeta)]
    require(min(*eta,*zeta,*within,*leading)>0,'fixture positivity only')
    require(base.psd_rank(G)==9 and base.psd_rank(budget)==6,'literal full-rank mean metric/budget')
    return {'ci':ci,'eta':eta,'zeta':zeta,'W':W,'normK':normK,'G':G,'F0':F0,'R':R,'update_coordinates':updates,'Wc':Wc,'budget':budget,'congruent_budget':changed,'leading_minors':leading,'within_slacks':within}

def border_minors(M):
    from itertools import combinations
    A=[row[:4] for row in M[:4]];X=[row[4:] for row in M[:4]];E=[row[4:] for row in M[4:]]
    detA=determinant(A)
    adj=[[(-1)**(i+j)*determinant([[A[a][b] for b in range(4) if b!=i] for a in range(4) if a!=j]) for j in range(4)] for i in range(4)]
    require(mm(A,adj)==[[detA*int(i==j) for j in range(4)] for i in range(4)],'all leading adjugate identities')
    Y=mm(mm(transpose(X),adj),X)
    pairs=list(combinations(range(4),2))
    plucker={I:X[I[0]][0]*X[I[1]][1]-X[I[0]][1]*X[I[1]][0] for I in pairs}
    compound=F(0)
    for I in pairs:
        for J in pairs:
            complement=[[A[a][b] for b in range(4) if b not in I] for a in range(4) if a not in J]
            compound+=plucker[I]*plucker[J]*(-1)**(sum(I)+sum(J))*determinant(complement)
    fifth=detA*E[0][0]-Y[0][0]
    sixth=detA*determinant(E)-E[1][1]*Y[0][0]-E[0][0]*Y[1][1]+2*E[0][1]*Y[0][1]+compound
    require(fifth==determinant([row[:5] for row in M[:5]]) and sixth==determinant(M),'literal fifth/sixth bordered cofactor identities')
    require(compound*detA==determinant(Y),'literal second-compound Jacobi identity')
    return {'fifth':str(fifth),'sixth':str(sixth),'nonzero_two_by_two_border_minors':sum(bool(x) for x in plucker.values()),'cofactor_entries':16,'second_compound_terms':sum(bool(plucker[I]*plucker[J]) for I in pairs for J in pairs),'division_by_leading_determinant_in_reconstruction':False}

def check(n,D,t,v):
    started=time.monotonic();signal.alarm(60)
    require(D>t>v>=1,'three strictly decreasing loads')
    loads=[D,t,v];m=sum(loads);family,s,c,raw,Traw,params=build(n,loads)
    q=params['q'];N=len(family);coreN=N-1;oldN=2*q-1
    model=scalars(q,loads);ci,zeta=model['ci'],model['zeta']
    require(min(model['eta'])==F(params['minimum_eta']) and min(zeta)==F(params['minimum_zeta']),'full/scalar three-type variances')
    oldsum=[F(i<oldN) for i in range(coreN)]
    h0=scale(F(-1,2),vecadd(oldsum,unit(coreN,oldN-1)));gp=vecadd(oldsum,h0)
    hi=[[-F(i<oldN and bool(family[i+1]&(1<<mark))) for i in range(coreN)] for mark in range(3)]
    ai=[vecadd(x,scale(-1,h0)) for x in hi]
    spokes=[unit(coreN,oldN+2*j+1) for j in range(m)];leaves=[unit(coreN,oldN+2*j) for j in range(m)]
    offsets=[0,D,D+t]
    L=[scale(F(1,d),vecadd(*spokes[o:o+d])) for o,d in zip(offsets,loads)]
    require(two.matvec(c,L[0])==scale(F(1,D),two.matvec(c,hi[0])),'physical saturated heavy spoke mean')
    Z=[vecadd(L[i],scale(F(-1,D),hi[i])) for i in (1,2)]
    K=vecadd(oldsum,*spokes);Csum=vecadd(*(scale(d*a,l) for d,a,l in zip(loads,ci,L)))
    sigma=[vecadd(scale(a,l),scale(F(-1,m),Csum)) for a,l in zip(ci,L)]
    W=[vecadd(scale(F(1,d),vecadd(*leaves[o:o+d])),scale(F(1,m+1),K),scale(-1,y)) for o,d,y in zip(offsets,loads,sigma)]
    require(not any(two.matvec(c,vecadd(*(scale(d,w) for d,w in zip(loads,W))))),'all weighted W mean products vanish')
    sigma=[vecadd(y,w) for y,w in zip(sigma,W)]
    require(not any(two.matvec(c,vecadd(*(scale(d,y) for d,y in zip(loads,sigma))))),'all weighted singleton contrasts vanish')
    coords=[gp,h0,*ai,*Z,*W[:2]];groups=[]
    for o,d,a,z in zip(offsets,loads,ci,zeta):
        ts=[vecadd(spokes[j],scale(-1,spokes[o+d-1])) for j in range(o,o+d-1)]
        ww=[vecadd(leaves[j],scale(-1,leaves[o+d-1]),scale(-a,ts[j-o])) for j in range(o,o+d-1)]
        groups.append((len(coords),d-1,a,z));coords+=ts+ww
    changed=len(coords);images=[two.matvec(c,x) for x in coords]
    gram=[[dot(coords[i],images[j]) for j in range(changed)] for i in range(changed)]
    expected=zero(changed)
    for i in range(9):
        for j in range(9):expected[i][j]=model['G'][i][j]
    for o,d,a,z in groups:
        for i in range(d):
            for j in range(d):
                expected[o+i][o+j]=(q+D)*(1+int(i==j));expected[o+d+i][o+d+j]=z*(1+int(i==j))
    require(gram==expected and base.psd_rank(gram)==changed,'every changed-sector Gram entry and independence')
    # Check the actual nine mean-coordinate update maps, not just their norms.
    updates=L+[K]+sigma[:2]
    for physical,abstract in zip(updates,model['update_coordinates']):
        require(two.matvec(c,physical)==two.matvec(c,vecadd(*(scale(x,coords[i]) for i,x in enumerate(abstract)))),'literal nine-coordinate update equality')
    empty=[-sum(x) for x in images]
    require(all(empty[i]==0 for i in range(9,changed)) and any(empty[:9]),'actual empty vector invariant and nonzero')
    frame=[[dot(images[i],images[j])+empty[i]*empty[j] for j in range(changed)] for i in range(changed)]
    target=zero(changed)
    for i in range(9):
        for j in range(9):target[i][j]=model['F0'][i][j]
    for weight,update in zip([*map(F,loads),F(1,m+1)],L+[K]):
        products=[dot(image,update) for image in images[:9]]
        for i in range(9):
            for j in range(9):target[i][j]+=weight*products[i]*products[j]
    products=[[dot(image,update) for update in sigma[:2]] for image in images[:9]]
    for i in range(9):
        for j in range(9):target[i][j]+=sum(products[i][a]*model['Wc'][a][b]*products[j][b] for a in range(2) for b in range(2))
    for o,d,a,z in groups:
        for i in range(d):
            for j in range(d):
                b=1+int(i==j);target[o+i][o+j]=(q+D)**2*(1+a*a)*b
                target[o+i][o+d+j]=target[o+d+j][o+i]=a*(q+D)*z*b
                target[o+d+i][o+d+j]=z*z*b
    require(frame==target,'every full mean/internal/cross frame entry including empty')
    require(any(frame[i][j]!=dot(images[i],images[j]) for i in range(9) for j in range(9)),'omitting actual empty changes the frame')
    full=oldN;pairs=[(x,full^x) for x in range(1,full) if x<(full^x)]
    highs=[vecadd(unit(coreN,x-1),unit(coreN,z-1),scale(-1,unit(coreN,pairs[0][0]-1)),scale(-1,unit(coreN,pairs[0][1]-1))) for x,z in pairs[1:]]
    constraints=[[-F(bool(x&(1<<mark)))+F(bool(z&(1<<mark))) for x,z in pairs] for mark in range(3)]
    lows=[]
    for weights in nullspace(constraints,len(pairs)):
        x=[F(0)]*coreN
        for weight,(a,b) in zip(weights,pairs):x[a-1]+=weight;x[b-1]-=weight
        lows.append(x)
    for label,rows,eigenvalue,count in [('high',highs,2*q,q-2),('low',lows,2*D,q-4)]:
        require(len(rows)==count,'complete untouched '+label+' count')
        for x in rows:
            require(two.matvec(c,x)==scale(eigenvalue,x),'physical untouched '+label+' action')
            require(all(dot(image,x)==0 for image in images),'every changed/untouched '+label+' cross product')
    require(changed+len(highs)+len(lows)==N-3,'complete seed frame dimension census')
    star=[F(bool(x&1)) for x in family[1:]]
    require(sum(star)==s and not any(two.matvec(c,star)) and not any(two.matvec(raw,star)),'actual heavy-star size and both core kernels')
    centered=[F(bool(x&1))-F(s,N) for x in family]
    matrix=base.lift(c,s);literal=base.check(family,matrix,s)
    require(literal['lower_rank']==N-2 and literal['upper_rank']==N-1,'three-value sample seed endpoint ranks')
    gap=[[(N-s)*(int(i==j)-matrix[i][j])-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(base.psd_rank(gap)==N-1 and base.psd_rank(raw)==N-2,'sample seed unit gap and exact raw rank')
    epsilon=F(1,2)/(1+Traw)
    mixed=[[(1-epsilon)*c[i][j]+epsilon*raw[i][j] for j in range(N-1)] for i in range(N-1)]
    mixedM=base.lift(mixed,s);mixed_check=base.check(family,mixedM,s)
    require(mixed_check['lower_rank']==N-1 and mixed_check['upper_rank']==N-1,'sample repaired greatest ranks')
    require(two.matvec(mixedM,centered)==scale(F(-s,N-s),centered),'actual centered heavy-star endpoint action')
    half=[[(N-s)*(int(i==j)-mixedM[i][j])-F(1,2)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(base.psd_rank(half)==N-1,'sample full repaired half-unit gap')
    bad=[row[:] for row in c];bad[oldN][oldN+1]+=1;bad[oldN+1][oldN]+=1
    try:base.check(family,base.lift(bad,s),s)
    except ValueError:pass
    else:raise ValueError('intersecting-entry damage accepted')
    bad=[row[:] for row in mixedM];bad[0][0]+=1
    try:base.check(family,bad,s)
    except ValueError:pass
    else:raise ValueError('empty-loop damage accepted')
    cofactors=border_minors(model['congruent_budget'])
    signal.alarm(0)
    return {'n':n,'loads':loads,'q':q,'N':N,'s':s,'mean_dimension':9,'internal_dimension':2*(m-3),'changed_dimension':changed,'untouched_high':len(highs),'untouched_low':len(lows),'full_frame_dimension':N-3,'every_Gram_and_frame_entry':changed**2,'all_cross_sectors_checked':True,'actual_empty_checked':True,'omitted_empty_changes_frame':True,'literal_update_coordinates_checked':6,'resolvent_identity_entries':81,'congruence_entries':36,'seed':literal,'raw_core_rank':N-2,'mixed':mixed_check,'seed_unit_gap':True,'mixed_half_unit_gap':True,'ci':list(map(str,ci)),'eta':list(map(str,model['eta'])),'zeta':list(map(str,zeta)),'within_slacks':list(map(str,model['within_slacks'])),'six_congruent_leading_minors':list(map(str,model['leading_minors'])),'congruent_budget':[[str(x) for x in row] for row in model['congruent_budget']],'bordered_cofactor_reconstruction':cofactors,'damage_checks':2,'elapsed_seconds':time.monotonic()-started}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);parser.add_argument('--expected',type=Path);parser.add_argument('--case',nargs=4,type=int);args=parser.parse_args();started=time.monotonic()
    signal.alarm(60)
    baseline=prior.build(3,[3,3,2]);require(build(3,[3,3,2])==baseline,'private whole constructor unchanged on9153 baseline')
    signal.alarm(0);rows=[]
    for case in ([tuple(args.case)] if args.case else [(3,3,2,1),(4,4,3,1),(5,5,3,2),(3,7,5,4),(6,3,2,1)]):
        row=check(*case);rows.append(row)
        if args.write:args.write.write_text(json.dumps({'agent':'six-downset-1','role':'researcher','status':'partial finite validation only','fixtures':rows},indent=2)+'\n')
        print(json.dumps({'finished_case':case,'elapsed_seconds':row['elapsed_seconds']}),flush=True)
    result={'agent':'six-downset-1','role':'researcher','status':'finite exact validation; uniform coverage uses PROOF.md and verify_signs.py','baseline_source':'733fd3c0067e8dd56a2c68a12361b50abe65fe42','whole9153_constructor_equal':True,'fixtures':rows,'elapsed_seconds':time.monotonic()-started,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.expected:
        expected=json.loads(args.expected.read_text())['full']
        def stable(out):
            return {k:([{a:b for a,b in row.items() if a!='elapsed_seconds'} for row in value] if k=='fixtures' else value) for k,value in out.items() if k not in ['elapsed_seconds','peak_RSS_KiB']}
        require(stable(result)==stable(expected),'frozen full-frame certificate mismatch')
    if args.write:args.write.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
