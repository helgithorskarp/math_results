"""Mathematical corruption controls for the independent exact checker."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
from verify import check_case,check_directory,read_case


def main():
    p = argparse.ArgumentParser()
    p.add_argument('certificate',type=Path)
    a = p.parse_args()
    good = json.loads(a.certificate.read_text())
    positive = check_case(good)
    mutations = []
    def add(name,change):
        v = copy.deepcopy(good)
        change(v)
        mutations.append((name,v))
    add('zero denominator',lambda v:v.update(denominator=0))
    add('zero step',lambda v:v['color0_APs'][0].__setitem__(1,0))
    add('negative weight',lambda v:v['color0_APs'][0].__setitem__(2,-1))
    add('boolean weight',lambda v:v['color0_APs'][0].__setitem__(2,True))
    add('coordinate outside word',lambda v:v['color0_APs'][0].__setitem__(0,-1))
    add('duplicate AP',lambda v:v['color0_APs'].append(v['color0_APs'][0][:]))
    add('overloaded position',lambda v:v['color0_APs'][0].__setitem__(2,v['denominator']+1))
    add('wrong phase relation',lambda v:v.update(t=(v['t']+1)%617))
    add('wrong relative orientation',lambda v:v.update(g=0))
    add('wrong modulus',lambda v:v.update(P=619))
    add('unknown field',lambda v:v.update(unchecked=True))
    def wrongcolor(v):
        aa,dd,num = v['color0_APs'][0]
        v['color0_APs'][0] = [3703-aa-6*dd,dd,num]
    add('opposite color AP presented as color0',wrongcolor)
    def pole(v):
        aa = 1852-v['s']
        if aa >= 1852:
            aa -= 617
        dd = max(1,(1852-aa+5)//6)
        v['color0_APs'][0] = [aa,dd,1]
    add('free pole in AP',pole)
    rejected = []
    for name,value in mutations:
        try:
            check_case(value)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError('Accepted corrupted certificate: '+name)
    with tempfile.TemporaryDirectory(prefix='controls-',dir=a.certificate.parent) as directory:
        d = Path(directory)
        source = d/f"phase-{good['s']:03d}.json"
        source.write_text(json.dumps(good))
        partial = check_directory(d)
        assert not partial['complete'] and partial['phase_count'] == 1
        try:
            check_directory(d,True)
        except ValueError:
            rejected.append('incomplete family passed as complete')
        else:
            raise AssertionError('Incomplete phase coverage accepted')
        wrong = d/f"phase-{(good['s']+1)%617:03d}.json"
        source.rename(wrong)
        try:
            check_directory(d)
        except ValueError:
            rejected.append('phase filename mismatch')
        else:
            raise AssertionError('Phase mismatch accepted')
        wrong.write_text(json.dumps(good)+' trailing')
        try:
            read_case(wrong)
        except ValueError:
            rejected.append('trailing non-JSON data')
        else:
            raise AssertionError('Trailing data accepted')
    print(json.dumps({'status':'EXACT_CHECKER_CONTROLS_PASSED','rejections':rejected,
                      'count':len(rejected),'positive_per_color':positive['required_edits_per_reference_color']}))


if __name__ == '__main__':
    main()
