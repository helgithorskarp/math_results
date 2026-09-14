"""Four-colouring of the pentagonal odd-denominator direction module."""
def fm(a,b):
    v=0
    for i in range(2):
        for j in range(2):
            if (a>>i)&1 and (b>>j)&1:v^=1<<(i+j)
    return v^7 if v&4 else v
def coefficient(a):
    out=0;weights=(1,1,1,2,3);omega=(1,2,3)
    for i,x in enumerate(a):
        if x%2:out^=fm(omega[i%3],weights[(2*i)%5])
    return out
def point(p):return coefficient(p[0])^fm(2,coefficient(p[1]))
