#!/usr/bin/env python3
"""Complete small controls and deliberately damaged reduction/model inputs."""
import argparse
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
from normalize import representatives
from check_orbits import check
from check_model import audit
from generate import generate

def need(condition,message):
    if not condition:raise ValueError(message)

def manifest(q):
    rows=representatives(q)
    return {'q':q,'representatives':rows,'representative_count':len(rows),
            'raw_skeleton_count':4*q*(q-1)*(q-2),'orientation_bits_per_representative':q,
            'global_complement_normalized_free_bits':q-1,'orientation_invariance_imposed':False}

def orbit_controls():
    results=[]
    for q in (7,11,13):
        result=check(manifest(q));result.pop('seconds');result.pop('peak_KiB');results.append(result)
    original=manifest(7);damaged=[]
    d=copy.deepcopy(original);d['representatives'].pop();d['representative_count']-=1;damaged.append(d)
    d=copy.deepcopy(original);d['representatives'].append(copy.deepcopy(d['representatives'][0]));d['representative_count']+=1;damaged.append(d)
    d=copy.deepcopy(original);d['representatives'][0]['raw_skeleton_orbit_size']+=1;damaged.append(d)
    d=copy.deepcopy(original);d['representatives'][0]['lambda']=1;damaged.append(d)
    d=copy.deepcopy(original);d['orientation_invariance_imposed']=True;damaged.append(d)
    d=copy.deepcopy(original);d['q']=9;damaged.append(d)
    for record in damaged:
        try:check(record)
        except ValueError:pass
        else:raise ValueError('Damaged orbit reduction accepted')
    return {'complete_small_orbit_controls':results,'damaged_orbit_inputs_rejected':len(damaged)}

def model_controls():
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'model.cnf';generate(7,'same',2,path);source=path.read_text().splitlines()
        valid=audit(path,7,'same',2);valid.pop('seconds');damaged=[]
        rows=source.copy();unit=rows.index('-1 0');rows[unit]='1 0';damaged.append(rows)
        rows=source.copy();index=next(i for i,row in enumerate(rows[1:],1) if row.count(' ')>1);rows.pop(index)
        header=rows[0].split();header[3]=str(int(header[3])-1);rows[0]=' '.join(header);damaged.append(rows)
        rows=source.copy();rows.append('-2 0');header=rows[0].split();header[3]=str(int(header[3])+1);rows[0]=' '.join(header);damaged.append(rows)
        rows=source.copy();rows[0]=rows[0].replace('p cnf 7 ','p cnf 8 ');damaged.append(rows)
        for rows in damaged:
            path.write_text('\n'.join(rows)+'\n')
            try:audit(path,7,'same',2)
            except ValueError:pass
            else:raise ValueError('Damaged orientation model accepted')
    return {'reference_small_model':valid,'damaged_models_rejected':len(damaged)}

def proof_controls(checker_path,production_cnf=None,production_lrat=None):
    spec=importlib.util.spec_from_file_location('credited_checker',checker_path)
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    with tempfile.TemporaryDirectory() as directory:
        cnf=Path(directory)/'tiny.cnf';proof=Path(directory)/'tiny.lrat'
        cnf.write_text('p cnf 2 3\n1 2 0\n-1 0\n-2 0\n');proof.write_text('4 0 2 3 1 0\n')
        need(checker.verify(cnf,proof)['mathematical_exclusion'],'Positive RUP control failed')
        bad=['4 1 0 3 1 0\n','4 0 -1 2 0\n','4 3 0 1 0\n','4 0 99 0\n',
             '4 0 2 3 1\n','4 0 1 0\n','4 d 2 0\n5 0 2 3 1 0\n','3 0 2 3 1 0\n']
        for body in bad:
            proof.write_text(body)
            try:checker.verify(cnf,proof)
            except (ValueError,KeyError,IndexError):pass
            else:raise ValueError('Malformed positive-RUP proof accepted')
        result={'positive_RUP_control':True,'generic_damaged_proofs_rejected':len(bad)}
        if production_cnf is not None:
            need(production_lrat is not None,'Missing production proof')
            rows=production_lrat.read_text().splitlines();changed=rows.copy()
            variables=int(production_cnf.read_text().splitlines()[0].split()[2])
            for index,row in enumerate(changed):
                words=row.split()
                if words[1] not in ('d','0'):
                    words[1]=str(variables+1);changed[index]=' '.join(words);break
            else:raise ValueError('No nonempty production addition')
            damage=['\n'.join(changed)+'\n','\n'.join(row for row in rows if row.split()[1]!='0')+'\n']
            for body in damage:
                proof.write_text(body)
                try:checker.verify(production_cnf,proof)
                except (ValueError,KeyError,IndexError):pass
                else:raise ValueError('Damaged production proof accepted')
            result['production_damaged_proofs_rejected']=2
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--checker',type=Path)
    parser.add_argument('--production-cnf',type=Path);parser.add_argument('--production-lrat',type=Path)
    args=parser.parse_args();result={**orbit_controls(),**model_controls()}
    if args.checker:result.update(proof_controls(args.checker,args.production_cnf,args.production_lrat))
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
