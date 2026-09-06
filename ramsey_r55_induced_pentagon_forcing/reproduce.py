"""Regenerate compact evidence and replay independent checks."""
import hashlib
import json
from pathlib import Path
from build import certificate
from check import check
from controls import main, fixture
from extract import extract
from verify import verify


def reproduce():
    root = Path(__file__).resolve().parent
    data = certificate()
    raw = (json.dumps(data, indent=2, sort_keys=True)+'\n').encode()
    if raw != (root/'certificate.json').read_bytes():
        raise ValueError('certificate regeneration mismatch')
    report = check(data)
    if report != json.loads((root/'expected.json').read_text()):
        raise ValueError('kernel replay mismatch')
    controls = main()
    if controls != json.loads((root/'controls_expected.json').read_text()):
        raise ValueError('control replay mismatch')
    graph = json.loads((root/'fixture.json').read_text())
    if graph != fixture():
        raise ValueError('fixture regeneration mismatch')
    witness = extract(graph)
    if witness != json.loads((root/'fixture_certificate.json').read_text()):
        raise ValueError('extractor replay mismatch')
    verify(graph, witness)
    return {'status':'REPRODUCED_INDUCED_PENTAGON_FORCING',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'physical_contact_pairs':report['physical_pairs'],
            'whole_family':'induced-C5-free graphs on43 vertices',
            'proved_order_threshold':42, 'new_R55_bound':False}


if __name__ == '__main__':
    print(json.dumps(reproduce(), sort_keys=True, indent=2))
