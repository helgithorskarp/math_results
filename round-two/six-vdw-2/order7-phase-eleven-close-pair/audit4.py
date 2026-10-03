"""Independent actual-field, full signed CNF, cyclic coverage and orientation audit."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import resource
import time
from common import COMMIT, REF, ROOT, pins, require, sha

PARAMETERS = [0,1]
def stem_for(background): return f'eleven4-fixed-b-{background}'

def head_phase(background):
    require(background in PARAMETERS,'unsupported background')
    selected={4*j for j in range(11)}
    return [1-background if i in selected else background for i in range(44)]

def literal_field():
    require(all(617%d for d in range(2,25)),'617 is not prime')
    require(len({pow(3,e,617) for e in range(616)})==616,'3 is not primitive')
    h={pow(3,88*j,617) for j in range(7)}
    require(len(h)==7 and {pow(3,44,617)*x%617 for x in h}=={-x%617 for x in h},'wrong antipodes')
    slots={}
    for exponent in range(44):
        for side in (0,1):
            for multiplier in h:
                point=((-1)**side)*pow(3,exponent,617)*multiplier%617
                require(point not in slots,'overlapping actual cosets'); slots[point]=(exponent,side)
    require(set(slots)==set(range(1,617)),'incomplete nonzero field')
    supports=set();kept=omitted=0
    for start in range(617):
        for step in range(1,617):
            points=[(start+j*step)%617 for j in range(7)]
            if 0 in points: omitted+=1;continue
            kept+=1; support=tuple(sorted({slots[x] for x in points}))
            require(len({i%2 for i,side in support})==2,'quadratic-residue control failed')
            supports.add(support)
    require((kept,omitted,len(supports))==(375760,4312,26488),'incomplete literal field AP census')
    return slots,supports

def semantic_rows(slots,supports,phases):
    def signed(point):
        index,side=slots[point]
        return (index+1)*(-1 if side and phases[index] else 1)
    field,color=set(),set()
    def both(rows,values):
        values=set(values)
        if not any(-v in values for v in values):
            rows.add(tuple(sorted(values))); rows.add(tuple(sorted(-v for v in values)))
    for support in supports:
        both(field,[(i+1)*(-1 if side and phases[i] else 1) for i,side in support])
    for end in range(88):
        both(color,[signed(pow(3,end-j,617)) for j in range(7)])
        first=pow(3,end,617)
        both(color,[signed(first*pow(57,j,617)%617) for j in range(8)])
    return field,color

def audit_case(record,cnf,slots,supports):
    background=record['background']; phases=head_phase(background)
    field,color=semantic_rows(slots,supports,phases)
    expected=dict(stem=stem_for(background),background=background,phase_K=sum(phases),
        selected_phase_count=11,selected_indices=[4*j for j in range(11)],fixed_phases=phases,
        minimum_selected_distance=4,fully_fixed_phase=True,variables=44,clauses=len(field|color)+1,
        lower_orientation_variables=44,phase_auxiliary_variables=0,xor_auxiliary_variables=0,
        counter_auxiliary_variables=0,only_global_y0_zero=True,root3_color_cut=True,
        root57_color_cut=True,nonconstant_phase8_checked=True,orientation_period_four_required=False,
        exact_TEN_rules_used=False,proposed_ELEVEN_exclusion_used=False,
        unpublished_exclusion_used_as_input=False,unrelated_family_cut=False,
        field_clauses=len(field),universal_color_clauses=len(color),
        new_universal_color_clauses=len(color-field),cnf_sha256=sha(cnf),
        premise_ref=REF,source_commit=COMMIT,mathematical_exclusion=False)
    require(record==expected,'entire fixed phase/count/orientation/premise record differs')
    require(all(len({phases[(i+j)%44] for j in range(8)})==2 for i in range(44)),
            'fixed phase violates the nonconstant phase8 theorem')
    lines=cnf.read_text().splitlines()
    require(lines[0].split()==['p','cnf','44',str(expected['clauses'])],'wrong fixed CNF dimensions')
    rows=[]
    for line in lines[1:]:
        values=list(map(int,line.split()))
        require(values and values[-1]==0 and all(1<=abs(v)<=44 for v in values[:-1]),'invalid fixed CNF row')
        rows.append(tuple(sorted(values[:-1])))
    require(Counter(rows)==Counter(list(field|color)+[(-1,)]) and len(rows)==expected['clauses'],
            'entire actual-field fixed signed CNF differs')
    return {k:expected[k] for k in ('stem','background','phase_K','variables','clauses','cnf_sha256',
                                   'field_clauses','universal_color_clauses','new_universal_color_clauses')}

def ordinary_spacing_controls():
    words=normalizations=orientation_checks=0;counts=[]
    # A complete small check supplements the ordinary average-gap proof.
    for selected_count in (1,2,3):
        length=4*selected_count;regular=0
        for selected in itertools.combinations(range(length),selected_count):
            distances=[(selected[(j+1)%selected_count]-i)%length or length for j,i in enumerate(selected)]
            if min(distances)<4:continue
            require(sum(distances)==length and set(distances)=={4},'small gap-average cover failed')
            regular+=1;words+=1
            for origin in selected:
                rotated={(i-origin)%length for i in selected}
                require(rotated==set(range(0,length,4)),'small normalization misses a regular phase')
                for background in (0,1):
                    phase=[background^int(i in rotated) for i in range(length)]
                    require(sum(v!=background for v in phase)==selected_count,'wrong small selected count')
                    normalizations+=1
        require(regular==4,'regular spacing phases have four labeled shifts');counts.append([length,selected_count,regular])
    # All actual phase translations, including side exchanges, retain 44 independent lower variables.
    scalar_truths=normalized=0
    for background in (0,1):
        for shift in range(4):
            phases=[background^int((i-shift)%4==0) for i in range(44)]
            selected=[i for i,v in enumerate(phases) if v!=background]
            require(len(selected)==11,'incorrect actual labeled phase')
            for origin in range(88):
                lower=[(i+origin)%44 for i in range(44)]
                require(set(lower)==set(range(44)),'translation identifies lower orientation variables')
                def literal(exponent,bit):
                    exponent%=88
                    return bit^(phases[exponent%44] if exponent>=44 else 0)
                for index in range(44):
                    for bit in (0,1):
                        require(literal(index+origin,bit)^literal(index+origin+44,bit)==phases[(index+origin)%44],
                                'scalar phase transport loses a side exchange');scalar_truths+=1
                if origin%44 in selected:
                    require([phases[(i+origin)%44] for i in range(44)]==head_phase(background),
                            'actual selected-anchor normalization misses a head');normalized+=1
            lower=[0]*44;lower[4]=1
            upper=[v^f for v,f in zip(lower,phases)]
            require([v^w for v,w in zip(lower,upper)]==phases and lower[0]!=lower[4],
                    'phase period four was incorrectly imposed on orientations');orientation_checks+=1
            for bits in itertools.product((0,1),repeat=8):
                u=[v^phases[i] for i,v in enumerate(bits)]
                require([v^w for v,w in zip(bits,u)]==phases[:8]
                        and [(1-v)^(1-w) for v,w in zip(bits,u)]==phases[:8],
                        'global complement changes the phase');orientation_checks+=1
    return dict(small_cyclic_words=words,small_both_background_normalizations=normalizations,
        small_regular_counts=counts,actual_scalar_phase_truth_rows=scalar_truths,
        actual_selected_anchor_normalizations_including_side=normalized,orientation_controls=orientation_checks,
        labeled_phases_per_background=4,normalized_fixed_heads=2,
        phase_period_does_not_restrict_orientation_period=True,
        ordinary_cover_is_eleven_positive_distances_summing_44=True,
        counts_are_not_feasible_field_colorings=True,no_free_orbit_division=True)

def main(work):
    began=time.monotonic();pins();models=json.loads((work/'models.json').read_text())
    require(models['producer_sha256']==sha(ROOT/'generate4.py')
            and [r['stem'] for r in models['records']]==[stem_for(b) for b in PARAMETERS],
            'incomplete two-background spacing-four cover')
    slots,supports=literal_field()
    records=[audit_case(record,work/(record['stem']+'.cnf'),slots,supports) for record in models['records']]
    controls=ordinary_spacing_controls()
    out=dict(agent='six-vdw-2',role='researcher',status='EXACT_H7_ELEVEN4_DEFINITION_AUDIT',
        literal_field_APs=375760,omitted_zero_APs=4312,distinct_signed_supports=26488,records=records,
        ordinary_spacing_controls=controls,seconds=time.monotonic()-began,
        maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    mode='normal' if __debug__ else 'optimized'
    (work/('audit-'+mode+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','ordinary_spacing_controls')}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    main(p.parse_args().work.absolute())
