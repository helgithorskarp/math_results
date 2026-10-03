"""Reject fixed-phase, orientation, coverage, whole-premise/source and RUP damages."""
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
import audit3 as audit

ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def main(work,output):
    began=time.monotonic();dependency=pins()
    require(not output.exists(),'fresh guard output required');output.mkdir(parents=True)
    models=json.loads((work/'models.json').read_text());slots,supports=audit.literal_field();tests=[]
    def rejected(label,record,text):
        cnf=output/'damaged.cnf';cnf.write_text(text);record['cnf_sha256']=sha(cnf)
        try: audit.audit_case(record,cnf,slots,supports)
        except ValueError: tests.append(label);return
        raise ValueError('semantic damage accepted: '+label)
    def change(label,function,index=0):
        record=copy.deepcopy(models['records'][index]);function(record)
        rejected(label,record,(work/(models['records'][index]['stem']+'.cnf')).read_text())
    for label,function in [
        ('wrong-selected-count',lambda r:r.update(selected_phase_count=10)),
        ('wrong-phase-K',lambda r:r.update(phase_K=10)),
        ('wrong-background-b0',lambda r:r.update(background=1)),
        ('wrong-minimum-distance',lambda r:r.update(minimum_selected_distance=2)),
        ('wrong-fixed-phase',lambda r:r['fixed_phase_positions'].__setitem__('1',1)),
        ('missing-outer-fixed-background',lambda r:r['fixed_phase_positions'].pop('43')),
        ('missing-free-phase',lambda r:r['free_phase_indices'].pop()),
        ('wrong-free-count',lambda r:r.update(free_selected_count=8)),
        ('wrong-anchor-count',lambda r:r.update(selected_anchor_count=3)),
        ('wrong-counter-levels',lambda r:r.update(counter_levels=9)),
        ('wrong-normalized-pair',lambda r:r.update(normalized_selected_pair=[0,2])),
        ('identified-orientation-variables',lambda r:r.update(lower_orientation_variables=11)),
        ('missing-conditional-spacing',lambda r:r.update(conditional_minimum_distance_rule=False)),
        ('conditional-rule-declared-universal',lambda r:r.update(minimum_distance_rule_is_universal=True)),
        ('wrong-spacing-clause-count',lambda r:r.update(conditional_spacing_clauses=1)),
        ('transferred-exact-TEN-rule',lambda r:r.update(exact_TEN_rules_used=True)),
        ('unproved-ELEVEN-endpoint-input',lambda r:r.update(proposed_ELEVEN_exclusion_used=True)),
        ('regular-spacing-refutation-used-as-cut',lambda r:r.update(regular_spacing_exclusion_used_as_input=True)),
        ('false-gauge-flag',lambda r:r.update(only_global_y0_zero=False)),
        ('missing-root3',lambda r:r.update(root3_color_cut=False)),
        ('missing-root57',lambda r:r.update(root57_color_cut=False)),
        ('missing-phase8',lambda r:r.update(nonconstant_phase8_cut=False)),
        ('unpublished-exclusion-premise',lambda r:r.update(unpublished_exclusion_used_as_input=True)),
        ('unrelated-family-cut',lambda r:r.update(unrelated_family_cut=True)),
        ('wrong-premise-ref',lambda r:r.update(premise_ref='changed')),
        ('wrong-premise-source',lambda r:r.update(source_commit='changed')),
    ]:change(label,function)
    change('wrong-background-b1',lambda r:r.update(background=0),1)
    for index,original in enumerate(models['records']):
        lines=(work/(original['stem']+'.cnf')).read_text().splitlines()
        parsed=[tuple(map(int,line.split()[:-1])) for line in lines[1:]]
        field=next(j for j,row in enumerate(parsed,1) if len(row)>3 and max(map(abs,row))<=80)
        for label,j in [('removed-field',field),('removed-gauge',len(lines)-1)]:
            record=copy.deepcopy(original);bad=lines[:j]+lines[j+1:];record['clauses']-=1
            bad[0]=f'p cnf 431 {record["clauses"]}'
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')
        for label,j in [('reversed-field-sign',field),('reversed-color-gauge',len(lines)-1)]:
            record=copy.deepcopy(original);bad=lines.copy();values=list(map(int,bad[j].split()))
            values[0]=-values[0];bad[j]=' '.join(map(str,values))
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')
        for label,row in [('unjustified-orientation-period','1 -5 0'),('unjustified-empty-clause','0'),
                          ('duplicate-field-clause',lines[field])]:
            record=copy.deepcopy(original);bad=lines+[row];record['clauses']+=1
            bad[0]=f'p cnf 431 {record["clauses"]}'
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')

    for index,original in enumerate(models['records']):
        lines=(work/(original['stem']+'.cnf')).read_text().splitlines()
        parsed=[tuple(sorted(map(int,line.split()[:-1]))) for line in lines[1:]]
        fixed=audit.head_fixed(original['background']);free=original['free_phase_indices']
        spacing,_=audit.spacing_rows(fixed,free,original['background'])
        locations=[('conditional-spacing',next(j for j,row in enumerate(parsed,1) if row in spacing and len(row)==2)),
                   ('counter-unit',next(j for j,row in enumerate(parsed,1) if len(row)==1 and abs(row[0])>116)),
                   ('counter-gate',next(j for j,row in enumerate(parsed,1) if len(row)>1 and max(map(abs,row))>116))]
        for kind,j in locations:
            record=copy.deepcopy(original);bad=lines[:j]+lines[j+1:];record['clauses']-=1
            bad[0]=f'p cnf 431 {record["clauses"]}'
            rejected('removed-'+kind+'-b'+str(index),record,'\n'.join(bad)+'\n')
            record=copy.deepcopy(original);bad=lines.copy();values=list(map(int,bad[j].split()))
            values[0]=-values[0];bad[j]=' '.join(map(str,values))
            rejected('reversed-'+kind+'-b'+str(index),record,'\n'.join(bad)+'\n')

    isolated=output/'isolated';isolated.mkdir()
    for path in ROOT.iterdir():
        if path.is_file():shutil.copyfile(path,isolated/path.name)
    for name in dependency['relative_files']:
        target=isolated.parent/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT.parent/name,target)
    python=Path(sys.executable).absolute();flags=[] if __debug__ else ['-O']
    def import_rejected(label,path,data,repair_manifest=False):
        before=path.read_bytes();manifest=isolated/'SHA256SUMS';original_manifest=manifest.read_text()
        path.write_bytes(data)
        try:
            if repair_manifest:
                rows=original_manifest.splitlines()
                manifest.write_text(''.join((sha(path)+'  '+path.name if row.endswith('  '+path.name) else row)+'\n' for row in rows))
            p=subprocess.run([str(python),*flags,str(isolated/'common.py')],capture_output=True,text=True,env=ENV,timeout=10)
            require(p.returncode!=0 and 'ValueError' in p.stderr,'source/provenance damage accepted: '+label)
            tests.append(label)
        finally:path.write_bytes(before);manifest.write_text(original_manifest)
    producer=isolated/'generate3.py'
    import_rejected('changed-current-producer-before-execution',producer,producer.read_bytes()+b'#changed\n')
    helper=isolated.parent/'order7-geometric-cut/encode.py'
    import_rejected('changed-field-helper-before-execution',helper,helper.read_bytes()+b'#changed\n')
    premise=isolated/'SOURCE_PINS.json';data=json.loads(premise.read_text());data['premise']['artifact_ref']='changed'
    import_rejected('changed-parent-identity-with-repaired-manifest',premise,(json.dumps(data,indent=2)+'\n').encode(),True)
    for label,key,value in [('transferred-TEN-rule-with-repaired-manifest','exact_TEN_rules_used',True),
        ('conditional-spacing-declared-universal-with-repaired-manifest','minimum_distance_rule_is_universal',True),
        ('identified-orientations-with-repaired-manifest','all_44_lower_orientations_retained',False)]:
        data=json.loads(premise.read_text());data[key]=value
        import_rejected(label,premise,(json.dumps(data,indent=2)+'\n').encode(),True)

    cover=output/'damaged-cover';cover.mkdir()
    for original in models['records']:shutil.copyfile(work/(original['stem']+'.cnf'),cover/(original['stem']+'.cnf'))
    for label,indices in [('missing-background-b0',[1]),('missing-background-b1',[0]),('reversed-background-order',[1,0])]:
        damaged=copy.deepcopy(models);damaged['records']=[damaged['records'][j] for j in indices]
        (cover/'models.json').write_text(json.dumps(damaged,indent=2)+'\n')
        p=subprocess.run([str(python),*flags,str(ROOT/'audit3.py'),'--work',str(cover)],capture_output=True,text=True,env=ENV,timeout=10)
        require(p.returncode!=0 and 'incomplete two-background minimum-distance-three cover' in p.stderr,'cover damage accepted: '+label)
        tests.append(label)

    cnf=output/'control.cnf';cnf.write_text('p cnf 1 2\n1 0\n-1 0\n');proof=output/'control.lrat';positives=[]
    for label,rows,expected in [('valid','3 0 1 2 0\n',True),('unknown-hint','3 0 1 8 0\n',False),
        ('deleted-hint','3 d 1 0\n4 0 1 2 0\n',False),('no-contradiction','3 0 1 0\n',False),
        ('missing-empty','3 1 0 1 0\n',False)]:
        pins();proof.write_text(rows)
        p=subprocess.run([str(python),*flags,str(BASE/'check_rup_lrat.py'),str(cnf),str(proof)],capture_output=True,text=True,env=ENV,timeout=10)
        require((p.returncode==0)==expected,'strict RUP control failed: '+label)
        (positives if expected else tests).append('RUP-'+label)
    out=dict(agent='six-vdw-2',role='researcher',status='ELEVEN3_MODE_DAMAGES_REJECTED',
        tests=tests,positive_controls=positives,seconds=time.monotonic()-began)
    (output/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();main(args.work.absolute(),args.output.absolute())
