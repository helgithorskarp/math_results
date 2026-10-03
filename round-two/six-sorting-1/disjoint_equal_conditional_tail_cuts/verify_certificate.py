"""Compare newly reconstructed entire records against the published certificate.

Uses no packed arithmetic, old corpus, graph, signing key or network. The
separate scalar mathematical reconstruction is performed by verify.py.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXPECTED_FILES={'.gitignore','fixture.json','generate.py','verify.py','run.py','check_controls.py',
                'freeze.py','verify_certificate.py','PROOF.md','README.md','SOURCE-CREDITS.md','DEPENDENCIES.json'}


def need(test,message):
    if not test:raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def main():
    certificate=json.loads((ROOT/'certificate.json').read_text())
    manifest_bytes=(ROOT/'source-manifest.json').read_bytes();manifest=json.loads(manifest_bytes)
    need(certificate['agent']=='six-sorting-1' and certificate['role']=='researcher' and
         certificate['schema']=='six-literal-route-conditional-cuts-v1' and
         certificate['status']=='SCOPED_AUTHOR_PROOF_INDEPENDENT_PERSON_REVIEW_PENDING',
         'Wrong certificate claim status')
    need(digest(certificate['finite'])==certificate['finite_sha256'],'Changed full certificate transport hash')
    need(certificate['finite']['whole_source_manifest_sha256']==hashlib.sha256(manifest_bytes).hexdigest(),
         'Changed source manifest binding')
    need(len(manifest['files'])==len(EXPECTED_FILES) and {r['path'] for r in manifest['files']}==EXPECTED_FILES,
         'Missing or substituted owned source')
    for row in manifest['files']:
        raw=(ROOT/row['path']).read_bytes()
        need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],
             'Owned source binding differs: '+row['path'])
    records={}
    for name,path in [('result','result.json'),('producer','proposal.json'),
                      ('scalar','checked.json'),('controls','controls.json')]:
        actual=json.loads((ROOT/'work'/path).read_text())
        need(digest(actual['finite'])==actual['finite_sha256'],'Changed actual reconstruction binding')
        records[name]=actual['finite']
        need(certificate['finite']['records'][name]==actual['finite'],'Whole mathematical record differs: '+name)
    need(records['scalar']==json.loads((ROOT/'work/checked-O.json').read_text())['finite'],
         'Whole normal/optimized scalar record differs')
    need((ROOT/'work/samples.json').read_bytes()==(ROOT/'work/samples-O.json').read_bytes(),
         'Whole normal/optimized illustrative record differs')
    need(json.loads((ROOT/'checks.json').read_text())['finite']==records['result'],
         'Published execution receipt mathematical record differs')
    need(records['result']['all16_semantic_rejections_pass'] and records['result']['cold_source_only_complete'],
         'Incomplete actual proof/control execution')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher',
                      'status':'ALL_FROZEN_SOURCES_AND_ENTIRE_RECONSTRUCTED_MATHEMATICAL_RECORDS_MATCH',
                      'certificate_finite_sha256':certificate['finite_sha256'],
                      'result_finite_sha256':digest(records['result']),
                      'source_files':len(manifest['files']),
                      'independent_person_review_claimed':False,'formalized':False}))


if __name__=='__main__':main()
