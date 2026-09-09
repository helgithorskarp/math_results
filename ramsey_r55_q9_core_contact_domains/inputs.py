"""Pinned public input and parent source validation; no survivor inputs."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib,importlib,json,sys,urllib.request
HERE=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)
def sha(raw):return hashlib.sha256(raw).hexdigest()

def catalogue(cache,download=False):
    pin=next(x for x in json.loads((HERE/'INPUTS.json').read_text()) if x['n']==7)
    p=Path(cache)/pin['name']
    if not p.exists() and download:
        p.parent.mkdir(parents=True,exist_ok=True)
        raw=urllib.request.urlopen(pin['url'],timeout=60).read()
        need(sha(raw)==pin['sha256'],'download digest');p.write_bytes(raw)
    raw=p.read_bytes();need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'catalogue identity')
    words=[]
    for line in raw.splitlines():
        need(len(line)==5 and line[0]==70 and all(63<=x<=126 for x in line),'graph6')
        bits=[((x-63)>>b)&1 for x in line[1:] for b in range(5,-1,-1)]
        need(not any(bits[21:]),'graph6 padding');a=[[0]*7 for _ in range(7)];k=0
        for j in range(1,7):
            for i in range(j):a[i][j]=a[j][i]=bits[k];k+=1
        need(all(len({a[i][j] for i,j in combinations(s,2)})==2 for s in combinations(range(7),4)),'core R44')
        words.append(sum(a[i][j]<<k for k,(i,j) in enumerate(combinations(range(7),2))))
    need(len(words)==362 and len(set(words))==362,'catalogue count');return words

@lru_cache(None)
def parents():
    for pin in json.loads((HERE/'DEPENDENCIES.json').read_text()):
        directory=HERE.parent/pin['directory'];raw=(directory/pin['manifest']).read_bytes()
        need(sha(raw)==pin['sha256'],'dependency manifest')
        files=dict((name,digest) for digest,name in (line.split('  ',1) for line in raw.decode().splitlines())) if pin['manifest']=='SHA256SUMS' else json.loads(raw)
        for name,digest in files.items():need(sha((directory/name).read_bytes())==digest,'dependency '+name)
    directory=HERE.parent/'ramsey_r55_maximal_block_order';sys.path.insert(0,str(directory))
    module=importlib.import_module('carrier');need(Path(module.__file__).resolve().parent==directory.resolve(),'parent origin')
    module.dependencies.load();return module
