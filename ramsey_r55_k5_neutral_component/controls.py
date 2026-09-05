#!/usr/bin/env python3
"""Entry-level digest comparison, malformed certificates and frozen-K5 audit."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_verify():
    spec = importlib.util.spec_from_file_location('neutral_verifier',HERE/'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def must_reject(function, message):
    try:
        function()
    except ValueError as error:
        require(message in str(error),'unexpected rejection: '+str(error))
        return str(error)
    raise ValueError('malformed certificate accepted: '+message)


def compare(discovery, reference):
    require(discovery['status']=='NEUTRAL_COMPONENT_CLOSED','discovery is not closed')
    require(discovery['processed']==discovery['discovered']==reference['component_size'],'state coverage mismatch')
    records = discovery['records']
    require(len(records)==reference['component_size'],'record coverage mismatch')
    for i,record in enumerate(records):
        exact = reference['complete_censuses'][i]
        require(record['node']==i,'record index')
        for field in ('counts','admissible_K5_delta_histogram','canonical_supports_sha256'):
            require(record[field]==exact[field],'census mismatch: '+field)
        require(record['canonical_projected_classification_sha256']==reference['canonical_projected_classification_sha256_by_vertex'][i],
                'entry-level classification mismatch')
        require(record['neutral_neighbors']==reference['neutral_adjacency'][i],'neutral adjacency mismatch')
        require(record['color_counts']==reference['component_audits'][i]['color_counts']
                and record['phi']==reference['component_audits'][i]['phi'],'graph audit statistics mismatch')
    def key(item):
        return item['source'],tuple(map(tuple,item['support'])),tuple(item['color_counts']),item['changes_quotas']
    require(Counter(map(key,discovery['negative_exits']))==Counter(map(key,reference['negative_exits'])),
            'complete lower-exit incidence mismatch')
    return {'support_classifications_compared':sum(r['counts']['all_switches'] for r in records),
            'admissible_color_count_vectors_compared':sum(r['counts']['admissible'] for r in records),
            'negative_exit_incidences_compared':len(discovery['negative_exits'])}


def frozen_audit(initial, endpoint, checker):
    # Fixing all exceptional incidences and all six induced color-neighborhood
    # graphs leaves exactly the antipodal central-cell edges unexposed.
    free = {edge for edge in combinations(range(3,43),2) if (initial[edge[0]]&7)^(initial[edge[1]]&7)==7}
    visible = set()
    for root in range(3):
        for red in (True,False):
            side = [v for v in range(3,43) if bool(initial[root] >> v & 1)==red]
            visible.update(combinations(side,2))
    require(visible==set(combinations(range(3,43),2))-free,'literal visibility vs antipodal classification')
    require(all(bool(initial[u] >> v & 1)==bool(endpoint[u] >> v & 1) for u,v in visible),'visible edge changed')
    before = checker.mono_fives_literal(initial)
    after = checker.mono_fives_literal(endpoint)
    for rows,lists in ((initial,before),(endpoint,after)):
        require(lists==tuple(tuple(sorted(checker.monochromatic_bitsets(rows,color))) for color in (True,False)),
                'literal versus recursive full five-set comparison')
    immutable = []
    totals = []
    for red,old,new in zip((True,False),before,after):
        old,new = set(old),set(new)
        fixed = sorted(five for five in old if not free.intersection(combinations(five,2)))
        independently_fixed = sorted(five for five in old if all(edge in visible for edge in combinations(five,2)))
        require(fixed==independently_fixed and all(five in new for five in fixed),'frozen five-set discrepancy')
        for five in fixed:
            immutable.append([int(red),five])
        one_neighborhood = [five for five in old if any(all(bool(initial[e] >> v & 1)==color for v in five)
                             for e in range(3) for color in (True,False))]
        totals.append({'color':'red' if red else 'blue','before':len(old),'after':len(new),
                       'destroyed':len(old-new),'created':len(new-old),'immutable_under_all_antipodal_edits':len(fixed),
                       'contained_in_one_exceptional_color_neighborhood':len(one_neighborhood),
                       'first_immutable_example':fixed[0] if fixed else None})
    digest = hashlib.sha256((json.dumps(immutable,separators=(',',':'))+'\n').encode()).hexdigest()
    floor = sum(item['immutable_under_all_antipodal_edits'] for item in totals)
    require(floor>0,'no frozen obstruction found')
    return {'unexposed_antipodal_edges':len(free),'visible_central_edges':len(visible),'colors':totals,
            'immutable_K5_lower_bound_for_every_fixed_neighborhood_completion':floor,
            'canonical_immutable_K5_list_sha256':digest,
            'scope':'All recolorings of the 124 unexposed edges with the other edges fixed; no degree assumption needed. This is a lower bound, not an attained minimum or a whole degree-profile exclusion.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--component',type=Path,default=HERE/'COMPONENT.json')
    parser.add_argument('--graph',type=Path,default=HERE/'EXIT_GRAPH.json')
    parser.add_argument('--reference',type=Path,default=HERE/'report.json')
    parser.add_argument('--discovery',type=Path,default=HERE/'discovery_report.json')
    parser.add_argument('--work',type=Path,required=True)
    args = parser.parse_args()
    require(not args.work.exists(),'fresh control work directory required')
    args.work.mkdir(parents=True)
    start = time.monotonic()
    verify = load_verify()
    parent = verify.load_parent()
    literal = parent.load_parent()
    checker = literal.load_audit()
    require(hashlib.sha256(verify.SEED.read_bytes()).hexdigest()==verify.SEED_SHA,'seed pin')
    initial = checker.decode(json.loads(verify.SEED.read_text()))
    endpoint = checker.decode(json.loads(args.graph.read_text()))
    certificate = json.loads(args.component.read_text())
    graphs = verify.decode_component(certificate,parent,checker,initial)
    reference = json.loads(args.reference.read_text())
    discovery = json.loads(args.discovery.read_text())
    comparisons = compare(discovery,reference)
    rejected = {}
    bad = deepcopy(certificate)
    bad['level'] -= 1
    rejected['wrong_level'] = must_reject(lambda:verify.decode_component(bad,parent,checker,initial),'component seed/level')
    bad = deepcopy(certificate)
    bad['graphs'][-1] = bad['graphs'][0]
    rejected['duplicate_graph'] = must_reject(lambda:verify.decode_component(bad,parent,checker,initial),'duplicate component graph')
    bad = deepcopy(certificate)
    bad['parent_moves'][1][2:] = bad['parent_moves'][1][2:][::-1]
    rejected['reversed_switch'] = must_reject(lambda:verify.decode_component(bad,parent,checker,initial),'nonalternating move')
    rejected['omitted_neutral_vertex'] = must_reject(lambda:verify.closure(graphs[:-1],reference['complete_censuses'][:-1],parent,literal),
                                                  'neutral neighbor missing from component')
    bad = deepcopy(reference['complete_censuses'])
    bad[0]['nonincreasing_switches'] = []
    rejected['omitted_neutral_edges'] = must_reject(lambda:verify.closure(graphs,bad,parent,literal),'asymmetric neutral edges')
    bad = deepcopy(discovery)
    bad['records'][0]['canonical_projected_classification_sha256'] = '0'*64
    rejected['altered_entry_digest'] = must_reject(lambda:compare(bad,reference),'entry-level classification mismatch')
    bad = deepcopy(discovery)
    bad['negative_exits'].pop()
    rejected['omitted_lower_exit'] = must_reject(lambda:compare(bad,reference),'complete lower-exit incidence mismatch')
    command = [sys.executable,'-B',str(HERE/'search.py'),'--work',str(args.work/'cap-one'),'--max-states','1']
    first = subprocess.run(command,check=True,capture_output=True,text=True)
    limited = json.loads((args.work/'cap-one/result.json').read_text())
    require(limited['status']=='STATE_LIMIT' and limited['processed']==1 and limited['discovered']==4,'state cap mislabeled')
    subprocess.run(command+['--resume'],check=True,capture_output=True,text=True)
    resumed = json.loads((args.work/'cap-one/result.json').read_text())
    require(resumed['records']==limited['records'] and resumed['status']=='STATE_LIMIT','capped resume advanced or claimed closure')
    changed_contract = command[:-1]+['2','--resume']
    failure = subprocess.run(changed_contract,capture_output=True,text=True)
    require(failure.returncode!=0 and 'resume contract mismatch' in failure.stderr,'changed resume contract accepted')
    report = {'entry_comparison':comparisons,'rejected_mutations':rejected,
              'bounded_runner_controls':{'cap_status':limited['status'],'processed':1,'discovered':4,
                                         'same_contract_resume_preserved_records':True,'changed_contract_rejected':True},
              'frozen_neighborhood_audit':frozen_audit(initial,endpoint,checker)}
    (args.work/'controls_report.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True),flush=True)
    print(json.dumps({'elapsed_seconds':round(time.monotonic()-start,6),
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True),flush=True)


if __name__=='__main__':
    main()
