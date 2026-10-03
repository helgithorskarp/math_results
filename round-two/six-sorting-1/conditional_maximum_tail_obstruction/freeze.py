"""Bind compact cold result and defining evidence, excluding self manifests."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def main():
    result = json.loads((ROOT/'work/result.json').read_text())
    if digest(result['finite']) != result['finite_sha256']:
        raise ValueError('Complete result finite binding differs')
    n = json.loads((ROOT/'work/checked.json').read_text())
    o = json.loads((ROOT/'work/checked-O.json').read_text())
    if n['finite'] != o['finite'] or n['finite_sha256'] != o['finite_sha256']:
        raise ValueError('Full normal/O evidence differs')
    source = [{'path': p.name, 'bytes': p.stat().st_size,
               'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in sorted(ROOT.iterdir()) if p.is_file() and p.name not in
              ('certificate.json', 'source-manifest.json')]
    evidence = [{'path': 'work/'+name, 'bytes': (ROOT/'work'/name).stat().st_size,
                 'sha256': hashlib.sha256((ROOT/'work'/name).read_bytes()).hexdigest()}
                for name in ('proposal.json', 'checked.json', 'checked-O.json', 'controls.json', 'result.json')]
    manifest = {'agent': 'six-sorting-1', 'role': 'researcher', 'files': source,
                'files_sha256': digest(source), 'generated_evidence': evidence,
                'generated_evidence_sha256': digest(evidence)}
    certificate = {'agent': 'six-sorting-1', 'role': 'researcher',
                   'status': result['status'], 'finite': result['finite'],
                   'finite_sha256': result['finite_sha256'],
                   'source_manifest_files_sha256': manifest['files_sha256'],
                   'generated_evidence_sha256': manifest['generated_evidence_sha256'],
                   'python_version': result['python_version'],
                   'cold_serial_stages': result['stages'], 'cold_seconds': result['seconds'],
                   'statement': 'For arbitrary-length standard F on ports2/3/4/5/7/8, choose p in5/7/8 with F(24)[p]=0. Literal P28;F;(p,9);(6,10);(9,11);(10,11) has no standard size<=44 sorting completion.',
                   'external_person_review_claimed': False, 'formalized': False,
                   'large_external_lower_bound_corpus_reproved': False}
    (ROOT/'source-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (ROOT/'certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'finite_sha256': result['finite_sha256'],
                      'source_files': len(source), 'source_bytes': sum(r['bytes'] for r in source),
                      'cold_seconds': result['seconds']}), flush=True)


if __name__ == '__main__':
    main()
