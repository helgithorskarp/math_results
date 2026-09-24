# Shortened syndrome templates give an upper constant six

Write `+` for addition in a binary vector space (integer bitwise XOR in the
certificate). A graph is square-saturated in `Q_n` if it contains no square
and adding any missing cube edge creates one.

**Theorem.** For every integer `n >= 14`,

\[
 \operatorname{sat}(Q_n,Q_2)
 < \left(6+\frac{49}{n+2}\right)2^n.
\]

Consequently

\[
 \limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le6.
\]

This is an upper bound, not an exact saturation number or a proof that the
normalized sequence converges. The finite certificate checks and the universal
lemmas below have separate roles: the checks prove three finite premises; the
lemmas extend those premises to every required dimension.

## 1. A finite certificate and its replication

Let `U = F_2^k`, `q = |U|`, and let `T` be a subset of `U` containing zero and
spanning `U`. Let `C,D` be nonempty disjoint subsets of `U`, and put `A=C union D`.
The certificate consists of a graph `R_0` on `U` and sets `N_x subset A` for
all `x in U`.

An **affine square** is a four-cycle on four distinct vertices whose sum is
zero. We require the following finite conditions.

1. Every edge `uv` of `R_0` has `u+v in T` and meets `A`. The sets `C,D` are
   independent dominating sets in `R_0`. The graph has no affine square.
2. Every missing edge `uv` with `u+v in T` and `{u,v}` meeting `A` has a
   three-edge path `u,w,u+v+w,v` in `R_0`.
3. Each `N_x` meets both `C` and `D`, and `x+a in T` for every `a in N_x`.
4. For distinct `a,b in A` and every `x in U`, it is not the case that both
   `N_x` and `N_{x+a+b}` contain `{a,b}`.
5. If `a in A`, `x+a in T`, and `a not in N_x`, there is `b in N_x` with
   `{a,b} subset N_{x+a+b}`.

Let

\[
 r_0=e(R_0),\qquad r_1=\sum_{x\in U}|N_x|,\qquad a=|A|,\quad t=|T|.
\]

Take any `m=2^s`, with `s>=0`, and `W=F_2^s`. In `V=U x W`, use the coordinate
labels

\[
 S=(T\times W)\setminus\{(0,0)\},\qquad \ell=tm-1.
\]

The quotient graph `R` has the copy of `R_0` on `U x {0}` and, for each
nonzero `z in W`, the edges

\[
 (a,0)(x,z)\quad\text{for }a\in N_x.
\]

There are no other edges. Its centers are `A x {0}`.

**Replication lemma.** `R` is affine-square-free, has the two disjoint
independent dominating classes `C x {0}` and `D x {0}`, and every missing
allowed edge incident with its centers has an affine three-edge witness.
Moreover

\[
 |V|=qm,\qquad e(R)=r_0+(m-1)r_1.
\]

*Proof.* Independence and domination follow from conditions 1 and 3. Every
edge meets the centers. An affine square wholly in `U x {0}` is excluded by
condition 1. Any other possible square must have exactly two opposite center
vertices: adjacent centers would force an edge between two noncenters, while
three centers and one vertex with nonzero `W` coordinate cannot sum to zero.
With opposite centers `(a,0),(b,0)`, the other vertices must be `(x,z)` and
`(x+a+b,z)` for the same nonzero `z`. Condition 4 excludes it.

For a missing allowed boundary edge wholly in the core, condition 2 supplies
the witness. For `(a,0)(x,z)`, `z!=0`, condition 5 supplies

\[
 (a,0),\ (x+a+b,z),\ (b,0),\ (x,z).
\]

These are distinct: `a!=b` because `a not in N_x`, and the two noncenter
vertices have distinct `U` coordinates. All three path edges are present.
The edge count follows by separating the core and the `m-1` other layers. QED.

## 2. From quotient to cube block

Give the `ell` cube coordinates the distinct nonzero labels in `S`. The
syndrome map is

\[
 \sigma:\mathbb F_2^\ell\longrightarrow V,
 \qquad \sigma(v)=\sum_{i:v_i=1}s_i.
\]

