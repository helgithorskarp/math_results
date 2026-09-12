"""Definition-level controls for scope, matching capacity and forged proofs."""
from itertools import combinations
from pathlib import Path
import argparse,json,tempfile
import problem,verify

def rejected(f):
    try:f()
    except (ValueError,FileNotFoundError):return 1
    raise ValueError('invalid input/certificate accepted')

def run(checker=None):
    pairs=[(i,7-i) for i in range(4)];blue_fours=[]
    for S in combinations(range(8),4):
        if not any(u in S and v in S for u,v in pairs):blue_fours.append(set(S))
    problem.require(len(blue_fours)==16,'matching transversal census');admissible=0
    for w in range(256):
        red={i for i in range(8) if w>>i&1};valid=all(S&red for S in blue_fours);full=any(u in red and v in red for u,v in pairs)
        problem.require(valid==full,'matching contact cover');admissible+=valid
    problem.require(admissible==175 and 4*3<15,'matching capacity')
    result=json.loads((problem.HERE/'EXPECTED.json').read_text());positive=next(r for r in result['results'] if r['status']=='SAT_TAIL_ONLY');rep=positive['representative'];graph=problem.graph_from_word(positive['physical_tail_word']);problem.check_graph(rep,graph)
    reject=0
    reject+=rejected(lambda:verify.check_tail(rep,'0'*136))
    reject+=rejected(lambda:verify.check_tail(rep,positive['physical_tail_word'][:-1]))
    reject+=rejected(lambda:problem.check_graph(rep,{'order':43,'red_edges':graph['red_edges']}))
    graph2={'order':23,'red_edges':graph['red_edges']+[graph['red_edges'][0]]};reject+=rejected(lambda:problem.check_graph(rep,graph2))
    proof_rejected=False
    if checker:
        with tempfile.TemporaryDirectory() as temporary:
            d=Path(temporary);cnf=d/'satisfiable.cnf';proof=d/'fake.drat';cnf.write_bytes(problem.dimacs(rep));proof.write_bytes(b'a\x00')
            reject+=rejected(lambda:verify.checked_proof(cnf,proof,checker));proof_rejected=True
            reject+=rejected(lambda:verify.checked_proof(cnf,d/'missing.drat',checker))
    return {'matching_contact_words':256,'admissible_matching_contacts':admissible,'core_capacity':12,'invalid_objects_rejected':reject,'forged_empty_proof_on_literal_SAT_tail_rejected':proof_rejected,'original_task_status':'UNKNOWN'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--drat-trim');p.add_argument('--output');a=p.parse_args();r=run(a.drat_trim)
    if a.output:Path(a.output).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
