#!/usr/bin/env python3
"""Full canonical core formulas with intrinsic two-empty-anchor constraints."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PREVIOUS = ROOT.parent/'ramsey_r55_order3_eleven_anchor_equality'
BASES = ROOT.parent/'ramsey_r55_order3_eleven_residual_sweep'/'result.json'
PINS = {'anchors.json':'7c9afff91b862308deea340d11a8576a7f7773b5880749c3a8793e00cf340464',
        'result.json':'ec54563bf4046e81411f6b0a35171917e116e2ed286e30adf331999ac9300ed4',
        'verification.json':'a45d1a3b65b5825aa23062011b419e81e8a4499821fd7cdde133b3c8586d668d'}
BASES_PIN = 'aa6fe619507d058d69aadf36f5ef92ec7bc073f5cfab2d1e99b3191d8b2e658c'
PARENT_PIN = 'c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f'
CORE_VARIABLES = (1,2,3,4,5,6,7,8,9,31,32,33,34,35,36,58,59,60)


def require(ok, why):
    if not ok: raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned '+name)
    result=json.loads((PREVIOUS/'result.json').read_text())
    verification=json.loads((PREVIOUS/'verification.json').read_text())
    require(result['complete'] and result['excluded']==['a11_equality','a13_equality'] and not result['open'],'complete inherited equality closure')
    require(verification['verified'] and verification['proof_replays']==2,'inherited second replay')
    require(info(BASES)['sha256']==BASES_PIN,'pinned full bases')
    original={r['index']:r for r in json.loads(BASES.read_text())['cases']}
    rows=[]
    for r in json.loads((PREVIOUS/'anchors.json').read_text())['residual']:
        old=original[r['index']];require(old['bits']==r['bits'] and old['status']=='open','original core base')
        rows.append(dict(index=r['index'],bits=r['bits'],labeled=r['labeled'],
                         omitted=[a['omitted'] for a in r['anchors']],base=old['formula']))
    require(len(rows)==34 and sum(len(r['omitted']) for r in rows)==56,'complete residual applications')
    require([r['index'] for r in rows]==sorted({r['index'] for r in rows}),'unique sorted cases')
    return rows


def make_base(parent, output, case):
    with parent.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34280 615920\n','full parent header')
        g.write(b'p cnf 34280 615938\n');shutil.copyfileobj(f,g)
        for v,b in zip(CORE_VARIABLES,case['bits']):g.write(f'{v if b=="1" else -v} 0\n'.encode())
    answer=info(output);require(answer==case['base'],'base differs from inherited exact full cube')
    return answer


def clauses(case):
    rows=[]
    for q,omitted in enumerate(case['omitted']):
        group=[]
        for f in range(10):
            a=34281+10*q+f;group.append(a)
            links=[211+11*f+i for i in range(4) if i!=omitted]
            rows.extend([(-a,-v) for v in links])
            rows.append(tuple([a]+links))
        # Every nine-subset contains a true indicator iff at least two are true.
        rows.extend(tuple(a for j,a in enumerate(group) if j!=f) for f in range(10))
    return rows


def make(base, output, case):
    rows=clauses(case);g=len(case['omitted'])
    require(len(rows)==50*g,'consequence count')
    with base.open('rb') as f,output.open('wb') as out:
        require(f.readline()==b'p cnf 34280 615938\n','complete base header')
        out.write(f'p cnf {34280+10*g} {615938+len(rows)}\n'.encode());shutil.copyfileobj(f,out)
        for row in rows:out.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
