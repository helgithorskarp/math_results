"""Exact corroboration of PROOF.md; Python standard library only.

No old682-core census, solver output, or published verdict is an input.
The written proof supplies the structural/completeness bridges.
"""
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json, time
import formulas as algebra
import literal

START=time.monotonic()
F=literal.FORCED_Q

def require(test,message):
    if not test:raise ValueError(message)

def guard():
    if time.monotonic()-START>30:raise RuntimeError('30s phase guard; incomplete is no exclusion')

def mask(S):return sum(1<<i for i in S)
def members(w):return frozenset(i for i in range(6) if w>>i&1)
def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n'

def cut_and_cycle():
    require(sum(map(len,literal.OLD))==26,'literal neighborhood count')
    cut=99-26-10
    require(10+13+cut==86,'edge cut identity')
    out=[]
    for center,left,right in ((True,7,6),(False,6,6)):
        physical=[];formula=[]
        for a,b in product(range(32),repeat=2):
            A=frozenset(i for i in range(5) if a>>i&1);B=frozenset(i for i in range(5) if b>>i&1)
            qa,qb=left-len(A),right-len(B)
            if qa<3 or qb<3:continue
            if 1+len(A&B)+max(0,qa+qb-6)<=3:
                physical.append((a,b,len(A|B),3-1-len(A&B)-max(0,qa+qb-6)))
            union=(a|b).bit_count()
            if union>=(5 if center else 4):formula.append((a,b,union,0 if center else union-4))
        require(physical==formula,'whole endpoint pair identity')
        out.append({'center_other':center,'pairs':len(physical),'union_sizes':sorted({z[2] for z in physical}),
                    'slacks':sorted({z[3] for z in physical})})
    covers=[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in algebra.E4)]
    missing=[w for w in range(64) if all(not(w>>i&1 and w>>j&1) for i,j in algebra.E4)]
    require(sorted(63-w for w in covers)==missing,'whole cover/missing bridge')
    T2=[w for w in covers if (w&40).bit_count()<=1 and (w&20).bit_count()<=1]
    require(T2==[3,7,11,13,15,19,27,35,39,50,51],'eleven T2 masks')
    independent_covers=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in algebra.E4)]
    require(independent_covers==[3,13,50,60],'independent cover bipartition classes')
    admissible=[];rejected=[]
    cycle_neighbors={i:{j for a,b in algebra.CYCLE for j in ((b,) if a==i else (a,) if b==i else ())} for i in range(6)}
    for R in T2:
        witness=next(((i,j) for i,j in algebra.E4 if R>>i&1 and R>>j&1),None)
        if witness is None:admissible.append(R);continue
        i,j=witness;bounds=[]
        for sy0 in covers:
            # Physical own SX points, SY0 occurrences, and actual cycle-neighbor pages.
            common=sum(int(v>=2)+int(sy0>>v&1)+len(cycle_neighbors[v]&members(R)) for v in (i,j))
            upper=6-common
            require(upper<=2,'T2 rank3 versus union allowance at most2')
            bounds.append(upper)
        rejected.append({'T2_row':R,'witness_edge':witness,'SY0_covers_checked':25,'largest_union_allowance':max(bounds)})
    require(admissible==[3,13,50],'whole ordinary three-row reduction')
    return {'neighborhood_edges':13,'neighbor_degree_sum':99,'Nu_B_cut':cut,'edge_offset':86,
            'Bu_degree_floor':4,'Bu_edges_under_bound':22,'cycle_pair_records':out,
            'covers':covers,'missing':missing,'T2_masks':T2,'independent_covers':independent_covers,
            'T2_union_rejections':rejected,'T2_rows_after_union_budget':admissible}

