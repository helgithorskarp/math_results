"""Direct independent checker for any complete 537-digit candidate."""
import argparse
from pathlib import Path


def defects(word):
    assert len(word)==537 and set(word)==set('123456')
    bad=[]
    triples=0
    doubling=0
    for x in range(1,538):
        for y in range(x,538-x):
            z=x+y
            triples+=1
            doubling+=(x==y)
            if word[x-1]==word[y-1]==word[z-1]:
                bad.append((x,y,z))
    assert triples==72092 and doubling==268
    return bad


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('word',type=Path)
    a=p.parse_args()
    bad=defects(a.word.read_text(encoding='ascii').strip())
    print(f'triples=72092 doubling=268 defects={len(bad)} bad={bad}')
