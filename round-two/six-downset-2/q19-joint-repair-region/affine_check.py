"""All original rows/entries and physical actions at every affine generator.

Five rational generators span the four-coordinate affine recipe. Positivity
is deliberately not asserted at these generators, which are outside the
feasible region. Their role is to bind all coefficient-level identities.
"""
from binding import check_current
check_current()
from fractions import Fraction as F
from collections import Counter
import json
import resource
import time
from entries import affine_rows, evaluate
from joint import model, physical, table_at, PARENT


def entry_key(v,w):
    if not v and not w:return ('loop',)
    if not v or not w:
        nonempty=v or w
        return ('empty_anchor',) if nonempty==(0,) else ('empty',model.type_of(nonempty,9))
    if v==(0,) or w==(0,):
        other=w if v==(0,) else v
        return ('anchor',model.type_of(other,9))
    return ('proper',)+tuple(sorted((model.type_of(v,9),model.type_of(w,9))))


def run():
    start=time.monotonic()
    raw=model.coefficient_input(PARENT/'COEFFICIENTS.json')
    rows=affine_rows(raw)
    coords=[(F(0),)*4]+[tuple(F(int(i==j)) for i in range(4)) for j in range(4)]
    records=[];basis=None;previous_members=None
    for x in coords:
        table,recipe=table_at(raw,*x)
        literal=model.literal_point(table,9,10)
        point=physical.original(table,9,10)
        if basis is None:
            basis,gram=physical.complete_basis(point)
            previous_members=point['members']
        else:
            model.require(point['members']==previous_members,
                          'all affine generators have exactly the same full physical basis')
        actions=physical.literal_actions(point,table,basis)
        counts=Counter()
        for i,v in enumerate(literal['members']):
            for j,w in enumerate(literal['members']):
                if not set(v).isdisjoint(w):continue
                key=entry_key(v,w)
                model.require(key in rows,'every original allowed position is covered by the scalar rows')
                surplus=literal['L'][i][j]-literal['s']*int(i==j)-x[0]
                model.require(evaluate(rows[key],x)==surplus,
                              'ENTIRE original affine entry system at every generator')
                counts[key]+=1
        model.require(sum(counts.values())==72817 and len(counts)==180,
                      'all original allowed entries and all actual scalar rows')
        hashes={}
        for name in ('L','T'):
            literal_hash=model.digest([[str(a) for a in row] for row in literal[name]])
            physical_hash=model.digest([[str(F(a,point['den'])) for a in row] for row in point[name]])
            model.require(literal_hash==physical_hash,
                          'entire literal/named-set original '+name+' agrees at each generator')
            hashes[name]=literal_hash
        records.append(dict(coords=[str(a) for a in x],
                            original_positions_each_lift=303**2,
                            inverse_metric_positions_each_product=301**2,
                            all_allowed_entry_checks=72817,
                            actual_scalar_row_coverage=180,
                            row_multiplicities_sha256=model.digest(sorted(
                                ((repr(key),number) for key,number in counts.items()))),
                            matrix_hashes=hashes,actions=actions))
    return dict(agent='six-downset-2',role='researcher',affine_generators=records,
                entire_physical_Gram=gram,
                five_generators_span_the_four_dimensional_affine_recipe=True,
                outside_region_generator_positivity_not_asserted=True,
                all_original_entry_lift_metric_and_action_identities_verified=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
