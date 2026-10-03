"""Exact local source interfaces for the ordinary SX-repeated argument."""
from functools import lru_cache
from itertools import combinations, permutations, product
import hashlib, json
import literal as L
import reference as R

MIXED=((0,4),(0,5),(1,2),(1,3))
QMASKS={k:tuple(sum(1<<i for i in c) for c in combinations(range(6),k)) for k in range(7)}
QS={w:frozenset(16+i for i in range(6) if w>>i&1) for w in range(64)}
def canonical(x):
    return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()

def core(require,rows=(L.L,L.C,L.C),sy=(L.P,L.S),qend=(2,2,2,3,3),rename=(0,1,2),sx_q=(4,4)):
    n,d,q=L.build(rows,sy,qend,rename,sx_q)
    bits,bd,bq=R.build(rows,sy,qend,rename,sx_q)
    require(tuple(sum(1<<j for j in s) for s in n)==bits and d==bd and q==bq,
            'full original/coordinate known16 adjacency, degrees and Q ranks')
    caps=L.allowances(n,d)
    require(caps==R.allowances(bits,bd),'all120 actual known16 pair allowances')
    require(d[9:11]==(6+sx_q[0],6+sx_q[1]),'SX degrees free, no degree10 mark')
    return n,d,q,caps,bits

