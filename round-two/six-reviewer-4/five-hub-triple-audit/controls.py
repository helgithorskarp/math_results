"""Independent controls fixed before access to the new author packet."""
import copy
import itertools
import json
from pathlib import Path
from columns import allocations, compositions, same_owner_necessary
from populations import inventories, scalar_cases
from rows import reconstruct, require

def expect_bad(operation):
    try:
        operation()
    except ValueError:
        return
    raise ValueError('semantic damage accepted')

def run():
    stars=json.loads(Path(__file__).with_name('fixtures.json').read_text())['stars']
    raw,capped,types=reconstruct(stars)
    damages=0
    for what in ('omitted_star','duplicate_block','repeat_pair','boolean_point','out_of_range'):
        bad=copy.deepcopy(stars)
        if what=='omitted_star': bad.pop()
        if what=='duplicate_block': bad[0][1]=bad[0][0][:]
        if what=='repeat_pair': bad[0][1]=[0,1,3,4]
        if what=='boolean_point': bad[0][0][0]=False
        if what=='out_of_range': bad[0][0][0]=17
        expect_bad(lambda:reconstruct(bad)); damages+=1
    transports=0
    for shift in (1,3,7):
        p=[(5*x+shift)%17 for x in range(17)]
        inverse={y:x for x,y in enumerate(p)}
        changed=[[[p[x] for x in b] for b in star] for star in stars]
        r,c,ts=reconstruct(changed)
        undo=lambda records:sorted((sid,tuple(sorted(inverse[x] for x in m)),row) for sid,m,row in records)
        require(undo(r)==sorted(raw) and undo(c)==sorted(capped) and ts==types,'full point transport')
        transports+=len(r)
    # Exhaust all weak compositions for a small zero-charge/nonzero-charge carrier.
    # Duplicate charge factors remain DISTINCT coordinate types, as in a coefficient product.
    small=[(0,0,0,False,5,5,0,0,0,0,0),
           (0,1,0,True,5,4,4,1,0,0,1),
           (1,0,0,False,4,3,-3,0,1,0,0),
           (1,1,0,True,4,3,0,0,0,0,2),
           (0,1,0,False,5,4,0,1,0,0,1)]
    calibrations=0
    for n in range(5):
        literal=list(compositions(n,5,0,4))
        for e,k,margin in itertools.product(range(3),repeat=3):
            for sigma in (0,2):
                case=(3,sigma//2,0,0,e,k,margin)
                wanted=sorted(v for v in literal
                              if sum(v[i]*small[i][0] for i in range(5))==e
                              and sum(v[i]*small[i][1] for i in range(5))==k
                              and sum(v[i]*small[i][8] for i in range(5))==sigma
                              and sum(v[i]*small[i][7] for i in range(5))<=margin)
                got,_=inventories(small,case,n)
                require(got==wanted,'full weak-composition coefficient calibration')
                calibrations+=1
    cases=scalar_cases()
    require(len(cases)==92 and {c[0] for c in cases}==set(range(3,8)),'complete broad T range')
    require(any(c[0]>=5 for c in cases),'do not impose unqualified exceptional surcharge')
    require(not allocations(12) and not allocations(13),'negative abstract allocations')
    relaxed={str(k):len(allocations(k,False)) for k in (12,13)}
    require(all(relaxed[str(k)]>0 for k in (12,13)),'heavy support premise is material')
    require(same_owner_necessary(7,5,2,4),'double-owner positive necessary control')
    require(not same_owner_necessary(7,5,2,3),'local triple boundary control')
    require(not same_owner_necessary(8,5,2,5) and same_owner_necessary(8,5,2,6),'strong local support threshold')
    # Nineteen-star tests involve no no-LOW-LOW assertion. Every 4-hub role marking
    # is included at each of these three literal deleted-block stars.
    zgraphs=0
    for sid in (0,8,17):
        blocks=[set(b) for b in stars[sid][1:]]
        rho=[sum(x in b for b in blocks) for x in range(17)]
        covered={tuple(p) for b in blocks for p in itertools.combinations(sorted(b),2)}
        require(len(covered)==19*6,'nineteen-star pair ownership')
        for hubtuple in itertools.combinations(range(17),4):
            hubs=set(hubtuple); sat=set(range(17))-hubs
            pa=sum(rho[a] for a in hubs)
            d=sum(5-rho[s] for s in sat)
            ta=sum(len(hubs.intersection(b))*(len(hubs.intersection(b))-1)//2 for b in blocks)
            uncovered={p for p in itertools.combinations(sorted(sat),2) if p not in covered}
            require(d==pa-11 and len(uncovered)==3*d-3-ta,'Z mass identity')
            for s in sat:
                hh_degree=sum(tuple(sorted((s,a))) not in covered for a in hubs)
                require(sum(s in p for p in uncovered)==1+3*(5-rho[s])-hh_degree,'Z named degree identity')
            require(d>=1,'all columns positive without nineteen-star no-LOW-LOW')
            zgraphs+=1
    return {'fixture_semantic_damages_rejected':damages,'full_transported_marks':transports,
            'weak_composition_calibrations':calibrations,'nineteen_star_named_graphs':zgraphs,
            'relaxed_heavy_support_allocations':relaxed,
            'abstract_positive_controls':['K14','D7 N5 double-B Ta4','D8 N5 double-B Ta6'],
            'conditional_exceptional_surcharge_guard':True}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True))
