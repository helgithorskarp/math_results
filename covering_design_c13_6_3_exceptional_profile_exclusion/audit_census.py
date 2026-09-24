"""Independent exploratory census by adjoining rows to column cells."""
from itertools import permutations
from collections import Counter
import json,time

def canonical(counts,k):
    out=[]
    for p in permutations(range(k)):
        transformed=[0]*(1<<k)
        for m,n in enumerate(counts):
            image=sum(1<<p[i] for i in range(k) if m>>i&1)
            transformed[image]=n
        out.append(tuple(transformed))
    return min(out)

def independent():
    states={(11,)}
    counts_by_row=[]
    for k in range(5):
        new=set()
        for counts in states:
            occupied=[m for m,n in enumerate(counts) if n]
            selection=[0]*len(counts)
            def extend(i,left):
                if i==len(occupied):
                    if left:return
                    # The new row cannot equal an existing four-element row.
                    if any(sum(selection[m] for m in occupied if m>>j&1)>3 for j in range(k)):return
                    output=tuple(counts[m]-selection[m] for m in range(1<<k))+tuple(selection)
                    if output[0]>4*(4-k):return
                    support=[m for m,n in enumerate(output) if n]
                    # A pair of columns may share at most two rows.
                    for a,m in enumerate(support):
                        if output[m]>1 and m.bit_count()>2:return
                        if any((m&t).bit_count()>2 for t in support[a+1:]):return
                    new.add(canonical(output,k+1))
                    return
                m=occupied[i]
                for n in range(min(counts[m],left)+1):
                    selection[m]=n
                    extend(i+1,left-n)
                selection[m]=0
            extend(0,4)
        states=new
        counts_by_row.append(len(states))
    return states,counts_by_row
