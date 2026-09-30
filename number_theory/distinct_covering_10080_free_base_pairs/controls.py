"""Nine invalid mathematical fixtures must be rejected, including with -O."""
import copy
import json
from check import ROOT, check_certificate


def main():
    original = json.loads((ROOT/'certificate.json').read_text())
    fixtures = []
    c = copy.deepcopy(original);c['period'] += 1;fixtures.append(('wrong period',c))
    c = copy.deepcopy(original);c['families'][0]['fixed_classes'].append(c['families'][0]['fixed_classes'][-1]);fixtures.append(('duplicate prescribed modulus',c))
    c = copy.deepcopy(original);c['families'][0]['weight'][0][1] = -1;fixtures.append(('negative weight',c))
    c = copy.deepcopy(original);c['families'][0]['weight'].append(c['families'][0]['weight'][-1]);fixtures.append(('duplicate weight point',c))
    c = copy.deepcopy(original);c['families'][0]['free_base_moduli'].pop();fixtures.append(('missing free resource',c))
    c = copy.deepcopy(original);z = c['families'][0]['weight'][0][0];c['families'][0]['fixed_classes'][0][1] = z%8;fixtures.append(('weight touches an anchor',c))
    c = copy.deepcopy(original);c['families'][0]['claimed_gap'] += 1;fixtures.append(('wrong strict gap',c))
    c = copy.deepcopy(original);c['pair_example']['points'][1] = c['pair_example']['points'][0];fixtures.append(('repeated pair point',c))
    c = copy.deepcopy(original);c['pair_example']['claimed_pair_gap'] += 1;fixtures.append(('wrong pair gap',c))
    rejected = []
    for name,c in fixtures:
        try:
            check_certificate(c)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError(f'Invalid fixture accepted: {name}')
    print(json.dumps(dict(invalid_fixtures_rejected=len(rejected),rejected=rejected)))


if __name__=='__main__':
    main()
