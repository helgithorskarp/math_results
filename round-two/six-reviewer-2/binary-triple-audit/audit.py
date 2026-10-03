"""Fresh reviewer arithmetic. No target imports, data files or expected values.

Two representations: projected Boolean incidence versus actual 5040-point
physical progressions. Physical target sets are discovered from all Q states;
incidence targets are generated from the ordinary colour/row/parity argument.
The orchestration/record schema is shared and explicitly part of the trust boundary.
"""
import argparse, hashlib, itertools, json, math
from pathlib import Path

def need(ok, why):
    if not ok:
        raise ValueError(why)

def main(mode):
    D = [d for d in range(1,721) if 720%d == 0 and d not in (1,2,4)]
    E = {d:d//math.gcd(d,4) for d in D}
    if mode == 'incidence':
        F = tuple(t for t in range(180) if t%9 != 3)
        encode = lambda xs:sum(1<<t for t in xs)
        decode = lambda m:tuple(t for t in range(180) if m>>t&1)
        empty = 0
        union = lambda xs:__import__('functools').reduce(int.__or__,xs,0)
        size = int.bit_count
        intersect = int.__and__
        phase = {d:[encode(t for t in F if t%E[d] == r) for r in range(E[d])] for d in D}
        native = []
        for d in D:
            g = math.gcd(d,4)
            masks = [empty if (b-3)%g else phase[d][((b-3)//g*pow(4//g,-1,E[d]))%E[d]] for b in range(d)]
            native.extend([d,s,[list(decode(m)) for m in masks]] for s in range(5))
    else:
        physical = [[n for n in range(5040) if n%4 == 3 and ((n-3)//4)%9 != 3 and n%7 == s+2] for s in range(5)]
        F = tuple(sorted({(n%720-3)//4 for n in physical[0]}))
        encode = frozenset
        decode = lambda s:tuple(sorted(s))
        empty = frozenset()
        union = lambda xs:frozenset().union(*xs)
        size = len
        intersect = frozenset.intersection
        native = []
        physical_family = {}
        for d in D:
            for s in range(5):
                masks = []
                for b in range(d):
                    A = b+d*((s+2-b)*pow(d,-1,7)%7)
                    masks.append(encode((n%720-3)//4 for n in physical[s] if n%(7*d) == A))
                native.append([d,s,[list(decode(m)) for m in masks]])
                if s == 0:physical_family[d] = masks
        phase = {d:[physical_family[d][(4*r+3)%d] for r in range(E[d])] for d in D}
    need(len(F)==160 and len(D)==27, 'whole original domain')
    need(sum(len(row[2])for row in native)==12055, 'all original phase/owner maps')
    P = {e:phase[next(d for d in D if E[d]==e)] for e in (2,3,4,6,9,12)}
    qstates = list(itertools.product(range(-1,3),range(-1,9),range(-1,6)))
    singleton = [empty]+[encode([t]) if t in F else empty for t in range(180)]
    qvalues = []; discovered = {}; large = {}; smallmax = 0
    for r3,r9,r6 in qstates:
        base = union([empty if r<0 else P[e][r] for e,r in ((3,r3),(9,r9),(6,r6))])
        row = []
        for one in singleton:
            q = union([base,one]); k = size(q);row.append(k)
            if k>=108:
                points = decode(q);large[points]=k
                if k==111:discovered[points]=q
            else:smallmax=max(smallmax,k)
        qvalues.append(row)
    def describe(points):
        a = [a for a in (1,2) if sum(t%3==a for t in points)==60]
        need(len(a)==1,'unique full positive colour')
        a=a[0];u=[u for u in (0,6)if sum(t%9==u for t in points)==20]
        need(len(u)==1,'unique whole zero-colour row');u=u[0]
        p=[p for p in (0,1)if sum(t%3==3-a and t%2==p for t in points)==30]
        need(len(p)==1,'unique half positive colour');p=p[0]
        t0=tuple(t for t in F if t%3==a or t%9==u or(t%3==3-a and t%2==p))
        z=sorted(set(points)-set(t0));need(len(z)==1 and len(t0)==110,'target has one extra point')
        return a,u,p,z[0]
    if mode=='incidence':
        targets=[]
        for a,u,p in itertools.product((1,2),(0,6),(0,1)):
            t0=tuple(t for t in F if t%3==a or t%9==u or(t%3==3-a and t%2==p))
            for z in sorted(set(F)-set(t0)):targets.append(((a,u,p,z),encode((*t0,z))))
    else:
        targets=sorted((describe(points),mask)for points,mask in discovered.items())
    need(len(targets)==400 and len(discovered)==400,'complete target catalogue')
    need({decode(m)for _,m in targets}==set(discovered),'all raw Q large targets')
    binary_states=list(itertools.product(range(-1,2),range(-1,4),range(-1,12)))
    pools=[]
    for d3,d9 in itertools.product((3,6,12),(9,18,36)):
        q={d3,d9,24,720}
        pools.append({'Q':[d3,d9,24,720], 'four':[d for d in D if d not in q|{8,16,48,144}],
                      'triple':[d for d in D if d not in q|{8,16,48}],
                      'alternate':[d for d in D if d not in q|{8,16,48,72}]})
    records=[];max_bad=0;structural_bad=0;forced_active=0;affordable_nonfive=set();g_entries=0
    for (a,u,p,z),T in targets:
        capacity={d:[size(intersect(T,m))for m in phase[d]] for d in D}
        maxcap={d:max(capacity[d])for d in D}
        sums=[[sum(maxcap[d]for d in pool[k])for k in ('four','triple','alternate')]for pool in pools]
        binaries=[];bad=0;structural=0;rowrecords=[]
        for r2,r4,r12 in binary_states:
            B=union([empty if r<0 else P[e][r]for e,r in ((2,r2),(4,r4),(12,r12))])
            k=size(intersect(T,B));binaries.append(k)
            forced=(r2==p and r4>=0 and r4%2!=p and r12>=0 and r12%4==(r4+2)%4 and r12%3==a)
            structural_pattern=(r2==p and r4>=0 and r4%2!=p and r12>=0 and r12%4==(r4+2)%4)
            if not structural_pattern:structural=max(structural,k)
            if not forced:bad=max(bad,k)
            elif all(r>=0 for r in(r2,r4,r12)):forced_active+=1
        max_bad=max(max_bad,bad);structural_bad=max(structural_bad,structural)
        for h in range(4):
            if h%2==p:continue
            for v in (u,a):
                G=encode(t for t in F if t%9==v and t%4==(h+2)%4)
                need(size(G)==5 and len({t%5 for t in decode(G)})==5,'five-point mandatory repair transversal')
                counts={d:[size(intersect(G,m))for m in phase[d]]for d in D}
                g_entries+=sum(map(len,counts.values()))
                affordable=[d for d in pools[0]['triple'] if maxcap[d]<=16]
                affordable_nonfive.update(d for d in affordable if E[d]%5)
                rowrecords.append({'h':h,'v':v,'points':list(decode(G)),'phase_intersections':counts})
        records.append({'parameters':[a,u,p,z],'points':list(decode(T)),'phase_capacities':capacity,
                        'pool_sums':sums,'binary_sizes':binaries,'bad_binary_max':bad,'structural_bad_max':structural,'repair_rows':rowrecords})
    return {'domain':{'F':list(F),'originals':D,'projected':E},'native_maps':native,'Q_states':[list(s)for s in qstates],
            'Q_sizes':qvalues,'Q_small_max':smallmax,'large_Q_size_histogram':{k:sum(v==k for v in large.values())for k in sorted(set(large.values()))},
            'pools':pools,'binary_states':[list(s)for s in binary_states],'records':records,
            'summary':{'native_original_phase_owner_maps':sum(len(r[2])for r in native),'Q_states_with_omission':len(qstates)*len(singleton),
                       'targets':len(targets),'opposite_extra_targets':sum(z%2!=p for (a,u,p,z),_ in targets),
                       'binary_states_with_omission':len(targets)*len(binary_states),'forced_active_binary_states':forced_active,
                       'bad_binary_max':max_bad,'structural_bad_max':structural_bad,'all_original_G_phase_entries':g_entries,'affordable_nonfive':sorted(affordable_nonfive)}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['incidence','physical']);ap.add_argument('output');args=ap.parse_args()
    result=main(args.mode);raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode();Path(args.output).write_bytes(raw+b'\n')
    print(json.dumps({'mode':args.mode,'canonical_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'summary':result['summary'],'large_Q_size_histogram':result['large_Q_size_histogram'],'Q_small_max':result['Q_small_max']},sort_keys=True))
