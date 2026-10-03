"""Complete physical star and canonical matrix transport for the six low relabelings."""
import hashlib
import itertools
import json
import time

import physical


def run():
    started=time.monotonic();work=0
    counts,types,low_rows,budget,matrices,census,domains,raw=physical.build()
    lookup={tuple(m):t for t,m in enumerate(matrices)}
    physical.require(len(lookup)==len(matrices)==32,'Complete physical matrix list differs')
    actions=[];checked_domains=0;checked_stars=0

    def tick():
        nonlocal work
        if work>=2000000 or time.monotonic()-started>=40:
            raise ValueError('Operational transport guard; no complete action verdict')
        work+=1

    def star_image(star,phi):
        tick()
        return sum(1<<phi[z] for z in range(18) if star & (1<<z))

    for tail in itertools.permutations((1,2,3)):
        low=(0,)+tail
        type_image=[sum(1<<low[i] for i in range(4) if m & (1<<i)) for m in range(16)]
        physical.require(all(counts[m-1]==counts[type_image[m]-1] for m in range(1,16))
            and all(budget[i]==budget[low[i]] for i in range(4)),
            'Low transport changes exact ordinary degree/type/budget scope')
        matrix_image=[];high_images=[]
        for source,columns in enumerate(matrices):
            groups={}
            for x,(t,c) in enumerate(zip(types,columns)):
                newcolumn=sum(((c>>(2*i))&3)<<(2*low[i]) for i in range(4))
                groups.setdefault(type_image[t],[]).append((newcolumn,x))
            phi=[None]*18;newcolumns=[None]*18
            for nt in sorted(groups):
                target_vertices=[y for y,t in enumerate(types) if t==nt]
                physical.require(len(target_vertices)==len(groups[nt]),'Type class size changed')
                for y,(c,x) in zip(target_vertices,sorted(groups[nt])):
                    phi[x]=y;newcolumns[y]=c
            physical.require(sorted(phi)==list(range(18)),'High transport is not a bijection')
            target=lookup[tuple(newcolumns)]
            for x in range(18):
                y=phi[x]
                physical.require(types[y]==type_image[types[x]],'Mixed incidence not transported')
                image={star_image(s,phi) for s in domains.get((x,columns[x]),[])}
                target_domain=set(domains.get((y,newcolumns[y]),[]))
                physical.require(image==target_domain,'Full physical high-star transport differs')
                checked_domains+=1;checked_stars+=len(image)
            matrix_image.append(target);high_images.append(phi)
        physical.require(sorted(matrix_image)==list(range(32)),
                         'Canonical matrix action is not a bijection')
        actions.append(dict(low_image=list(low),matrix_image=matrix_image,high_images=high_images))
    by_low={tuple(a['low_image']):a for a in actions}
    compositions=0
    for first in actions:
        for second in actions:
            composed=by_low[tuple(second['low_image'][i] for i in first['low_image'])]
            physical.require([second['matrix_image'][t] for t in first['matrix_image']]
                ==composed['matrix_image'],'Canonical low actions do not compose')
            compositions+=32
    covered=set();orbits=[]
    for t in range(32):
        if t in covered:continue
        orbit=sorted({a['matrix_image'][t] for a in actions})
        physical.require(all({a['matrix_image'][s] for a in actions}==set(orbit) for s in orbit),
                         'Canonical orbit not closed')
        orbits.append(orbit);covered.update(orbit)
    physical.require(covered==set(range(32)) and len(orbits)==11,
                     'Incomplete physical matrix orbit coverage')
    residual=[19,28,31]
    physical.require(residual in orbits, 'Residual class is not one full low-label orbit')
    digest=hashlib.sha256(json.dumps(dict(actions=actions,orbits=orbits),
        sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(agent='six-books-3',role='researcher',
        status='COMPLETE_PHYSICAL_MATRIX_STAR_TRANSPORT_CHECKED',counts=counts,
        actions=actions,orbits=orbits,matrices=32,low_permutations=6,
        whole_matrix_images=192,whole_original_domain_images=checked_domains,
        whole_original_star_images=checked_stars,canonical_compositions_checked=compositions,
        work_units=work,work_guard=2000000,internal_seconds_guard=40,
        private_packet_probe_required=False,residual_orbit=residual,whole_action_sha256=digest,
        actual_host_automorphism_assumed=False,
        transport_of_checked_deletion_certificates_claimed=False)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
