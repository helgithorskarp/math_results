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
import audit as audit

ENV = dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
           BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')

def main(work,output):
    began = time.monotonic();dependency = pins()
    require(not output.exists(),'fresh guard output required');output.mkdir(parents=True)
    models = json.loads((work/'models.json').read_text());slots,supports = audit.literal_field()
    tests = []
    # Compute each physical reference once through the full independent
    # literal-field/counter/rule auditor. Repeated damage probes compare
    # whole rows and whole metadata with this audited reference; the
    # producer supplies neither a trusted clause set nor a trusted record.
    references={}
    for original in models['records'][:2]:
        cnf=work/(original['stem']+'.cnf')
        audit.audit_case(original,cnf,slots,supports)
        references[original['stem']]=(copy.deepcopy(original),cnf.read_text())
    def cached_whole_damage_check(record,cnf):
        require(record['stem'] in references,'unknown damage reference head')
        original,text=references[record['stem']]
        expected=copy.deepcopy(original);expected['cnf_sha256']=sha(cnf)
        require(record==expected,'changed full independently audited metadata')
        expected_lines=text.splitlines();lines=cnf.read_text().splitlines()
        require(lines and lines[0].split()==expected_lines[0].split(),'changed complete DIMACS header')
        def rows(values):
            result=[]
            for line in values[1:]:
                values=list(map(int,line.split()))
                require(values and values[-1]==0 and all(1<=abs(v)<=original['variables'] for v in values[:-1]),
                        'invalid damage physical row')
                result.append(tuple(sorted(values[:-1])))
            return audit.Counter(result)
        require(rows(lines)==rows(expected_lines),'changed whole independently audited physical CNF multiset')
    def rejected(label,record,text):
        cnf = output/'damaged.cnf';cnf.write_text(text)
        record['cnf_sha256'] = sha(cnf)
        try:
            cached_whole_damage_check(record,cnf)
        except ValueError:
            tests.append(label);return
        raise ValueError('semantic damage accepted: '+label)
    def change(label,function,index=0):
        record = copy.deepcopy(models['records'][index]);function(record)
        rejected(label,record,(work/(models['records'][index]['stem']+'.cnf')).read_text())
    for label,function in [
        ('wrong-selected-count',lambda r:r.update(selected_phase_count=10)),
        ('wrong-phase-K',lambda r:r.update(phase_K=10)),
        ('wrong-maximum-gap',lambda r:r.update(maximum_background_gap=6)),
        ('wrong-next-selected',lambda r:r.update(next_selected=7)),
        ('wrong-background-b0',lambda r:r.update(background=1)),
        ('wrong-fixed-head',lambda r:r['fixed_phase_positions'].__setitem__('1',1)),
        ('missing-fixed-background-after-selected',lambda r:r['fixed_phase_positions'].pop('6')),
        ('missing-free-phase',lambda r:r['free_phase_indices'].pop()),
        ('wrong-free-count',lambda r:r.update(free_selected_count=8)),
        ('wrong-counter-levels',lambda r:r.update(counter_levels=9)),
        ('wrong-anchor-count',lambda r:r.update(selected_anchor_count=3)),
        ('wrong-normalized-pair',lambda r:r.update(normalized_selected_pair=[0,7])),
        ('wrong-minimum-pair-start',lambda r:r.update(minimum_pair_start=23)),
        ('wrong-minimum-pair-endpoints',lambda r:r.update(minimum_pair_selected_positions=[22,25])),
        ('wrong-minimum-pair-neighbors',lambda r:r.update(minimum_pair_background_positions=[21,23,26])),
        ('minimum-pair-declared-universal',lambda r:r.update(minimum_pair_rule_is_universal=True)),
        ('missing-conditional-minimum-pair',lambda r:r.update(conditional_minimum_pair_head=False)),
        ('identified-lower-orientations',lambda r:r.update(lower_orientation_variables=11)),
        ('wrong-minimum-distance',lambda r:r.update(minimum_selected_distance_at_least=3)),
        ('missing-conditional-isolation',lambda r:r.update(conditional_all_selected_isolated=False)),
        ('conditional-isolation-made-universal',lambda r:r.update(isolation_rule_is_universal=True)),
        ('missing-max-gap-normalization',lambda r:r.update(maximum_gap_normalization=False)),
        ('false-global-max-gap-rule',lambda r:r.update(maximum_gap_rule_is_global_phase_restriction=True)),
        ('false-next-background',lambda r:r.update(next_phase_after_selected_fixed_background=False)),
        ('false-gauge-flag',lambda r:r.update(only_global_y0_zero=False)),
        ('missing-root3',lambda r:r.update(root3_color_cut=False)),
        ('missing-root57',lambda r:r.update(root57_color_cut=False)),
        ('missing-phase8',lambda r:r.update(nonconstant_phase8_cut=False)),
        ('transferred-exact-TEN-rule',lambda r:r.update(exact_TEN_rules_used=True)),
        ('proposed-ELEVEN-exclusion',lambda r:r.update(proposed_ELEVEN_exclusion_used=True)),
        ('close-pair-refutation-used-as-native-cut',lambda r:r.update(gap_four_lemma_used_as_unconditional_native_cut=True)),
        ('unpublished-exclusion-premise',lambda r:r.update(unpublished_exclusion_used_as_input=True)),
        ('unrelated-family-cut',lambda r:r.update(unrelated_family_cut=True)),
        ('wrong-premise-ref',lambda r:r.update(premise_ref='changed')),
        ('wrong-premise-source',lambda r:r.update(source_commit='changed')),
    ]:
        change(label,function)
    change('wrong-background-b1',lambda r:r.update(background=0),1)
    for index in (0,1):
        original=models['records'][index]
        lines=(work/(original['stem']+'.cnf')).read_text().splitlines()
        m,b=original['next_selected'],original['background']
        fixed=audit.head_fixed(m,b);free=[i for i in range(44) if i not in fixed];n=len(free)
        kinds,_=audit.rules(fixed,free,b,m);outside=kinds['isolation'];windows=kinds['maxgap']
        parsed=[tuple(sorted(map(int,row.split()[:-1]))) for row in lines[1:]]
        counter_unit=next(j for j,row in enumerate(parsed,1) if len(row)==1 and abs(row[0])>44+2*n)
        gate=next(j for j,row in enumerate(parsed,1) if len(row)>1 and max(map(abs,row))>44+2*n)
        exterior=next(j for j,row in enumerate(parsed,1) if row in outside and len(row)==2)
        window=next(j for j,row in enumerate(parsed,1) if row in windows and len(row)>2)
        for label,j in [('removed-field',next(j for j,row in enumerate(parsed,1) if len(row)>3 and max(map(abs,row))<=44+n)),
                        ('removed-conditional-isolation',exterior),('removed-max-gap-window',window),('removed-counter-unit',counter_unit),('removed-counter-gate',gate)]:
            record=copy.deepcopy(original);bad=lines[:j]+lines[j+1:];record['clauses']-=1
            bad[0]=f'p cnf {record["variables"]} {record["clauses"]}'
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')
        for label,j in [('reversed-conditional-isolation',exterior),('reversed-max-gap-window',window),('reversed-counter-gate',gate),('reversed-field-sign',1)]:
            record=copy.deepcopy(original);bad=lines.copy();values=list(map(int,bad[j].split()))
            values[0]=-values[0];bad[j]=' '.join(map(str,values))
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')
        record=copy.deepcopy(original);bad=lines.copy();bad[-1]='1 0'
        rejected('reversed-color-gauge-b'+str(index),record,'\n'.join(bad)+'\n')
        record=copy.deepcopy(original);bad=lines.copy()+['0'];record['clauses']+=1
        bad[0]=f'p cnf {record["variables"]} {record["clauses"]}'
        rejected('proposed-global-empty-clause-b'+str(index),record,'\n'.join(bad)+'\n')
    for index in (0,1):
        original=models['records'][index]
        lines=(work/(original['stem']+'.cnf')).read_text().splitlines()
        for label,row in [('unjustified-orientation-period','1 -5 0'),('duplicate-field-clause',lines[-2])]:
            record=copy.deepcopy(original);bad=lines+[row];record['clauses']+=1
            bad[0]=f'p cnf {record["variables"]} {record["clauses"]}'
            rejected(label+'-b'+str(index),record,'\n'.join(bad)+'\n')
    record=copy.deepcopy(models['records'][0]);record['clauses']+=1
    lines=(work/(record['stem']+'.cnf')).read_text().splitlines()+['2 0']
    lines[0]=f'p cnf {record["variables"]} {record["clauses"]}'
    rejected('unjustified-lower-color-unit',record,'\n'.join(lines)+'\n')

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
                manifest.write_text(''.join((sha(path)+'  '+path.name if row.endswith('  '+path.name) else row)+'\n'
                    for row in original_manifest.splitlines()))
            p=subprocess.run([str(python),*flags,str(isolated/'common.py')],capture_output=True,text=True,env=ENV,timeout=10)
            require(p.returncode!=0 and 'ValueError' in p.stderr,'source/provenance damage accepted: '+label)
            tests.append(label)
        finally:path.write_bytes(before);manifest.write_text(original_manifest)
    producer=isolated/'generate.py'
    import_rejected('changed-current-producer-before-execution',producer,producer.read_bytes()+b'#changed\n')
    helper=isolated.parent/'order7-geometric-cut/encode.py'
    import_rejected('changed-field-helper-before-execution',helper,helper.read_bytes()+b'#changed\n')
    premise=isolated/'SOURCE_PINS.json'
    for label,key,value in [('changed-parent-identity-with-repaired-manifest','premise','changed'),
        ('transferred-TEN-rule-with-repaired-manifest','exact_TEN_rules_used',True),
        ('conditional-isolation-declared-universal-with-repaired-manifest','isolation_rule_is_universal',True),
        ('identified-orientations-with-repaired-manifest','all_44_lower_orientations_retained',False),
        ('minimum-pair-declared-universal-with-repaired-manifest','minimum_pair_rule_is_universal',True),
        ('missing-conditional-max4-with-repaired-manifest','conditional_maximum_gap_four',False),
        ('missing-conditional-minimum-pair-with-repaired-manifest','minimum_pair_heads_conditional',False),
        ('missing-minimum-pair-domain-with-repaired-manifest','minimum_pair_starts',[])]:
        data=json.loads(premise.read_text())
        if key=='premise':data['premise']['artifact_ref']=value
        else:data[key]=value
        import_rejected(label,premise,(json.dumps(data,indent=2)+'\n').encode(),True)

    cover = output/'damaged-cover';cover.mkdir()
    for original in models['records']:
        shutil.copyfile(work/(original['stem']+'.cnf'),cover/(original['stem']+'.cnf'))
    for label,indices in [('missing-background-head',[1]),('missing-minimum-pair-head',[6,7])]:
        damaged = copy.deepcopy(models)
        damaged['records'] = [r for j,r in enumerate(damaged['records']) if j not in indices]
        (cover/'models.json').write_text(json.dumps(damaged,indent=2)+'\n')
        p = subprocess.run([str(python),*flags,str(ROOT/'audit.py'),'--work',str(cover)],
                           capture_output=True,text=True,env=ENV,timeout=10)
        require(p.returncode != 0 and 'incomplete seventy-two conditional max4/min2 pair heads' in p.stderr,
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
    out = dict(agent='six-vdw-2',role='researcher',status='ELEVEN_GAP4_PAIRS_MODE_DAMAGES_REJECTED',
               tests=tests,positive_controls=positives,seconds=time.monotonic()-began)
    (output/'result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__ == '__main__':
    p = argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    main(args.work.absolute(),args.output.absolute())