def forced_pattern():
    # Fixed C={c0,c1,n} labels. Full225 choices of the two rank4 SX rows.
    physical=[]
    for a,b in product(range(64),repeat=2):
        if a.bit_count()!=4 or b.bit_count()!=4:continue
        if 2+(a&7).bit_count()<=3 and 2+(b&7).bit_count()<=3 and 3+(a&b).bit_count()<=6:
            physical.append((a,b))
    ordinary=sorted((56|(1<<i),56|(1<<j)) for i in range(3) for j in range(3) if i!=j)
    require(physical==ordinary,'whole SX/C pattern')
    local=[]
    for xi,sxword,tbit,extra in ((2,mask(F[10]),0,0),(3,mask(F[9]),1,1)):
        physical=[];ordinary=[]
        for D,row in product(range(32),range(64)):
            if not D>>4&1 or D.bit_count()>3 or row.bit_count()!=6-D.bit_count():continue
            endpoint=frozenset(i for i in range(5) if D>>i&1)
            sxT=frozenset((2,4)) if xi==2 else frozenset((3,4))
            # Physical known common neighbors: u plus actual SX--T intersection,
            # and the single own SX point plus actual SY0 adjacency on T2--Xi.
            a=1+len(endpoint&sxT)+len(members(row)&members(sxword))
            b=1+int(0 in endpoint)+len(members(row)&members(7))
            if a<=3 and b<=3:physical.append((D,row))
        D=(2+8+16) if xi==2 else (2+4+16)
        ordinary=sorted((D,(1<<extra)|4|(1<<z)) for z in (3,4,5))
        require(physical==ordinary,'whole X2/X3 forced incidence')
        local.append({'Xi':xi,'whole_records':physical})
    actual=[];expected=[]
    for z2,z3 in product((3,4,5),repeat=2):
        q2={0,2,z2};q3={1,2,z3}
        for sy1 in (0,1):
            rank=4-sy1
            for row in range(64):
                R=members(row)
                if len(R)==rank and R|q2==set(range(6)) and R|q3==set(range(6)):
                    actual.append((z2,z3,sy1,row))
    expected=sorted((z,z,0,63-(1<<2)-(1<<z)) for z in (3,4,5))
    require(actual==expected,'whole X1 and common z bridge')
    return {'SX_rows_examined':225,'SX_accepted':ordinary_SX(),
            'X2_X3':local,'X1_common_z':actual,'named_complete_Q_rows':{str(i):mask(v) for i,v in F.items()}}

def ordinary_SX():return sorted((56|(1<<i),56|(1<<j)) for i in range(3) for j in range(3) if i!=j)

def SY0_options():
    # Only the spines used to remove rows0145/145 and constrain C marker points.
    roles=((0,1,0,1,1,0),(1,0,1,1,0,1),(2,0,0,1,1,1),
           (3,1,1,0,1,1),(4,1,1,0,0,0),(5,1,1,0,0,0))
    result=[]
    for R in (3,19,35,51,50):
        accepted={}
        for q,p0,p1,t2,x2,x3 in roles:
            x1=int(q in F[4]);patterns=[]
            for x0,x4,x5,s1,t0,t1 in product((0,1),repeat=6):
                X=(x0,x1,x2,x3,x4,x5);M=frozenset(i for i,b in enumerate(X) if not b)
                h=4-1-s1-t0-t1-t2
                if h<0 or not(t0 or t1 or t2):continue
                if any(i in M and j in M for i,j in algebra.E4):continue
                # Red T2 if present; blue a and red SY0. Q contributions may only increase red pages.
                if t2 and p0+p1+x0+x2+x3+1>3:continue
                if len(M)>1+h:continue
                known=1+sum(X[i] for i in members(R))+t1+t2
                if known>3:continue
                patterns.append((mask(M),s1,t0,t1,h))
            accepted[str(q)]=patterns
        require(not accepted['0'] and not accepted['1'] if R!=3 else True,'C0/C1 marker implication')
        if R in (51,50):require(not accepted['2'],'n marker missing-set bound')
        if R==51:require(not accepted['4'] and not accepted['5'],'rank4 marker excludes w/wprime')
        result.append({'R_SY0':R,'allowed_point_roles':sorted(int(q) for q,z in accepted.items() if z),
                       'whole_C_patterns':{q:accepted[q] for q in ('0','1','2')},
                       'w_pattern_counts':[len(accepted['4']),len(accepted['5'])]})
    # Row145: marker rank2, all allowed point roles in O; blue SX0 budget1.
    require(result[-1]['allowed_point_roles']==[3,4,5],'S marker location')
    require(4+(2)>9+10-14,'ordinary S marker budget')
    return result

