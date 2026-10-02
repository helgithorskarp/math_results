#!/usr/bin/env python3
"""Strict checker positive calibration and intentionally malformed proofs."""
import argparse
import importlib.util
import json
import tempfile
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def controls(checker_path,cnf_path=None,lrat_path=None):
    spec=importlib.util.spec_from_file_location('credited_positive_RUP_checker',checker_path)
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    with tempfile.TemporaryDirectory() as directory:
        cnf=Path(directory)/'tiny.cnf';proof=Path(directory)/'tiny.lrat'
        cnf.write_text('p cnf 2 3\n1 2 0\n-1 0\n-2 0\n');proof.write_text('4 0 2 3 1 0\n')
        need(checker.verify(cnf,proof)['mathematical_exclusion'],'Positive RUP calibration failed')
        bad=['4 1 0 3 1 0\n','4 0 -1 2 0\n','4 3 0 1 0\n','4 0 99 0\n',
             '4 0 2 3 1\n','4 0 1 0\n','4 d 2 0\n5 0 2 3 1 0\n','3 0 2 3 1 0\n']
        for raw in bad:
            proof.write_text(raw)
            try:checker.verify(cnf,proof)
            except (ValueError,KeyError,IndexError):pass
            else:raise ValueError('Malformed RUP calibration accepted')
        result={'positive_RUP_control':True,'generic_damaged_proofs_rejected':len(bad)}
        if cnf_path is not None:
            need(lrat_path is not None,'Missing production trace')
            lines=lrat_path.read_text().splitlines();changed=lines.copy();n=int(cnf_path.read_text().splitlines()[0].split()[2])
            for i,line in enumerate(changed):
                entries=line.split()
                if entries[1] not in ('d','0'):
                    entries[1]=str(n+1);changed[i]=' '.join(entries);break
            else:raise ValueError('Production trace has no nonempty addition')
            damages=['\n'.join(changed)+'\n','\n'.join(line for line in lines if line.split()[1]!='0')+'\n']
            for raw in damages:
                proof.write_text(raw)
                try:checker.verify(cnf_path,proof)
                except (ValueError,KeyError,IndexError):pass
                else:raise ValueError('Damaged production RUP trace accepted')
            result['production_damaged_proofs_rejected']=len(damages)
        return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--checker',type=Path,required=True)
    p.add_argument('--cnf',type=Path);p.add_argument('--lrat',type=Path)
    a=p.parse_args();print(json.dumps(controls(a.checker,a.cnf,a.lrat)))
