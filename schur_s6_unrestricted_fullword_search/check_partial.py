"""Independently check the two-hole local-search output and its completions."""
from itertools import permutations,product
from pathlib import Path
import json

from check import defects

HERE=Path(__file__).resolve().parent


def check():
    partial=(HERE/'partial537.txt').read_text(encoding='ascii').strip()
    assert len(partial)==537 and set(partial)<=set('123456?')
    holes=[v for v,c in enumerate(partial,1) if c=='?']
    assert holes==[2,4]
    partial_bad=[(x,z-x,z) for z in range(2,538)
                 for x in range(1,z//2+1)
                 if partial[x-1]!='?' and partial[x-1]==partial[z-x-1]==partial[z-1]]
    assert not partial_bad
    scores=[]
    for a,b in product('123456',repeat=2):
        word=list(partial);word[1]=a;word[3]=b
        scores.append((len(defects(''.join(word))),a,b))
    scores.sort()
    assert scores[0]==(11,'2','2') and sum(t[0]==11 for t in scores)==1
    complete=(HERE/'completed11.txt').read_text(encoding='ascii').strip()
    assert complete==partial.replace('?','2') and len(defects(complete))==11
    best=(HERE/'best4.txt').read_text(encoding='ascii').strip()
    assert defects(best)==[(1,1,2),(1,2,3),(4,4,8),(4,5,9)]
    sources=json.loads((HERE.parent/'schur_s6_multi_alignment_recombination'/'sources.json').read_text())
    distances={}
    for name,row in sources.items():
        word=row['word']
        distances[name]=min(sum(c!='?' and c!=perm[int(word[i])-1]
                                for i,c in enumerate(partial))
                            for perm in permutations('123456'))
    assert distances=={'W':401,'190':421,'359':407,'best3':409,'347':414}
    print('PASS holes=2,4 partial_bad=0 completions=36 '
          f'min_completion_defects=11 best4_defects=4 distances={distances}')


if __name__=='__main__':check()
