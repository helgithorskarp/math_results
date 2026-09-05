#!/usr/bin/env python3
"""Complete one-empty / multiple-empty split of four pinned full bases."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent/'ramsey_r55_order3_eleven_empty_signature'
PARENT = ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
INPUT = PREVIOUS/'result.json'
PIN = '5f7fdc79445a91a4467a140d76fa4949779e5ef1fc7bb9fc263db05d1e24f040'
PARENT_PIN = 'c8f355b256de55727b18efcbd47ef9e777ac2b3b4ae69e09676fcddd51afa05f'
CORE_VARIABLES = (1,2,3,4,5,6,7,8,9,31,32,33,34,35,36,58,59,60)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while data:=f.read(1<<20):h.update(data)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cores():
    require(info(INPUT)['sha256']==PIN,'pinned preceding result')
    data=json.loads(INPUT.read_text())
    require(data['complete'] and data['open']==[131,139,162,173],'four residual cores')
    return [r for r in data['cases'] if r['index'] in data['open']]


def cases():
    return sorted([dict(id=f"c{r['index']}_{branch}",index=r['index'],bits=r['bits'],branch=branch)
                   for r in cores() for branch in ('one','multiple')], key=lambda r:r['id'])


def make_base(parent, output, core):
    with parent.open('rb') as f, output.open('wb') as g:
        require(f.readline()==b'p cnf 34280 615920\n','parent header')
        g.write(b'p cnf 34280 615942\n');shutil.copyfileobj(f,g)
        for variable,bit in zip(CORE_VARIABLES,core['bits']):
            g.write(f'{variable if bit=="1" else -variable} 0\n'.encode())
        for variable in (211,212,213,214):g.write(f'{-variable} 0\n'.encode())
    result=info(output)
    require(result==core['formula'],'base differs from preceding full formula')
    return result


def clauses(branch):
    require(branch in ('one','multiple'),'branch')
    return [(222,223,224,225)] if branch=='one' else [(-x,) for x in (222,223,224,225)]


def make(base, output, branch):
    tail=clauses(branch)
    with base.open('rb') as f, output.open('wb') as g:
        require(f.readline()==b'p cnf 34280 615942\n','full inherited base header')
        g.write(f'p cnf 34280 {615942+len(tail)}\n'.encode());shutil.copyfileobj(f,g)
        for row in tail:g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
