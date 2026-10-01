"""Replay the pinned full prerequisite chain and identify reference data."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
import check

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def replay(prerequisite_root,completion_root,cyclic_root,near_root):
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    folders={'asymmetric':prerequisite_root/inputs['asymmetric']['directory'],
             'completion':completion_root,'cyclic':cyclic_root}
    for tag,folder in folders.items():
        for name,sha in inputs[tag]['files_sha256'].items():
            check.require(hashlib.sha256((folder/name).read_bytes()).hexdigest()==sha,'pinned prior '+tag+'/'+name)
    flags=['-O'] if sys.flags.optimize else []
    r=subprocess.run([sys.executable,*flags,'-B',str(cyclic_root/'replay.py'),
                      '--prerequisite-root',str(prerequisite_root),'--completion-root',str(completion_root),
                      '--near-pattern-root',str(near_root)],check=True,capture_output=True,text=True,timeout=50)
    old=json.loads(r.stdout)
    check.require(old['status']=='VERIFIED' and old['full_completion_prerequisites_replayed']
                  and old['asymmetric_local_replayed'] and old['cyclic_local_verified'],'full prerequisite chain')
    c=json.loads((HERE/'certificate.json').read_text())
    prior=json.loads((completion_root/'certificate.json').read_text())
    check.require(c['incumbent_vectors']==prior['incumbent_vectors'],'same exact incumbent reference')
    check.require((HERE/'field.py').read_bytes()==(completion_root/'field.py').read_bytes(),'same pinned field arithmetic')
    result=check.verify(c)
    return {'status':'VERIFIED','core_cap_verified':True,'reference_vectors_identified':True,
            'full_completion_and_local_chain_replayed':True,'twenty_four_contact_tolerance':result['exclusion_max']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prerequisite-root',type=Path,default=ROOT)
    parser.add_argument('--completion-root',type=Path,default=ROOT/'round-two/six-tammes-2/fourteen-point-completion')
    parser.add_argument('--cyclic-root',type=Path,default=ROOT/'round-two/six-tammes-2/cyclic-local-exclusion')
    parser.add_argument('--near-pattern-root',type=Path,default=ROOT/'round-two/six-tammes-2/robust-incumbent-pattern')
    a=parser.parse_args()
    print(json.dumps(replay(a.prerequisite_root,a.completion_root,a.cyclic_root,a.near_pattern_root),sort_keys=True))
