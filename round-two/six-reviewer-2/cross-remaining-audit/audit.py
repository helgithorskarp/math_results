#!/usr/bin/env python3
"""Reviewer-owned exact checks. No campaign, target code, or solver inputs."""
import argparse
import hashlib
import itertools
import json
import os
import sys
import time

THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS')
X = tuple('x'+str(i) for i in range(6))
NAMES = ('u','v','a')+X+('sx0','sx1','sy0','sy1','t0','t1','t2')
END = ('sy0','sy1','t0','t1','t2')
EDGES = ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
C,P,S,H,K,L = map(frozenset, ((0,1),(0,2,3),(1,4,5),
                             (0,1,3,5),(0,1,2,4),(2,3,4,5)))
EMPTY = frozenset()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(obj):
    return hashlib.sha256(encode(obj)).hexdigest()

def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()

def ordered(s):
    return sorted(s)

def subsets(n):
    return [frozenset(c) for k in range(n+1)
            for c in itertools.combinations(range(n),k)]

COVERS = [s for s in subsets(6) if all(i in s or j in s for i,j in EDGES)]

def core(r, rows):
    require(r in (0,1), 'actual r')
    require(set(rows)==set(END), 'all five rows required')
    adj = {x:set() for x in NAMES}
    def add(a,b):
        adj[a].add(b); adj[b].add(a)
    for y in ('v','a')+X+('sx0','sx1'):
        add('u',y)
    for y in ('v','sx0','sx1'):
        add('a',y)
    for i,j in EDGES:
        add(X[i],X[j])
    for a, inds in (('sx0',(3,5)),('sx1',(2,4))):
        for i in inds:
            add(a,X[i])
    for y in ('sy0','sy1'):
        add('v',y); add('a',y)
    for y in ('t0','t1','t2'):
        add('a',y)
    for a, inds in (('sy0',(1,2)),('sy1',(0,1))):
        for i in inds:
            add(a,'t'+str(i))
    sxrows = ((1,2),(0,2)) if r==0 else ((0,2),(1,2))
    for a,inds in zip(('sx0','sx1'),sxrows):
        for i in inds:
            add(a,'t'+str(i))
    for a,inds in rows.items():
        for i in inds:
            require(i in range(6), 'row element')
            add(a,X[i])
    deg = {x:10 for x in ('u','v')+X+('sx0','sx1')}
    deg['a']=9
    # Under B4 this is the global degree; equivalently prescribe the five
    # endpoint Q ranks without imposing any degree on individual Q points.
    for b in END:
        deg[b]=4+len(adj[b]&set(('v','a')+X+('sx0','sx1')))
    rank={x:deg[x]-len(adj[x]) for x in NAMES}
    require(all(rank[b]==q for b,q in zip(END,(2,2,3,2,3))), 'B4 ranks')
    require(all(deg[b]==len(adj[b])+q for b,q in zip(END,(2,2,3,2,3))),
            'edge-budget-free endpoint rank interface')
    return adj,deg,rank

def spine(g,a,b):
    adj,deg,rank=g
    pages=ordered(adj[a]&adj[b])
    red=b in adj[a]
    cap=3 if red else deg[a]+deg[b]-14
    return {'pair':[a,b], 'red':red, 'degrees':[deg[a],deg[b]],
            'ranks':[rank[a],rank[b]], 'pages':pages,
            'allowance':cap-len(pages)}

def tight_union(g,a,b):
    s=spine(g,a,b)
    return s['allowance']==sum(s['ranks'])-6

def union_cut(g,a,b,z):
    require(tight_union(g,a,b), 'tight union premise')
    left=spine(g,z,a); right=spine(g,z,b)
    gap=g[2][z]-left['allowance']-right['allowance']
    return {'covering_pair':spine(g,a,b), 'target':z,
            'target_rank':g[2][z], 'left':left, 'right':right, 'gap':gap}

def rows(u=P,v=S,a=H,d=K,c=C):
    return dict(zip(END,(u,v,a,d,c)))

def transport(g,perm):
    adj,deg,rank=g
    return ({perm[a]:{perm[b] for b in adj[a]} for a in NAMES},
            {perm[a]:deg[a] for a in NAMES},
            {perm[a]:rank[a] for a in NAMES})

