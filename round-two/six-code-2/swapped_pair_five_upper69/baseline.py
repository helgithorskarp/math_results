from paths import INPUTS, WORK
"""Transport the regenerated classical68 into the new swapped-pair carrier."""
import json
from pathlib import Path
import sys
from carrier import STANDARD_G, anchor, check_code, image, literal_residual, require
from quotient import compose, encoded, inverse
from groups import normalizer

HERE=Path(__file__).resolve().parent


def main():
    import steiner
    classical=steiner.code()
    check_code(classical,STANDARD_G)
    star=tuple(w for w in classical if w&1)
    relabel=tuple(17 if v==0 else v-1 for v in range(18))
    quads=tuple(sorted(tuple(sorted(relabel[v] for v in range(18) if w>>v&1 and v!=0))
                       for w in star))
    audit=normalizer()
    data=json.loads((INPUTS/'fixtures.json').read_text())
    target=audit.key(audit.blocks(data['stars'][0]))
    p=next(g for k,g in audit.normalized(quads) if k==target)+(17,)
    phi=compose(p,relabel)
    raw=tuple(sorted(image(w,phi) for w in classical))
    iphi=inverse(phi)
    g=tuple(phi[STANDARD_G[iphi[v]]] for v in range(18))
    mate=phi[1]
    raw_anchor=anchor(tuple(tuple(q) for q in data['stars'][0]),mate,g)
    require(raw_anchor is not None and set(raw_anchor)<=set(raw),'classical anchor inclusion')
    roots=json.loads((WORK/'swapped-m5-roots.json').read_text())
    cover=next(c for c in roots['coverage'] if c['fixture']==0 and c['mate']==mate and tuple(c['mapping'])==g)
    ri=cover['root']; root=roots['roots'][ri]
    psi=compose(tuple(root['transport']),inverse(tuple(cover['from_root'])))
    normalized=tuple(sorted(image(w,psi) for w in raw))
    reps=check_code(normalized,STANDARD_G)
    require(len(normalized)==68 and reps[:2]==(20,20),'classical68 saturated pair')
    require(set(root['normalized'])<=set(normalized),'root anchor inclusion')
    residual=literal_residual(tuple(root['normalized']))
    extension=set(normalized)-set(root['normalized'])
    chosen=tuple(orbit for orbit in residual if set(orbit)<=extension)
    require({w for orbit in chosen for w in orbit}==extension and sum(map(len,chosen))==33,
            'complete classical residual decomposition')
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_CLASSICAL_BASELINE_VALIDATION_ONLY',
            'root':ri,'fixture':0,'raw_mate':mate,'raw_mapping':g,'original_to_normalized':compose(psi,phi),
            'words':normalized,'replications':reps,'fixed_words':sum(image(w,STANDARD_G)==w for w in normalized),
            'anchor_words':35,'residual_words':33,'residual_orbits':chosen,
            'eligible_residual_orbits':len(residual),'eligible_fixed_orbits':sum(len(o)==1 for o in residual),
            'construction':'classical GF16 sublines; prior art, not a new lower bound'}
    (WORK/'swapped-classical68.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('words','residual_orbits','raw_mapping','original_to_normalized')},sort_keys=True))


if __name__=='__main__':main()