def endpoint_cases():
    literal_valid=[];formula_valid=[];transports=0
    for s0,s1,t0,t1 in product(*algebra.SHAPES):
        rows=(t0,t1,13);sy=(s0,s1)
        red,d,qr=literal.build(0,rows,sy)
        bits,bd,bq=algebra.build(0,rows,sy)
        require(tuple(mask(x) for x in red)==bits and d==bd and qr==bq,'whole literal/coordinate core')
        item=(t0,t1,s0,s1)
        if not literal.pair_failures(red,d,qr):literal_valid.append(item)
        if algebra.valid(bits,bd,bq):formula_valid.append(item)
        for r,side in product((0,1),('P','S')):
            k,qperm=algebra.transport(r,side)
            newrows=tuple(algebra.transport_row(w,k) for w in rows)
            newsy=tuple(algebra.transport_row(w,k) for w in sy)
            nr,nd,nq=literal.build(r,newrows,newsy)
            moved=[frozenset() for _ in range(16)];md=[0]*16;mq=[0]*16
            for i in range(16):
                moved[k[i]]=frozenset(k[j] for j in red[i]);md[k[i]]=d[i];mq[k[i]]=qr[i]
            require(tuple(moved)==nr and tuple(md)==nd and tuple(mq)==nq,'complete core/degree/rank transport')
            require(algebra.transport_row(13,k)==(13 if side=='P' else 50),'P/S row transport')
            transports+=1
        guard()
    require(literal_valid==formula_valid,'whole necessary500 endpoint result')
    elementary=algebra.elementary_endpoint_cases()
    expected=[(43,23,3,60),(43,23,35,60),(43,54,35,29)]
    require(elementary==expected,'entire elementary case cover before one rank contradiction')
    # The third case is eliminated by union of Q_X1 and Q_X2 covering Q.
    red,d,qr=literal.build(0,(43,54,13),(35,29))
    limits=[]
    for j in (4,5):limits.append((3 if j in red[8] else d[8]+d[j]-14)-len(red[8]&red[j]))
    require(F[4]|F[5]==set(range(6)) and sum(limits)<qr[8],'ordinary X5 union contradiction')
    survivors=[z for z in elementary if z!=(43,54,35,29)]
    require(len(literal_valid)==9,'pre-strengthening nine-core check')
    return {'full_cover_tuples':500,'whole_literal_formula_necessary_records':literal_valid,
            'elementary_cover_records':elementary,'X5_union_limits':limits,'X5_rank':qr[8],
            'remaining_records':survivors,'complete_transports':transports}

def all_Q_graphs():
    pairs=tuple(combinations(range(6),2));A=[];B=[]
    for edges in combinations(pairs,6):
        red=[set() for _ in range(6)]
        for i,j in edges:red[i].add(j);red[j].add(i)
        A.append(tuple(mask(x) for x in red))
    for word in range(1<<15):
        if word.bit_count()!=6:continue
        rows=[0]*6
        for k,(i,j) in enumerate(pairs):
            if word>>k&1:rows[i]|=1<<j;rows[j]|=1<<i
        B.append(tuple(rows))
    A.sort();B.sort();require(A==B,'entire two-algorithm six-edge Q graphs')
    buckets={}
    for graph in A:buckets.setdefault(tuple(w.bit_count() for w in graph),[]).append(graph)
    return A,buckets

def full_graph(red,qr,H):
    graph=[set(x) for x in red]+[set() for _ in range(6)]
    for i,w in enumerate(qr):
        for q in members(w):graph[i].add(16+q);graph[16+q].add(i)
    for q,w in enumerate(H):graph[16+q]|={16+j for j in members(w)}
    return graph

def whole_physical_failures(graph):
    universe=frozenset(range(22));bad=[]
    for i,j in combinations(range(22),2):
        if j in graph[i]:
            pages=graph[i]&graph[j];cap=3
        else:pages=(universe-graph[i]-{i})&(universe-graph[j]-{j});cap=6
        if len(pages)>cap:bad.append((i,j,sorted(pages),cap))
    return bad

def whole_bit_valid(graph):
    words=[mask(x) for x in graph];full=(1<<22)-1
    for i,j in combinations(range(22),2):
        if words[i]>>j&1:
            if (words[i]&words[j]).bit_count()>3:return False
        else:
            a=full^words[i]^(1<<i);b=full^words[j]^(1<<j)
            if (a&b).bit_count()>6:return False
    return True