def run(require,guard,digest):
    B=set(range(11,22));Nu=set(range(1,11));floors=[]
    for b in sorted(B):
        fixed={13,15} if b==11 else {13,14} if b==12 else {11,12} if b==13 else {12} if b==14 else {11} if b==15 else set()
        free=list(range(16,22)) if b<16 else sorted(B-{b})
        for w in range(1<<len(free)):
            nb=fixed|{z for i,z in enumerate(free) if w>>i&1}
            blue=[z for z in range(22) if z not in (0,b) and z not in Nu and z not in nb]
            require(len(blue)==10-len(nb),'physical original22 blue u-B floor')
            if b in (11,12):
                k=len(nb&set(range(16,22)))
                require((len(blue)<=6 and 1+k<=3)==(k==2),'derived SY Q rank2')
            elif b in (13,14,15):
                k=len(nb&set(range(16,22)))
                require((len(blue)<=6)==(k>=(2 if b==13 else 3)),'initial free T Q floors2,3,3')
            floors.append([b,w,len(nb),blue])
        guard()
    require(len(floors)==6464,'entire6464 local B projections')

    def columns(i,wi,j=None,wj=0):
        words=[L.P,L.S,L.L,L.C,L.C]
        for z in range(5):
            words[z]=(words[z]&~(1<<i))|(((wi>>z)&1)<<i)
            if j is not None:
                words[z]=(words[z]&~(1<<j))|(((wj>>z)&1)<<j)
        return core(require,tuple(words[2:]),tuple(words[:2]))
    acells=[];cycles=[]
    for i,wi in product(range(6),range(32)):
        n,d,q,c,b=columns(i,wi)
        known=len(n[2]&n[3+i]);ok=known<=5
        require(known==1+wi.bit_count()+int(i>=2) and ok==(wi.bit_count()<=(4 if i<2 else 3)),
                'actual blue a-X degree10 column bound')
        require(q[3+i]==(7 if i<2 else 6)-wi.bit_count(),'original degree10 X Q rank')
        if ok:require(q[3+i]>=3,'necessary X Q lower bound under actual a-X cap')
        # A zero center column gives rank7 and is separately impossible in
        # six-point Q; these are local incidence projections, not hosts.
        acells.append([i,wi,known,q[3+i],ok,0<=q[3+i]<=6])
    for i,j in MIXED:
        cells=[]
        for wi,wj in product(range(32),repeat=2):
            n,d,q,c,b=columns(i,wi,j,wj)
            Di=n[3+i]&set(range(11,16));Dj=n[3+j]&set(range(11,16))
            known=len(n[3+i]&n[3+j]);lower=max(0,q[3+i]+q[3+j]-6)
            axok=len(Di)<=4 and len(Dj)<=3
            possible=axok and lower<=c[tuple(sorted((3+i,3+j)))]
            require(known==1+len(Di&Dj),'all original mixed-edge known pages')
            require(possible==(axok and (Di|Dj)==set(range(11,16))),
                    'entire actual mixed union under necessary a-X caps')
            if possible:
                require(known+lower==3 and q[3+i]+q[3+j]>=6,'mixed Q intersection is tight')
            cells.append([wi,wj,q[3+i],q[3+j],known,axok,possible])
        cycles.append([i,j,len(cells),sum(x[-1] for x in cells),digest(cells)])
        guard()
    covers=[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in MIXED)]
    independent=[w for w in covers if all(not(w>>i&1 and w>>j&1) for i,j in MIXED)]
    require(len(covers)==25 and independent==[L.C,L.P,L.S,L.L],
            'entire mixed covers and four independent star choices')

    doubled=[];tcells=[];states={}
    for t in (14,15):
        kept=[]
        for w,k in product(range(64),range(3,7)):
            rows=[L.L,L.C,L.C];rows[t-13]=w
            qs=[2,2,2,3,3];qs[t-11]=k
            n,d,q,c,b=core(require,tuple(rows),qend=tuple(qs))
            counts=[len(n[s]&n[t]) for s in (9,10)]
            require(counts==[1+(w&owner).bit_count() for owner in R.OWN],
                    'both actual RED SX/Ti known-page formulas')
            budget=c[9,t]+c[10,t]
            require(budget==4-(w&L.L).bit_count(),'joint SX red budget counts all leaves')
            if w in independent and k<=budget:kept.append([w,k])
            tcells.append([t,w,k,counts,budget,w in covers,w in independent,k<=budget])
        require(kept==[[L.C,3],[L.C,4]],'entire necessary Ti row/rank list after joint union')
        states[str(t)]=kept
        neighbor=12 if t==14 else 11
        for w,syword in product(covers,repeat=2):
            rows=[L.L,L.C,L.C];rows[t-13]=w
            sy=[L.P,L.S];sy[neighbor-11]=syword
            n,_,_,_,bits=core(require,tuple(rows),tuple(sy))
            for i,j in MIXED:
                if not(w>>i&1 and w>>j&1):continue
                known=len(n[t]&n[3+i])+len(n[t]&n[3+j])
                require(known==(bits[t]&bits[3+i]).bit_count()+(bits[t]&bits[3+j]).bit_count()
                        and known>=4,'all arbitrary mixed-cover doubled-spine budgets')
                doubled.append([t,w,syword,i,j,known])
            guard()
    require(len(doubled)==2000,'all2000 actual doubled mixed-edge occurrences')

    @lru_cache(maxsize=None)
    def sxmodel(ka,kb):
        return core(require,sx_q=(ka,kb))
    sx_pairs=[];cover_pairs=[];U22=set(range(22));full=(1<<22)-1
    six=[1,3,4,11,12,13]
    for a,b in product(range(64),repeat=2):
        n,d,q,c,bits=sxmodel(a.bit_count(),b.bit_count())
        knownblue=sorted((set(range(16))-n[9]-{9})&(set(range(16))-n[10]-{10}))
        require(knownblue==six and 10 not in n[9],'six literal pages on actual BLUE SX spine')
        na,nb=n[9]|QS[a],n[10]|QS[b]
        ba,bb=bits[9]|(a<<16),bits[10]|(b<<16)
        require(len(na)==d[9] and len(nb)==d[10],'complete actual original22 free SX degrees')
        blue=sorted((U22-na-{9})&(U22-nb-{10}))
        bitblue=[z for z in range(22) if ((full&~(ba|(1<<9)))&(full&~(bb|(1<<10))))>>z&1]
        require(blue==bitblue and len(blue)==12-(a|b).bit_count(),
                'all original22 arbitrary SX Q pairs actual BLUE pages')
        ok=len(blue)<=6
        require(ok==((a|b)==63),'BLUE saturation forces actual SX Q union')
        if ok:cover_pairs.append((a,b))
        sx_pairs.append([a,b,d[9],d[10],blue,ok])
    require(len(cover_pairs)==729 and len(sx_pairs)==4096,
            'all4096 arbitrary SX Q pairs, exactly729 covering roles')
    guard()

    @lru_cache(maxsize=None)
    def trimodel(t,w,ka,kb,k):
        rows=[L.L,L.C,L.C];rows[t-13]=w
        qs=[2,2,2,3,3];qs[t-11]=k
        return core(require,tuple(rows),qend=tuple(qs),sx_q=(ka,kb))
    joint_hash=hashlib.sha256();joint_count=0;bad_spine_counts={14:0,15:0}
    for a,b in cover_pairs:
        for k in range(3,7):
            for f in QMASKS[k]:
                for t,w in product((14,15),(L.P,L.S,L.L)):
                    n,d,q,c,bits=trimodel(t,w,a.bit_count(),b.bit_count(),k)
                    nt=n[t]|QS[f];bt=bits[t]|(f<<16)
                    require(len(nt)==d[t],'complete actual original22 free Ti degree')
                    counts=[];pages=[]
                    for s,m in ((9,a),(10,b)):
                        require(t in n[s],'joint budget uses actual RED SX/T spine')
                        ns=n[s]|QS[m];bs=bits[s]|(m<<16)
                        require(len(ns)==d[s],'complete original22 free SX joint-spine degree')
                        ps=sorted(ns&nt)
                        require(len(ps)==(bs&bt).bit_count()
                                and len(ps)==1+(w&R.OWN[s-9]).bit_count()+(m&f).bit_count(),
                                'complete original22 RED pages, free SX ranks')
                        pages.append(ps);counts.append(len(ps))
                    require(k<=(a&f).bit_count()+(b&f).bit_count(),'same-six-point joint union budget')
                    require(max(counts)>3,'every non-C independent Ti cover violates an actual RED cap')
                    bad_spine_counts[t]+=1
                    joint_hash.update(canonical([a,b,f,t,w,pages]))
                    joint_count+=1
        guard()
    require(joint_count==729*42*3*2==183708,'entire joint-Q labeled role box')
    guard()
    return {'agent':'six-books-1','role':'researcher','complete':True,
            'scope':'Ordinary local source interfaces; not a census of Ramsey hosts',
            'B_floors':[len(floors),digest(floors)],'blue_a_X_cells':acells,
            'four_mixed_union_tables':cycles,'whole25_mixed_covers':covers,
            'four_independent_mixed_covers':independent,
            'Ti_free_row_rank_cells':[len(tcells),digest(tcells)],'necessary_Ti_states':states,
            'all_doubled_mixed_records':[len(doubled),digest(doubled)],
            'all_arbitrary_SX_Q_pairs':[len(sx_pairs),digest(sx_pairs)],
            'all729_covering_SX_Q_roles':cover_pairs,
            'SX_saturated_BLUE_pages':six,'SX_degree10_assumed':False,
            'nonC_actual_RED_Q_roles':[joint_count,joint_hash.hexdigest()],
            'nonC_role_counts_each_T':bad_spine_counts,
            'T0_X_and_Q_prescribed':False,'E_bound':None,
            'Y_or_cross_theorem_input':False,'ordinary_completion_bridges_unformalized':True}

