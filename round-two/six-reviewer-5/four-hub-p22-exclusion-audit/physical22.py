"""Fresh actual four-hub row reconstruction from explicitly credited literal stars.
All pressure-surviving types; actual LOW-SAT friend degrees retained jointly.
"""
import collections,itertools as it,json,time
from independent import local,enc,P,F,PAIRS,TRIPLES,need

def main():
    stars,raw,types,hist=local();lookup={(r['star'],tuple(r['hubs'])):r for r in raw}
    typeid={t:i for i,t in enumerate(types)};signatures=collections.Counter();witness={}
    bytype=collections.Counter();bits=[];first_bad=[];start=time.monotonic()
    for si,star in enumerate(stars):
        words=[set(w) for w in star];delta=[5-sum(a in w for w in words) for a in range(17)]
        high={a for a in range(17) if delta[a]};low=set(range(17))-high
        covered={tuple(p) for w in words for p in it.combinations(sorted(w),2)}
        leave=set(it.combinations(range(17),2))-covered
        adj=[{b if a==v else a for a,b in leave if v in (a,b)} for v in range(17)]
        need(all(len(adj[a])==1 and adj[a]<=high for a in low),'all LOW unique HIGH friends')
        triples={tuple(t) for w in words for t in it.combinations(sorted(w),3)}
        for Ht in it.combinations(range(17),4):
            H=set(Ht);r=lookup[si,tuple(sorted(H&high))];typ=typeid[tuple(r[f] for f in F)]
            friends={a:len(adj[a] & (low-H)) for a in high}
            wc=tuple(sum(len(w&H)==j for w in words) for j in range(5))
            for heavy in Ht:
                bad=[a for a in sorted(high) if delta[a]+friends[a]>
                     5+4*(2 if a==heavy else int(a in H))]
                bits.append(int(not bad));first_bad.append(bad[0] if bad else -1)
                if bad:continue
                bytype[typ]+=1
                for lights in it.permutations(H-{heavy}):
                    role=(heavy,)+lights;d=tuple(delta[a] for a in role)
                    hh=sum(1<<j for j,(a,b) in enumerate(PAIRS) if tuple(sorted((role[a],role[b]))) in leave)
                    hhh=sum(1<<j for j,t in enumerate(TRIPLES) if tuple(sorted(role[a] for a in t)) in triples)
                    iso=sum(1<<a for a,p in enumerate(role) if p in high and not(adj[p]&high))
                    L=tuple(friends[p] if p in high else 0 for p in role)
                    sig=(typ,d,hh,hhh,wc,iso,L);signatures[sig]+=1
                    witness[sig]=min(witness.get(sig,(si,role)),(si,role))
        if time.monotonic()-start>45:raise RuntimeError('INCOMPLETE fixed45-second physical phase guard')
        print(json.dumps(dict(star=si,seconds=time.monotonic()-start,signatures=len(signatures))),flush=True)
    rows=[dict(signature=s,frequency=n,witness=witness[s]) for s,n in sorted(signatures.items())]
    base=collections.Counter()
    for s,n in signatures.items():base[s[:-1]]+=n
    need(len(bits)==218960,'all physical H4/heavy placements')
    result=dict(fields=['type','delta4','hh_leave_mask','hhh_covered_mask','word_hub_counts','isolated_mask','LOW_SAT_friends4'],
                pressure_membership_bits=bits,first_bad_points=first_bad,
                accepted_types=sorted(bytype),accepted_type_mark_counts=sorted(bytype.items()),
                physical_rows=rows,base_signatures=[dict(signature=s,frequency=n) for s,n in sorted(base.items())],
                summary=dict(placements=len(bits),accepted=sum(bits),role_transports=sum(signatures.values()),
                             accepted_types=len(bytype),base_signatures=len(base),joint_friend_signatures=len(rows)))
    (P/'physical22.json').write_bytes(enc(result));print(json.dumps(result['summary'],sort_keys=True),flush=True)

if __name__=='__main__':main()
