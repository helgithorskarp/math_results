"""Independent ordered integer support convolution, using all physical marks.
No orbit quotient: every raw56/1764 (lambda6,triple) carrier (1704 necessary plus60 relaxed) is checked.
Same-delta coordinate minima enlarge physical patterns; actual support
counts use all marks' exact LOW-SAT friends rather than a first witness.
"""
from independent import *

def carriers(T):
    need(T in (0,1),'T0/T1 used only after complete graph reduction')
    out=[]
    triples=[None] if T==0 else list(range(4))
    # Bounded-sum recursion, no five nested Cartesian generators.
    tuples=[]
    def visit(pos,total,path):
        if pos==6:
            if total==21:tuples.append(tuple(path))
            return
        lo=max(0,21-total-5*(5-pos));hi=min(5,21-total)
        for lam in range(lo,hi+1):visit(pos+1,total+lam,path+[lam])
    visit(0,0,[])
    for triple in triples:
        extra=set(it.combinations(TRIPLES[triple],2)) if triple is not None else set()
        for lam in tuples:
            quota=tuple(14-3*l+int(pair in extra) for pair,l in zip(PAIRS,lam))
            D=tuple(sum(l for pair,l in zip(PAIRS,lam) if a in pair)-(2 if a==0 else 6) for a in range(4))
            if min(quota)>=0 and min(D)>=0:out.append((triple,lam,quota,D))
    return out

def patterns(data,carrier,mode):
    triple,lam,quota,D=carrier;allowed_mask=0 if triple is None else 1<<triple
    groups={}
    source=data['whole_signatures'] if mode=='weak' else data['full_mark_support_fibers']
    for row in source:
        typ,d4,hh,hhh,wc,iso=row['signature']
        if hhh not in (0,allowed_mask):continue
        if any(q==0 and hh>>j&1 for j,q in enumerate(quota)):continue
        need(wc[4]==0,'complete survivors permit no4-hub words')
        if mode=='weak':
            q=data['types'][typ][2]
            b=tuple(2+3*d4[a]-sum(int(hh>>j&1) for j,pair in enumerate(PAIRS) if a in pair)-q if d4[a] else 0 for a in range(4))
        else:b=row['exact_support']
        key=(typ,tuple(d4));old=groups.get(key)
        groups[key]=tuple(b) if old is None else tuple(min(x,y) for x,y in zip(old,b))
    bytype=collections.defaultdict(list)
    for (typ,d4),b in sorted(groups.items()):
        # N_a<=D_a universally; reject patterns whose support is too large.
        if all(d<=target and requirement<=target for d,requirement,target in zip(d4,b,D)):
            bytype[typ].append((d4,tuple(int(d>0) for d in d4),b))
    return bytype

def convolution(counts,patterns,D):
    order=sorted([i for i,n in enumerate(counts) if n],key=lambda i:(len(patterns.get(i,[])),i))
    if any(not patterns.get(i) for i in order):return {'retained':0,'states_peak':1,'first_empty':'missing_type_factor'}
    factors=[i for i in order for _ in range(counts[i])]
    states={(0,)*12};peak=1;st=start_guard();first_empty=None
    for step,typ in enumerate(factors):
        nxt=set();remaining=len(factors)-step-1
        for state in states:
            for d,n,b in patterns[typ]:
                nd=tuple(state[a]+d[a] for a in range(4))
                if any(x>y for x,y in zip(nd,D)):continue
                nn=tuple(state[a+4]+n[a] for a in range(4));nb=tuple(max(state[a+8],b[a]) for a in range(4))
                if any(nn[a]+remaining<nb[a] for a in range(4)):continue
                nxt.add(nd+nn+nb)
        states=nxt;peak=max(peak,len(states));guard(st,len(states))
        if not states:first_empty=step;break
    retained=[s for s in sorted(states) if tuple(s[:4])==tuple(D) and all(s[a+4]>=s[a+8] for a in range(4))]
    return {'retained':len(retained),'whole_final_retained_states':retained,'states_peak':peak,'first_empty':first_empty}

def permute_carrier(carrier,p):
    triple,lam,quota,D=carrier;new=[0]*6
    for pair,value in zip(PAIRS,lam):new[PAIRS.index(tuple(sorted(p[a] for a in pair)))]=value
    nt=None if triple is None else TRIPLES.index(tuple(sorted(p[a] for a in TRIPLES[triple])))
    return nt,tuple(new)

def compute():
    data=json.loads((P/'independent-physical.json').read_text());flow_data=json.loads((P/'independent-unit-flow.json').read_text())
    survivors=flow_data['survivors'];need(all(s['case']['tau']==0 and s['case']['T']<=1 for s in survivors),'complete prior reduction establishes tau0/T<=1')
    perms=[(0,)+p for p in it.permutations((1,2,3))];summary={};carrier_sets={}
    for T in (0,1):
        raw=carriers(T);keys={(r[0],r[1]) for r in raw};orbits={min(permute_carrier(r,p) for p in perms) for r in raw}
        need(all(permute_carrier(r,p) in keys for r in raw for p in perms),'every rawcarrier light transport')
        carrier_sets[T]=raw;summary[T]={'raw':len(raw),'orbits_diagnostic_not_used_for_exclusion':len(orbits),'all_raw_carriers':raw}
    records=[]
    # Pattern factors are cached for identical (T,carrier,mode); every raw carrier
    # is visited even if its factor was seen earlier under a role transport.
    for s in survivors:
        rows=[]
        for ci,carrier in enumerate(carrier_sets[s['case']['T']]):
            weak=convolution(s['counts'],patterns(data,carrier,'weak'),carrier[3])
            exact=convolution(s['counts'],patterns(data,carrier,'exact'),carrier[3])
            need(weak['retained']==exact['retained']==0,'UNEXCLUDED necessary support carrier')
            rows.append({'carrier':ci,'weak_bound':weak,'exact_friend_bound':exact})
        records.append({'case':s['case'],'counts':s['counts'],'all_raw_carrier_results':rows})
    wanted={i for s in survivors for i,n in enumerate(s['counts']) if n}
    selected=[s for s in data['whole_signatures'] if s['signature'][0] in wanted]
    finer=[s for s in data['full_mark_support_fibers'] if s['signature'][0] in wanted]
    physical_selected=sum(1 for m in data['accepted_full_marks'] if m[3] in wanted)
    result={'methods':'all raw lambda carriers; exact integer one-center convolution; coordinatewise support minima are a necessary relaxation','carrier_domains':summary,'whole_population_checks':records,'eleven_types':sorted(wanted),'selected_physical_marks':physical_selected,'selected_assignments':sum(s['frequency'] for s in selected),'selected_signatures':selected,'selected_exact_support_fibers':finer}
    (P/'independent-support.json').write_bytes(enc(result));print(json.dumps({'populations':len(records),'raw_carrier_domains':[(T,summary[T]['raw'],summary[T]['orbits_diagnostic_not_used_for_exclusion']) for T in (0,1)],'full_population_carriers':sum(len(r['all_raw_carrier_results']) for r in records),'selected_marks':physical_selected,'assignments':result['selected_assignments'],'signatures':len(selected),'sha256':sha(result)}),flush=True)
    return result
if __name__=='__main__':compute()
