"""Independent literal checker for the complete supplied words."""
import json
import math
import itertools
from pathlib import Path


def check(data):
    a,p=data['axis_factor'],data['short_factor'];n=a*p;t=(p-1)//2
    word=data['word']
    if a%2!=1 or p not in (5,7,11) or math.gcd(a,p)!=1 or len(word)!=n-1:
        raise ValueError('invalid word dimensions')
    if any(type(c) is not int or not 0<=c<6 for c in word):raise ValueError('bad colour')
    representatives=data.get('short_representatives',list(range(1,t+1)))
    T=set(representatives)
    if len(representatives)!=t or len(T)!=t or T|{-b%p for b in T}!=set(range(1,p)):
        raise ValueError('invalid short representatives')
    pair_colour={b:c for c,j in enumerate(representatives) for b in (j,-j%p)}
    row=[-1]+word;U=p*pow(p,-1,a);V=a*pow(a,-1,p)
    axis=[-1]+[row[U*x%n] for x in range(1,a)]
    Q=[row[(U*x+V*representatives[0])%n] for x in range(a)]
    if Q[0]!=0 or any(c in range(1,t) for c in Q):raise ValueError('bad fibre partition')
    for x in range(1,n):
        if row[x]!=row[n-x]:raise ValueError('global reflection fails')
        u,b=x%a,x%p
        if b==0:expected=axis[u]
        else:
            state=Q[u] if b in T else Q[-u%a]
            expected=state if state else pair_colour[b]
        if row[x]!=expected:raise ValueError('fibre rule fails')
    E=[{x for x in range(1,a) if axis[x]==c} for c in range(6)]
    C={c:{x for x in range(a) if Q[x]==c} for c in (0,*range(t,6))}
    sf=lambda S:all((x+y)%a not in S for x in S for y in S)
    diff=lambda S:{(x-y)%a for x in S for y in S}
    if not all(sf(S) for S in E):raise ValueError('axis condition fails')
    if any(not sf(C[c]|{-x%a for x in C[c]}) for c in range(t,6)):
        raise ValueError('common support not sum-free')
    if set().union(*E[:t])&diff(C[0]):raise ValueError('special difference collision')
    if any(E[c]&diff(C[c]) for c in range(t,6)):raise ValueError('common difference collision')
    modular=ordinary=0
    for x in range(1,n):
        for y in range(x,n):
            z=(x+y)%n
            if z:
                modular+=1
                if row[x]==row[y]==row[z]:raise ValueError(('modular violation',x,y,z))
            if x+y<n:
                ordinary+=1
                if row[x]==row[y]==row[x+y]:raise ValueError(('ordinary violation',x,y,x+y))
    if data.get('normalize_axis') and axis[1]!=0:raise ValueError('axis normalization fails')
    return dict(status='ODD_FACTOR_WORD_OK',modulus=n,endpoint=n-1,
                class_sizes=[word.count(c) for c in range(6)],modular_pairs=modular,
                integer_pairs=ordinary,residual_size=len(C[0]),
                common_sizes=[len(C[c]) for c in range(t,6)],
                asymmetric_pairs=sum(Q[u]!=Q[-u%a] for u in range(1,(a+1)//2)),
                special_axis_union_sum_free=sf(set().union(*E[:t])))



def orientation_variants(data):
    a,p=data['axis_factor'],data['short_factor'];n=a*p
    row=[-1]+data['word'];U=p*pow(p,-1,a);V=a*pow(a,-1,p)
    E=[-1]+[row[U*x%n] for x in range(1,a)]
    Q=[row[(U*x+V)%n] for x in range(a)]
    count=0
    for signs in itertools.product((1,-1),repeat=3):
        representatives=[sign*x%7 for sign,x in zip(signs,(1,2,3))]
        T=set(representatives)
        special={b:c for c,j in enumerate(representatives) for b in (j,-j%7)}
        word=[]
        for x in range(1,n):
            u,b=x%a,x%p
            if not b:colour=E[u]
            else:
                state=Q[u] if b in T else Q[-u%a]
                colour=state if state else special[b]
            word.append(colour)
        check(dict(axis_factor=a,short_factor=p,modulus=n,word=word,
                   short_representatives=representatives))
        count+=1
    return count


if __name__=="__main__":
    folder=Path(__file__).resolve().parent
    controls=json.loads((folder/"controls.json").read_text())
    report={"status":"PASS","controls":[check(c) for c in controls],
            "orientation_variants_checked":sum(orientation_variants(c) for c in controls)}
    expected=json.loads((folder/"expected.json").read_text())["controls"]
    if report!=expected:raise RuntimeError(("control report differs",report))
    print(json.dumps(report,indent=2))