def transports(require,guard,digest):
    records=[]
    for z,w in product(range(5),range(64)):
        words=[L.P,L.S,L.L,L.C,L.C];words[z]=w
        n,d,q,c,_=core(require,tuple(words[2:]),tuple(words[:2]))
        for rename in permutations(range(3)):
            nn,dd,qq,cc,_=core(require,tuple(words[2:]),tuple(words[:2]),rename=rename)
            p=list(range(16))
            for t in range(3):p[13+t]=13+rename[t]
            require(all(nn[p[i]]=={p[j] for j in n[i]} and dd[p[i]]==d[i] and qq[p[i]]==q[i] for i in range(16)),
                    'arbitrary original endpoint row and T-label transport')
            require(all(cc[tuple(sorted((p[i],p[j]))) ]==v for (i,j),v in c.items()),
                    'all120 original transported allowances')
            records.append(['row',z,w,rename])
        guard()
    rank_records=[]
    for ka,kb,k0,k1,k2 in product(range(7),range(7),range(2,7),range(3,7),range(3,7)):
        n,d,q,c,_=core(require,qend=(2,2,k0,k1,k2),sx_q=(ka,kb))
        for rename in permutations(range(3)):
            nn,dd,qq,cc,_=core(require,qend=(2,2,k0,k1,k2),rename=rename,sx_q=(ka,kb))
            p=list(range(16))
            for t in range(3):p[13+t]=13+rename[t]
            require(all(nn[p[i]]=={p[j] for j in n[i]} and dd[p[i]]==d[i] and qq[p[i]]==q[i] for i in range(16)),
                    'all free SX/T Q ranks under six original T namings')
            require(all(cc[tuple(sorted((p[i],p[j]))) ]==v for (i,j),v in c.items()),
                    'all120 free-rank transported allowances')
            rank_records.append([ka,kb,k0,k1,k2,rename])
        guard()
    require(len(records)==1920 and len(rank_records)==23520,'two entire stated original-label boxes')
    return {'complete':True,'arbitrary_single_row_transports':[len(records),digest(records)],
            'free_SX_T_rank_transports':[len(rank_records),digest(rank_records)],
            'total_transport_cells':25440,'original_T_label_permutations':list(permutations(range(3))),
            'whole_joint_five_X_row_census':False,'host_automorphism_assumed':False}
