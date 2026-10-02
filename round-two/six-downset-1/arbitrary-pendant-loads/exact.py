"""Small exact primitives, credited copies of the published own checker.

Definition-level PSD/support/row/empty checks originate in ../verify.py;
Gram products in ../verify_two_marks.py; vectors/nullspace in
../two-unequal-loads/verify_full.py. The matrix operations originate in
../three-distinct-loads/verify_full.py. No research-package imports are
used, and these copies do not constitute independent review.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

def require(condition, message):
    if not condition:
        raise ValueError(message)

def rational_matrix(a):
    n = len(a)
    require(n > 0 and all(len(row) == n for row in a), "nonsquare matrix")
    return [[F(x) for x in row] for row in a]

def psd_rank(a):
    """Exact symmetric Schur elimination, including singular residuals."""
    a = rational_matrix(a)
    n = len(a)
    require(all(a[i][j] == a[j][i] for i in range(n) for j in range(n)),
            "nonsymmetric PSD input")
    rank = 0
    for k in range(n):
        pivot = a[k][k]
        require(pivot >= 0, "negative PSD pivot")
        if pivot == 0:
            require(all(a[k][j] == 0 for j in range(k + 1, n)),
                    "zero PSD pivot with nonzero residual")
            continue
        rank += 1
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k] * a[k][j] / pivot
                a[j][i] = a[i][j]
    return rank

def family_star(family):
    require(family and family[0] == 0 and len(set(family)) == len(family),
            "bad family indexing")
    require(all(isinstance(a, int) and a >= 0 for a in family), "bad set mask")
    present = set(family)
    for a in family:
        sub = a
        while True:
            require(sub in present, "family is not a downset")
            if sub == 0:
                break
            sub = (sub - 1) & a
    require(len(family) >= 2, "trivial family")
    return max(sum(bool(a & (1 << i)) for a in family)
               for i in range(max(family).bit_length()))

def fingerprint(a):
    encoded = json.dumps([[str(x) for x in row] for row in a],
                         separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()

def check(family, a, s):
    a = rational_matrix(a)
    n = len(family)
    require(len(a) == n and family_star(family) == s, "wrong dimension or star")
    require(0 < s <= n // 2, "invalid largest-star bound")
    for i in range(n):
        require(sum(a[i]) == 1, "wrong row sum")
        for j in range(n):
            require(a[i][j] == a[j][i], "nonsymmetric certificate")
            if family[i] & family[j]:
                require(a[i][j] == 0, "intersecting entry is nonzero")
    lower = [[(n - s) * a[i][j] + s * int(i == j)
              for j in range(n)] for i in range(n)]
    upper = [[F(int(i == j)) - a[i][j] for j in range(n)] for i in range(n)]
    return {"N": n, "s": s, "lower_rank": psd_rank(lower),
            "upper_rank": psd_rank(upper), "matrix_sha256": fingerprint(a)}

def lift(c, s):
    """Core constructor, distinct from the factor-entry union constructor."""
    c = rational_matrix(c)
    m = len(c)
    n = m + 1
    rows = [sum(row) for row in c]
    q = [[sum(rows)] + [-v for v in rows]]
    q += [[-rows[i]] + c[i] for i in range(m)]
    return [[(q[i][j] + 1 - s * int(i == j)) / (n - s)
             for j in range(n)] for i in range(n)]

def matvec(a, v):
    return [dot(row, v) for row in a]

def gram(a, coefficients, independent):
    images = [matvec(a, c) for c in coefficients]
    sparse = [[(i, x) for i, x in enumerate(c) if x] for c in coefficients]
    return [[sum(x*images[j][k] for k, x in sparse[i])+independent[i][j]
             for j in range(len(coefficients))] for i in range(len(coefficients))]

def vecadd(*terms):return [sum(z) for z in zip(*terms)]

def scale(a,x):return [a*z for z in x]

def dot(x,y):return sum(a*b for a,b in zip(x,y))

def unit(length,i):return [F(j==i) for j in range(length)]

def nullspace(rows,width):
    rows=[[F(x) for x in row] for row in rows];pivots=[];row=0
    for col in range(width):
        pivot=next((i for i in range(row,len(rows)) if rows[i][col]),None)
        if pivot is None:continue
        rows[row],rows[pivot]=rows[pivot],rows[row];v=rows[row][col]
        rows[row]=[x/v for x in rows[row]]
        for i in range(len(rows)):
            if i!=row:rows[i]=[x-rows[i][col]*y for x,y in zip(rows[i],rows[row])]
        pivots.append(col);row+=1
        if row==len(rows):break
    answer=[]
    for col in range(width):
        if col in pivots:continue
        v=unit(width,col)
        for i,p in enumerate(pivots):v[p]=-rows[i][col]
        answer.append(v)
    return answer

def mm(A,B):
    return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*B)] for row in A]

def transpose(A):return list(map(list,zip(*A)))

def zero(n,m=None):return [[F(0)]*(n if m is None else m) for _ in range(n)]
