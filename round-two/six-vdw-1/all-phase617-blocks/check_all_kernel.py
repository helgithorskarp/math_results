"""Standalone Gauss/physical AP/local-domain/whole compact CNF/positive-RUP proof.

No generator, native solver, converter, full model, ledger or prior exclusion.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from check_all_domains import check,gauss_keys
from strict_rup import verify


def need(ok,message):
    if not ok:
        raise ValueError(message)


def necessary_clauses(rows):
    clauses=[]
    for row in rows:
        domain=row['truth_tables'];selectors=row['selector_variables_little_endian']
        for high_first in itertools.product((0,1),repeat=len(selectors)):
            bits=list(reversed(high_first))
            index=sum(x*2**j for j,x in enumerate(bits))
            mismatch=[v if bit==0 else -v for v,bit in zip(selectors,bits)]
            if index>=len(domain):
                clauses.append(mismatch)
            else:
                for key,v in enumerate(row['color_variables_by_key']):
                    clauses.append(mismatch+[v if (domain[index]//2**key)%2 else -v])
    clauses.extend([[-v] for v in [63,158,253,354,449,544]])
    need(len(clauses)==29502,'entire necessary36-local-row selector encoding')
    return clauses


def check_kernel(record,cnf,proof,plan):
    scope={'schema':'ALL_SIX_BLOCK_PHASE_AP_AND_NECESSARY_LOCAL_ROW_RUP_KERNEL_V1',
           'q':617,'N':3704,'block_length':617,'global_phases':[],
           'block_varying_phases':list(range(6)),'roots':[0,1,4,16],'phase_period':6,
           'variables':818,'color_helpers':602,'actually_realized_color_helpers':596,
           'selector_helpers':216,'actual_root_bits':26,
           'unused_regular_entries':[63,158,253,354,449,544],
           'extra_foreign_constraints':[],'old_global_projection_assumed':False,
           'old_constant_tail_projection_assumed':False,'mathematical_exclusion':False}
    for name,value in scope.items():
        need(record[name]==value,'whole standalone compact scope:'+name)
    rows,domains=check(plan);choices=necessary_clauses(rows);keys=gauss_keys()
    roots=[n for n in range(3704) if n%617 in (0,1,4,16)]
    free={n:577+i for i,n in enumerate(roots)}
    tags=[free[n] if n in free else 1+96*(n//617)+6*keys[n%617]+n%6 for n in range(3704)]
    need(len(roots)==26 and set(tags)==set(range(1,603))-{63,158,253,354,449,544},
         'every actual root independent and only harmless absent entries canonicalized')
    leaves=record['leaves'];need(type(leaves) is list and leaves,'nonempty direct mathematical leaves')
    initial=['p cnf 818 %d\n'%len(leaves)];aps=set();row_indices=set();ap_count=row_count=0
    for leaf in leaves:
        if leaf['kind']=='actual_original_AP':
            start,step=leaf['original_AP']
            need(type(start) is int and type(step) is int and start>=0 and step>0
                 and start+6*step<3704,'actual positive-step original interval AP')
            need(type(leaf['polarity']) is int and leaf['polarity'] in (-1,1),'actual color polarity')
            clause=[leaf['polarity']*v for v in sorted({tags[start+j*step] for j in range(7)})]
            need(leaf['literals']==clause,'all seven original AP points mapped to actual colors')
            aps.add((start,step));ap_count+=1
        elif leaf['kind']=='proved_necessary_local_row_choice':
            index=leaf['choice_clause_index']
            need(type(index) is int and 0<=index<len(choices),'real necessary local row-clause index')
            clause=choices[index]
            need(leaf['literals']==clause,'independently proved LOCAL row necessity, no global cut')
            row_indices.add(index);row_count+=1
        else:
            raise ValueError('foreign or unsupported mathematical proof leaf')
        initial.append(' '.join(map(str,clause))+' 0\n')
    expected=''.join(initial).encode()
    need(cnf.read_bytes()==expected,'whole physical AP/necessary local row compact formula')
    need(record['kernel_cnf_sha256']==hashlib.sha256(expected).hexdigest()
         and record['kernel_lrat_sha256']==hashlib.sha256(proof.read_bytes()).hexdigest(),
         'whole compact signed formula and proof bytes')
    replay=verify(cnf,proof)
    need(replay['variables']==818 and replay['initial_clauses']==len(leaves)
         and replay['checked_additions']==record['proof_additions'],'every exact compact RUP step and empty clause')
    return {'author':'six-vdw-1','role':'researcher',
            'status':'EXACT_ALL_SIX_BLOCK_PHASE_FOUR_CHARACTER_FAMILY_EXCLUDED_AT3704',
            'q':617,'N_excluded':3704,'roots':[0,1,4,16],'phase_period':6,'block_length':617,
            'global_phases':[],'block_varying_phases':list(range(6)),
            'all_original_roots_independently_free':True,
            'AP_leaf_clauses':ap_count,'necessary_local_row_choice_leaves':row_count,
            'distinct_actual_APs':len(aps),'distinct_necessary_local_row_clauses':len(row_indices),
            'literal_original_AP_points':7*ap_count,'maximum_original_AP_endpoint':max(a+6*d for a,d in aps),
            'necessary_domain_proof':domains,'strict_compact_RUP':replay,
            'family_exclusion_at3704':True,'larger_N_requires_same_first3704_restriction':True,
            'attainment_at3703_requires_separate_checked_known_word':True,
            'unrestricted_W_upper_or_exact_value_claimed':False,'new_W_lower_bound_claimed':False,
            'valid3704_coloring':False,'ordinary_bridges_formalized':False,'external_review_claimed':False}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent)
    a=p.parse_args();h=a.directory
    print(json.dumps(check_kernel(json.loads((h/'kernel.json').read_bytes()),h/'kernel.cnf',h/'kernel.lrat',
                                  json.loads((h/'ALL_PHASE_BLOCKS_NEXT_PLAN.json').read_bytes())),sort_keys=True))
