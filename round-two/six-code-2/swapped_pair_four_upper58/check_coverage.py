"""Literal coverage and damage controls for the multiplicity-four result."""
import maps4 as M
from copy import deepcopy
import json
from pathlib import Path
from paths import INPUTS
from quotient import inverse
from check58 import check


def verify(data,carriers):
    M.require(len(carriers)==23 and len(data['roots'])==8 and len(data['coverage'])==26,
              'incomplete fixture/root/coverage domain')
    fixtures=json.loads((INPUTS/'fixtures.json').read_text())['stars'];expected={}
    for fi,c in enumerate(carriers):
        quads=fixtures[fi];mates=tuple(v for v in range(17) if sum(v in q for q in quads)==4)
        M.require(c['fixture']==fi and c['status']=='COMPLETE_LABELLED_LAMBDA4_STAR_UNION_CARRIER' and
                  tuple(r['mate'] for r in c['mates'])==mates and all(r['raw_maps']==1620 for r in c['mates']) and
                  len(c['rows'])==sum(r['valid_maps'] for r in c['mates']), 'incomplete mate carrier')
        for row in c['rows']:
            key=(fi,row['mate'],tuple(row['mapping']))
            M.require(key not in expected,'duplicate carrier map');expected[key]=row
    seen=set()
    for row in data['coverage']:
        key=(row['fixture'],row['mate'],tuple(row['mapping']))
        M.require(key in expected and key not in seen,'false coverage key');seen.add(key)
        root=data['roots'][row['root']];p=tuple(row['from_root'])
        M.require(root['fixture']==row['fixture'] and sorted(p)==list(range(18)), 'false transport domain')
        ip=inverse(p)
        M.require(p[root['mate']]==row['mate'] and
                  tuple(p[root['mapping'][ip[v]]] for v in range(18))==key[2] and
                  tuple(sorted(M.image(w,p) for w in root['words']))==tuple(expected[key]['words']),
                  'false positive literal transport')
    M.require(seen==set(expected),'omitted actual labelled map')
    for root in data['roots']:
        key=(root['fixture'],root['mate'],tuple(root['mapping']))
        M.require(key in seen and root['words']==expected[key]['words'],'false root words')
        words,p=M.normalize(tuple(root['words']),tuple(root['mapping']),root['mate'])
        M.require(words==tuple(root['normalized']) and p==tuple(root['transport']), 'false normalization')


def main():
    from paths import WORK
    carriers=[json.loads((WORK/'swapped-m4-full'/f'fixture-{i:02d}.json').read_text()) for i in range(23)]
    data=json.loads((WORK/'swapped-m4-roots.json').read_text());verify(data,carriers)
    w=json.loads((WORK/'swapped-m4-witness58.json').read_text());positive=check(w);rejected=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TimeoutError):rejected.append(name)
        else:raise ValueError('damage accepted: '+name)
    reject('omitted-zero-valid-fixture',lambda:verify(data,carriers[:-1]))
    bad=deepcopy(data);bad['coverage'].pop();reject('omitted-positive-map',lambda:verify(bad,carriers))
    bad=deepcopy(data);bad['roots'].pop();reject('omitted-root',lambda:verify(bad,carriers))
    bad=deepcopy(data);bad['coverage'][0]['from_root'][0]=bad['coverage'][0]['from_root'][1]
    reject('false-transport',lambda:verify(bad,carriers))
    bad=deepcopy(w);bad['words'][0]=bad['words'][1];reject('duplicate-witness-word',lambda:check(bad))
    bad=deepcopy(w);bad['words'][0]^=1<<17;reject('wrong-weight',lambda:check(bad))
    bad=deepcopy(w);bad['centers']=[16,17];reject('fixed-centers',lambda:check(bad))
    bad=deepcopy(w);bad['replications'][0]-=1;reject('false-degree',lambda:check(bad))
    fixtures=json.loads((INPUTS/'fixtures.json').read_text())['stars'];mate=carriers[1]['mates'][0]['mate']
    reject('point-node-guard',lambda:M.point_maps(fixtures[1],mate,node_cap=0))
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_LAMBDA4_LITERAL_COVER_AND_CONTROLS',
            'positive':positive,'rejected_damages':rejected}
    (WORK/'swapped-m4-controls.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
