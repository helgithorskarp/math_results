"""Private first-prior-HIGH-equal-merge preparation intake, five ports only.
All states carry their complete 32-row functions. Necessary LOW D9 activity
uses all39 whole original domains. Guard stops are operational, never exclusions.
Depth12 is a derived comparator-budget ceiling:26+6 HIGH events+F <=44.
"""
import argparse
from collections import Counter, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent


def need(test,message):
    if not test:
        raise ValueError(message)


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--partner',type=int,choices=(4,),required=True)
    args = parser.parse_args()
    start = time.monotonic()
    deadline = start+42
    MAX_STATES = 20000
    c = json.loads((ROOT/f'work/low26-partner{args.partner}-construction-pilot.json').read_text())
    a = json.loads((ROOT/f'work/low26-partner{args.partner}-activity-pilot.json').read_text())
    states = c['core_states']
    columns = tuple(sum((x >> j & 1) << i for i,x in enumerate(states)) for j in range(10))
    domains = [r['core_image_index_mask'] for r in a['all39_original_domains']]
    need(len(domains)==39,'Original domain count changed')
    branches=[]
    for gate in combinations((5,6,7,9,10),2):
        swapped=columns[gate[0]-2] & ~columns[gate[1]-2]
        if not all(swapped & mask for mask in domains):
            branches.append({'HIGH_zero_gate':gate,'status':'INITIAL_GATE_INACTIVE_ON_A_LOW_D9_DOMAIN',
                'original_LOW_witness_mask':next(r['original_LOW_mask'] for r in a['all39_original_domains'] if not swapped & r['core_image_index_mask'])})
            continue
        live=tuple(sorted([p for p in (5,6,7,9,10,11) if p not in gate]+[gate[1]]))
        dead=tuple(p for p in range(2,12) if p not in live)
        need(len(dead)==5,'A single equal HIGH merge has not freed exactly one port')
        current=list(columns)
        current[gate[0]-2],current[gate[1]-2]=columns[gate[0]-2]&columns[gate[1]-2],columns[gate[0]-2]|columns[gate[1]-2]
        patterns=[sum((current[p-2] >> i & 1) << j for j,p in enumerate(dead)) for i in range(len(states))]
        pattern_columns=[sum((x==k) << i for i,x in enumerate(patterns)) for k in range(32)]
        initial=tuple(sum((x >> j & 1) << x for x in range(32)) for j in range(5))
        todo, words, edge_count=deque([initial]),{initial:()},0
        status='COMPLETE_WITHIN_DERIVED_SIZE44_PREPARATION_BUDGET'
        cutoff_states=0
        while todo:
            if time.monotonic()>deadline:
                status='INCOMPLETE_OPERATIONAL42_SECOND_GUARD'
                break
            f=todo.popleft()
            if len(words[f])==12:
                cutoff_states+=1
                continue
            image=[]
            for truth in f:
                image.append(sum(pattern_columns[k] for k in range(32) if truth >> k & 1))
            for i,j in combinations(range(5),2):
                active=image[i] & ~image[j]
                if not all(active & mask for mask in domains):
                    continue
                fresh=list(f)
                fresh[i],fresh[j]=f[i]&f[j],f[i]|f[j]
                fresh=tuple(fresh)
                need(fresh!=f,'Accepted preparation comparator is an identity')
                edge_count+=1
                if fresh not in words:
                    if len(words)>=MAX_STATES:
                        status='INCOMPLETE_OPERATIONAL20000_STATE_GUARD'
                        break
                    words[fresh]=words[f]+((dead[i],dead[j]),)
                    todo.append(fresh)
            if status.startswith('INCOMPLETE'):
                break
        rows=[{'full_five_variable_columns':list(f),'shortest_word':list(word)} for f,word in sorted(words.items())]
        branches.append({'HIGH_zero_gate':gate,'HIGH_live_ports':live,'dead_preparation_ports':dead,
            'status':status,'complete':not status.startswith('INCOMPLETE'),
            'full_functions_seen':len(words),'admissible_transition_count':edge_count,
            'shortest_lengths':dict(sorted(Counter(map(len,words.values())).items())),
            'states_at_derived_budget12':cutoff_states,'pending_function_states':len(todo),
            'full_functions_sha256':digest(rows),'functions':rows})
        if status.startswith('INCOMPLETE'):
            break
    complete=len(branches)==10 and all(not b['status'].startswith('INCOMPLETE') for b in branches)
    out={'agent':'six-sorting-1','role':'researcher','partner':args.partner,
        'status':'COMPLETE_PRIVATE_FIVEPORT_NECESSARY_FUNCTION_FRONTIER' if complete else 'INCOMPLETE_PRIVATE_FIVEPORT_OPERATIONAL_INTAKE',
        'all_ten_first_HIGH_equal_merges_accounted':len(branches)==10,
        'derived_preparation_budget':12,'derivation':'LOW26 plus exactly6 HIGH events to saturation/one secondary root gives32+F<=44.',
        'source_commit_for_base_and_generic_bounds':'d6a2bbdaabed14fdbcfd901256240a6f59c6c407',
        'branches':branches,'seconds':time.monotonic()-start,
        'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'Exactly one equal HIGH merge precedes the first strict singleton. Necessary five-port preparation functions only; no singleton/tail/nested exclusion yet. Two/three prior merges and unrestricted44 remain open.'}
    (ROOT/f'work/low26-fiveport-preparation-partner{args.partner}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='branches'}|{'branches_summary':[{k:v for k,v in b.items() if k!='functions'} for b in branches]},sort_keys=True))


if __name__=='__main__':
    main()
