"""Entry-level geometry comparisons and rejection controls."""
import json,random
from pathlib import Path
from itertools import combinations
from verify import edges,decode,colouring,require,digest,mandatory
from lattice import edges as fast_edges,directions
from graph import spindle,crossunit
import radicals as r

def run():
    rng=random.Random(375);cases=[]
    for n in (0,1,2,7,30,100):
        cases.append(sorted(set(tuple(rng.randrange(-20,21) for _ in range(4)) for _ in range(n))))
    ds=directions();cases += [ds,[(0,0,0,0)]+ds]
    for pts in cases:require(fast_edges(pts)==edges(pts),'Lattice generator mismatch')
    ps=[[0,0,0,0],[0,0,96,0],[0,0,-96,0],[0,0,36,0]]
    rows,es,cs=spindle(ps)
    require(es==edges(rows,spindle=True),'Full small spindle mismatch')
    for _ in range(400):
        p=[rng.randrange(-30,31) for _ in range(4)];q=[rng.randrange(-30,31) for _ in range(4)]
        direct=r.distance(decode([0]+p,True),decode([1]+q,True))==r.scalar((128*36)**2)
        require(crossunit(p,q)==direct,'Cross equation mismatch')
    rejected=0
    def bad(f):
        nonlocal rejected
        try:f()
        except (ValueError,TypeError):rejected+=1
        else:raise ValueError('Malformed control accepted')
    bad(lambda:edges([[0,0,0,0]]*2))
    bad(lambda:edges([[0,0,0,0]],0))
    bad(lambda:decode([2,0,0,0,0],True))
    bad(lambda:decode([True,0,0,0,0],True))
    bad(lambda:decode([0,0,0]))
    bad(lambda:decode([0,0,0,0.0]))
    bad(lambda:colouring([0,0],2,[[0,1]],4))
    bad(lambda:colouring([0],2,[],4))
    bad(lambda:colouring([0,4],2,[],4))
    bad(lambda:colouring([0,True],2,[],4))
    b=json.loads((Path(__file__).resolve().parent/'separating_basis.json').read_text())
    require(digest(b['points'])==b['parent_point_sha256'],'Parent point mismatch')
    es=edges(b['points']);n=len(b['points'])
    for c in b['colourings']:colouring(c,n,es,4)
    require(len({tuple(c[v] for c in b['colourings']) for v in range(n)})==n,'Basis not separating')
    root=Path(__file__).resolve().parent
    cert=json.loads((root/'certificate.json').read_text())['equal'];he=edges(cert['points']);nn=len(cert['points'])
    rows=json.loads((root/'mandatory_vertices.json').read_text())
    mandatory(rows,nn,he)
    bad(lambda:mandatory(rows[:-1],nn,he))
    bad(lambda:mandatory(rows[:-1]+[rows[0]],nn,he))
    for field,value in [('deleted',0),('deleted',nn),('colouring',rows[0]['colouring'][:-1]),('colouring','1'+rows[0]['colouring'][1:]),('colouring','4'+rows[0]['colouring'][1:])]:
        changed=[dict(z) for z in rows];changed[0][field]=value
        bad(lambda changed=changed:mandatory(changed,nn,he))
    changed=[dict(z) for z in rows];v=changed[0]['deleted'];ua,ub=next((a,b) for a,b in he if a>1 and b>1 and v not in (a,b));word=list(changed[0]['colouring']);word[ub]=word[ua];changed[0]['colouring']=''.join(word)
    bad(lambda:mandatory(changed,nn,he))
    return {'geometry_cases':len(cases),'cross_cases':400,'full_small_spindle_checked':True,'malformed_rejected':rejected,'unit_directions':len(ds),'separating_colourings':len(b['colourings']),'separated_vertices':n}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
