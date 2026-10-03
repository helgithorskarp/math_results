"""Exact corroboration of ordinary local deductions; not a host census."""
from itertools import combinations, permutations, product
import literal as L
import reference as R

def core(require,rows,sy,qend=(2,2,4,2,2),rename=(0,1,2)):
    n,d,q=L.build(rows,sy,qend,rename)
    bits,bd,bq=R.build(rows,sy,qend,rename)
    require(tuple(sum(1<<j for j in z) for z in n)==bits and d==bd and q==bq,
            'full literal/coordinate original16 adjacency, degrees and Q ranks')
    caps=L.allowances(n,d)
    require(caps==R.allowances(bits,bd),'all120 physical pair allowances')
    return n,d,q,caps,bits

def run(require,guard,digest):
    B=set(range(11,22));Nu=set(range(1,11));floors=[]
    for b in sorted(B):
        fixed={14,15} if b in (11,12) else {11,12} if b in (14,15) else set()
        free=list(range(16,22)) if b<16 else sorted(B-{b})
        for w in range(1<<len(free)):
            nb=fixed|{z for i,z in enumerate(free) if w>>i&1}
            blue=[z for z in range(22) if z not in (0,b) and z not in Nu and z not in nb]
            require(len(blue)==10-len(nb),'physical blue u-B degree floor')
            if b in (11,12):
                rank=len(nb&set(range(16,22)))
                require((len(blue)<=6 and 1+rank<=3)==(rank==2),'SY Q rank forced2')
            elif b in (13,14,15):
                rank=len(nb&set(range(16,22)))
                require((len(blue)<=6)==(rank>=(4 if b==13 else 2)),'all three T rank floors')
            else:
                s=len(nb&{11,12});t=len(nb&{13,14,15});h=len(nb&set(range(16,22)))
                if len(nb)>=4 and s+h<=3:require(t>=1,'pointwise T incidence floor')
            floors.append([b,w,len(nb),len(blue)])
        guard()
    require(len(floors)==6464,'complete labelled B local projection domain')
    t0=[];survivors=[]
    for w,k in product(range(64),range(4,7)):
        n,d,q,c,_=core(require,(w,L.P,L.S),(L.P,L.S),(2,2,k,2,2))
        known=[len(n[s]&n[13]) for s in (9,10)]
        require(known==[1+(w&owner).bit_count() for owner in R.OWN],'T0 red SX spine counts')
        redok=all(max(0,4+k-6)<=c[s,13] for s in (9,10))
        require(redok==all(k+(w&owner).bit_count()<=4 for owner in R.OWN),'T0 Q rank and leaf cut')
        # v has its complete six-point Q row, so their intersection is k.
        blueok=k<=c[1,13]
        require(blueok==(w.bit_count()>=2),'blue v-T0 center forcing')
        if redok and blueok:survivors.append([w,k])
        t0.append([w,k,known,d[13],redok,blueok])
    require(survivors==[[L.C,4]],'entire T0 rank4..6 and arbitrary X row forced C')
    tcaps=[]
    for t,w,k in product((14,15),range(64),range(2,7)):
        rows=[L.C,L.P,L.S];rows[t-13]=w;qs=[2,2,4,2,2];qs[t-11]=k
        n,d,q,c,_=core(require,tuple(rows),(L.P,L.S),tuple(qs))
        partner=10 if t==14 else 9
        known=len(n[partner]&n[t]);possible=max(0,4+k-6)<=c[partner,t]
        require(q[partner]==4 and known==1+(w&R.OWN[partner-9]).bit_count(),'Ti partner/rank correspondence')
        if k>4:require(not possible,'Ti Q ranks5/6 excluded')
        tcaps.append([t,w,k,known,possible])
    ranks=list(product(range(2,5),repeat=2))
    require(len(ranks)==9,'all nine initial T-rank triples after local caps')

    def column_core(i,di,j=None,dj=0):
        endpoint_rows=[]
        for k in range(4):
            endpoint_rows.append((1<<i if di>>k&1 else 0)|(1<<j if j is not None and dj>>k&1 else 0))
        return core(require,(L.C,*endpoint_rows[2:]),tuple(endpoint_rows[:2]))
    acells=[];vcells=[]
    for i,w in product(range(6),range(16)):
        n,d,q,c,_=column_core(i,w)
        fullD=w.bit_count()+int(i<2)
        known=len(n[2]&n[3+i]);ok=known<=5
        require(known==1+fullD+int(i>=2) and ok==(fullD<=(4 if i<2 else 3)),
                'blue a-Xi bounds every endpoint incidence column')
        acells.append([i,w,fullD,known,ok])
        if not ok:continue
        s=(w&3).bit_count();t=(w>>2).bit_count()+int(i<2)
        nv=n[1]|set(range(16,22));nx=n[3+i]|set(range(16,16+q[3+i]))
        blue=[z for z in range(22) if z not in (1,3+i) and z not in nv and z not in nx]
        require(len(blue)==1+s+q[3+i] and (len(blue)<=6)==(t>=(2 if i<2 else 1)),
                'complete physical v-Xi union deduction')
        vcells.append([i,w,t,q[3+i],blue])
    cycle=[]
    for i,j in R.CYCLE:
        records=[]
        for wi,wj in product(range(16),repeat=2):
            di=wi.bit_count()+int(i<2);dj=wj.bit_count()+int(j<2)
            if di>(4 if i<2 else 3) or dj>(4 if j<2 else 3):continue
            n,d,q,c,_=column_core(i,wi,j,wj)
            known=len(n[3+i]&n[3+j]);lower=max(0,q[3+i]+q[3+j]-6)
            possible=lower<=c[tuple(sorted((3+i,3+j)))]
            universe={11,12,14,15}|({13} if i<2 or j<2 else set())
            Di=n[3+i]&set(range(11,16));Dj=n[3+j]&set(range(11,16))
            require(known==1+len(Di&Dj) and possible==((Di|Dj)==universe),'whole cycle union equivalence')
            if possible:require(known+lower==3 and q[3+i]+q[3+j]>=6,'tight cycle Q union')
            records.append([wi,wj,q[3+i],q[3+j],known,possible])
        cycle.append([i,j,len(records),sum(z[-1] for z in records),digest(records)])
    covers=L.cycle_covers()
    require(covers==[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in R.CYCLE)] and len(covers)==18,
            'entire six-cycle vertex-cover domain')
    paths=[]
    for t,path in ((14,R.PATH1),(15,R.PATH2)):
        records=[]
        for w in covers:
            for i,j in path:
                if not (w>>i&1 and w>>j&1):continue
                for u,v in product(covers,repeat=2):
                    rows=[L.C,L.P,L.S];rows[t-13]=w
                    n,_,_,_,bits=core(require,tuple(rows),(u,v))
                    known=len(n[t]&n[3+i])+len(n[t]&n[3+j])
                    require(known==(bits[t]&bits[3+i]).bit_count()+(bits[t]&bits[3+j]).bit_count() and known>=5,
                            'all arbitrary SY covers give doubled-path bound5')
                    records.append([w,i,j,u,v,known])
                guard()
        paths.append([t,len(records),min(z[-1] for z in records),digest(records)])
    cases=L.terminal_cases();other=R.terminal_cases()
    require(cases==other and len(cases)==14,'whole literal/coordinate fourteen ordered terminal cores')
    a=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in R.PATH1)]
    b=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in R.PATH2)]
    pairs=sorted((x,y) for x,y in product(a,b) if x|y==63)
    require(a==[L.P,L.H,L.S] and b==[L.P,L.K,L.S] and pairs==[(L.P,L.S),(L.H,L.K),(L.S,L.P)],
            'three independent-path cover pairs')
    sycells=[];final=[]
    for k1,k2 in ranks:
        retained=[]
        for x,y in pairs:
            for u,v in product(covers,repeat=2):
                n,d,q,c,_=core(require,(L.C,x,y),(u,v),(2,2,4,k1,k2))
                redok=all(c[s,t]>=0 for s,t in product((11,12),(14,15)))
                blueok=c[11,12]>=0
                require(redok==all((z&w).bit_count()<=2 for z,w in product((u,v),(x,y))),
                        'all four actual red SY/T X intersection bounds')
                require(blueok==((u|v)==63),'blue SY pair forces whole X union')
                # 4+|U intersect V|+|Q_U intersect Q_V| <= |U|+|V|-2.
                if blueok:require(c[11,12]==0,'blue SY pair saturated and Q rows disjoint')
                if redok and blueok:
                    retained.append((x,y,u,v))
                    require(all(c[s,t]==0 for s,t in product((11,12),(14,15))),
                            'all four red SY-Ti spines saturated')
                    rankok=k1<=2 and k2<=2
                    if rankok:final.append([x,y,u,v,k1,k2])
                sycells.append([k1,k2,x,y,u,v,redok,blueok])
        require(sorted(retained)==cases,'whole fourteen core set agrees for EACH initial rank triple')
        guard()
    require(len(final)==14,'only derived T ranks4,2,2 survive all saturated Q cuts')
    return {'complete':True,'scope':'Ordinary local projections, not a census of actual Ramsey hosts',
            'B_floors':[len(floors),digest(floors)],'T0_free_row_rank_domain':[len(t0),digest(t0)],
            'T0_surviving_row_rank':survivors,'Ti_free_row_rank_domain':[len(tcaps),digest(tcaps)],
            'initial_T_rank_triples':[[4,*z] for z in ranks],
            'blue_a_X_cells':[len(acells),digest(acells)],'blue_v_X_cells':[len(vcells),digest(vcells)],
            'six_cycle_union_records':cycle,'whole18_cycle_covers':covers,'doubled_path_records':paths,
            'three_T_row_pairs':pairs,'SY_cells_each_rank_triple':[len(sycells),digest(sycells)],
            'whole14_X_cores':cases,'final_rank_core_records':final}

