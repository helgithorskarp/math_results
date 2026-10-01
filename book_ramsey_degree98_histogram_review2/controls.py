"""Independent positive, exact-arithmetic, signed-host and literal-star controls.

Reads only reviewer-generated positive Grams. No author certificate is used.
"""
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction as F
from collections import Counter
import argparse,json,time
from incidence import need,canonical,image
from domains import matrix,gram,marked_cubic8
from exact import psd,quadratic,inverse_integer
from parent import search
from zero import stars,points,mask


def determinant(a):
    """Fraction-free Bareiss elimination, separate from congruence/inversion."""
    n=len(a)
    if not n:return 1
    r=[list(row) for row in a];previous=1;sign=1
    for k in range(n-1):
        p=next((p for p in range(k,n) if r[p][k]),None)
        if p is None:return 0
        if p!=k:r[k],r[p]=r[p],r[k];sign=-sign
        pivot=r[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=pivot*r[i][j]-r[i][k]*r[k][j]
                need(numerator%previous==0,'nonintegral Bareiss division')
                r[i][j]=numerator//previous
        for i in range(k+1,n):r[i][k]=0
        previous=pivot
    return sign*r[-1][-1]


def rejected(call):
    try:call()
    except ValueError:return
    raise ValueError('malformed/limited control was accepted')


def positive_parent():
    # Two repeated111 rows; four one-tail rows; seven distinct tail triples.
    tail=range(3,8);removed={(3,7),(4,7),(5,6)}
    rows=[(0,1,2),(0,1,2),(0,2,3),(0,2,4),(1,2,5),(1,2,6)]
    rows += [tuple(z for z in tail if z not in pair) for pair in combinations(tail,2) if pair not in removed]
    capacity=[[sum(i in row and j in row for row in rows) for j in range(8)] for i in range(8)]
    counts=(2,2,2,0,0,7)
    answer,states=search(capacity,counts)
    need(answer is not None,'positive repeated-row search failed')
    families=[tuple(c for c in combinations(range(8),3) if sum(1<<z for z in c if z<3)==p) for p in (7,5,6,1,2,0)]
    actual=[families[f][i] for f,i in answer]
    need(Counter(f for f,i in answer)==Counter({0:2,1:2,2:2,5:7}),'wrong positive profile')
    need(all(sum(z in row for row in actual)==(4,4,6,5,5,5,5,5)[z] for z in range(8)),'wrong positive columns')
    need(all(sum(i in row and j in row for row in actual)<=capacity[i][j] for i,j in combinations(range(8),2)),'wrong positive pair bound')
    need(actual.count((0,1,2))==2,'repeated rows were discarded')
    bad=[list(row) for row in capacity];bad[0][1]=bad[1][0]=0
    need(search(bad,counts)[0] is None,'negative pair control failed')
    rejected(lambda:search(capacity,counts,cap=0))
    rejected(lambda:search(capacity,counts,cap=200001))
    rejected(lambda:search(capacity,counts,seconds=11))
    bad=[list(row) for row in capacity];bad[0][0]+=1
    rejected(lambda:search(bad,counts))
    return rows,dict(positive_rows=len(rows),positive_search_states=states,repeated111=2,negative_pair_control=True,guard_and_quota_rejections=4)


def arithmetic(records):
    # All729 ternary symmetric3x3 matrices, checked by every principal minor.
    checked=0
    for entries in product((-1,0,1),repeat=6):
        a=[[0]*3 for _ in range(3)]
        for x,(i,j) in zip(entries,[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]):a[i][j]=a[j][i]=x
        minors=[(len(c),determinant([[a[i][j] for j in c] for i in c])) for k in range(1,4) for c in combinations(range(3),k)]
        ok,rank,q=psd(a)
        need(ok==all(d>=0 for k,d in minors),'PSD/principal-minor mismatch')
        if ok:need(rank==max([0]+[k for k,d in minors if d]),'PSD rank mismatch')
        else:need(quadratic(a,q)<0,'negative witness did not verify')
        checked+=1
    cofactors=0
    for rec in records:
        a=gram(matrix(10,rec['canonical_edges']));q,d=inverse_integer(a);det=determinant(a)
        need(det>0,'positive representative determinant failed')
        for i in range(10):
            for j in range(10):
                co=(-1)**(i+j)*determinant([[a[u][v] for v in range(10) if v!=i] for u in range(10) if u!=j])
                need(F(q[i][j],d)==F(co,det),'inverse/adjugate mismatch');cofactors+=1
    rejected(lambda:psd([[1,2],[0,1]]))
    rejected(lambda:inverse_integer([[1,1],[1,1]]))
    rejected(lambda:canonical((3,),2,((0,1),),cap=0))
    rejected(lambda:canonical((3,),2,((0,1),),cap=200001))
    return dict(ternary_symmetric3_matrices=checked,all_principal_minors=checked*7,independent_adjugate_entries=cofactors,malformed_and_guard_rejections=4)


def roots():
    pairs=tuple(combinations(range(4),2));accepted=[];types=Counter()
    for w in range(64):
        es={p for i,p in enumerate(pairs) if w>>i&1}
        s=[sum(tuple(sorted((a,b))) in es for b in range(3) if b!=a) for a in range(3)]
        eps=[int((a,3) in es) for a in range(3)]
        if any(-2+2*(s[a]-eps[a])<0 for a in range(3)):continue
        k=sum(eps);shape='K3' if sum(s)==6 else 'P3';accepted.append(w);types[(shape,k)]+=1
        qA=sum(-2+2*(s[a]-eps[a]) for a in range(3));qz=2+2*k
        need(24-qA-qz==(16 if shape=='K3' else 20),'root defect budget failed')
    need(types==Counter({('P3',0):3,('P3',1):3,('K3',0):1,('K3',1):3,('K3',2):3,('K3',3):1}),'incomplete root census')
    path=0
    for eps,gamma,rho in product(range(2),repeat=3):
        if gamma<eps:continue
        need(2+eps+rho>gamma-eps,'path containment contradiction failed');path+=1
    for gamma,rho in product(range(2),repeat=2):need(4+rho>2+gamma,'k2 containment contradiction failed')
    need(3<7,'k3 bound failed')
    return dict(root_words=64,necessary_root_words=len(accepted),root_types=[dict(shape=s,k=k,labeled=n) for (s,k),n in sorted(types.items())],path_parameter_checks=path,k2_parameter_checks=4)


def exterior(degrees,A):
    """Bounded exact degree completion with the three forced triangle edges."""
    n=len(degrees);fixed={tuple(p) for p in combinations(sorted(A),2)}
    residual=[degrees[z]-sum(z in e for e in fixed) for z in range(n)]
    states=0;start=time.monotonic()
    def visit(q,es):
        nonlocal states
        states+=1;need(states<=200000 and time.monotonic()-start<=10,'INCOMPLETE signed-host guard')
        if not any(q):return es
        v=max(range(n),key=lambda z:q[z]);available=[u for u in range(n) if u!=v and q[u]>0 and tuple(sorted((u,v))) not in es]
        for other in combinations(available,q[v]):
            nq=list(q);nq[v]=0
            for u in other:nq[u]-=1
            if any(x<0 for x in nq):continue
            answer=visit(nq,es|{tuple(sorted((u,v))) for u in other})
            if answer is not None:return answer
        return None
    answer=visit(residual,fixed)
    need(answer is not None,'signed exterior completion missing')
    return answer


def host_check(a,root,A):
    n=22;d=[sum(r) for r in a];e=sum(d)//2
    need(Counter(d)==Counter({8:3,9:18,10:1}),'signed host degree histogram wrong')
    blue=[[int(i!=j and not a[i][j]) for j in range(n)] for i in range(n)]
    c=[[sum(a[i][k]*a[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    cb=[[sum(blue[i][k]*blue[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    f=[[0 if i==j else (3-c[i][j] if a[i][j] else 6-cb[i][j]) for j in range(n)] for i in range(n)]
    need(any(f[i][j]<0 for i in range(n) for j in range(n)),'signed fixture accidentally claimed a Ramsey host')
    z=d.index(10)
    for i in range(n):
        tR=sum(a[i][j]*a[i][k]*a[j][k] for j,k in combinations(range(n),2))
        tB=sum(blue[i][j]*blue[i][k]*blue[j][k] for j,k in combinations(range(n),2))
        fr=sum(f[i][j] for j in range(n) if a[i][j]);fb=sum(f[i][j] for j in range(n) if blue[i][j])
        need(fr==3*d[i]-2*tR and fb==6*(21-d[i])-2*tB,'signed parity identity failed')
        neighbor_sum=sum(d[j] for j in range(n) if a[i][j]);sA=sum(a[i][j] for j in A);epsilon=a[i][z]
        need(sum(f[i])==2*e-294+38*d[i]-d[i]**2-2*neighbor_sum==2-(d[i]-10)**2+2*(sA-epsilon),'signed incident identity failed')
        need(tR+tB==(21-d[i])*(20-d[i])//2-e+neighbor_sum,'signed triangle identity failed')
    N=[j for j in range(n) if a[root][j]];V=[j for j in range(n) if j!=root and not a[root][j]]
    for x in N:
        for y in N:
            local=sum(a[x][u]*a[y][u] for u in N)
            actual=sum(a[x][v]*a[y][v] for v in V)
            target=d[x]-1-sum(a[x][u] for u in N) if x==y else (2 if a[x][y] else d[x]+d[y]-15)-local-f[x][y]
            need(actual==target,'signed literal local Gram failed')
    if d[root]==10:
        h=[sum(a[x][y] for y in N) for x in N];t=[f[root][x] for x in N];g=[f[root][v] for v in V]
        for k,x in enumerate(N):
            sx=sum(a[u][x] for u in A)
            rhs=sx-2-t[k]+sum(a[x][y]*t[l] for l,y in enumerate(N))+sum(a[x][v]*g[l] for l,v in enumerate(V))
            need(sum(f[x][y] for y in N)==rhs,'signed zero defect-row identity failed')
    else:
        b,c=sorted(A-{root})
        for v in V:
            delta=a[v][b]+a[v][c]-a[v][z]
            need(sum(f[v][x] for x in N)==1+delta and sum(f[v][u] for u in V)==delta,'signed one-attachment exterior identity failed')
    return len(N)**2


def hosts(parent_rows,fixtures):
    # Parent root21, N0..7=(b,c,z,U), V8..20.
    a=[[0]*22 for _ in range(22)]
    def edge(a,u,v):a[u][v]=a[v][u]=1
    for u,v in marked_cubic8()[0]:edge(a,u,v)
    for x in range(8):edge(a,21,x)
    for v,row in enumerate(parent_rows):
        for x in row:edge(a,8+v,x)
    for v in range(13):
        for step in (1,2,3):edge(a,8+v,8+(v+step)%13)
    entries=host_check(a,21,{21,0,1});count=1
    for rec in fixtures:
        rows=rec['rows'];pair=next(p for p in combinations(range(5),2) if not rows[p[0]]&rows[p[1]])
        A=set(range(5))-set(pair);a=[[0]*22 for _ in range(22)]
        for u,v in rec['edges']:edge(a,u,v)
        for x in range(10):edge(a,21,x)
        for v,row in enumerate(rows):
            for x in points(row):edge(a,10+v,x)
        for u,v in exterior([5 if z in pair else 4 for z in range(11)],A):edge(a,10+u,10+v)
        entries+=host_check(a,21,{10+v for v in A});count+=1
    return dict(signed_hosts=count,incident_and_parity_rows=22*count,local_Gram_entries=entries,signed_controls_are_not_Ramsey_constructions=True)


def star_comparison(fixtures):
    placements=cases=forced=relaxed=0;forced_zero=relaxed_zero=0
    for rec in fixtures:
        rows=rec['rows'];j=matrix(10,rec['edges'])
        need([[sum((w>>i&1)*(w>>k&1) for w in rows) for k in range(10)] for i in range(10)]==gram(j),'positive fixture Gram mismatch')
        for pair in combinations(range(5),2):
            if rows[pair[0]]&rows[pair[1]]:continue
            A=set(range(5))-set(pair);placements+=1
            for forced_triangle in (True,False):
                literal=stars(j,rows,pair,forced_triangle);separate=[]
                for a in sorted(A):
                    accepted=[]
                    for tail in combinations([v for v in range(11) if v!=a],4):
                        if forced_triangle and not A-{a}<=set(tail):continue
                        if forced_triangle:forced+=1
                        else:relaxed+=1
                        common=[sum(j[x][y] for y in points(rows[a]))+sum(rows[v]>>x&1 for v in tail) for x in range(10)]
                        if max(common)<=3:accepted.append(mask(tail))
                    separate.append(tuple(accepted));cases+=1
                    if not accepted:
                        if forced_triangle:forced_zero+=1
                        else:relaxed_zero+=1
                need(tuple(separate)==literal,'full permitted-star sets disagree')
                need(any(not ss for ss in separate),'positive star placement survives')
    return dict(positive_Grams=len(fixtures),exceptional_placements=placements,star_set_comparisons=cases,forced_candidates=forced,relaxed_candidates=relaxed,forced_empty_stars=forced_zero,relaxed_empty_stars=relaxed_zero)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--grams',required=True);ap.add_argument('--work-dir',required=True);ap.add_argument('--expected');args=ap.parse_args()
    source=Path(__file__).resolve().parent;fixtures=json.loads(Path(args.grams).read_text());record=json.loads((source/'expected.json').read_text())
    rows,p=positive_parent()
    result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',parent_positive=p,arithmetic=arithmetic(record['zero']['positive_classes']),root_census=roots(),signed_hosts=hosts(rows,fixtures),stars=star_comparison(fixtures),all_pass=True)
    if args.expected:need(result==json.loads(Path(args.expected).read_text()),'control result differs from expected')
    work=Path(args.work_dir);work.mkdir(parents=True,exist_ok=True);(work/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
