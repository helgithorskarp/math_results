# Independent proof audit

## 1. Exact source and isolated root

Let K=Q(rho), with rho^2-rho+1=0. In the basis 1,rho,

    (a+b rho)(c+d rho) = (ac-bd) + (ad+bc+bd) rho
    N(a+b rho) = a^2+ab+b^2.

Write z=(x,y), w=(u,v). The four source equations independently reconstructed
from the displayed affine points are

    F0 = N(x,y)-1,
    F1 = N(u-1,v)-1,
    F2 = N(u-x,v-y)-3,
    F3 = N(u-v-x-y,u+2v-1+x)-1.

The certificate supplies a rational midpoint m, rational matrix Y, and
radius r=10^-35. The checker derives each gradient and constant Hessian
directly from these equations. In the infinity norm it computes

    beta = ||I-Y DF(m)||,
    q = beta + r max_a sum_i |Y[a,i]| sum_jk |H_i[j,k]|,
    d = ||Y F(m)|| + q r.

Exact rational arithmetic proves beta<10^-64, q<10^-33, and d<10^-68<r.
Thus T(s)=s-YF(s) is a strict contraction from the closed radius-r box into
itself. Banach's theorem gives a unique fixed point there. The independently
computed determinant of Y is nonzero, so fixed points of T are precisely
zeros of F. This proves existence and uniqueness inside the certified box;
it makes no assertion about roots elsewhere.

## 2. Exact source edges

The nine source points are independently written as affine triples over K in
1,z,w. Dense polynomial expansion finds exactly five squared-norm classes on
the 15 declared source edges:

    1, 1+F0, 1+F1, 1+F2/3, 1+F3.

At the isolated root all are one. Multiplication by each of the six powers of
rho yields exactly 30 oriented unit directions. The checker constructs an
edge only when a formal point difference is one of these directions.

## 3. Complete closure and physical realization

For every current unit segment a,b, the next support adds

    a + rho (b-a),  a + (1-rho)(b-a).

All affine triples are exact and equal triples are merged. At each round the
review rebuilds the full formal unit graph, rather than carrying only the
generating edges. It reproduces all ten point/edge censuses and independently
records the redundant completion attempts caused by old points and
collisions.

Formal equality alone does not exclude accidental equality or unit distance
at the selected algebraic root. For that bridge, every coordinate affine in
x,y,u,v is evaluated at m. The coordinate error is bounded by r times the
sum of the absolute affine coefficients. Rational interval multiplication
then encloses N(A,B) for every pair.

The audit checks all C(432,2)+C(533,2)=234,874 pairs. Every distinct formal
pair has squared distance greater than 10^-4. Every undeclared pair has
squared distance separated from one by more than 10^-3. Declared edges are
already exactly unit by the symbolic direction proof. Therefore rounds 8 and
9 are genuine complete plane unit-distance graphs with 432/1,134 and
533/1,415 points/edges. Because earlier supports are subsets, the same late
audit also rules out missed earlier collisions or unit edges.

## 4. Chromatic conclusion

Canonical restricted-growth enumeration fixes the first source colour to
zero and explores every colouring up to colour relabelling. It finds no
proper source three-colouring and 72 proper canonical four-colourings. Hence
the source, and every closure containing it, needs at least four colours.

The target's literal 432-character word is checked directly against every
round-8 edge and is proper. Thus round 8 has chromatic number exactly four.
No SAT result is a proof premise.

Round 9 has 533 distinct points. Consequently round 8 is the last complete
stage of this exact closure sequence with at most 508 points.

## 5. Upstream correspondence

At Shibuya commit 218097c9971db2b60ab94a0b8dae20d76741cc43, function
ud93_vertices builds A,B,p0,...,p6 from one angular parameter using circle
intersections. Evaluating that pinned parametrization and this review's
ordered affine points at 100 digits gives maximum coordinate disagreement
1.0579e-90 and identical 15-pair unit edge lists. This is a source-integrity
check, not part of the exact theorem.
