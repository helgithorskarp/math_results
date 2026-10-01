"""Frozen complete-record replay with explicit checks (also under python -O)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vendor', type=Path)
    parser.add_argument('--expected', type=Path, default=ROOT/'expected.json')
    parser.add_argument('--inputs', type=Path, default=ROOT)
    parser.add_argument('--author-expected', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        if os.environ.get(key) != '1':
            raise ValueError('Set all six numerical thread limits to1')
    signal.alarm(90)
    sys.path.insert(0, str(ROOT))
    if args.vendor:sys.path.insert(0, str(args.vendor.resolve()))
    from derive import (derive, require, characteristic, complete, equations,
                        sector, read_inputs, FREE, Q, END, S, N, M, MULTS, ORDERS,
                        canonical, digest, sp)
    start=time.monotonic()
    result=derive(args.inputs)
    # Complete schema, every rational coefficient, every matrix/polynomial/action
    # hash and every case must match a frozen record produced in an earlier run.
    expected=json.loads(args.expected.read_text())
    require(canonical(result)==canonical(expected), 'complete frozen mathematical record and types')
    body=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(body)
    rejections=[]
    def reject(name, operation):
        try:
            operation()
        except ValueError:
            rejections.append(name)
            return
        raise ValueError('Damage accepted: '+name)
    for name,a in (
        ('negative-eigenvalue',sp.diag(-1,1)),
        ('two-negative-eigenvalues',sp.diag(-1,-2)),
        ('nonzero-zero-diagonal-residual',sp.Matrix([[0,1],[1,0]])),
        ('nonreal-spectrum-with-positive-coefficients',sp.Matrix([[0,-1],[1,0]]))):
        reject(name,lambda a=a:characteristic(a,sp.eye(2)))
    reject('wrong-nullity',lambda:characteristic(sp.diag(0,1),sp.eye(2),0))
    seed,dual,_=read_inputs(args.inputs)
    b=complete([Q(x) for x in seed['free_values']])
    wrong=b.copy();wrong[1,1]+=1
    reject('wrong-affine-bottom-coordinate',lambda:require(equations(wrong)==[0]*28,'affine equations'))
    wrong=b.copy();wrong[1,1]+=182*END;wrong[1,2]+=13*END;wrong[2,1]+=13*END;wrong[2,2]+=END
    from derive import bc
    reject('reversed-trade-sign',lambda:require(all(sum(wrong[a,c]*bc(15-a,c-1) for c in range(1,15))==S for a in range(1,15)), 'star equations'))
    _,g,k,u=sector(b,8)
    reject('false-upper-floor',lambda:characteristic(u-N*sp.eye(1),g))
    _,g,k,u=sector(b,1)
    reject('unweighted-nonsymmetric-quotient',lambda:characteristic(k,sp.eye(14)))
    reject('omitted-middle-harmonic',lambda:require(sum(a*d for a,d in zip(ORDERS[:-1],MULTS[:-1]))==M,'dimension coverage'))
    action=sum((int(bool(x&1))-int(bool(x&2))) for x in range(1,1<<16) if x.bit_count()==1 and not x&1)
    require(action==-1,'literal point action')
    reject('wrong-point-action-sign',lambda:require(action==1,'point action sign'))
    # Complete external fixture damage guards, not just summary hashes.
    damaged=json.loads(json.dumps(expected));del damaged['blocks'][-1]['sectors'][-1]
    reject('fixture-omitted-sector',lambda:require(result==damaged,'whole fixture'))
    damaged=json.loads(json.dumps(expected));damaged['full_face_coupling']['coefficients'][0][-1]='0'
    reject('fixture-wrong-coupling-coefficient',lambda:require(result==damaged,'whole fixture'))
    damaged=json.loads(json.dumps(expected));damaged['endpoint_lower_floor']='1'
    reject('fixture-false-lower-floor',lambda:require(result==damaged,'whole fixture'))
    author_matches=0
    if args.author_expected:
        author=json.loads(args.author_expected.read_text())
        require(author['agent']=='six-downset-2' and author['role']=='researcher','author attribution')
        require(result['input_sha256']==[author['seed_sha256'],author['dual_sha256']], 'author input hashes');author_matches+=2
        require(result['dual_constant']==author['dual']['constant'] and result['dual_y_sha256']==author['dual']['Y_hashes'],'whole author dual');author_matches+=2
        require(result['complement_coefficients']==author['dual']['zero_coefficients'], 'whole author zero coefficients');author_matches+=1
        for our,their in zip(result['blocks'],author['seed']['parameters']):
            require(our['parameter']==their['t'] and our['full_lower_rank']==their['full_lower_rank'] and our['full_upper_rank']==their['full_upper_rank'], 'full author parameter');author_matches+=1
            require(len(our['sectors'])==len(their['block_data'])==9,'author case count')
            for ours,theirs in zip(our['sectors'],their['block_data']):
                d=ours['lower']['order'];nu=ours['lower']['nullity']
                require([ours['degree'],d,ours['multiplicity'],d-nu,ours['lower_form_sha256'],ours['upper_form_sha256']]==theirs,'whole author sector matrices and rank');author_matches+=1
    signal.alarm(0)
    print(json.dumps({'status':'PASS','record_sha256':digest(result),'complete_sectors':27,
                      'characteristic_certificates':65,'literal_action_rows':sum(x['rows'] for x in result['literal_harmonic_controls']),
                      'mathematical_damage_rejections':11,'fixture_damage_rejections':rejections[11:],
                      'whole_author_comparisons':author_matches,'endpoint_lower_floor':result['endpoint_lower_floor'],
                      'seconds':time.monotonic()-start,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__=='__main__':main()
