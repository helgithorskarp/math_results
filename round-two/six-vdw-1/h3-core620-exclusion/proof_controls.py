"""Valid unit/binary-chain contradictions and damaged actual strict RUP proofs."""
import argparse
import importlib.util
import json
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def run(cnf,lrat,work):
    spec=importlib.util.spec_from_file_location('credited_strict_rup',Path(__file__).resolve().parent/'strict_rup.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    require(not work.exists(),'fresh proof-control directory');work.mkdir()
    tiny=work/'tiny.cnf';proof=work/'tiny.lrat'
    tiny.write_text('p cnf 1 2\n1 0\n-1 0\n');proof.write_text('3 0 1 2 0\n');module.verify(tiny,proof)
    invalid=['3 0 0\n','3 0 -1 0\n','3 0 99 0\n','2 0 1 2 0\n','3 2 0 1 2 0\n',
             '3 1 0 1 0\n','3 0 1 0\n','3 d 1 0\n4 0 1 2 0\n','3 1 0 1 0\n3 0 1 2 0\n']
    rejected=0
    for text in invalid:
        proof.write_text(text)
        try:module.verify(tiny,proof)
        except (ValueError,KeyError,IndexError):rejected+=1
        else:raise ValueError('bad tiny proof accepted')
    tiny.write_text('p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n')
    proof.write_text('5 2 0 1 2 0\n6 -2 0 3 4 0\n7 0 5 6 0\n');module.verify(tiny,proof)
    lines=lrat.read_text().splitlines();empty=[i for i,l in enumerate(lines) if l.split()[1]=='0']
    require(empty,'actual proof has no closing record')
    damaged=['\n'.join(l for l in lines if l.split()[1]!='0')+'\n']
    n=int(cnf.read_text().splitlines()[0].split()[2]);changed=lines.copy()
    for i,l in enumerate(changed):
        tokens=l.split()
        if tokens[1]!='d':tokens.insert(1,str(n+1));changed[i]=' '.join(tokens);break
    damaged.append('\n'.join(changed)+'\n')
    changed=lines.copy();i=empty[0];changed[i]=changed[i].split()[0]+' 0 0';damaged.append('\n'.join(changed)+'\n')
    for text in damaged:
        proof.write_text(text)
        try:module.verify(cnf,proof)
        except (ValueError,KeyError,IndexError):rejected+=1
        else:raise ValueError('bad actual production proof accepted')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_H3_STRICT_PROOF_CONTROLS',
            'tiny_positive_refutations':2,'tiny_damages_rejected':len(invalid),
            'production_damages_rejected':len(damaged),'all_damages_rejected':rejected,
            'scope':'Pinned strict RUP kernel controls, including actual100-input proof; no extra family theorem.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cnf',type=Path);p.add_argument('lrat',type=Path);p.add_argument('work',type=Path);a=p.parse_args()
    print(json.dumps(run(a.cnf,a.lrat,a.work),sort_keys=True),flush=True)
