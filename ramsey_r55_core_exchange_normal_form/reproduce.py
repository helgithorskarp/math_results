"""Replay in fresh scratch. No solver, owner queue, or historical workspace access."""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from catalog import obtain
from census import inputs, global_bound
from check_pair import verify as verify_pair
from check_global import verify as verify_global
from controls import run as physical_controls
from interface_controls import check as interface_controls
from exchange import need
HERE=Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(argv, stdout=None):
    p=subprocess.run(list(map(str,argv)),capture_output=True)
    if stdout is not None: Path(stdout).write_bytes(p.stdout)
    need(p.returncode==0, 'command failed: '+p.stderr.decode(errors='replace'))
    return p.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--catalog');p.add_argument('--residual-counts');a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    for name,sha in json.loads((HERE/'DEPENDENCIES.json').read_text()).items():
        need(digest(HERE.parent/name)==sha,'dependency identity: '+name)
    data=Path(a.catalog).resolve() if a.catalog else out/'catalog';lines=obtain(data)
    residual=Path(a.residual_counts).resolve() if a.residual_counts else out/'residual'
    if not a.residual_counts:
        residual.mkdir()
        command(['g++','-std=c++20','-O3',HERE.parent/'ramsey_r55_maximal_residual_domains/produce.cpp','-o',out/'imported_residual_counter'])
        # Regenerate reviewed count files in this fresh scratch directory. Profiles are not needed.
        for n,rows in lines.items():
            command([out/'imported_residual_counter',n,data/f'r44_{n}.g6',0,len(rows),residual/f'{n}.tsv','/dev/null'],out/f'residual_{n}.log')
    _,_,keys=inputs(data);need(keys==json.loads((HERE/'KEYS.json').read_text()),'complete keys')
    input_bytes=''.join(f"{i} {k['n']} "+' '.join(map(str,k['degrees']))+'\n' for i,k in enumerate(keys)).encode()
    outputs=[]
    for name,flags in [('release',['-O3']),('sanitized',['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer'])]:
        binary=out/name
        command(['g++','-std=c++20','-Wall','-Wextra','-Wconversion','-Werror',*flags,HERE/'count_pair.cpp','-o',binary])
        r=subprocess.run([str(binary)],input=input_bytes,capture_output=True)
        need(r.returncode==0,'native '+name+': '+r.stderr.decode(errors='replace'))
        (out/(name+'.tsv')).write_bytes(r.stdout);outputs.append(r.stdout)
    need(outputs[0]==outputs[1]==(HERE/'COUNTS.tsv').read_bytes(),'native exact count identity')
    counts=[list(map(int,row.split())) for row in outputs[0].splitlines()]
    pair=verify_pair(keys,counts)
    result=global_bound(data,residual,keys,counts)
    expected=json.loads((HERE/'EXPECTED.json').read_text());need(result==expected,'whole result')
    global_check=verify_global(data,residual,result)
    physical,fixtures=physical_controls(data)
    need(physical==json.loads((HERE/'PHYSICAL_VALIDATION.json').read_text()),'physical expected')
    interfaces=interface_controls(data)
    need(interfaces==json.loads((HERE/'INTERFACE_VALIDATION.json').read_text()),'interface expected')
    # Controlled malformed finite certificates are rejected, with no second large census.
    rejected=0
    for column in (0,1,2):
        damaged=[row[:] for row in counts];damaged[0][column]+=1
        try:verify_pair(keys,damaged)
        except ValueError:rejected+=1
        else:raise ValueError('corrupt count accepted')
    need(rejected==3,'negative controls')
    packet=dict(status='REPRODUCED_GLOBAL_CORE_EXCHANGE_NORMAL_FORM',pair=pair,global_check=global_check,
                physical=physical,interfaces=interfaces,corrupt_count_files_rejected=rejected,expected_sha256=digest(HERE/'EXPECTED.json'),
                counts_sha256=digest(HERE/'COUNTS.tsv'),source_python=platform.python_version(),
                cxx=command(['g++','--version']).decode().splitlines()[0],seconds=time.monotonic()-start,
                catalogue_completeness='Imported',residual_census='Imported reviewed count values, hashes checked',
                new_original_task_decisions=0,target_found=False,external_review_of_this_result=False)
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    (out/'REPLAY.json').write_text(json.dumps(packet,sort_keys=True,indent=2)+'\n')
    (out/'FIXTURES.json').write_text(json.dumps(fixtures,sort_keys=True,indent=2)+'\n')
    print(json.dumps(packet,sort_keys=True))

if __name__=='__main__':main()
