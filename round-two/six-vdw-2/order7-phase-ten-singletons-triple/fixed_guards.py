"""Definition, full signed premise, pre-import source and strict RUP damage controls."""
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from common import ROOT, BASE, SOURCE, pins, require, sha
import fixed_audit as audit

ENV = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def main(work,output):
    began = time.monotonic();dependency = pins()
    require(not output.exists(),'fresh guard output required');output.mkdir(parents=True)
    models = json.loads((work/'models.json').read_text());slots,supports = audit.literal_field()
    tests = []
    def rejected(label,record,text):
        cnf = output/'damaged.cnf';cnf.write_text(text)
        record['cnf_sha256'] = sha(cnf)
        try:
            audit.audit_case(record,cnf,slots,supports)
        except ValueError:
            tests.append(label);return
        raise ValueError('semantic damage accepted: '+label)
    def change(label,function,index=0):
        record = copy.deepcopy(models['records'][index]);function(record)
        rejected(label,record,(work/(models['records'][index]['stem']+'.cnf')).read_text())
    for label,function in [
        ('wrong-selected-count',lambda r:r.update(selected_phase_count=9)),
        ('wrong-phase-K',lambda r:r.update(phase_K=9)),
        ('wrong-gap-vector',lambda r:r['gaps'].__setitem__(0,7)),
        ('wrong-background-b0',lambda r:r.update(background=1)),
        ('wrong-selected-anchor',lambda r:r['selected'].__setitem__(5,6)),
        ('missing-fixed-phase',lambda r:r['phases'].pop()),
        ('swapped-fixed-phase',lambda r:r['phases'].__setitem__(12,0)),
        ('unfixed-phase',lambda r:r.update(all_phases_fixed=False)),
        ('extra-color-auxiliary',lambda r:r.update(color_auxiliaries=1)),
        ('extra-phase-auxiliary',lambda r:r.update(phase_auxiliaries=1)),
        ('extra-counter-auxiliary',lambda r:r.update(counter_auxiliaries=1)),
        ('false-gauge-flag',lambda r:r.update(only_global_y0_zero=False)),
        ('unjustified-reflection',lambda r:r.update(reflection_assumed=True)),
        ('unjustified-phase-exchange',lambda r:r.update(phase_exchange_assumed=True)),
        ('missing-TWO-check',lambda r:r.update(actual_TWO_checked=False)),
        ('missing-FOURTH4-check',lambda r:r.update(actual_FOURTH4_checked=False)),
        ('missing-phase8-check',lambda r:r.update(phase8_checked=False)),
        ('proposed-length6-exclusion',lambda r:r.update(proposed_length6_exclusion_cut=True)),
        ('proposed-no-adjacency',lambda r:r.update(proposed_no_adjacency_cut=True)),
        ('unrelated-family-cut',lambda r:r.update(unrelated_family_cut=True)),
        ('wrong-premise-ref',lambda r:r.update(premise_ref='changed')),
        ('wrong-premise-source',lambda r:r.update(source_commit='changed')),
    ]:
        change(label,function)
    change('wrong-background-b1',lambda r:r.update(background=0),1)
    for index in (0,1):
        original = models['records'][index];lines = (work/(original['stem']+'.cnf')).read_text().splitlines()
        record = copy.deepcopy(original);removed = lines[:1]+lines[2:];record['clauses'] -= 1
        removed[0] = f'p cnf 44 {record["clauses"]}'
        rejected('removed-field-b'+str(index),record,'\n'.join(removed)+'\n')
        record = copy.deepcopy(original);bad = lines.copy();bad[-1] = '1 0'
        rejected('reversed-color-gauge-b'+str(index),record,'\n'.join(bad)+'\n')
        record = copy.deepcopy(original);bad = lines.copy()+['0'];record['clauses'] += 1
        bad[0] = f'p cnf 44 {record["clauses"]}'
        rejected('proposed-length6-empty-clause-b'+str(index),record,'\n'.join(bad)+'\n')
        record = copy.deepcopy(original);bad = lines.copy()
        values = list(map(int,bad[1].split()))
        values[0] = -values[0];bad[1] = ' '.join(map(str,values))
        rejected('wrong-upper-sign-b'+str(index),record,'\n'.join(bad)+'\n')
    record = copy.deepcopy(models['records'][0]);record['clauses'] += 1
    lines = (work/(record['stem']+'.cnf')).read_text().splitlines()+['2 0']
    lines[0] = f'p cnf 44 {record["clauses"]}'
    rejected('unjustified-lower-color-unit',record,'\n'.join(lines)+'\n')

    isolated=output/'isolated';isolated.mkdir()
    for path in ROOT.iterdir():
        if path.is_file():shutil.copyfile(path,isolated/path.name)
    for name in dependency['relative_files']:
        target=isolated.parent/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT.parent/name,target)
    python=Path(sys.executable).absolute();flags=[] if __debug__ else ['-O']
    def import_rejected(label,path,data):
        before=path.read_bytes();path.write_bytes(data)
        try:
            p=subprocess.run([str(python),*flags,str(isolated/'common.py')],capture_output=True,text=True,env=ENV,timeout=10)
            require(p.returncode!=0 and 'ValueError' in p.stderr,'pre-import source damage accepted: '+label)
            tests.append(label)
        finally:path.write_bytes(before)
    producer=isolated/'fixed_generate.py'
    import_rejected('changed-current-producer-before-math',producer,producer.read_bytes()+b'#changed\n')
    helper=isolated.parent/'order7-geometric-cut/encode.py'
    import_rejected('changed-field-helper-before-math',helper,helper.read_bytes()+b'#changed\n')
    premise=isolated/'SOURCE_PINS.json'
    data=json.loads(premise.read_text());data['premise']['artifact_ref']='changed'
    import_rejected('changed-parent-identity-before-math',premise,(json.dumps(data,indent=2)+'\n').encode())

    cover = output/'damaged-cover';cover.mkdir()
    for original in models['records']:
        shutil.copyfile(work/(original['stem']+'.cnf'),cover/(original['stem']+'.cnf'))
    for label,indices in [('missing-background-head',[1]),('missing-gap-head',[8,9])]:
        damaged = copy.deepcopy(models)
        damaged['records'] = [r for j,r in enumerate(damaged['records']) if j not in indices]
        (cover/'models.json').write_text(json.dumps(damaged,indent=2)+'\n')
        p = subprocess.run([str(python),*flags,str(ROOT/'fixed_audit.py'),'--work',str(cover)],
                           capture_output=True,text=True,env=ENV,timeout=10)
        require(p.returncode != 0 and 'incomplete ten-head cover' in p.stderr,
                'incomplete whole-cover damage accepted: '+label)
        tests.append(label)

    cnf = output/'control.cnf';cnf.write_text('p cnf 1 2\n1 0\n-1 0\n')
    proof = output/'control.lrat';positives = []
    controls = [('valid','3 0 1 2 0\n',True),('unknown-hint','3 0 1 8 0\n',False),
                ('deleted-hint','3 d 1 0\n4 0 1 2 0\n',False),
                ('no-contradiction','3 0 1 0\n',False),('missing-empty','3 1 0 1 0\n',False)]
    for label,rows,expected in controls:
        pins();proof.write_text(rows)
        p = subprocess.run([str(python),*flags,str(BASE/'check_rup_lrat.py'),str(cnf),str(proof)],
                           capture_output=True,text=True,env=ENV,timeout=10)
        require((p.returncode == 0) == expected,'strict RUP control failed: '+label)
        (positives if expected else tests).append('RUP-'+label)
    out = dict(agent='six-vdw-2',role='researcher',status='LENGTH6_FIXED10_MODE_DAMAGES_REJECTED',
               tests=tests,positive_controls=positives,seconds=time.monotonic()-began)
    (output/'result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    main(args.work.absolute(),args.output.absolute())
