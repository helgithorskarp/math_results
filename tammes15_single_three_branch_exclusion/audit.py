"""Separate original-label audit. Production invoked only to supply an
untrusted, hash-guarded comparison trace; no production functions imported.
Independent review and formalization pending; same author.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
import audit_contact,audit_noncontact
ROOT=Path(__file__).resolve().parent

def serialized(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def component_bytes(rows):
    # Restore depth integers before serialization: the original enumerator
    # sorts integer depths numerically, whereas JSON object keys are strings.
    for row in rows:
        for field in ('passing_counts','passing_partitions_by_depth'):
            row['cover'][field]={int(k):v for k,v in row['cover'][field].items()}
    return serialized(rows)

def run(path):
    deps=json.loads((ROOT/'DEPENDENCIES.json').read_text())
    for name,meta in deps['files'].items():
        data=(ROOT.parent/name).read_bytes()
        if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:
            raise RuntimeError('Prior PUBLIC dependency changed: '+name)
    expected=json.loads((ROOT/'EXPECTED.json').read_text())
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=expected['combined_trace_sha256']:
        raise RuntimeError('Regenerated comparison trace differs')
    trace=json.loads(data)
    c=audit_contact.run(component_bytes(trace['contact']))
    n=audit_noncontact.run(component_bytes(trace['noncontact']),trace['noncontact_terminal_obstructions'])
    if n['terminal_obstructions']!=expected['noncontact']['terminal_obstructions']:
        raise RuntimeError('Independent final obstructions differ from compact result')
    collar=ROOT.parent/'tammes15_nine_quad_single_three_fan_reduction'
    result=subprocess.run([sys.executable,'-B',str(collar/'audit.py')],capture_output=True,timeout=45)
    if result.returncode or result.stdout!=(collar/'AUDIT_EXPECTED.json').read_bytes():
        raise RuntimeError('Imported7912 separate collar audit differs')
    covers=sum(c['counts'][k] for k in ('original_face','ordinary_strip_stars','forced_last_face'))
    covers+=sum(n['counts'][k] for k in ('original_face','ordinary_L_star','forced_last_face'))
    boundaries=c['counts']['entrywise_compared_boundaries']+n['counts']['entrywise_compared_boundaries']
    if covers!=448 or boundaries!=1626:
        raise RuntimeError('Complete audit totals differ')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'SEPARATE_SAME_AUTHOR_ALL_ORIGINAL_BRANCH_BOUNDARIES_AND_OBSTRUCTIONS_AUDITED',
            'contact':c,'noncontact':n,
            'all_448_covers_audited':covers==448,
            'all_1626_boundaries_compared_entrywise':boundaries==1626,
            'imported7912_separate_Bernstein_audit_replayed_exactly':True,
            'combined_trace_sha256':hashlib.sha256(data).hexdigest(),
            'scope':'No production schema/predicate/enumerator/forcing imports. Unformalized geometric/original-face bridges; independent mathematical review pending; no global Tammes15 bound.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--production-partitions',type=Path)
    args=parser.parse_args()
    if args.production_partitions:result=run(args.production_partitions)
    else:
        with tempfile.TemporaryDirectory(prefix='tammes15-single-three-') as folder:
            path=Path(folder)/'partitions.json'
            subprocess.run([sys.executable,'-B',str(ROOT/'check.py'),'--export-partitions',str(path)],
                           capture_output=True,check=True,timeout=45)
            result=run(path)
    if json.loads(serialized(result))!=json.loads((ROOT/'AUDIT_EXPECTED.json').read_text()):
        raise RuntimeError('Result differs from AUDIT_EXPECTED.json')
    print(serialized(result).decode(),end='')
