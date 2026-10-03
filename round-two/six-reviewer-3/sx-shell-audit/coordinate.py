"""Separate reversed-coordinate bit model; no import of the set shell."""
from itertools import combinations

ORDER=('Q5','Q4','Q3','Q2','Q1','Q0','T2','T1','T0','SY1','SY0','SX1','SX0','X5','X4','X3','X2','X1','X0','a','v','u')

def specification():
    fixed_red_words={
      'u':'v a X0 X1 X2 X3 X4 X5 SX0 SX1',
      'v':'a SY0 SY1 Q0 Q1 Q2 Q3 Q4 Q5',
      'a':'SX0 SX1 SY0 SY1 T0 T1 T2',
      'X0':'X4 X5','X1':'X2 X3','X2':'X5 SX1','X3':'X4 SX0',
      'X4':'SX1','X5':'SX0','SX0':'T1 T2','SX1':'T1 T2',
      'SY0':'T0 T2','SY1':'T0 T1'}
    red=set()
    for a,word in fixed_red_words.items():
        for b in word.split():red.add(tuple(sorted((a,b))))
    result={}
    for a,b in combinations(ORDER,2):
        aQ=a.startswith('Q');bQ=b.startswith('Q')
        free=(aQ and b!='u' and b!='v' and b!='a')or(bQ and a!='u' and a!='v' and a!='a')
        free=free or(a.startswith('X') and b in ['SY0','SY1','T0','T1','T2'])or(b.startswith('X') and a in ['SY0','SY1','T0','T1','T2'])
        p=tuple(sorted((a,b)));result[p]=None if free else int(p in red)
    return result

def rows(spec):
    ix={v:i for i,v in enumerate(ORDER)};r=[0]*22;b=[0]*22
    for (a,c),v in spec.items():
        if v is not None:
            table=r if v==1 else b;table[ix[a]]|=1<<ix[c];table[ix[c]]|=1<<ix[a]
    return r,b,ix

def pages(spec,a,b,color):
    r,bl,ix=rows(spec);mask=(r if color else bl)[ix[a]]&(r if color else bl)[ix[b]]
    return sorted(v for i,v in enumerate(ORDER) if mask>>i&1)

def independent_cover(mask):
    # A star is covered independently exactly by its center or both leaves.
    first=((mask&49)==1 or(mask&49)==48)
    second=((mask&14)==2 or(mask&14)==12)
    return first and second
