"""Full actual4-hub/heavy placements; pair-set vs inverse LOW-friend checks.
Every physical mark's exact LOW-SAT friends are retained before projection.
"""
from independent import *

def compute():
    stars,raw,types,hist=local();tid={t:i for i,t in enumerate(types)}
    rows={(r['star'],tuple(r['hubs'])):r for r in raw}
    census=json.loads((P/'independent-census.json').read_text())
    wanted={i for s in census['survivors'] for i,n in enumerate(s['counts']) if n}
    fullbits=[];failures=[];accepted=[];typecounts=collections.Counter();sig=collections.Counter();fibers=collections.Counter();witness={}
    start=start_guard();assignments=marks_used=0;strict=0
    for si,star in enumerate(stars):
        words=[set(w) for w in star];degree=[sum(a in w for w in words) for a in range(17)];delta=[5-d for d in degree]
        covered={tuple(t) for w in words for t in it.combinations(sorted(w),2)};leave=set(it.combinations(range(17),2))-covered
        adj=[{b if a==p else a for a,b in leave if p in (a,b)} for p in range(17)]
        high={a for a in range(17) if delta[a]};low=set(range(17))-high
        inverse={a:{t for t in low if a in adj[t]} for a in high}
        need(all(len(adj[t])==1 for t in low),'LOW unique actual leave friend')
        need(all(inverse[a]==adj[a]&low for a in high),'inverse LOW-friend list equals every actual HIGH neighborhood')
        wordtriples={tuple(t) for w in words for t in it.combinations(sorted(w),3)}
        for Ht in it.combinations(range(17),4):
            H=set(Ht);J=tuple(sorted(H&high));r=rows[si,J];typ=tid[tuple(r[f] for f in F)]
            L={a:len(adj[a]&low-H) for a in high};L2={a:sum(t not in H for t in inverse[a]) for a in high}
            need(L==L2,'whole physical LOW-global-SAT friend counts')
            for heavy in Ht:
                bad=[a for a in sorted(high) if delta[a]+L[a]>5+4*(2 if a==heavy else (1 if a in H else 0))]
                bad2=[a for a in sorted(high) if delta[a]+L2[a]>(13 if a==heavy else (9 if a in H else 5))]
                need(bad==bad2,'each physical pressure failure list')
                fullbits.append(int(not bad));failures.append(bad[0] if bad else -1)
                if bad:continue
                accepted.append([si,list(Ht),heavy,typ]);typecounts[typ]+=1
                if typ not in wanted:continue
                marks_used+=1
                for light in it.permutations([a for a in Ht if a!=heavy]):
                    role=(heavy,)+light;d4=tuple(delta[a] for a in role)
                    hh=sum(1<<j for j,(a,b) in enumerate(PAIRS) if tuple(sorted((role[a],role[b]))) in leave)
                    hhh=sum(1<<j for j,t in enumerate(TRIPLES) if tuple(sorted(role[a] for a in t)) in wordtriples)
                    wc=tuple(sum(len(w&H)==j for w in words) for j in range(5))
                    isolated=sum(1<<j for j,a in enumerate(role) if a in high and not(adj[a]&high))
                    signature=(typ,d4,hh,hhh,wc,isolated)
                    weak=tuple(2+3*delta[a]-len(adj[a]&H)-r['q'] if delta[a] else 0 for a in role)
                    exact=tuple(1+L[a] if delta[a] else 0 for a in role)
                    need(all(x>=w for x,w in zip(exact,weak)),'actual stronger pointwise support covers weak q bound')
                    strict+=int(exact!=weak);sig[signature]+=1;fibers[signature,exact]+=1;assignments+=1
                    witness.setdefault(signature,[si,list(role)])
                guard(start,len(fullbits),218960,30)
    need(len(fullbits)==23*2380*4,'every full physical4H/heavy placement covered')
    signatures=[{'signature':s,'frequency':n,'first_witness':witness[s]} for s,n in sorted(sig.items())]
    finer=[{'signature':s,'exact_support':b,'frequency':n} for (s,b),n in sorted(fibers.items())]
    # Counts of each signature and refined fiber may never cap global centers.
    result={'fields':F,'types':types,'histograms':hist,'all_218960_membership_bits':fullbits,'first_failure_points':failures,'accepted_full_marks':accepted,'accepted_types':dict(sorted(typecounts.items())),'requested_types':sorted(wanted),'selected_physical_marks':marks_used,'role_assignments':assignments,'whole_signatures':signatures,'full_mark_support_fibers':finer,'strict_exact_support_assignments':strict}
    (P/'independent-physical.json').write_bytes(enc(result))
    print(json.dumps({'placements':len(fullbits),'accepted':sum(fullbits),'types':len(typecounts),'selected':marks_used,'roles':assignments,'signatures':len(sig),'refined_support_fibers':len(fibers),'strict_support_assignments':strict,'sha256':sha(result)}),flush=True)
    return result
if __name__=='__main__':compute()