It is surjective. Indeed `T x {0}` spans `U x {0}`, and the labels `(0,z)`
span `{0} x W`; these labels exist because `0 in T`. Thus every fiber has
`2^ell/(qm)` vertices.

Select a cube edge precisely when its two syndromes form an edge of `R`.
Call the resulting graph `H`, and use the syndrome inverse images of the
center classes as `C_H,D_H,A_H`.

Two distinct nonzero coordinate labels are linearly independent over `F_2`.
Hence every cube square maps to an affine square on four distinct syndrome
vertices, so `H` has no square. The classes are independent and dominating:
any incident quotient edge prescribes a unique coordinate to flip.
Every edge of `H` meets `A_H`.

Every missing cube edge incident with `A_H` is saturated inside `H`. To see
this, let its syndrome difference be `d in S`. An affine three-edge quotient
witness uses the directions `e,d,e` for a distinct `e in S`. Flipping those
physical coordinates lifts the witness through the specified cube edge.

Each unordered quotient edge corresponds to exactly `2^ell/(qm)` cube
edges: orient it from one specified syndrome fiber. Consequently the exact
block parameters are

\[
 h:=\frac{e(H)}{2^\ell}=\frac{r_0+(m-1)r_1}{qm},
 \qquad
 \delta:=\frac{|A_H|}{2^\ell}=\frac{a}{qm}.
 \tag{1}
\]

Only distinct labels are used. Repeating a coordinate label would invalidate
the square-projection argument.

## 3. The three finite certificates

All integers below denote binary vectors, with the least significant bit
first. The complete data are in [templates.json](templates.json).

| Name | q | C | D | T | r_0 | r_1 |
|---|---:|---|---|---|---:|---:|
| H | 4 | {0} | {1,2} | {0,1,2,3} | 4 | 8 |
| S | 4 | {0,1} | {2,3} | {0,2,3} | 3 | 8 |
| F | 16 | {0,1} | {2,4,8} | {0,1,2,5,7,8,11,12,14,15} | 29 | 33 |

For H, the core edges are `01,02,03,13`, and the four rows `N_0,...,N_3`
are `{0,1},{0,2},{0,2},{0,1}`. This recovers the accepted Hamming-block
construction.

For S, the core edges are `03,12,13`, and the four rows are
`{0,2},{1,3},{1,2},{0,3}`. The sole missing allowed core edge is `02`, with
path `0,3,1,2`. For the missing outside incidence in rows `x=0,1,2,3`, the
missing center `a` and witness center `b` are respectively
`(3,0),(2,1),(0,2),(1,3)`; condition 5 follows immediately. Each unordered
pair of centers occurs in just one row, establishing condition 4.

For F, the core edges, grouped by smaller endpoint, are

```text
0: 2 5 7 8 11 12
1: 3 4 6 9 10 13 14 15
2: 3 7 10 12 14
3: 8
4: 5 6 11 12 15
6: 8
7: 8
8: 9 13
```

Its outside rows are

| x | N_x | x | N_x |
|---:|---|---:|---|
| 0 | {1,8} | 8 | {0,8} |
| 1 | {1,4} | 9 | {1,2} |
| 2 | {0,2} | 10 | {1,8} |
| 3 | {1,2} | 11 | {0,4} |
| 4 | {1,8} | 12 | {0,4} |
| 5 | {0,4} | 13 | {1,2} |
| 6 | {1,4,8} | 14 | {0,2} |
| 7 | {0,2} | 15 | {0,8} |

There is one row of degree three and fifteen of degree two, giving `r_1=33`.
[check_templates.py](check_templates.py) verifies every condition directly:
for F this includes all 420 core affine cycles, 160 outside rectangle tests,
11 missing core boundary edges, and 17 missing outside incidences.
[audit.py](audit.py) independently reconstructs the full quotient graphs at
`m=1,2,4,8` and checks their defining graph properties without importing the
finite-condition checker or the constructor.

The three block families therefore have these exact parameters:

| Name | ell | h | delta |
|---|---|---|---|
| H(m) | 4m-1 | 2-1/m | 3/(4m) |
| S(m) | 3m-1 | 2-5/(4m) | 1/m |
| F(m) | 10m-1 | 33/16-1/(4m) | 5/(16m) |

Here and below every scale `m` is a positive power of two. Solver searches
found S and F; the theorem uses their explicit certificates, not solver
soundness or any claim that these certificates are optimal.

## 4. General two-block composition

Suppose two blocks `H_I subset Q_i`, `H_J subset Q_j`, with `i,j>=2`, have
all the properties proved in Section 2. Their center classes need not have
equal sizes. Write their normalized edge counts and center densities as
`h_I,h_J,delta_I,delta_J`. Let `n=i+j+r`, `r>=0`, and write vertices as
`(x,y,z)` on coordinate blocks `I,J,K`.

For any cube edge, its **lower parity** means the parity of the Hamming weight
of its lower endpoint in the specified coordinate set (the endpoint with
zero in the changing coordinate).

Start with the following union of edges:

- copies of `H_I` and `H_J` in their coordinate directions;
- at each fixed `x in C_I`, all complementary edges of lower parity zero,
  and at each fixed `x in D_I`, those of lower parity one;
- the analogous complementary edges at `y in C_J` and `y in D_J`.

Delete every edge incident with

\[
 B=A_I\times A_J\times Q_r,
 \qquad |B|=\delta_I\delta_J2^n.
\]

Call the graph after deletion `G`.

**Square-freeness.** Every selected edge has an endpoint whose `I` or `J`
part is a center. Suppose a putative square has an `I` part in `A_I`. If it
also had a `J` part in `A_J`, the Cartesian face would contain their combined
corner in `B`, which is isolated. Thus all its `J` parts avoid `A_J`.

If two free coordinates lie in `I`, its edges must be in `H_I`, impossible.
If neither lies in `I`, the edges come from a single parity layer; each
2-face has two edges of each lower parity, so it is not a square. If exactly
one lies in `I`, the two complementary edges have the same lower parity
outside `I`. Both `I` endpoints must therefore belong to the same class
`C_I` or `D_I`. The two `I`-edges must be edges of `H_I`, contradicting
independence of that class. The case starting with a center in `J` is
symmetric.

**Saturation away from B.** Consider a missing edge whose endpoints avoid B.
For an edge changing a coordinate in `I`, there are three cases.

- If `y not in A_J` and at least one `I` endpoint is in `A_I`, the block's
  boundary witness lies in the same `I` layer and avoids `B`.
- If `y not in A_J` and both `I` endpoints avoid `A_I`, choose an `H_J`
  neighbor of `y` in the `C_J` or `D_J` class matching the edge's lower
  parity outside `J`. Domination supplies this neighbor. The two `J` edges
  and the opposite parity-layer edge form the required three-edge path.
- If `y in A_J`, both `I` endpoints avoid `A_I`. The missing edge has the
  wrong parity for the class containing `y`. Domination by the other class
  supplies an `H_J` neighbor in that class; its layer contains the opposite
  edge. Again the two `J` edges complete the witness.

All these witnesses avoid `B`. Edges changing `J` follow symmetrically.
For an edge changing `K`, its `I,J` parts cannot both be centers. If neither
is a center, choose an `H_I` neighbor in the class matching the lower parity
outside `I`. If exactly one is a center, use a neighbor in the opposite
class of that same block. The two block edges and the opposite `K` edge
are the witness; they again avoid `B`.

Greedily consider all remaining missing edges incident with `B`, adding an
edge precisely when it does not create a square. At most `n|B|` edges are
added. Previously witnessed missing edges remain witnessed. A rejected edge
has a permanent witness, so the final graph is square-saturated.

**Counting.** In a cube of dimension `d>=2`, each lower parity contains
exactly `d*2^(d-2)` edges: for each changing coordinate the remaining `d-1`
coordinates split equally by parity. Count the starting union with
multiplicity and ignore deleted edges. Including greedy completion gives

\[
 \frac{\operatorname{sat}(Q_n,Q_2)}{2^n}
 \le h_I+h_J+
       \frac{(n-i)\delta_I+(n-j)\delta_J}{4}
       +n\delta_I\delta_J.
 \tag{2}
\]

