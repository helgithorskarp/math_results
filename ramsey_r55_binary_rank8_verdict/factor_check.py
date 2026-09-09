"""Small exhaustive checks of the alternating-form coverage argument."""
from itertools import combinations
import json
from counter import require
from witness import form

def rank(rows,n):
    work=list(rows);r=0
    for col in range(n):
        pivot=next((i for i in range(r,n) if work[i]>>col&1),None)
        if pivot is None:continue
        work[r],work[pivot]=work[pivot],work[r]
        for i in range(n):
            if i!=r and work[i]>>col&1:work[i]^=work[r]
        r+=1
    return r

def factor(rows,n):
    remainder=list(rows);coords=[0]*n;planes=0
    while any(remainder):
        p=next(i for i in range(n) if remainder[i]);q=(remainder[p]&-remainder[p]).bit_length()-1
        u,v=remainder[p],remainder[q]
        old=rank(remainder,n)
        remainder=[x^(v if u>>i&1 else 0)^(u if v>>i&1 else 0) for i,x in enumerate(remainder)]
        require(rank(remainder,n)==old-2,'rank drop')
        require(planes<4,'rank greater than eight')
        for i in range(n):coords[i]|=((u>>i)&1)<<planes|((v>>i)&1)<<(planes+4)
        planes+=1
    require(2*planes==rank(rows,n),'rank identity')
    for i,j in combinations(range(n),2):require(form(coords[i],coords[j])==(rows[i]>>j&1),'all factor entries')
    return planes

def main():
    histogram={};graphs=0
    for n in range(1,7):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            rows=[0]*n
            for bit,(i,j) in enumerate(pairs):
                if word>>bit&1:rows[i]|=1<<j;rows[j]|=1<<i
            r=2*factor(rows,n);histogram[r]=histogram.get(r,0)+1;graphs+=1
    # Full 8-dimensional basis; repeated/zero labels are allowed in this
    # algebraic identity, and are excluded only under the good43 hypothesis.
    labels=[0]+[1<<i for i in range(8)]+[1,2,255,255]
    rows=[sum(form(u,v)<<j for j,v in enumerate(labels)) for u in labels]
    require(factor(rows,len(labels))==4,'rank-eight boundary')
    print(json.dumps({'graphs':graphs,'rank_histogram':histogram,'rank_eight_zero_and_repeated_label_control':True},indent=2,sort_keys=True))

if __name__=='__main__':main()
