"""Verify the fixed-prefix application and the limits of the pair exclusions."""
import argparse
from collections import Counter,deque
import hashlib
import json
from pathlib import Path

from corners import cells,disc,footprint,normalize,variants,vertices
from patterns import find_forbidden,pattern_classes
from verify import check_motif

HERE=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('certificate checks require Python assertions; omit -O and -OO')
SEED_SHA='24ceb5aefe2e0843d16d7ab7ced16f17356789426a12607b00cf956df02dbe51'
WITNESS_SHA='c5f4c30ceff27b40a39ef006960b7b5de22489c52e71b429196d1f51cdc32f04'


def check_coronas(tile,patch,depth):
    shapes=variants(tile);copies=[];occupied=set();distances=[]
    for level,shape,translation in patch:
        assert type(level) is int and 0<=level<=depth and cells(shape) in shapes
        squares=footprint(shape,translation)
        assert not squares&occupied
        occupied.update(squares);copies.append(squares)
    roots=[i for i,p in enumerate(patch) if p[0]==0]
    assert len(roots)==1 and copies[roots[0]]==set(normalize(tile))
    graph=[set() for p in patch]
    for i,a in enumerate(copies):
        for j,b in enumerate(copies[:i]):
            if any((x+dx,y+dy) in b for x,y in a for dx in (-1,0,1) for dy in (-1,0,1)):
                graph[i].add(j);graph[j].add(i)
    distance={roots[0]:0};pending=deque(roots)
    while pending:
        i=pending.popleft()
        for j in graph[i]:
            if j not in distance:distance[j]=distance[i]+1;pending.append(j)
    assert len(distance)==len(patch) and all(distance[i]==p[0] for i,p in enumerate(patch))
    prefixes=[]
    for level in range(depth+1):
        current=set().union(*(copies[i] for i,p in enumerate(patch) if p[0]<=level))
        assert disc(current)
        if level<depth:
            target={(x+dx,y+dy) for x,y in current for dx in (-1,0,1) for dy in (-1,0,1)}
            extended=set().union(*(copies[i] for i,p in enumerate(patch) if p[0]<=level+1))
            assert target<=extended
        prefixes.append({'level':level,'cells':len(current),'tiles':sum(p[0]==level for p in patch),'disc':True})
    return prefixes


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prior-directory',type=Path,default=HERE.parent/'heesch_polyomino_euler_cnf')
    args=parser.parse_args();prior=args.prior_directory
    for name,digest in (('kaplan17.json',SEED_SHA),('kaplan17_depth3.witness.json',WITNESS_SHA)):
        assert hashlib.sha256((prior/name).read_bytes()).hexdigest()==digest
    tile=normalize(json.loads((prior/'kaplan17.json').read_text())['cells'])
    records=json.loads((prior/'kaplan17_depth3.witness.json').read_text())['patch']
    patch=[]
    for record in records:
        raw=cells(record['cells']);translation=min(x for x,y in raw),min(y for x,y in raw)
        patch.append((record['level'],normalize(raw),translation))
    prefix_check=check_coronas(tile,patch,3)
    motif=json.loads((HERE/'motif.json').read_text());assert normalize(motif['tile'])==tile
    assert check_motif(motif)==1
    application=motif['source_application'];world=application['world_translation']
    for old_index,copy in zip(application['old_patch_indices'],motif['fixed_copies']):
        absolute=tuple(a+b for a,b in zip(copy['translation'],world))
        assert patch[old_index][0]==3 and footprint(copy['shape'],absolute)==footprint(patch[old_index][1],patch[old_index][2])
    library=json.loads((HERE/'pairs.json').read_text());classes=pattern_classes(library)
    assert len(classes)==1896
    old_bad=find_forbidden([(shape,translation) for level,shape,translation in patch],classes)
    assert tuple(application['old_patch_indices']) in old_bad
    # A different valid three-corona patch survives every listed forbidden
    # pair. Survival is only a necessary condition for extension.
    new=json.loads((HERE/'surviving_third.json').read_text());shapes=variants(tile)
    assert normalize(new['cells'])==tile and new['depth']==3 and new['last_prefix_relaxed'] is False
    new_patch=[]
    for code in new['pose_codes']:
        assert len(code)==4 and all(type(x) is int for x in code) and 0<=code[1]<len(shapes)
        level,orientation,x,y=code;new_patch.append((level,shapes[orientation],(x,y)))
    new_check=check_coronas(tile,new_patch,3)
    new_bad=find_forbidden([(shape,translation) for level,shape,translation in new_patch],classes)
    assert not new_bad
    print(json.dumps({'agent':'six-heesch-1','role':'researcher','original_prefixes':prefix_check,
                      'motif_old_patch_indices':application['old_patch_indices'],
                      'original_forbidden_pairs':len(old_bad),'directed_D4_pattern_classes':len(classes),
                      'surviving_prefixes':new_check,'surviving_forbidden_pairs':len(new_bad),
                      'scope':'Original three-corona prefix has no all-real fourth extension. Pair survival alone does not imply extendibility.'},indent=2))


if __name__=='__main__':main()