This composition is the accepted upper-seven argument with arbitrary
certified blocks substituted for its Hamming blocks. The proof above makes
explicit why unequal class sizes and shortened label sets are permitted.

## 5. Parameter selection and the constant six

Set `x=n+2`. There is a unique power of two `m` with
`16m <= x < 32m`. This exists for `n>=14`. Choose blocks according to the
following table; the unused coordinates form `K`.

For a block let `L=ell+1`, and let `h_infty` be its limiting normalized edge
count: `2` for H and S, `33/16` for F. The table bounds

\[
 P(x)=h_{I,\infty}+h_{J,\infty}
      +\frac{\delta_I(x-L_I)+\delta_J(x-L_J)}4,
 \qquad M(x)=x^2\delta_I\delta_J.
\]

Both functions are increasing on each listed interval. Values in the last
two columns are their values at the excluded upper endpoint.

| Range of x/m | Blocks | (L_I,L_J)/m | P at upper endpoint | M at upper endpoint |
|---|---|---|---:|---:|
| [16,18) | H(2m), H(2m) | (8,8) | 47/8 | 729/16 |
| [18,20) | H(2m), F(m) | (8,10) | 191/32 | 375/8 |
| [20,22) | H(2m), S(4m) | (8,12) | 95/16 | 363/8 |
| [22,24) | F(m), S(4m) | (10,12) | 189/32 | 45 |
| [24,28) | S(4m), S(4m) | (12,12) | 6 | 49 |
| [28,32) | S(4m), H(4m) | (12,16) | 6 | 48 |

In each row `L_I+L_J<=x`, so the padding is nonnegative. For example, the
second row has

\[
 P(x)=\frac{81}{32}+\frac{11x}{64m},\qquad
 M(x)=\frac{15x^2}{128m^2}.
\]

All six leading endpoints are at most six, and all completion endpoints are
at most 49. Since `h<h_infty`, `n-ell=x-L-1<x-L`, and `n<x`, equation (2)
is strictly smaller than

\[
 P(x)+\frac{M(x)}x\le6+\frac{49}x.
\]

This proves the theorem. [audit.py](audit.py) checks these exact rational
identities, parameter choices for `14<=n<=4096`, and dyadic endpoint cases
through exponent 60. The table and inequalities, rather than that finite
range of arithmetic tests, prove the assertion for all n.

## 6. Scope, literature, and trust boundary

Johnson and Pinto's [Saturated Subgraphs of the Hypercube](https://arxiv.org/abs/1406.1766)
proves a uniform coefficient ten and records coefficient six on the special
dimensions `n=2(2^t-1)` in Section 4.2. Morrison, Noel, and Scott's
[Saturation in the Hypercube and Bootstrap Percolation](https://arxiv.org/abs/1408.5488)
proves the order `Theta(2^n)` for fixed forbidden subcubes.

The immediately preceding graph contribution
`bafkreihymxy3z5qbwukjqnahkhym24ummet7sxwoqtbno5t4isz2phazv4`
proved a uniform asymptotic coefficient seven and a subsequence coefficient
`11/2`; see the [upper-seven source](../hypercube_square_saturation_upper7/README.md)
and its [independent review](../hypercube_square_saturation_upper7_review1/REVIEW.md).
The new replication lemma, shortened S and F blocks, and six-interval
selection improve the uniform coefficient to six. They do not improve the
previous `11/2` subsequence bound. Targeted primary-source searches on
2026-09-24 found no prior uniform constant-six proof; this is search-relative
novelty, not a historical priority claim.

The three finite premises are small, explicit exact certificates. They are
checked by ordinary Python integer/set operations and by an independent full
quotient reconstruction. No external dataset, floating-point decision, solver
optimality, or retained UNSAT trace is used. The universal replication,
syndrome lift, composition, completion, and counting arguments remain
ordinary mathematical proofs, not proof-assistant formalizations. Expanded
cube checks are corroborating finite evidence, not the reason the universal
quantifiers hold. External review of this new contribution is pending.