def terminal_cases():
    Hgraphs,buckets=all_Q_graphs();records=[];control_graph=None
    for s0 in (3,35):
        red,d,qr=literal.build(0,(43,23,13),(s0,60))
        require(literal.row_options(red,d,qr,7)==[53],'whole X4 forced row')
        require(d[11]==(8 if s0==3 else 9),'derived SY0 degree, no outside floor')
        forced=dict(F)|{7:members(53),12:members(3)}
        unknown=(3,8,11,13,14)
        domains=[literal.row_options(red,d,qr,i) for i in unknown]
        prefixesA=[];prefixesB=[];all_tuples=0
        for rows in product(*domains):
            all_tuples+=1
            qrows=[0]*16
            for i,R in forced.items():qrows[i]=mask(R)
            for i,w in zip(unknown,rows):qrows[i]=w
            validA=True;validB=True
            for i,j in combinations(range(16),2):
                if j in red[i]:
                    pages=len(red[i]&red[j])+len(members(qrows[i])&members(qrows[j]));cap=3
                else:
                    U=frozenset(range(16))
                    pages=len((U-red[i]-{i})&(U-red[j]-{j}))+len(set(range(6))-members(qrows[i])-members(qrows[j]));cap=6
                if pages>cap:validA=False
                codegree=len(red[i]&red[j])+(qrows[i]&qrows[j]).bit_count()
                if codegree>(3 if j in red[i] else d[i]+d[j]-14):validB=False
            if validA:prefixesA.append(tuple(qrows))
            if validB:prefixesB.append(tuple(qrows))
            guard()
        require(prefixesA==prefixesB,'entire complete sixteen-spine prefix records')
        fullA=[];fullB=[];degree_matched=0;usable=[]
        for qrows in prefixesA:
            h=tuple(4-sum(qrows[i]>>q&1 for i in range(11,16)) for q in range(6))
            if any(not 0<=z<=5 for z in h):continue
            # Sum endpoint-to-Q ranks12 and six Bu-degrees24 give exactly6 Q edges.
            require(sum(h)==12,'Q internal six-edge bridge')
            usable.append((qrows,h))
            for H in buckets.get(h,[]):
                degree_matched+=1;graph=full_graph(red,qrows,H)
                require(sum(map(len,graph))==216,'full completion edge108 bridge')
                if not whole_physical_failures(graph):fullA.append((qrows,H))
                if whole_bit_valid(graph):fullB.append((qrows,H))
                if control_graph is None:control_graph=graph
                guard()
        require(fullA==fullB and not fullA,'entire physical/bit22 completions')
        records.append({'R_SY0':s0,'SY0_degree':d[11],'unknown_row_domain_counts':[len(z) for z in domains],
                        'complete_row_tuples':all_tuples,'whole_accepted_prefixes':prefixesA,
                        'whole_degree_prefixes':usable,'degree_matched_Q_graphs':degree_matched,
                        'ordinary_22_vertex_survivors':fullA})
    if control_graph is None:
        # A literal invalid graph preserving all marked degrees, edge108 and Bu4.
        # This is a checker control, not an accepted prefix or a Ramsey witness.
        red,d,qr=literal.build(0,(43,23,13),(35,60))
        fixture=(0,63,0,11,51,13,14,53,52,57,58,36,3,56,24,7)
        H=tuple((1<<((i-1)%6))|(1<<((i+1)%6)) for i in range(6))
        control_graph=full_graph(red,fixture,H)
        require(all(len(control_graph[i])==d[i] for i in range(16)),'invalid control retains marked/derived degrees')
        require(sum(map(len,control_graph))==216,'invalid control retains edge108')
        B=set(range(11,22))
        require(all(len(control_graph[i]&B)==4 for i in B),'invalid control retains Bu4')
        require(len(control_graph[8]&control_graph[13])==4,'invalid control has four physical X5--T0 red pages')
    failures=whole_physical_failures(control_graph)
    require(failures and not whole_bit_valid(control_graph),'literal invalid full22 control')
    return {'Q_graphs':len(Hgraphs),'degree_buckets':len(buckets),'records':records,
            'invalid22_control_first_spine':failures[0]}

def controls():
    rejected=[]
    try:literal.build(0,(43,23,13),(3,60),old_map=(2,1,3,4,7,8,6,5,10,9))
    except ValueError:rejected.append('wrong old-label mapping')
    else:raise ValueError('wrong old-label mapping accepted')
    red,d,qr=literal.build(0,(43,23,13),(35,60))
    # An injected SY1 marker n would have v,X2,X3,X4 as four red pages.
    known={1,5,6,7,12,15}
    require(len(red[12]&known)==4,'named SY1-n four-page damage')
    rejected.append('SY1 marker at n: four named red pages')
    # A damaged row having only three points cannot meet X4 target4.
    require(qr[7]==4 and mask(F[5]).bit_count()!=qr[7],'X4 rank damage')
    rejected.append('rank3 substituted for rank4 X4 row')
    # Actual red X1-w: SY0,T0 plus Q neighbors c0,c1 is a four-page obstruction.
    common=red[4]&frozenset((1,4,7,8,9,10,11,13))
    require(common==frozenset((11,13)) and len(common)+len(F[4]&{0,1})==4,'named X1-w damage')
    rejected.append('X1-w: SY0,T0,c0,c1 four named red pages')
    return {'explicit_damages_rejected':rejected,'actual_SY0_degree8_accepted':literal.build(0,(43,23,13),(3,60))[1][11]==8}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--check',type=Path)
    args=p.parse_args()
    record={'agent':'six-books-1','role':'researcher','schema':'cross-T2-ordinary-v1',
            'claim':'specified broader cross shell with root degrees/E<=108 forces T2={X0,X1}, arbitrary outside global degrees',
            'status':'same-author exact corroboration of ordinary written proof; unformalized bridges; independent review pending',
            'cut_cycle':cut_and_cycle(),'forced_pattern':forced_pattern(),'SY0_row_controls':SY0_options(),
            'endpoint_cases':endpoint_cases(),'terminal_cases':terminal_cases(),'controls':controls()}
    guard();raw=canonical(record).encode();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(raw)
    if args.check:require(raw==args.check.read_bytes(),'whole canonical expected record differs')
    print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'wall_seconds':time.monotonic()-START}))

if __name__=='__main__':main()
