"""Meaningful full-model, gate/constant, source and strict-RUP controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import symbolic6_audit as audit
from symbolic6_common import BASE, PUBLIC, ROOT, pins, require, sha, write
from symbolic6_stage import ENV
from eleven_run6_six_operations import operations_check


def main(work,output):
    began=time.monotonic();old,new=pins();operations_check()
    require(not output.exists(),'partial/completed damage controls are frozen');output.mkdir(parents=True)
    produced=json.loads((work/'models.json').read_text());audit.validate_manifest(produced)
    slots,supports=audit.field();references={};groups={};rejected=[];positives=[]
    for record in produced['records']:
        cnf=work/(record['stem']+'.cnf');group=audit.components(record['background'],slots,supports)
        audit.audit_case(record,cnf,slots,supports,group)
        references[record['stem']]=(copy.deepcopy(record),audit.read_cnf(cnf));groups[record['stem']]=group
    def reject(label,function):
        try:function()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(label);return
        raise ValueError('damage accepted: '+label)
    def cached(record,cnf):
        original,rows=references[record['stem']]
        expected=copy.deepcopy(original);expected['cnf_sha256']=sha(cnf)
        require(record==expected,'changed whole independently derived metadata')
        require(audit.read_cnf(cnf)==rows,'changed entire independently checked signed physical CNF')
    def damaged(label,record,rows):
        cnf=output/'damaged.cnf'
        cnf.write_text('p cnf 348 %d\n'%len(rows)+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
        record['cnf_sha256']=sha(cnf);reject(label,lambda:cached(record,cnf))
    changes=[
        ('background',lambda r:r.update(background=1-r['background'])),
        ('phase-weight',lambda r:r.update(phase_K=12)),
        ('physical-dimension',lambda r:r.update(color_variables=44)),
        ('phase-dimension',lambda r:r.update(phase_variables=43)),
        ('counter-dimension',lambda r:r.update(counter_variables=215)),
        ('actual-AP-count',lambda r:r.update(literal_kept_APs=375759)),
        ('omitted-zero-count',lambda r:r.update(omitted_zero_APs=4311)),
        ('supports',lambda r:r.update(physical_supports=26487)),
        ('profile',lambda r:r.update(minority_profile=[6,2,1,1,1])),
        ('normalization',lambda r:r.update(normalized_minor_run=[1,2,3,4,5,6])),
        ('tail-first-position',lambda r:r['tail_positions'].__setitem__(0,6)),
        ('tail-cardinality',lambda r:r.update(tail_weight=4)),
        ('necessary-count',lambda r:r.update(necessary_phase_heads=1875)),
        ('foreign-gap-three-cut',lambda r:r.update(following_background_gap_cut=3,private_gap_cut=True)),
        ('unjustified-preceding-gap',lambda r:r.update(preceding_gap_cut=2)),
        ('palette-gauge-sign',lambda r:r.update(palette_gauge=[[1]])),
        ('extra-color-gauge',lambda r:r.update(palette_gauge=[[-1],[-2]])),
        ('field-zero-alias',lambda r:r.update(color_zero_is_coset_of_one=False)),
        ('constant-boundary-alias',lambda r:r.update(threshold_definition='S(0,t)=Y0')),
        ('foreign-premise',lambda r:r['numerical_premises'].append(10133)),
        ('circular-classification-cut',lambda r:r.update(ordinary_classification_numerical_cut=True)),
        ('source-commit',lambda r:r.update(source_commit='changed')),
        ('unsupported-negative',lambda r:r.update(mathematical_exclusion=True)),
        ('extra-metadata',lambda r:r.update(extra_cut=True)),
    ]
    for record in produced['records']:
        original,rows=references[record['stem']];label_end='-b%d'%record['background']
        for label,modify in changes:
            bad=copy.deepcopy(original);modify(bad);damaged(label+label_end,bad,rows)
        for name,group in groups[record['stem']].items():
            index=next(i for i,row in enumerate(rows) if row in group)
            bad=copy.deepcopy(original);bad['clauses']-=1
            damaged('remove-'+name+label_end,bad,rows[:index]+rows[index+1:])
            changed=list(rows[index]);changed[0]=-changed[0]
            damaged('sign-'+name+label_end,copy.deepcopy(original),rows[:index]+[tuple(sorted(changed))]+rows[index+1:])
        for label,extra in [('empty',()),('extra-unit',(2,)),('color-identification',(-2,5)),
                            ('duplicate-field',next(iter(groups[record['stem']]['field']))),
                            ('counter-initial-color-alias',(-1,133)),('foreign-following-gap-cut',(-96,))]:
            bad=copy.deepcopy(original);bad['clauses']+=1;damaged(label+label_end,bad,rows+[extra])
        for name in groups[record['stem']]:
            bad=copy.deepcopy(original);bad['component_counts'][name]+=1
            damaged('component-count-'+name+label_end,bad,rows)
    for label,modify in [('missing-model',lambda d:d['records'].pop()),
                          ('model-order',lambda d:d['records'].reverse()),
                          ('duplicate-model',lambda d:d['records'].__setitem__(1,copy.deepcopy(d['records'][0]))),
                          ('wrong-cover',lambda d:d.update(covered_necessary_phase_heads=3542)),
                          ('wrong-producer',lambda d:d.update(producer_sha256='changed')),
                          ('false-status',lambda d:d.update(status='EXACT')),
                          ('foreign-manifest-field',lambda d:d.update(extra_cut=True))]:
        bad=copy.deepcopy(produced);modify(bad);reject(label,lambda: audit.validate_manifest(bad))
    gate,xor=audit.gate_controls();constant_controls=0
    # Boundary constants and literal signs are independently exercised on every local row.
    for a,c,sign in itertools.product((False,True,2),(False,True,4),(-1,1)):
        clauses=[audit.substitute(row,[1,a,sign*3,c]) for row in gate]
        for bits in itertools.product((False,True),repeat=4):
            value=lambda v: v if type(v) is bool else (bits[abs(v)-1] if v>0 else not bits[abs(v)-1])
            actual=all(row is None or any(bits[abs(v)-1]==(v>0) for v in row) for row in clauses)
            require(actual==(bits[0]==(value(a) or (value(sign*3) and value(c)))),'typed boundary truth row failed')
            constant_controls+=1
    require(constant_controls==288,'constant boundary coverage differs')
    for label,bad in [('missing-counter-prime',gate[:-1]),('wrong-counter-sign',[tuple(-v for v in gate[0])]+gate[1:])]:
        reject(label,lambda bad=bad:require(all(
            all(any(bits[abs(v)-1]==(v>0) for v in row) for row in bad)
            ==(bits[0]==(bits[1] or (bits[2] and bits[3])))
            for bits in itertools.product((False,True),repeat=4)), 'altered gate has wrong semantics'))
    isolated=output/'source-isolated';isolated.mkdir()
    for category,directory,target in [('published_files',PUBLIC,isolated/'credited'),
                                     ('private_files',ROOT,isolated),('provenance_files',ROOT,isolated)]:
        for name in old[category]:
            dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(directory/name,dest)
    for name in list(new['files'])+['symbolic6-source-pins.json','symbolic6-freeze.json']:
        dest=isolated/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
    python=Path(sys.executable).absolute();flags=[] if __debug__ else ['-O']
    for label,path in [('new-producer',isolated/'symbolic6_generate.py'),
                       ('new-auditor',isolated/'symbolic6_audit.py'),
                       ('public-physical',isolated/'credited/encode.py'),
                       ('source-provenance',isolated/'CREDITED_SOURCES.json')]:
        operations_check();raw=path.read_bytes();path.write_bytes(raw+b'changed\n')
        try:
            child=subprocess.run([python,*flags,isolated/'symbolic6_common.py'],capture_output=True,text=True,env=ENV,timeout=10)
            require(child.returncode!=0 and 'ValueError' in child.stderr,'pre-import source damage accepted: '+label)
            rejected.append('pre-import-'+label)
        finally:path.write_bytes(raw)
    cnf=output/'control.cnf';cnf.write_text('p cnf 1 2\n1 0\n-1 0\n');proof=output/'control.lrat'
    for label,text,wanted in [('valid','3 0 1 2 0\n',True),('unknown-hint','3 0 1 8 0\n',False),
        ('deleted-hint','3 d 1 0\n4 0 1 2 0\n',False),('no-conflict','3 0 1 0\n',False),
        ('no-empty','3 1 0 1 0\n',False),('RAT-hint','3 0 -1 2 0\n',False),('stale-id','2 0 1 2 0\n',False)]:
        operations_check();pins();proof.write_text(text)
        child=subprocess.run([python,*flags,BASE/'check_rup_lrat.py',cnf,proof],capture_output=True,text=True,env=ENV,timeout=10)
        require((child.returncode==0)==wanted,'RUP control differs: '+label);checked=json.loads(child.stdout)
        if wanted:
            require(checked['status']=='EXACT_RUP_LRAT_VERIFIED' and checked['checked_additions']==1
                    and checked['propagation_hints_checked']==2,'positive RUP counts differ');positives.append(label)
        else:
            require(checked['status']=='REJECTED','RUP damage not explicitly rejected');rejected.append('RUP-'+label)
    require(len(rejected)==len(set(rejected)),'duplicate controls')
    result=dict(agent='six-vdw-2',role='researcher',status='ALL_SYMBOLIC_PHYSICAL_GATE_SOURCE_RUP_DAMAGES_REJECTED',
        rejected=rejected,positive_controls=positives,typed_boundary_truth_rows=constant_controls,
        full_physical_models_prechecked=2,mathematical_exclusion=False)
    write(output/'result.json',result)
    print(json.dumps(dict(status=result['status'],rejected=len(rejected),positive_controls=len(positives),
                         receipt_sha256=sha(output/'result.json'),seconds=time.monotonic()-began),sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();main(args.work.absolute(),args.output.absolute())
