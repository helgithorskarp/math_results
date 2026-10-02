"""Seal the newly regenerated whole capacity inputs, before either kernel."""
import hashlib
import json
from pathlib import Path

R = Path('round-two/six-code-3')
S = R / 'scratch'
B = R / 'four_hub_p21_endpoint_cut'

def need(c, m):
    if not c:
        raise ValueError(m)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    out = S / 'pass21-T1-capacity-source-preparation.json'
    need(not out.exists(), 'fresh capacity input seal')
    scope = S / 'pass21-T1-column-scope.json'
    live = S / 'pass21-T1-live-column-cases.json'
    data = json.loads(live.read_text())
    need(data['scope_sha256'] == sha(scope), 'raw scope provenance')
    need(data['catalogue_sha256'] == sha(S / 'pass21-T1-hub-friend-catalogue.json'), 'raw catalogue provenance')
    need(data['complete_preliminary_populations'] == 1787 and
         data['canonical_carriers'] == 182 and
         data['complete_carrier_population_records'] == 325234 and
         len(data['live_cases']) == 29, 'complete actual capacity domain')
    result = dict(live_cases_sha256=sha(live),
                  catalogue_sha256=sha(S / 'pass21-T1-hub-friend-catalogue.json'),
                  type_basis_sha256=sha(B / 'expected.json'),
                  fixture_sha256=sha(B / 'fixtures.json'))
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps(dict(status='REGENERATED_COMPLETE_CAPACITY_INPUTS_SEALED', actual_cases=29)))

if __name__ == '__main__':
    main()