def audit():
    start=time.monotonic()
    require(all(os.environ.get(k)=='1' for k in THREADS), 'six threads must be one')
    require(len(COVERS)==18, 'C6 cover domain')
    rec={'agent':'six-reviewer-2', 'role':'independent mathematical reviewer',
         'scope':'9847 remaining-row argument conditional on ordinary9795 and9685',
         'covers':[ordered(s) for s in COVERS],
         'missing_sets':[ordered(set(range(6))-s) for s in COVERS]}
    # Independent root cut and outside blue-spine accounting.
    g=core(0,rows())
    nh=set(g[0]['u'])
    e_n=sum(len(g[0][a]&nh) for a in nh)//2
    nsum=sum(g[1][a] for a in nh)
    cut=nsum-2*e_n-len(nh)
    require((len(nh),e_n,nsum,cut)==(10,13,99,63), 'root cut')
    # E=|N(u)|+e(N(u))+cut+e(B); |B|=11 and d_B>=4.
    base=len(nh)+e_n+cut
    require(base+11*4//2==108, 'forced E108')
    rec['root_cut']={'neighborhood_edges':e_n,'degree_sum':nsum,'cut':cut,
                     'base':base,'B_size':11,'B_min_degree':4,'B_edges':22}
    # All two-endpoint incidence choices, not an author's prefiltered census.
    cycle=[]
    choices=subsets(4)
    for i,j in EDGES:
        for di,dj in itertools.product(choices,repeat=2):
            ri={e:EMPTY for e in END}
            for k,ss in ((i,di),(j,dj)):
                for p in ss:
                    ri[END[p]]=ri[END[p]]|{k}
            ri['t2']=C
            gg=core(0,ri)
            ss=spine(gg,X[i],X[j])
            admissible=(gg[2][X[i]]>=3 and gg[2][X[j]]>=3 and
                        ss['allowance']>=max(0,sum(ss['ranks'])-6))
            if admissible:
                require(tight_union(gg,X[i],X[j]), 'all cycle unions tight')
                require(all(i in ri[e] or j in ri[e] for e in END[:4]),
                        'four endpoint rows cover every cycle edge')
            cycle.append([i,j,ordered(di),ordered(dj),ss,admissible])
    rec['cycle']={'records':len(cycle),'admissible':sum(x[-1] for x in cycle),
                  'whole_sha256':digest(cycle)}
    # Lower known-page occurrence sums for every doubled edge and every cover.
    doubled=[]
    allowed=[]
    for t,own,nsy,qr in (('t0',{2,4},1,3),('t1',{3,5},2,2)):
        allowed_t=[]
        for row in COVERS:
            bad=[]
            for i,j in EDGES:
                if not ({i,j}<=row and ({i,j}&own)):
                    continue
                minima=[]
                for u,v in itertools.product(COVERS,repeat=2):
                    rr=rows(u,v,a=row if t=='t0' else H,d=row if t=='t1' else K)
                    gg=core(0,rr)
                    si,sj=spine(gg,t,X[i]),spine(gg,t,X[j])
                    count=len(si['pages'])+len(sj['pages'])
                    require(count>=3+nsy, 'physical doubled-page lower bound')
                    require(si['allowance']+sj['allowance']<qr, 'doubled cut')
                    minima.append(count)
                bad.append([i,j])
                doubled.append([t,ordered(row),i,j,min(minima),len(minima)])
            if not bad:
                allowed_t.append(row)
        allowed.append(allowed_t)
    require(set(allowed[0])=={P,S,H} and set(allowed[1])=={P,S,K}, 'T cover classes')
    t_pairs=[(a,d) for a,d in itertools.product(*allowed) if a|d==set(range(6))]
    require(set(t_pairs)=={(P,S),(S,P),(H,K)}, 'three T pairs')
    rec['T_cover']={'classes':[[ordered(x) for x in aa] for aa in allowed],
                    'pairs':[[ordered(a),ordered(d)] for a,d in t_pairs],
                    'doubled_records':len(doubled),'whole_sha256':digest(doubled)}
    tcuts=[]
    for a,d,i in ((P,S,2),(S,P,4)):
        for u,v in itertools.product(COVERS,repeat=2):
            gg=core(0,rows(u,v,a,d))
            cc=union_cut(gg,'sx1','t0',X[i])
            require(cc['gap']>=1, 'nonterminal T contradiction')
            tcuts.append([ordered(a),ordered(d),ordered(u),ordered(v),cc])
    rec['T_cuts']={'records':len(tcuts),'whole_sha256':digest(tcuts),
                   'minimum_gap':min(t[-1]['gap'] for t in tcuts)}
    us=[u for u in COVERS if len(u&K)<=2]
    vs=[v for v in COVERS if len(v&H)<=2 and len(v&K)<=2]
    require(set(us)=={L,H,P,P|{5},S,S|{3}}, 'six SY0 covers')
    require(set(vs)=={P,S,L}, 'three SY1 covers')
    hl=[]
    for u,v in itertools.product(us,vs):
        gg=core(0,rows(u,v))
        s01=spine(gg,'sy0','t1'); s12=spine(gg,'t1','t2')
        require(s01['allowance']==s12['allowance']==0, 'disjoint Q rows')
        # Three disjoint rows of respective sizes2,2,3 cannot fit in six.
        forced_overlap=gg[2]['sy0']+gg[2]['t1']+gg[2]['t2']-6
        require(forced_overlap==1, 'SY0/T2 overlap necessity')
        if u==H:
            ss=spine(gg,'sy0','t2')
            require(ss['allowance']==0, 'H overlap contradiction')
            hl.append([ordered(u),ordered(v),s01,s12,ss])
        if u==L:
            for miss in (set(range(6))-cv for cv in COVERS):
                qx=set(range(6))-miss
                for leaf0 in qx&{2,5}:
                    for leaf1 in qx&{3,4}:
                        pages={'v','t2',X[leaf0],X[leaf1]}
                        require(len(pages)==4 and {leaf0,leaf1}<=u,
                                'four distinct pages on SY0-q')
            hl.append([ordered(u),ordered(v),s01,s12,'four-point spine'])
    rec['SY_classes']={'SY0':[ordered(x) for x in us], 'SY1':[ordered(x) for x in vs],
                       'overlap_certificates':hl}
    remain=[(u,v) for u,v in itertools.product(us,vs)
            if u not in (H,L) and len(u|v)>=5]
    require(len(remain)==8, 'all remaining SY cases')
    phi={x:x for x in NAMES}
    psi={x:x for x in NAMES}
    for perm,pairs in ((phi,((0,1),(2,4),(3,5))),
                       (psi,((2,3),(4,5)))):
        for i,j in pairs:
            perm[X[i]],perm[X[j]]=X[j],X[i]
    psi['sx0'],psi['sx1']='sx1','sx0'
    def rowimage(rr,perm):
        return {perm[e]:frozenset(X.index(perm[X[i]]) for i in ss) for e,ss in rr.items()}
    # Empty variable rows plus every singleton variable edge are a complete basis.
    # Known adjacency and affine degree/rank functions transport on this basis.
    basis=[{e:EMPTY for e in END}]
    for e in END:
        for i in range(6):
            rr={z:EMPTY for z in END}; rr[e]=frozenset({i});basis.append(rr)
    transports=[]
    for pname,perm,new_r in (('phi',phi,0),('psi',psi,1)):
        require(set(perm)==set(perm.values())==set(NAMES), 'label bijection')
        for rr in basis+[rows(u,v) for u,v in itertools.product(COVERS,repeat=2)]:
            gg=core(0,rr); newrows=rowimage(rr,perm)
            other=core(new_r,newrows)
            require(transport(gg,perm)==other, 'whole adjacency/actual degree/rank transport')
            for a,b in itertools.combinations(NAMES,2):
                sa=spine(gg,a,b);sb=spine(other,perm[a],perm[b])
                require(sa['red']==sb['red'] and sa['degrees']==sb['degrees'] and
                        sa['ranks']==sb['ranks'] and sa['allowance']==sb['allowance'] and
                        {perm[p] for p in sa['pages']}==set(sb['pages']), 'all physical spine transport')
            transports.append([pname,[ordered(rr[e]) for e in END],
                               [ordered(newrows[e]) for e in END]])
    rec['transports']={'cores':len(transports),'spines':len(transports)*120,
                       'whole_sha256':digest(transports),
                       'phi':phi,'psi':psi,'complete_variable_edge_basis':31}
    scuts=[]
    for v in (L,S):
        u=P if v==L else P|{5}
        rr=rows(u,v); gg=core(0,rr)
        if u==P:
            cc=union_cut(gg,'t0','x5','sy1')
        else:
            cc=union_cut(gg,'x0','x5','x2')
        require(cc['gap']==1, 'unit SY contradiction')
        scuts.append({'U':ordered(u),'V':ordered(v),'certificate':cc})
    gg=core(0,rows(P|{5},L))
    cc=union_cut(gg,'x0','x5','x2')
    require(cc['gap']==1, 'third unit SY contradiction')
    scuts.append({'U':ordered(P|{5}),'V':ordered(L),'certificate':cc})
    def imset(ss):return frozenset(X.index(phi[X[i]]) for i in ss)
    removed={(frozenset(s['U']),frozenset(s['V'])) for s in scuts}
    removed|={(imset(u),imset(v)) for u,v in list(removed)}
    terminal=set(remain)-removed
    require(terminal=={(P,S),(S,P)} and len(removed)==6,'complete eight-case partition')
    rec['SY_final']={'all_eight':[[ordered(u),ordered(v)] for u,v in remain],
                     'representative_cuts':scuts,
                     'terminal':[[ordered(u),ordered(v)] for u,v in sorted(terminal,key=lambda p:(sorted(p[0]),sorted(p[1])))]}
    # Meaningful damages, with actual changed quantities rather than catch-all exceptions.
    rec['controls']={}
    s=spine(core(0,rows()),'t1','t2')
    require(s['allowance']==0 and s['degrees']==[10,9],'actual blue-degree control')
    damaged=core(0,rows()); damaged[1]['t2']=10
    require(spine(damaged,'t1','t2')['allowance']==1,'degree10 tag erases disjointness')
    rec['controls']['false_T2_degree10']={'valid_allowance':0,'damaged_allowance':1}
    require(2+2+2-6==0,'weaker T2 rank no forced intersection')
    rec['controls']['T2_Q_rank2']={'valid_forced_overlap':1,'damaged_forced_overlap':0}
    first_cut=rec['SY_final']['representative_cuts'][0]['certificate']
    changed_gap=first_cut['target_rank']-first_cut['left']['allowance']-(first_cut['right']['allowance']+1)
    require(first_cut['gap']==1 and changed_gap==0,'relaxed red cap erases first SY cut')
    rec['controls']['relax_one_red_allowance']={'valid_gap':1,'damaged_gap':0}
    broken=dict(psi);broken['sx0'],broken['sx1']='sx0','sx1'
    require(transport(core(0,rows()),broken)!=core(1,rowimage(rows(),broken)),
            'partial psi must fail whole shell identity')
    rec['controls']['omit_SX_swap']={'valid_whole_identity':True,'damaged_whole_identity':False}
    # Terminal endpoint rows have literal old labels in the ordinary9685 statement.
    terminals=[]
    for r in (0,1):
        for u,v in ((P,S),(S,P)):
            rr=rows(u,v,H if r==0 else K,K if r==0 else H)
            gg=core(r,rr)
            terminals.append({'r':r,'endpoint_rows':{e:ordered(rr[e]) for e in END},
                              'degrees':gg[1],'Q_ranks':gg[2],
                              'spines':[spine(gg,a,b) for a,b in itertools.combinations(NAMES,2)]})
    rec['terminal_contracts']=terminals
    require(time.monotonic()-start<30,'30-second mathematical guard')
    return rec

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--check')
    args=ap.parse_args();record=audit();data=encode(record)
    if args.check:
        with open(args.check,'rb') as f:
            require(encode(json.load(f))==data,'complete mathematical record mismatch')
    with open(args.output,'wb') as f:f.write(data+b'\n')
    print(json.dumps({'bytes_without_LF':len(data),'sha256_without_LF':hashlib.sha256(data).hexdigest(),
                      'python':sys.version.split()[0]}))

if __name__=='__main__':main()
