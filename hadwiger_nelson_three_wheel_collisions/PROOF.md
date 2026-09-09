# Complete physical decision of the coincidence branch

Use the architecture and wheel order in README.md. Put `mu6={omega^j:0<=j<6}`
and `D=W-W`. Direct enumeration gives

```
D={0} union mu6 union (1+omega)mu6 union 2mu6.
```

Thus each nonzero squared norm `1,3,4` is one six-element rotation orbit.
The verifier checks this identity from the literal 49 wheel differences.
All statements refer to Euclidean point sets, not abstract graph quotients
with unverified edges.

## 1. Reduction of every collision

A collision of different labels gives `d+u e+v f=0`, with `d,e,f in D`.
One nonzero coefficient cannot vanish. With exactly two nonzero coefficients,
their lengths must agree. The orbit identity forces `u`, `v`, or `u/v` into
`mu6`. Such a graph is congruent to `H19+qW`, where `H19=W+W`, so it has at
most `19*7=133` points. Since `W subset H19`, the accepted h4005/h4031 theorem
on `H19+qH19` supplies a four-colouring. This uses that theorem as a premise;
it does not reopen its retired search family.

Suppose all three coefficients are nonzero. Permute the three summands so
their displacement squared norms satisfy `m<=n<=p`. Independent multiplication
of each summand rotation by a sixth root preserves its wheel. After these
changes and a global rotation, the equation takes the form

```
d+u e+v f=0,
d=r_m, e=r_n, f=r_p,
r_1=1, r_3=1+omega, r_4=2.
```

Set `K=p-m-n` and `Delta=4mn-K^2`. Taking the norm of `d+u e` gives

```
2 Re(conj(d)e u)=K,
u=(K +/- i sqrt(Delta))/(2 conj(d)e),
v=-(d+u e)/f.
```

All ten sorted triples from `{1,3,4}` have nonnegative discriminant. Their
two signs give congruent physical graphs: reflection in the line through
`d` is `z -> (d/conj(d))conj(z)`. Each ratio `r_j/conj(r_j)` is a sixth
root, so this reflection preserves W and changes the other wheel rotations
only by conjugation and harmless sixth roots. The degenerate sign is single.

| Norm triple | Delta | Classification |
|---|---:|---|
| 1,1,1 | 3 | aligned: representative u=omega^2 |
| 1,1,3 | 3 | aligned: u=omega |
| 1,1,4 | 0 | aligned: u=1 |
| 1,3,3 | 11 | physical case 1 |
| 1,3,4 | 12 | aligned: u=omega |
| 1,4,4 | 15 | physical case 2 |
| 3,3,3 | 27 | aligned: u=omega^2 |
| 3,3,4 | 32 | physical case 3 |
| 3,4,4 | 39 | physical case 4 |
| 4,4,4 | 48 | aligned: u=omega^2 |

The checker verifies the six alignment identities in Q[i sqrt(3)]. This
classifies every noninjective member. The four remaining graphs each have
more than 133 vertices, so none is secretly pair-aligned. Their distinct
(vertex count, edge count) signatures prove they are four distinct classes.

## 2. Exact physical coordinates and exhaustive unit edges

For each unaligned case let `s=i sqrt(3)`, `t=i sqrt(Delta)`. The positive
circle root above gives the exact parameter table in `verify.CASES`; the
checker validates both unit norms, the collision equation, and
`conj(d)e u=(K+t)/2`. The four basis elements `1,s,t,st` are independent over
Q: `-3` and `-Delta` are nonsquares and `3Delta` is a positive nonsquare.

The canonical sorted physical points are coefficient tuples `(A,B,C,D)/q`
representing the complex number `(A+B s+C t+D st)/q`. In ordinary real
coordinates this is

```
x=(A-D sqrt(3Delta))/q,
y=(B sqrt(3)+C sqrt(Delta))/q.
```

Every label is constructed directly from W and the parameters, equal tuples
are identified, and the common denominator is reduced. For a difference
tuple `(A,B,C,D)/q`, its squared absolute value is

```
[A^2+3B^2+Delta*C^2+3Delta*D^2 + 2(AD-BC)st]/q^2.
```

