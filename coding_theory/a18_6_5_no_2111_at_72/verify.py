"""Verify full streams and every literal residual coloring certificate."""
from itertools import combinations
import hashlib
import json
from paths import BASE, WORK


def digest(value, sort=False):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), sort_keys=sort).encode()).hexdigest()


def run():
    certificate = json.loads((BASE/'certificates.json').read_text())
    dependency = json.loads((BASE/'DEPENDENCY.json').read_text())
    if hashlib.sha256((BASE/'expected.json').read_bytes()).hexdigest() != dependency['extracted_fixture_sha256']:
        raise RuntimeError('imported fixture source differs')
    if hashlib.sha256((BASE/'automorphisms.py').read_bytes()).hexdigest() != dependency['literal_audit_source_sha256']:
        raise RuntimeError('literal audit source differs from published dependency')
    run_record = json.loads((WORK/'proof_run.json').read_text())
    if not run_record['status'].startswith('COMPLETE') or len(run_record['stages']) != 7:
        raise RuntimeError('INCOMPLETE proof reproduction cannot give a global certificate verdict')
    auto = json.loads((WORK/'automorphism_audit.json').read_text())
    tail = json.loads((WORK/'tail_carrier.json').read_text())
    spec = json.loads((WORK/'mapping_specs.json').read_text())
    census = json.loads((WORK/'census.json').read_text())
    joint = json.loads((WORK/'joint_classes.json').read_text())
    color = json.loads((WORK/'color_bounds.json').read_text())
    if any(not q['status'].startswith('COMPLETE') for q in (auto,tail,census,joint,color)):
        raise RuntimeError('INCOMPLETE mathematical stage')
    if auto['orders'] != certificate['star_automorphism_orders'] or digest([q['automorphisms'] for q in auto['cases']]) != certificate['automorphism_maps_sha256']:
        raise RuntimeError('literal point group differs')
    if (tail['canonical_tail_domain_sha256'] != certificate['canonical_tail_domain_sha256']
            or tail['total_orbits'] != certificate['total_tail_orbits']
            or [[q['orbit_count'] for q in tail['pairs'][i*8:(i+1)*8]] for i in range(8)] != certificate['tail_orbit_counts']):
        raise RuntimeError('complete shared-tail carrier differs')
    raw = (WORK/'mapping_fibers.txt').read_bytes()
    if hashlib.sha256(raw).hexdigest() != certificate['mapping_matrix_sha256']:
        raise RuntimeError('actual mapping matrices differ')
    # Independently reconstruct each actual input row from the literal blocks.
    rows = raw.decode().splitlines()
    if rows[0] != 'PAIR2111_V1 4404' or len(rows) != 4405 or len(spec['fibers']) != 4404:
        raise RuntimeError('mapping matrix coverage differs')
    pairs = {}
    for q in tail['pairs']:
        for orbit in q['orbits']:
            pairs[(q['first'],q['second'],orbit['index'])] = orbit
    for index, entry in enumerate(spec['fibers']):
        first = tail['stars'][entry['first']]
        second = tail['stars'][entry['second']]
        orbit = pairs[(entry['first'],entry['second'],entry['tail_orbit'])]
        fixed = [-1]*16
        for u,v in zip(second['tail'],orbit['representative']): fixed[u-1]=v-1
        a = sorted(w>>1 for w in first['words'] if not w&1)
        b = sorted(w>>1 for w in second['words'] if not w&1)
        if list(map(int,rows[index+1].split())) != [index]+a+b+fixed or fixed != entry['fixed']:
            raise RuntimeError('literal matrix reconstruction differs entrywise')
    stream = []
    with (WORK/'all_prune.jsonl').open() as a, (WORK/'all_literal.jsonl').open() as b:
        for index in range(4404):
            left = json.loads(a.readline()); right = json.loads(b.readline())
            if (left['index'] != index or right['index'] != index or left['status'] != 'COMPLETE'
                    or right['status'] != 'COMPLETE' or left['accepted'] != right['accepted']
                    or right['nodes'] != 5040):
                raise RuntimeError('full mapping streams differ or are incomplete')
            stream.append([index,left['accepted']])
        if a.read().strip() or b.read().strip(): raise RuntimeError('extra mapping output')
    if digest(stream) != certificate['all_accepted_mappings_sha256']:
        raise RuntimeError('complete compatible mapping corpus differs')
    for key in ('positive_fibers','normalized_compatible_maps','raw_compatible_maps','primary_nodes','literal_nodes'):
        if census[key] != certificate[key]: raise RuntimeError('census scalar differs: '+key)
    if [[q['raw_compatible_maps'] for q in census['pairs'][i*8:(i+1)*8]] for i in range(8)] != certificate['raw_compatible_counts']:
        raise RuntimeError('every pair mapping multiplicity differs')
    fields = ['index','first','second','left','right','center_fixing_automorphism_order','raw_map_multiplicity','orbit_size','orbit_sha256']
    if (joint['classes'] != 128 or joint['ordered_class_counts'] != certificate['ordered_joint_counts']
            or digest([{k:q[k] for k in fields} for q in joint['cases']], True) != certificate['joint_classes_sha256']):
        raise RuntimeError('ordered joint-star classification differs')
    if color['records'] != certificate['color_certificates'] or len(color['records']) != 128:
        raise RuntimeError('actual coloring records differ')
    maximum = 0
    # These checks use sets and the published certificate, never the producer's coloring algorithm.
    for case, claim in zip(joint['cases'],certificate['color_certificates']):
        fixed = {frozenset(u for u in range(18) if w>>u&1) for w in case['left']+case['right']}
        if (len(fixed) != 37 or any(len(w)!=5 for w in fixed)
                or any(len(a&b)>2 for a,b in combinations(fixed,2))):
            raise RuntimeError('literal joint-star witness fails')
        for x in (0,17):
            if sum(x in w for w in fixed)!=20: raise RuntimeError('wrong saturated point degree')
            deficits=[5-sum(x in w and y in w for w in fixed) for y in range(18) if y!=x]
            if sorted([v for v in deficits if v],reverse=True)!=[2,1,1,1]: raise RuntimeError('wrong deficit row')
        if sum({0,17}<=w for w in fixed)!=3: raise RuntimeError('wrong shared pair replication')
        domain=[frozenset(q) for q in combinations(range(1,17),5) if all(len(frozenset(q)&w)<=2 for w in fixed)]
        masks=[sum(1<<u for u in q) for q in domain]
        if len(domain)!=claim['candidates'] or digest(masks)!=claim['candidate_sha256']:
            raise RuntimeError('literal candidate domain differs')
        partition=claim['partition']
        flattened=[u for group in partition for u in group]
        if (sorted(flattened)!=list(range(len(domain)))
                or any(len(domain[a]&domain[b])<3 for group in partition for a,b in combinations(group,2))
                or len(partition)>29 or claim['certified_code_upper']!=37+len(partition)):
            raise RuntimeError('coloring certificate fails coverage or literal incompatibility')
        maximum=max(maximum,37+len(partition))
    if maximum!=66 or maximum!=certificate['maximum_code_upper']:
        raise RuntimeError('certified restricted bound differs')
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE',mapping_fibers=4404,
                joint_classes=128,color_certificates=128,certified_mutually_paired_2111_code_upper=66,
                ordinary_corollary_at72='every pair multiplicity4or5; all18 positive rows unit',
                global_interval=[69,72],sharpness_of66_claimed=False)
    (WORK/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)
    return result


if __name__=='__main__':
    run()
