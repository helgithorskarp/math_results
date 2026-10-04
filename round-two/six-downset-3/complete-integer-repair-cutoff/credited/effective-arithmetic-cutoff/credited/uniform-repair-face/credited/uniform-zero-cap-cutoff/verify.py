"""Exact complete proof phases, including repaired-hash semantic damages."""
from pathlib import Path
import sourcecheck
SOURCE=sourcecheck.check_bundle()
from copy import deepcopy
from fractions import Fraction as F
import json,sys,subprocess,tempfile,shutil,hashlib
import cap
import portable_frame as frame
import portable_fields as fields
import portable_minors as minors
import lower_branch as branch
import original_binding as original
import lower_checks as lower
import coefficient_checks as coefficient

HERE=Path(__file__).resolve().parent
PHASES=('uniform','zero-fields','coefficients','frame','fields','branch',
        'original','lower-structure','baseline','minor1','minor2','minor3',
        'damage','coefficient-damage','source-damage','recover7','recover19','recover100')


def damage():
    raw=frame.generated()|fields.generated()
    bad=[]
    def rejection(label,fn):
        try:fn()
        except ValueError:bad.append(label)
        else:raise ValueError('Accepted semantic damage: '+label)
    value=deepcopy(raw)
    value['complete_full11_gram4'][0][0][0][1]=str(F(value['complete_full11_gram4'][0][0][0][1])+1)
    rejection('whole original full11 coefficient changed',lambda:frame.verify(value))
    value=deepcopy(raw)
    value['complete_seven_solve_adjugate_action'][0][0][0][1]=str(F(value['complete_seven_solve_adjugate_action'][0][0][0][1])+1)
    rejection('one entire seven solve coefficient changed',lambda:frame.verify(value))
    value=deepcopy(raw)
    value['complete_four_short_numerator'][0][3][0][1]=str(F(value['complete_four_short_numerator'][0][3][0][1])+1)
    rejection('one original target normalization coefficient changed',lambda:frame.verify(value))
    value=deepcopy(raw)
    value['complete_seven_determinant'][0][1]=str(F(value['complete_seven_determinant'][0][1])+1)
    rejection('one entire determinant coefficient changed',lambda:frame.verify(value))
    value=deepcopy(raw)
    value['nu_U']['numerator'][0][1]=str(F(value['nu_U']['numerator'][0][1])+1)
    rejection('standard cap field coefficient changed',lambda:fields.fields(value))
    value=deepcopy(raw)
    value['a0']['denominator'][0][1]=str(F(value['a0']['denominator'][0][1])+1)
    rejection('lower deletion count denominator changed',lambda:fields.fields(value))
    rejection('duplicate monomial powers',lambda:frame.decode([[[1,0],'1'],[[1,0],'2']]))
    rejection('spurious noncanonical zero entry',lambda:frame.decode([[[1,0],'0']]))
    rejection('fractional monomial exponent',lambda:frame.decode([[[F(1,2),0],'1']]))
    rejection('inexact quotient coefficient',lambda:minors.divide({(1,0):1},{(1,0):2}))
    rejection('whole polynomial nondivisibility',lambda:minors.divide({(1,0):1,(0,0):1},{(1,0):1}))
    rejection('changed leading principal minor order',lambda:minors.numerator(minors.data(),4))
    cap.require(minors.z.surd_sign(180,-68)>0 and minors.z.surd_sign(749,-304)<0,
                'entire positive and negative quadratic-field controls')
    cap.require(minors.divide({(2,0):2,(1,0):2},{(1,0):1})=={(1,0):2,(0,0):2},
                'entire valid exact integer polynomial division control')
    return {'rejections':bad,'semantic_rejection_count':len(bad),
            'valid_controls_pass':True,'checks_active_in_optimized_mode':True,
            'generated_transcript_damage_checked_mathematically':True}


def source_damage():
    records=[]
    cases=(('unrepaired altered full source','cap.py',False),
           ('changed credited literal despite repaired outer hash','ancestral/small-deletion-boundary/literal.py',True),
           ('changed credited forms despite repaired outer hash','ancestral/core-edge-six-cutoff/forms.py',True),
           ('changed defining input closure despite repaired outer hash','ancestral/core-edge-six-cutoff/INPUTS.json',True))
    for label,target,repair in cases:
        with tempfile.TemporaryDirectory(prefix='zero-cap-damage-') as name:
            dest=Path(name)/'bundle'
            shutil.copytree(HERE,dest,ignore=shutil.ignore_patterns('work','__pycache__','*.pyc'))
            path=dest/target
            path.write_bytes(path.read_bytes()+b'\n')
            if repair:
                lines=[]
                for line in (dest/'SHA256SUMS').read_text().splitlines():
                    value,relative=line.split('  ',1)
                    if relative==target:value=hashlib.sha256(path.read_bytes()).hexdigest()
                    lines.append(value+'  '+relative)
                (dest/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
                sourcecheck.check_bundle(dest)
            command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(dest/'verify.py'),'--phase','fields','--out',str(dest/'work/result.json')]
            run=subprocess.run(command,cwd=dest,capture_output=True,text=True,timeout=10)
            cap.require(run.returncode!=0,'changed source closure rejected before mathematical use')
            reason=run.stderr.splitlines()[-1]
            cap.require('ValueError:' in reason,'intended input rejection rather than missing path')
            records.append({'name':label,'repaired_outer_hash':repair,'rejected':True,'reason':reason})
    return {'records':records,'source_rejection_count':len(records),
            'delivery_hash_alone_is_not_mathematical_validation':True}


def verify(phase):
    if phase=='uniform':return lower.uniform()
    if phase=='zero-fields':return cap.v.z.verify()
    if phase=='coefficients':return coefficient.coefficients()
    if phase=='frame':return frame.verify()
    if phase=='fields':return fields.fields()
    if phase=='branch':return branch.verify()
    if phase=='original':return [original.verify(q,k) for q,k in ((9,3),(12,4),(21,7))]
    if phase=='lower-structure':return [lower.coupled(9,3),lower.coupled(21,7)]
    if phase=='baseline':return {'published9826_positive_controls':[lower.positive(22),lower.positive(23)],'published9826_joint_q21':lower.joint()}
    if phase=='damage':return damage()
    if phase=='coefficient-damage':return coefficient.damages()
    if phase=='source-damage':return source_damage()
    if phase.startswith('minor'):return minors.verify(int(phase[-1]),True)
    if phase.startswith('recover'):
        k=int(phase[7:]);q=minors.z.cutoff(k)
        value=cap.v.verify_positive(q,k)
        cap.require(value['canonical_delta']==F(1,4),'whole canonical recovery uses proved uniform quarter branch')
        actual=cap.reduced(q,k,value['t'],value['sigma'])[0]
        cap.require(actual==value['canonical_even'],'ALL full permutation and original-counted cap recovery positions')
        return value
    raise ValueError('Unknown complete phase')


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=PHASES,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=verify(args.phase)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(cap.r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'phase':args.phase,'full_record_verified':True}))
