"""Literal ordinary-book replay of the credited21-point primary matrix."""
import ast
import collections
import hashlib
import json
from pathlib import Path

def require(ok,message):
    if not ok:
        raise ValueError(message)

def build():
    raw=Path(__file__).with_name('primary21.txt').read_bytes()
    text=raw.decode();start=text.index('[');depth=0;end=None
    for k,c in enumerate(text[start:],start):
        if c=='[':depth+=1
        elif c==']':
            depth-=1
            if depth==0:end=k+1;break
    require(end is not None,'unfinished matrix')
    matrix=ast.literal_eval(text[start:end])
    require(len(matrix)==21 and all(len(row)==21 for row in matrix),'matrix order')
    require(all(type(v) is int and v in (0,1) for row in matrix for v in row),'matrix entries')
    require(all(matrix[i][j]==matrix[j][i] for i in range(21) for j in range(21)),'matrix asymmetry')
    red=[set(j for j in range(21) if j!=i and matrix[i][j]==0) for i in range(21)]
    blue=[set(range(21))-{i}-red[i] for i in range(21)]
    counts=[0,0];maxima=[0,0]
    for i in range(21):
        for j in range(i):
            color=0 if j in red[i] else 1;rows=red if color==0 else blue
            pages=len(rows[i]&rows[j]);counts[color]+=1;maxima[color]=max(maxima[color],pages)
            require(pages<=(3 if color==0 else 6),'primary ordinary book')
    result={'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),
            'spines':sum(counts),'red_edges':counts[0],'blue_pairs':counts[1],
            'page_maxima':maxima,'red_degree_histogram':dict(sorted(collections.Counter(len(r) for r in red).items())),
            'prior_art_validation_only':True}
    require(result['raw_sha256']=='3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55','primary bytes differ')
    require(counts==[93,117] and maxima==[3,6],'primary baseline differs')
    return result

if __name__=='__main__':
    print(json.dumps(build(),sort_keys=True,separators=(',',':')))