def transports(require,guard,digest):
    records=[]
    # Arbitrary single-row perturbations in all five endpoint rows, every
    # initial rank triple, and every ORIGINAL-labelled T renaming.
    for k1,k2 in product(range(2,5),repeat=2):
        for z,w in product(range(5),range(64)):
            words=[L.P,L.S,L.C,L.P,L.S];words[z]=w
            rows=tuple(words[2:]);sy=tuple(words[:2]);qs=(2,2,4,k1,k2)
            n,d,q,c,_=core(require,rows,sy,qs)
            for rename in permutations(range(3)):
                nn,dd,qq,cc,_=core(require,rows,sy,qs,rename)
                p=list(range(16))
                for t in range(3):p[13+t]=13+rename[t]
                require(all(nn[p[i]]=={p[j] for j in n[i]} and dd[p[i]]==d[i] and qq[p[i]]==q[i] for i in range(16)),
                        'whole original16 T-label free-completion transport')
                require(all(cc[tuple(sorted((p[i],p[j]))) ]==v for (i,j),v in c.items()),
                        'all120 transported allowances')
                records.append([k1,k2,z,w,rename])
            guard()
    require(len(records)==17280,'whole five-row/rank/six-label transport box')
    return {'complete':True,'original_T_label_permutations':list(permutations(range(3))),
            'whole_arbitrary_row_rank_transports':[len(records),digest(records)],
            'host_automorphism_assumed':False,'whole_six_SY_repeated_omission_words_covered':True}
