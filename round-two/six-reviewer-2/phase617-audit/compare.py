"""Post-seal whole native row/basis and original-AP/RUP correspondence."""
from pathlib import Path
import json,sys,hashlib
from rup import dimacs,replay

def need(ok,why):
    if not ok:raise ValueError(why)

def run(native,rows,basis):
    own=json.loads(rows.read_text());B=json.loads(basis.read_text());cert=json.loads((native/'phase-rows-v2.json').read_text())
    need((cert['q'],cert['N'],cert['roots'],cert['phase_period'])==(617,3704,[0,1,4],6),'entire native physical phase scope')
    expected=[[None if v is None else v[1:]for v in row]for row in own['whole_witnesses']]
    need(cert['all256_table_obstruction_APs_by_phase']==expected,'EVERY1536 actual native row entry')
    need(cert['surviving_truth_table_bytes_by_phase']==[own['projection_bytes']]*6,'all six native survivor rows')
    need(cert['all_same_phase_positive_APs']==own['phase_ap_count'] and cert['all_root_free_same_phase_positive_APs']==own['root_free_count'],'entire same-phase counts')
    need(cert['necessary_projection_only_prefix_length']==max(own['phase_cutoffs'])==632,'whole actual projection cutoff')
    kernel=json.loads((native/'kernel.json').read_text());tags=B['variable_tags'];need((kernel['q'],kernel['N'],kernel['roots'],kernel['phase_period'],kernel['variables'])==(617,3704,[0,1,4],6,68),'all original68-variable scope')
    lines=[];pairs=set();ids=set()
    for leaf in kernel['original_integer_AP_leaves']:
        a,d=leaf['original_AP'];need(type(a)is int and type(d)is int and a>=0 and d>0 and a+6*d<3704,'actual original AP')
        polarity=leaf['polarity'];need(polarity in (-1,1),'actual mono polarity');cid=leaf['original_clause_id'];need(type(cid)is int and 1<=cid<=1316800 and cid not in ids,'distinct declared provenance ordinal');ids.add(cid)
        literals=[polarity*v for v in sorted({tags[a+j*d]for j in range(7)})];need(literals==leaf['literals'],'ENTIRE literal native AP clause including all independent roots');lines.append(' '.join(map(str,literals))+' 0\n');pairs.add((a,d))
    cnf=('p cnf 68 '+str(len(lines))+'\n'+''.join(lines)).encode();need(cnf==(native/'kernel.cnf').read_bytes(),'ENTIRE original-AP/CNF byte correspondence');need(hashlib.sha256(cnf).hexdigest()==kernel['kernel_cnf_sha256'],'native declared compact CNF hash')
    proof=(native/'kernel.lrat').read_bytes();need(hashlib.sha256(proof).hexdigest()==kernel['kernel_lrat_sha256'],'native declared RUP byte hash')
    n,C=dimacs(cnf.decode());result=replay(n,C,proof.decode());need(result['additions']==39 and result['positive_hints']==999 and len(lines)==198 and len(pairs)==179,'ENTIRE compact native kernel/proof domain')
    return dict(status='COMPLETE_LATE_NATIVE_CORRESPONDENCE',whole_row_entries=1536,actual_row_obstructions=1500,whole_variable_positions=len(tags),regular_variables=48,independent_root_occurrences=len(B['root_positions']),kernel_clauses=len(lines),distinct_actual_kernel_APs=len(pairs),strict_independent_RUP=result,cnf_sha256=hashlib.sha256(cnf).hexdigest(),proof_sha256=hashlib.sha256(proof).hexdigest(),private_full658400_support_census_rerun=False,private_solver_conflict_count_rerun=False)
if __name__=='__main__':print(json.dumps(run(*map(Path,sys.argv[1:4])),sort_keys=True,separators=(',',':')))
