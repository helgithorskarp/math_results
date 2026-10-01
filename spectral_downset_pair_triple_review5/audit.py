"""Literal set construction, independent compressions and exact fixed-line cap."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import comb,isqrt
from pathlib import Path
import argparse,json,os,platform,resource,time
from exact import canonical,require,determinant,inverse,leading,polynomial,value

N=502;S=247;SCALE=200
Z={2:1225,3:530,4:420,5:420,6:530,7:1225}

def literal():
    sets=tuple(frozenset(c) for k in range(2,8) for c in combinations(range(9),k))
    full=frozenset(range(9));m=len(sets);require(m==492,'middle coverage')
    base=[];slope=[]
    for a in sets:
        row=[];moving=[]
        for b in sets:
            v=SCALE*(S-1) if a==b else -SCALE
            if a|b==full and not a&b:v+=SCALE*S-Z[len(a)]
            row.append(v);moving.append(SCALE*int(not a&b and {len(a),len(b)}=={2,3}))
        base.append(row);slope.append(moving)
    return sets,base,slope

def apply(a,v):return tuple(sum(x*y for x,y in zip(row,v) if y) for row in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def lift(sets,v):
    return (sum((len(a)-1)*x for a,x in zip(sets,v)),)+tuple(-sum(x for a,x in zip(sets,v) if i in a) for i in range(9))+tuple(v)

def compress(matrix,vectors,normalization=1):
    images=[apply(matrix,v) for v in vectors]
    return [[F(dot(v,w),SCALE*normalization) for w in images] for v in vectors]

def blocks(sets,base,slope):
    constants=[tuple(int(len(a)==k) for a in sets) for k in range(2,8)]
    standard=[tuple((int(0 in a)-int(1 in a))*int(len(a)==k) for a in sets) for k in range(2,8)]
    output={};grams={};actions=0
    for number,vectors,normalization in ((0,constants,1),(1,standard,2)):
        q0=compress(base,vectors,normalization);q1=compress(slope,vectors,normalization)
        lifted=[lift(sets,v) for v in vectors]
        gram=[[F(dot(a,b),normalization) for b in lifted] for a in lifted]
        D=[F(dot(v,v),normalization) for v in vectors]
        require(all(dot(a,b)==0 for i,a in enumerate(vectors) for b in vectors[i+1:]),'layer basis orthogonality')
        inv=inverse(gram);upper=[[N*D[i]*D[j]*inv[i][j]-q0[i][j] for j in range(6)] for i in range(6)]
        output['Q'+str(number)]=(q0,q1)
        output['U'+str(number)]=(upper,[[-x for x in row] for row in q1]);grams['G'+str(number)]=gram
        for matrix,compressed in ((base,q0),(slope,q1)):
            for j,v in enumerate(vectors):
                actual=apply(matrix,v)
                predicted=tuple(SCALE*sum(vectors[i][r]*compressed[i][j]/D[i] for i in range(6)) for r in range(492))
                require(actual==predicted,'constant or point space not invariant');actions+=492
    weights={frozenset((0,1)):1,frozenset((2,3)):1,frozenset((0,2)):-1,frozenset((1,3)):-1}
    f=tuple(weights.get(a,0) if len(a)==2 else 0 for a in sets)
    u=tuple(sum(x for a,x in weights.items() if a<=b) if len(b)==3 else 0 for b in sets)
    lookup={a:i for i,a in enumerate(sets)}
    complement=lambda v:tuple(v[lookup[frozenset(range(9))-a]] for a in sets)
    vectors=[f,u,complement(u),complement(f)];norm=dot(f,f)
    require(norm==4 and [dot(v,v) for v in vectors]==[4,20,20,4],'coupled lift norms')
    require(all(not sum(v) and all(not sum(x for a,x in zip(sets,v) if i in a) for i in range(9)) for v in vectors),'residual point incidence')
    c0=compress(base,vectors,norm);c1=compress(slope,vectors,norm);D=[1,5,5,1]
    output['C2']=(c0,c1);output['U2']=([[N*D[i]*int(i==j)-c0[i][j] for j in range(4)] for i in range(4)],[[-x for x in row] for row in c1])
    for matrix,compressed in ((base,c0),(slope,c1)):
        for j,v in enumerate(vectors):
            require(apply(matrix,v)==tuple(SCALE*sum(vectors[i][r]*compressed[i][j]/D[i] for i in range(4)) for r in range(492)),
                    'coupled residual space not invariant');actions+=492
    return output,grams,actions

def full_matrix(sets,core):
    m=len(sets);require(m==492 and len(core)==m and all(len(row)==m and all(type(x)is int for x in row) for row in core),'scaled core dimension/domain')
    rows=[tuple(i for i,a in enumerate(sets) if point in a) for point in range(9)]
    rq=[[sum(core[i][j] for i in row) for j in range(m)] for row in rows]
    L=[[0]*N for _ in range(N)]
    for i in range(m):
        for j in range(m):L[10+i][10+j]=core[i][j]+SCALE
        for p in range(9):L[p+1][10+i]=L[10+i][p+1]=SCALE-rq[p][i]
    for p in range(9):
        for q in range(9):L[p+1][q+1]=SCALE+sum(rq[p][j] for j in rows[q])
    for i in range(1,N):L[0][i]=L[i][0]=SCALE*N-sum(L[i][1:])
    L[0][0]=SCALE*N-sum(L[0][1:])
    members=(frozenset(),)+tuple(frozenset((i,)) for i in range(9))+sets
    require(len(set(members))==N and all(len(a)<=7 for a in members),'full downset carrier')
    stars=[tuple(i for i,a in enumerate(members) if p in a) for p in range(9)]
    require(all(len(star)==S for star in stars),'star size')
    count=0
    for i,a in enumerate(members):
        require(sum(L[i])==SCALE*N and (not a or L[i][i]==SCALE*S),'affine rows/diagonal')
        for j,b in enumerate(members):
            require(L[i][j]==L[j][i] and (i==j or not a&b or not L[i][j]),'literal symmetry/support');count+=1
        require(all(sum(L[i][j] for j in star)==SCALE*S for star in stars),'forced stars')
    order=sorted(range(N),key=lambda i:sum(1<<x for x in members[i]))
    fingerprint=sha256(json.dumps([[str(F(L[i][j],SCALE)) for j in order] for i in order],separators=(',',':')).encode()).hexdigest()
    return dict(entries_checked=count,star_equations_checked=N*9,nonempty_diagonals_checked=N-1,
                author_binary_order_L_sha256=fingerprint,min_scaled_L_entry=min(map(min,L)),max_scaled_L_entry=max(map(max,L)))

def incidence_controls():
    records=[]
    for n in range(7,12):
        pairs=tuple(frozenset(a) for a in combinations(range(n),2));triples=tuple(frozenset(a) for a in combinations(range(n),3));q=n-4
        # Each side evaluated on actual finite incidence columns, not imported formulas.
        for a in pairs:
            for b in triples:require(int(not a&b)==1-len(a&b)+int(a<=b),'disjoint/inclusion bridge')
            for c in pairs:require(sum(a<=b and c<=b for b in triples)==q*int(a==c)+len(a&c),'U Gram identity')
            for i in range(n):require(sum(a<=b and i in b for b in triples)==1+(n-3)*int(i in a),'point lift identity')
            require(sum(not a&b for b in pairs)==comb(n-2,2),'pair-disjoint constant action')
            require(sum((int(0 in b)-int(1 in b)) for b in pairs if not a&b)==-(n-3)*(int(0 in a)-int(1 in a)),'pair-disjoint standard action')
            weights={frozenset((0,1)):1,frozenset((2,3)):1,frozenset((0,2)):-1,frozenset((1,3)):-1}
            require(sum(v for b,v in weights.items() if not a&b)==weights.get(a,0),'pair-disjoint residual action')
        for b in triples:
            for i in range(n):require(sum(a<=b and i in a for a in pairs)==2*int(i in b),'transpose point lift identity')
        W2=comb(n,2)-n;Z3=comb(n,3)-comb(n,2)
        dims=[n-3,(n-1)*(n-3),4*W2,2*Z3,sum(comb(n,k)-n for k in range(4,n-3))]
        require(sum(dims)==2**n-2*n-2 and W2>0 and Z3>0,'complete dimension sum')
        records.append(dict(n=n,pair_triple_entries=len(pairs)*len(triples),pair_Gram_entries=len(pairs)**2,
                            point_lift_entries=n*len(pairs),transpose_point_lift_entries=n*len(triples),components=dims,middle=sum(dims)))
    return records

def maximal_interval(polys):
    c=polys['Q0']['coefficients_ascending'];C,B,A=-c[0],c[1],-c[2];disc=B*B-4*A*C
    require(A>0 and B>0 and C>0 and disc>0 and isqrt(disc)**2!=disc,'quadratic endpoints')
    lower,inside,upper=F(1,3),F(17,50),F(7,20)
    require(value(c,lower)<0 and value(c,inside)>0 and value(c,upper)<0,'root bracketing')
    guards={}
    for name,p in polys.items():
        if name=='Q0':continue
        cs=p['coefficients_ascending'];require(cs[2]<0,'nonconcave Schur polynomial')
        endpoints=[value(cs,x) for x in (lower,upper)];require(min(endpoints)>0,'competing cap boundary')
        guards[name]=list(map(str,endpoints))
    intervals=[]
    for a,b,upward in ((lower,inside,True),(inside,upper,False)):
        for _ in range(64):
            mid=(a+b)/2
            if (value(c,mid)>0)==upward:b=mid
            else:a=mid
        intervals.append([str(a),str(b)])
    require(value(c,F(69,200))>0,'primary parameter outside exact interval')
    return dict(fixed_z=['49/8','53/20','21/10'],epsilon='0',quadratic_A=A,quadratic_B=B,quadratic_C=C,
                discriminant=disc,endpoints='(B minus/plus sqrt(discriminant))/(2A)',rational_outer_bracket=['1/3','7/20'],
                root_isolations=intervals,other_five_polynomial_endpoint_values=guards,
                lower_rank_interior=493,lower_rank_at_both_endpoints=492,upper_rank_on_closed_interval=501,
                exact_closed_feasibility_interval=True,exact_open_maximal_rank_interval=True)

def run(target):
    sets,base,slope=literal();b,grams,actions=blocks(sets,base,slope);polys={};ranks={};block_hashes={}
    for name,(fixed,moving) in b.items():
        p=polynomial(fixed,moving);cs=p['coefficients_ascending'];p['value_at_delta']=str(value(cs,F(69,200)));require(F(p['value_at_delta'])>0,'primary block not strict')
        require(cs==target['Schur_polynomials'][name]['coefficients_ascending'] and p['positive_scale']==target['Schur_polynomials'][name]['positive_scale'],'independent Schur polynomial mismatch')
        matrix=[[fixed[i][j]+F(69,200)*moving[i][j] for j in range(len(fixed))] for i in range(len(fixed))]
        leading(matrix);ranks[name]=len(matrix);polys[name]=p
        h=sha256(json.dumps([[str(F(x)) for x in row] for row in matrix],separators=(',',':')).encode()).hexdigest()
        require(h==target['blocks_sha256'][name],'literal block entries differ');block_hashes[name]=h
    core=[[base[i][j]+69*slope[i][j]//200 for j in range(492)] for i in range(492)]
    full=full_matrix(sets,core);require(full['author_binary_order_L_sha256']==target['L_sha256'],'independent full matrix differs')
    interval=maximal_interval(polys);incidence=incidence_controls()
    return dict(agent='six-reviewer-5',role='independent mathematical reviewer',status='COMPLETE',n=9,N=N,s=S,middle=492,
                full_matrix=full,constant_point_and_coupled_action_coordinates=actions,
                literal_block_sha256=block_hashes,strict_block_ranks=ranks,Schur_polynomials=polys,
                complete_component_dimensions=[6,48,108,96,234],derived_lower_rank=493,derived_upper_rank=501,
                incidence_controls=incidence,fixed_parameter_exact_cap_interval=interval,
                author_code_imported=False,dense_full_slack_eliminations=0,ordinary_decomposition_formalized=False)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--target',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):require(os.environ.get(name)=='1','set '+name+'=1')
    started=time.monotonic();result=run(json.loads(args.target.read_text()));args.output.write_bytes(canonical(result))
    print(json.dumps(dict(status=result['status'],seconds=time.monotonic()-started,peak_RSS_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                         result_bytes=len(canonical(result)),result_sha256=sha256(canonical(result)).hexdigest()),indent=2))
