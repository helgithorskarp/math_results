"""Independent local algebra, generalized grouping and semantic input controls."""
import copy
import itertools
import json
import pathlib
from fractions import Fraction
import audit

def run():
    mass=[audit.local_mass(m) for m in range(64)]
    telescopes=0
    for u,f,h in itertools.product(range(64),repeat=3):
        left=mass[u]-mass[u&~(f|h)]
        right=(mass[u]-mass[u&~f])+(mass[u&~f]-mass[u&~f&~h])
        audit.need(left==right and left>=0,'all-mask parent absorption identity')
        telescopes+=1
    grid=0
    for row in itertools.permutations(range(2)):
        for col in itertools.permutations(range(3)):
            image=[next(k for k in range(6) if k%2==row[j%2] and k%3==col[j%3])
                   for j in range(6)]
            for m in range(64):
                target=sum(1<<image[j] for j in range(6) if m>>j&1)
                audit.need(mass[m]==mass[target],'balanced-grid invariance')
                grid+=1
    # A genuine size-six group, load4/5 plus singletons1/5, has rho=4.
    # Check exact expectation against the old f5 credit on the full quarter grid.
    group_controls=0
    for values in itertools.product(range(5),repeat=6):
        # Product probability denominator4^6; avoid Fraction in the inner loop.
        product=1
        for value in values:product*=4-value
        total=sum(values)
        squares=sum(v*v for v in values)
        # Weighted true union is(4/5)(1-product/4^6)+(1/5)sum(v/4).
        # Credit sum is sum(v/4)-2sum(v^2/16).
        left=4*(4**6-product)+total*(4**6)//4
        right=5*(total*4**6//4-squares*4**6//8)
        audit.need(left>=right,'fractional size-six union credit')
        group_controls+=1
    # All53 resources in one positive group, lambda=1/13, with singleton12/13.
    # This lies outside the target cardinality restriction and meets rho=4.
    for seed in range(1,33):
        probabilities=[Fraction((i*seed)%13,12) for i in range(53)]
        miss=Fraction(1)
        for p in probabilities:miss*=1-p
        union=(1-miss)/13+Fraction(12,13)*sum(probabilities)
        credit=sum(p-2*p*p for p in probabilities)
        audit.need(union>=credit,'full-pool generalized grouping credit')

    certificate=json.loads(pathlib.Path(__file__).with_name('CERTIFICATE.json').read_text())
    damages=[]
    damaged=copy.deepcopy(certificate);damaged['fixture']['available_moduli'].remove(20)
    damages.append(('lost free20 resource',damaged))
    damaged=copy.deepcopy(certificate);damaged['fixture']['anchors'][-1]=[16,1]
    damages.append(('wrong16 phase',damaged))
    damaged=copy.deepcopy(certificate);damaged['resource_marginals'][0]['entries'][0]['numerator']=True
    damages.append(('boolean probability',damaged))
    damaged=copy.deepcopy(certificate);damaged['resource_marginals'][0]['entries'][0]['orbit_size']+=1
    damages.append(('wrong phase-orbit cardinality',damaged))
    damaged=copy.deepcopy(certificate);damaged['joint_mixture'][0]['phases']['top'][0][1]=288
    damages.append(('illegal actual TOP phase',damaged))
    damaged=copy.deepcopy(certificate)
    generators=audit.tree_generators()
    for record in damaged['resource_marginals']:
        d=record['resource'];orbit={0};queue=[0]
        for a in queue:
            for g in generators:
                b=g[a]%d
                if b not in orbit:orbit.add(b);queue.append(b)
        record['entries']=[{'phase_representative':0,'orbit_size':len(orbit),
                            'numerator':damaged['denominator']}]
    damaged['joint_mixture']=[{'numerator':damaged['denominator'],
                              'phases':{'outside':[0,0],
                                        'top':[[d,0,0] for d in (1,5,7,35)]}}]
    damages.append(('legal distributions fail actual domination',damaged))
    rejected=[]
    for name,damaged in damages:
        try:audit.reconstruct(damaged)
        except (ValueError,KeyError,TypeError) as error:
            rejected.append({'name':name,'reason':str(error)})
        else:raise ValueError('accepted semantic damage: '+name)
    audit.need(rejected[-1]['reason']=='ordinary coefficient domination',
               'legal damage must fail the mathematics')
    return {'parent_telescoping_masks':telescopes,'balanced_grid_controls':grid,
            'six_member_fractional_group_controls':group_controls,
            'full53_member_fractional_group_controls':32,
            'rho_in_both_generalized_examples':[4,1],
            'semantic_rejections':rejected,'semantic_damage_controls':len(rejected)}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
