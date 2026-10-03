"""Damaged source-only copies: ordinary and optimized entry points must reject."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import tempfile
import sourcecheck

HERE=Path(__file__).resolve().parent
SOURCE=sourcecheck.check_bundle(HERE)


def rewrite_outer(base):
    paths=sorted(p for p in base.rglob('*') if p.is_file() and p.relative_to(base).as_posix()!='SHA256SUMS')
    (base/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(base).as_posix()+'\n' for p in paths))


def damaged_sources():
    names=[line.split('  ',1)[1] for line in (HERE/'SHA256SUMS').read_text().splitlines()]+['SHA256SUMS']
    rejected=[]
    def trial(label,mutate,heal_outer=False):
        work=HERE/'work';work.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='source-damage-',dir=work) as temporary:
            base=Path(temporary)
            for name in names:
                target=base/name;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(HERE/name,target)
            mutate(base)
            if heal_outer:rewrite_outer(base)
            try:sourcecheck.check_bundle(base)
            except (ValueError,FileNotFoundError,UnicodeDecodeError):
                rejected.append(label)
            else:
                raise ValueError('accepted damaged source closure: '+label)
    old=sourcecheck.ANCESTOR
    helper=old+'/ancestral/core-edge-six-cutoff/original_checks.py'
    exact=old+'/ancestral/triangle-majority/exact.py'
    def append(base,name):
        p=base/name;p.write_bytes(p.read_bytes()+b'\n# damaged\n')
    trial('missing exact certificate',lambda b:(b/'CERTIFICATE.json').unlink())
    trial('changed exact certificate',lambda b:append(b,'CERTIFICATE.json'))
    trial('changed new mathematical reader',lambda b:append(b,'verify.py'))
    trial('unexpected unmanifested executable',lambda b:(b/'extra.py').write_text('raise ValueError()\n'))
    trial('changed credited original literal decoder',lambda b:append(b,helper))
    trial('changed original independent PSD decoder',lambda b:append(b,exact))
    trial('certificate damage with outer manifest repaired',lambda b:append(b,'CERTIFICATE.json'),True)
    trial('credited decoder damage with outer manifest repaired',lambda b:append(b,helper),True)
    trial('credited manifest omitted source with outer manifest repaired',
          lambda b:(b/old/'SHA256SUMS').write_text('\n'.join((b/old/'SHA256SUMS').read_text().splitlines()[:-1])+'\n'),True)
    def heal_inner(base):
        append(base,helper)
        p=base/old/'SHA256SUMS';lines=p.read_text().splitlines();target='ancestral/core-edge-six-cutoff/original_checks.py'
        p.write_text('\n'.join(hashlib.sha256((base/old/target).read_bytes()).hexdigest()+'  '+target
                             if line.split('  ',1)[1]==target else line for line in lines)+'\n')
    trial('credited decoder and inner manifest both repaired, immutable pin retained',heal_inner,True)
    trial('duplicate manifest path',lambda b:append_duplicate(b))
    trial('parent escape in manifest',lambda b:(b/'SHA256SUMS').write_text('0'*64+'  ../escape.py\n'))
    trial('omitted source from outer manifest',lambda b:(b/'SHA256SUMS').write_text('\n'.join((b/'SHA256SUMS').read_text().splitlines()[:-1])+'\n'))
    trial('source symlink to external path',lambda b:(b/'external.py').symlink_to('/dev/null'))
    return {'actual_agent':'six-downset-3','role':'researcher','count':len(rejected),
            'all_source_damages_rejected':rejected,'source_gate':SOURCE,
            'scope':'integrity controls; repository commit and checker remain the code trust boundary'}


def append_duplicate(base):
    p=base/'SHA256SUMS';lines=p.read_text().splitlines();p.write_text('\n'.join(lines+[lines[0]])+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=damaged_sources();raw=(json.dumps(value,sort_keys=True,indent=2)+'\n').encode();args.out.write_bytes(raw)
    print(json.dumps({'all_source_damages_rejected':value['count'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
