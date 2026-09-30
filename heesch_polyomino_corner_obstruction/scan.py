"""Reproduce the complete 352-pose integral contact scan for the fixed P17."""
import hashlib
import json
from pathlib import Path
import time

from corners import footprint,normalize,propagate,variants

HERE=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('certificate checks require Python assertions; omit -O and -OO')


def contact_inventory(tile):
    root=set(tile);result=[]
    for shape in variants(tile):
        translations=sorted({(x+dx-a,y+dy-b) for x,y in root for a,b in shape
                             for dx in (-1,0,1) for dy in (-1,0,1)})
        for translation in translations:
            if not root&footprint(shape,translation):result.append((shape,translation))
    return result


def bounding_inventory(tile):
    """Independent bounded translation loops with closed-rectangle contact."""
    root=set(tile);result=set()
    xmin=min(x for x,y in root)-1;xmax=max(x for x,y in root)+1
    ymin=min(y for x,y in root)-1;ymax=max(y for x,y in root)+1
    for shape in variants(tile):
        width=max(x for x,y in shape);height=max(y for x,y in shape)
        for tx in range(xmin-width,xmax+1):
            for ty in range(ymin-height,ymax+1):
                squares=footprint(shape,(tx,ty))
                if squares&root:continue
                if any(abs(x-a)<=1 and abs(y-b)<=1 for x,y in squares for a,b in root):
                    result.add((shape,(tx,ty)))
    return result


def main():
    start=time.monotonic();data=json.loads((HERE/'pairs.json').read_text())
    tile=normalize(data['tile']);shapes=variants(tile);inventory=contact_inventory(tile)
    assert set(inventory)==bounding_inventory(tile)
    digest=hashlib.sha256(json.dumps(inventory,separators=(',',':')).encode()).hexdigest()
    assert len(inventory)==data['contact_inventory']==352 and digest==data['inventory_sha256']
    proved=[];inconclusive=0;maximum=0
    for shape,translation in inventory:
        if time.monotonic()-start>40:
            raise RuntimeError('40-second guard; incomplete scan, no final scan claim')
        result=propagate(tile,[(tile,(0,0)),(shape,translation)])
        if result['status']=='contradiction':
            proved.append([shapes.index(shape),*translation]);maximum=max(maximum,len(result['trace']))
        elif result['status']=='propagation exhausted; inconclusive':inconclusive+=1
        else:raise RuntimeError('corner step guard; incomplete scan')
    assert sorted(proved)==data['forbidden_poses'] and len(proved)==237
    assert inconclusive==data['inconclusive_poses']==115 and maximum==4
    print(json.dumps({'agent':'six-heesch-1','role':'researcher','contact_inventory':len(inventory),
                      'inventory_sha256':digest,'independent_inventory_exact_match':True,
                      'proved_forbidden_poses':len(proved),'inconclusive_poses':inconclusive,
                      'maximum_forced_copies':maximum,'seconds':round(time.monotonic()-start,3)},indent=2))


if __name__=='__main__':main()
