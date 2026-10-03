"""Freeze compact records only after every reconstructed stage passed."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE_FILES=['.gitignore','fixture.json','generate.py','verify.py','run.py','check_controls.py',
              'freeze.py','verify_certificate.py','PROOF.md','README.md','SOURCE-CREDITS.md','DEPENDENCIES.json']


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def main():
    records={}
    for name,path in [('result','result.json'),('producer','proposal.json'),
                      ('scalar','checked.json'),('controls','controls.json')]:
        record=json.loads((ROOT/'work'/path).read_text())
        if digest(record['finite'])!=record['finite_sha256']:
            raise ValueError('Complete reconstructed binding differs: '+name)
        records[name]=record['finite']
    if records['scalar']!=json.loads((ROOT/'work/checked-O.json').read_text())['finite']:
        raise ValueError('Complete normal/optimized scalar records differ')
    if (ROOT/'work/samples.json').read_bytes()!=(ROOT/'work/samples-O.json').read_bytes():
        raise ValueError('Complete normal/optimized illustrative records differ')
    if not records['result']['all16_semantic_rejections_pass'] or not records['result']['cold_source_only_complete']:
        raise ValueError('Incomplete actual cold/control result')
    sources=[]
    for name in SOURCE_FILES:
        raw=(ROOT/name).read_bytes();raw.decode('utf-8')
        sources.append({'path':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    manifest={'agent':'six-sorting-1','role':'researcher','schema':'compact-source-manifest-v1',
              'files':sources,'source_files':len(sources),'source_bytes':sum(x['bytes'] for x in sources)}
    (ROOT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    finite={'records':records,'whole_source_manifest_sha256':hashlib.sha256(
        (ROOT/'source-manifest.json').read_bytes()).hexdigest()}
    certificate={'agent':'six-sorting-1','role':'researcher','schema':'six-literal-route-conditional-cuts-v1',
                 'status':'SCOPED_AUTHOR_PROOF_INDEPENDENT_PERSON_REVIEW_PENDING',
                 'finite':finite,'finite_sha256':digest(finite)}
    (ROOT/'certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    (ROOT/'checks.json').write_bytes((ROOT/'work/result.json').read_bytes())
    print(json.dumps({'certificate_finite_sha256':certificate['finite_sha256'],
                      'result_finite_sha256':digest(records['result']),
                      'source_files':len(sources),'source_bytes':manifest['source_bytes']}))


if __name__=='__main__':main()