It is exactly one if and only if the integer scalar coefficient equals
`q^2` and `AD=BC`. Independence of `1,st` proves both directions; no tolerance
or floating test occurs. Checking all distinct pairs gives the table in
README.md, with 210,996 pair tests in total. Each certificate digit refers to
one physical point in lexicographic coefficient order. Properness is checked
on every strict unit edge. The two four-colour words were discovered by SAT;
their validity, rather than the SAT solver's verdict, proves the upper bound.

## 3. Exact chromatic numbers

Each graph contains the unit triangle `0,1,omega`, so its chromatic number
is at least three. The wheel has the unique three-colouring
`c(a+b omega)=a-b mod3`, up to palette permutation. The h4047 affine-layer
argument, applied as in h4065 Section 2, proves that every three-colouring of
the three-wheel Cartesian product is, up to a global palette permutation,

```
C_s,t(a,b,c)=c(a)+s*c(b)+t*c(c),  s,t in {1,-1}.
```

For clarity, restrict to the first-wheel layers. Their palette permutations
are affine over F3; adjacent layers must have equal slopes because unequal
slopes agree at one colour. Connectivity makes the slope constant. The
offsets colour the product of the other two uniquely three-colourable wheels,
to which h4047 applies. This does not assume that a two-wheel product is
itself uniquely three-colourable.

Any physical three-colouring pulls back to such a product word: a Cartesian
edge changes one coordinate by a unit vector and can never collapse. For
case `(1,3,3)`, coincident labels `(0,5,5)` and `(1,1,1)` receive different
colours in all four words. For case `(3,3,4)`, the same is true of `(1,1,6)`
and `(3,3,3)`. The checker verifies the coincidences and all four failures;
these two physical graphs are therefore exactly four-chromatic. For cases
`(1,4,4)` and `(3,4,4)`, respectively `C_-1,-1` and `C_1,-1` descend and are
proper on every physical unit edge. Their certificate words use three colours.

## 4. Exact count of parameter pairs

Each of the four unaligned norm multisets has three distinct orderings.
For any ordering the displacement triple has `6^3` choices. Simultaneous
sixth-root multiplication leaves the equation unchanged and acts freely,
so there are `3*6^3/6=108` equations. Each has at most two unit-circle roots,
giving at most 216 ordered pairs `(u,v)` for that norm multiset.

For the converse bound the checker takes the representative rotations
`(1,u,v)`, permutes them, divides by the first rotation, independently
multiplies the two remaining rotations by sixth roots, and also conjugates.
These are physical symmetries and preserve a collision of the same norm
multiset. Exact coefficient comparison finds **216 distinct nonaligned
pairs** in each orbit. This matches the upper bound, so the count is exact.
The four orbits are disjoint, since equal parameters would give equal
physical graphs, whereas their size/edge signatures differ. Hence there
are exactly `4*216=864` nonaligned collision parameter pairs.

## 5. Whole-architecture consequence and trust boundary

All noninjective members are four-colourable. Outside alignment, the only
possible physical orders are therefore `301,331,337,343`; only order 343 can
possibly be non-four-colourable. In h4065 the injective common-failure
frontier already had bound 902,481; its separate 1,836-point collision
allowance can now be removed. This is a necessary frontier, not positive
non-four-colourability evidence and not a decision of the remaining graphs.

The final prepublication refresh found HN-3's h4071, which independently
classifies the same four collision norm types and bounds the injective
frontier by 5,110 physical classes across 800 representative factor pairs.
Our new chromatic decisions remove its four undecided collision classes:
the combined whole-architecture bound is now **5,110**, all of order 343.
`bridge.py` checks that h4071's exact quadratic Cayley representatives map
to precisely the complex rotations reconstructed here, by eight rational
coefficient identities `(1-s*x)u=1+s*x` and `(1-s*y)v=1+s*y`. It checks the
pinned h4071 certificate hash; no approximate root matching is used.
The 5,110-class corollary uses h4071 as a mathematical premise and does not
claim an independent review of its symmetry/intersection proof.

The proof uses the accepted alignment theorem, the written h4047/h4065
colour-lifting argument, exact enumeration and arithmetic in CPython, and
certificate decoding. The producer uses generic rational field multiplication
on labelled differences; the checker uses integer coordinates and all
physical point pairs. Entry-level point and edge hashes agree independently.
No CAS, floating predicate, SAT UNSAT verdict, external reviewer acceptance,
or proof-assistant formalization is assumed.
