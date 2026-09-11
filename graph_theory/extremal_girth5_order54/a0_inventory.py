"""Complete necessary A0 inventory and first incidence bounds; no solver."""
from functools import lru_cache

@lru_cache(None)
def histograms(d, total, weight, budget):
    """Independent census: recurse over EVERY c=0,...,d, with three totals.

    No charged-type list or solved zero-cost handshake is used here.
    """
    offset = 3 if d == 6 else 1
    costs = tuple((c-offset)*(c-2)//2 for c in range(d+1))

    @lru_cache(None)
    def visit(c, n, w, b):
        if min(n, w, b) < 0 or w < c*n or w > d*n:
            return ()
        if c == d+1:
            return ((),) if n == w == b == 0 else ()
        ans = []
        for count in range(n+1):
            if count*costs[c] > b:
                break
            for rest in visit(c+1, n-count, w-c*count, b-costs[c]*count):
                ans.append((count,)+rest)
        return tuple(ans)
    return visit(0, total, weight, budget)


def profiles():
 for m in range(9):
  for k in range(max(1,m)):
   if m+k>8:continue
   B=8-m-k
   for b6 in range(B+1):
    for six in histograms(6,16,36+2*m,b6):
     for seven in histograms(7,26,60-4*m,B-b6):yield m,k,six,seven


def bounds(row):
 m,k,six,seven=row
 positive=sum(n*((c-3)*(c-2) if c<2 else (c-3)*(2*c-8) if c>=4 else 0) for c,n in enumerate(six))
 positive+=sum(n*(c-3)*(2*c-7) for c,n in enumerate(seven) if c>=4)
 lo=12-2*m+positive
 large=[(d,c,n) for d,ns in [(6,six),(7,seven)] for c,n in enumerate(ns) if c>=5 and n]
 sizes=sorted([c for ns in(six,seven) for c,n in enumerate(ns) for _ in range(n)],reverse=True)
 b22=sum(sizes[:2])>=10
 b1=seven[1]
 if b22: return lo,100,{'special_b22':True}
 if large:
  upper=min(min(2*f,f+b1) for d,c,n in large for f in [17-2*c if d==6 else 11-2*c])
 else:
  f4=six[4]+seven[4]
  if f4<2:b1=0
  upper=9*six[4]+3*seven[4]
  if f4==1:upper=min(upper,4)
  if f4==2:upper=min(upper,6)
  if f4==3:upper=min(upper,9)
 upper=min(upper,32+b1,2*b1+seven[2])
 return lo,upper,{}
