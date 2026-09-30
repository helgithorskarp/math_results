"""Exact triangular-cell realization of the published marked hexapillar.

Agent six-heesch-2, researcher. Input fixture: six-heesch-3's reproduction of
Mann's known five-corona construction. No search and no novelty claim.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FIXTURE_SHA256 = 'd857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a'
DIRECTIONS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def triangle(points):
    return tuple(sorted(points))


def up(x,y):
    return triangle(((x,y),(x+1,y),(x,y+1)))


def down(x,y):
    return triangle(((x+1,y+1),(x,y+1),(x+1,y)))


def hexagon(side):
    cells=set()
    for x in range(-side,side+1):
        for y in range(-side,side+1):
            for t in (up(x,y),down(x,y)):
                if all(max(abs(a),abs(b),abs(a+b))<=side for a,b in t):
                    cells.add(t)
    assert len(cells)==6*side*side
    return cells


def coarse_motion(p,reflect,turns):
    x,y=p
    if reflect:x,y=x+y,-y
    for _ in range(turns):x,y=-y,x+y
    return x,y


def fine_motion(p,reflect,turns):
    x,y=p
    if reflect:x,y=y,x
    for _ in range(turns):x,y=-y,x+y
    return x,y


def center(p,side):
    return side*(p[0]-p[1]),side*(p[0]+2*p[1])


def translated(t,p):
    return triangle((x+p[0],y+p[1]) for x,y in t)


def main():
    raw=(BASE/'marked_fixture.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256
    w=json.loads(raw)
    assert w['tile']==[[0,0],[1,0],[2,0],[3,0]] and w['depth']==5
    side=3
    s={translated(t,center(c,side)) for c in w['tile'] for t in hexagon(side)}
    ports=sorted((tuple(c),(c[0]+dx,c[1]+dy)) for c in w['tile']
                 for dx,dy in DIRECTIONS if [c[0]+dx,c[1]+dy] not in w['tile'])
    assert len(ports)==len(w['signs'])==18
    assert [w['signs'].count(a) for a in (1,-1,0)]==[9,8,1]
    k=(side-1)//2
    for (c,n),sign in zip(ports,w['signs']):
        direction=DIRECTIONS.index((n[0]-c[0],n[1]-c[1]))
        # Exchange bump/nick labels globally: matching is preserved, and the
        # geometric tile has nine 300-degree bays versus eight 60-degree tips.
        if sign==1:
            nick=translated(triangle(fine_motion(p,False,direction) for p in up(k,k)),center(c,side))
            s.remove(nick)
        elif sign==-1:
            bump=translated(triangle(fine_motion(p,False,direction) for p in down(k,k)),center(c,side))
            assert bump not in s
            s.add(bump)
    assert len(s)==215
    placements=[]
    for p in w['patch']:
        f,r=p['reflect'],p['turns']
        raw=[coarse_motion(c,f,r) for c in w['tile']]
        shift=[p['translation'][j]-min(c[j] for c in raw) for j in (0,1)]
        a,c=fine_motion((1,0),f,r);b,d=fine_motion((0,1),f,r)
        placements.append({'level':p['level'],'matrix':[a,b,c,d],
                           'translation':list(center(shift,side))})
    (BASE/'tile.json').write_text(json.dumps({'grid':'unit-equilateral-triangles',
                                           'triangles':sorted(s)},separators=(',',':'))+'\n')
    (BASE/'coronas.json').write_text(json.dumps({'depth':5,'placements':placements},
                                              separators=(',',':'))+'\n')
    print(json.dumps({'cells':len(s),'copies':len(placements),'depth':5,
                      'fixture_sha256':FIXTURE_SHA256},sort_keys=True))


if __name__=='__main__':
    main()
