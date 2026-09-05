# Signature unions: 68 global hard-branch candidates and a forced half-cell

Common-neighborhood **union** bounds exclude five more global degree profiles
and 15 anchored splits in the hard branch of a hypothetical Ramsey `(5,5;43)`
graph. The inherited counts decrease from **73 to 68 global candidates** and
**290 to 275 split candidates**. This is a structural restriction, not a
43-vertex construction or an improvement to the Ramsey lower bound.

The complete finite scope is the 4,800 labeled exceptional cores with integer
signature-count witnesses in the preceding
[coupled-signature classification](../ramsey_r55_coupled_signature_counts/README.md).
They form 332 degree-preserving relabeling orbits in 17 global profiles,
all with at most six exceptional vertices. The new system has:

| status for the union-count system | orbits | labeled cores |
|---|---:|---:|
| integer feasible | 200 | 3,627 |
| infeasible even over the reals | 131 | 1,169 |
| real feasible, integer infeasible | 1 | 4 |

Every case has exact checked evidence. The last row is a genuine integrality
gap: a short argument forces a particular cell count to be `3/2`. Thus the
real/integer coincidence from the preceding, weaker system does not persist.

The 12 surviving small profiles have count witnesses only, not Ramsey graph
realizations. The 56 larger exceptional profiles remain unclassified here;
they are included in the 68 candidates. The low-deficiency branch remains
unresolved. No full-graph automorphism is assumed: the orbit quotient only
renames exceptional vertices having equal prescribed global degrees.

## 1. Inherited necessary conditions

Red denotes the sparser color of a hypothetical graph with no red or blue
five-clique. We assume the hard branch: every color-neighborhood has at least
seven fewer edges than the maximum for its order. The upstream
[degree sieve](../ramsey_r55_exceptional_degree_sieve/README.md) and
[vertex identity](../ramsey_r55_one_defect_anchor_localization/README.md) give
`m=231+M`, `214<=M<=220`, degrees 18 through 24, and

```text
sum_(w in N_R(v)) (d(w)-21) <= M-b(d(v)),
d       18   19   20   21   22   23   24
b(d)   220  221  220  220  221  223  223.                (1)
```

Let `E={v:d(v)!=21}`, `F=G[E]`, `k=|E|`, and `C=V(G)\E`, of size `N=43-k`.
The exceptional global degrees `d_i` are sorted increasingly. For a central
vertex its signature is `X=N_R(v) intersect E`; its cell multiplicity is `y_X`.
The inherited admissible signatures obey

```text
sum_(i in X) (d_i-21) <= M-220,
r_X=omega(F[X])<=3,     s_X=alpha(F[E\X])<=3.
```

The previous conservative capacity is
`c_X=min(N,choose(8-r_X-s_X,4-r_X)-1)`; all other signatures are forbidden.
The full old system, retained without weakening here, is

```text
sum_X y_X=N,
sum_(X containing i) y_X=d_i-deg_F(i),
0 <= y_X <= c_X,                  y_X integral.        (2)
```

We import the exact coverage and certificates of the prior system. Its 42
negative orbits, covering 137 labeled cores, are already excluded and are not
rerun as new cases. This contribution examines precisely its 332 positive
orbits. The new 131 real-negative orbits are different cases.

## 2. Common-neighborhood union cuts

Let `A,B` be disjoint subsets of `E`, with `A` a red clique and `B` a blue
clique (an independent set in `F`). Either may be empty, but not both.
Put `a=|A|`, `b=|B|`, and let `T_F(A,B)` be the exceptional vertices outside
`A union B` that are red-adjacent to all of `A` and blue-adjacent to all of `B`.
Write `t_F(A,B)=|T_F(A,B)|`.

The entire corresponding common neighborhood contains neither a red
`K_(5-a)` nor a blue `K_(5-b)`: either would extend through the fixed clique.
For any proved upper bound `U(p,q)>=R(p,q)`, therefore,

```text
W(A,B) := sum_(X superset A, X disjoint B) y_X
       <= U(5-a,5-b)-1-t_F(A,B).                       (3)
```

Subtracting `t_F` matters: the common neighborhood can include exceptional
vertices as well as central ones. Unlike individual cell bounds, (3) couples
many signatures that agree only on the rooted sets `A,B`. No requirement on
the cross edges between `A` and `B` is imposed.

The new system consists of (2) and **all** cuts (3) for the stated root pairs.
It introduces no unknown central-central edges. Positivity for this system
does not impose those edges, individual local edge-count caps, or full Ramsey
compatibility between the cells.

### A self-contained upper-bound table

Set `U(1,q)=U(p,1)=1`. If `P=U(p-1,q)` and `Q=U(p,q-1)`, use

```text
U(p,q)=P+Q-1 if P,Q are both even, and P+Q otherwise.   (4)
```

The usual neighborhood argument gives the sum bound. For the improvement,
a putative `(p,q)` graph on `P+Q-1` vertices must have every red degree at
most `P-1` and every blue degree at most `Q-1`. These bounds sum to its
degree sum `P+Q-2`, so every red degree equals the odd number `P-1`.
There are an odd number of vertices, contradicting the handshaking lemma.
This argument only needs valid upper bounds, not exact Ramsey numbers.

The resulting table is

| `p\q` | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 3 | 4 | 5 |
| 3 | 1 | 3 | 6 | 9 | 14 |
| 4 | 1 | 4 | 9 | 18 | 31 |
| 5 | 1 | 5 | 14 | 31 | 62 |

The `(5,5)` entry is unused because the roots are not both empty. In
particular we do not import a small-Ramsey catalog to justify these cuts.

## 3. New profile exclusions

An exponent is a vertex count, not an automorphism cycle multiplicity.

| excluded global degree multiset | `M` | input labeled cores | removed anchored splits |
|---|---:|---:|---:|
| `20^4 21^37 22^1 23^1` | 220 | 242 | 4 |
| `20^5 21^37 23^1` | 219 | 150 | 2 |
| `19^1 20^2 21^39 22^1` | 219 | 2 | 3 |
| `19^2 20^1 21^38 22^2` | 219 | 8 | 3 |
| `19^2 20^2 21^38 22^1` | 218 | 10 | 3 |

The complete entry-level table is [SUMMARY.tsv](SUMMARY.tsv). The remaining
global counts for `M=214,...,220` are `1,3,7,11,14,15,17`; the remaining
anchored split counts are `1,5,17,35,56,72,89`. The checker rederives these
from the pinned 104-profile upstream input and cumulative exclusions.

Corollary: if a hard-branch graph has at most six exceptional vertices, its
degrees **in the sparser color** belong to `{19,20,21,22}`. In particular,
a degree-23 vertex in this orientation requires at least seven exceptional
vertices. The preceding result already excludes degrees 18 and 24 in the
small stratum. The orientation qualifier must not be omitted for degree 23.

### A short hand proof of the four-exception profile

Take degrees `(19,20,20,22)` at labels `0,1,2,3`, with `M=219`.
The weighted row at vertex 0 forces edges `01,02` red and `03` blue; the
row at vertex 3 then forces `13,23` red. Only edge `12` is free. Thus `F`
is a four-cycle or the diamond `K_4` minus edge `03`, exactly masks 51 and 59.

For every central signature write `I_i=1[i in X]`. Its weighted condition is
`2I_0+I_1+I_2-I_3>=1`.

For the four-cycle it implies the pointwise inequality

```text
2-I_0-I_1-I_2 <= 1[I_0=I_3=0] + 1[I_0=1,I_1=I_2=0].
```

If `I_0=1`, this is immediate. Otherwise `I_1+I_2>=1`, and equality to
one forces `I_3=0`. Summing over the 39 central vertices gives
`25=78-17-18-18 <= W(empty,{0,3})+W({0},{1,2}) <= 13+8=21`, a contradiction.

For the diamond the same weighted condition implies

```text
1-I_0 <= 1[I_0=I_3=0] + 1[I_0=0,I_1=I_2=I_3=1].
```

When `I_0=0,I_3=1`, it forces `I_1=I_2=1`. Here `{1,2,3}` is a red
triangle, so summing gives `22=39-17 <= 13+3=16`, another contradiction.
These two proofs use union bounds, not numerical optimization.

## 4. The forced half-cell obstruction

Consider exceptional degree labels `(19,20,20,20,20,22)` and `M=218`.
Let `F` be the complete bipartite graph between `{0,1,5}` and `{2,3,4}`,
with the additional red edge `15`. Its edge mask is 27118. The central
incidence target vector is

```text
b=(N,r_0,r_1,r_2,r_3,r_4,r_5)=(37,16,16,17,17,17,18).
```

The weighted central condition is `2I_0+I_1+I_2+I_3+I_4-I_5>=2`.
There are 47 admissible signatures. Define

```text
D=2W(empty,{0,5})
  +W({0},{2,3})+W({0},{2,4})+W({0},{3,4})
  +2W({1},{0,5}),
T_j=W({1,5,j},{0})                   for j in {2,3,4}.
```

Equation (3) gives `D<=2*13+3*7+2*8=63` and `T_j<=3`.
Let `z=y_{ {1,2,3,5} }`, signature mask 46. Two pointwise inequalities,
summed with the multiplicities, give

```text
72=6N-3r_0-2(r_2+r_3+r_4) <= D+2T_4+2z <= 69+2z,
72=6N-3r_0-2(r_2+r_3+r_4) <= D+2T_2+2T_3-2z <= 75-2z.
```

Consequently **`2z=3`**, impossible for an actual cell count.

For completeness, the pointwise inequalities need no cell-size upper bound.
Let `a=I_0`, `b=I_1`, `c=I_5`, `t=I_2+I_3+I_4`. The left coefficient is
`L=6-3a-2t`; the coefficient in `D` is
`C=2(1-a)(1-c)(1+b)+a*choose(3-t,2)` (the binomial is zero for `t>1`).
We need `L<=C+2*1[T_4]+2*1[X=46]` and
`L<=C+2*1[T_2]+2*1[T_3]-2*1[X=46]`.

- If `a=1`, `L=3-2t<=choose(3-t,2)=C`; the other indicators vanish.
- If `a=c=0`, the weighted condition gives `b+t>=2`, hence `L<=2(1+b)=C`.
- If `a=0,c=1,b=0`, it forces `t=3`, so `L=C=0`.
- If `a=0,b=c=1`, it forces `t>=2`. For `t=3`, `L=0` and both right
  sides are nonnegative. For `t=2`, `L=2`: the two-element set in `{2,3,4}`
  either contains 4, when the `T_4` term and exactly one of `T_2,T_3`
  contribute, or is `{2,3}`, when `X=46`. Both bounds are then equalities.

The certificate also contains an exact denominator-two feasible solution to
**all** of (2)--(3) for this core. Thus this is not just a fractional solver
observation. The checker verifies that witness and the exhaustive integer
split `z<=1` or `z>=2`; both branches have exact contradictions `72<=71`.
There are four labeled copies under degree-preserving renaming. Other cores
of this global profile do survive, so the obstruction does not exclude the
whole profile.

## 5. Certificate format and exact checking

[CERTIFICATE.tsv](CERTIFICATE.tsv) has 332 rows, in precisely the order of
the prior positive records. Columns identify the degree counts, `M`, red
core mask, orbit size, kind, and a compact JSON payload. Pair-edge bit order
is lexicographic `(i,j)`, `i<j`; signature bit `i` means red adjacency to
exceptional vertex `i`.

- `primal`: sparse sorted `[signature,count]` pairs with positive integers;
  omitted cells are zero.
- `dual`: integer `lambda` for the equality rows and sorted `[A,B,mu]`
  triples, with positive integer `mu`, for the selected union rows.
- `split`: a signature and integer threshold, one dual for each halfspace,
  and a rational `real_primal` with one common positive denominator.

Write (2) as `Ay=b`, box upper bounds as `c`, and (3) as `Hy<=u`.
A dual certificate proves infeasibility by the strict integer inequality

```text
lambda*b > mu*u + sum_X c_X max(0,lambda*a_X-mu*h_X).   (5)
```

Indeed `lambda*b=lambda*Ay` is at most the right side for any nonnegative
real `y` satisfying the boxes and union rows. No floating tolerance occurs
in checking (5). The same rule handles either additional split inequality.
The largest coefficient magnitude among ordinary dual `lambda` vectors is
9, the largest root weight is 5, and at most ten root rows are used per dual.

The generator imports the pinned earlier generator only to reconstruct its
input systems. SciPy MILP discovers integer witnesses; LP proposes separators.
Rational reconstruction and exact checks authorize output. Every solver call
has a 20-second limit; any uncompleted or uncertified outcome aborts rather
than becoming an exclusion. Every call completed in the recorded run.

The solver-free checker does not import either generator or any numerical
package. It reruns the pinned upstream checker, which verifies all 209,443
raw cores of the 32-profile small universe and the preceding certificates.
It then reconstructs the input systems using that checker's Gray-code/set
implementation. For the new mathematics it enumerates root pairs by ternary
assignments, uses literal cliques and set intersections, and checks all
certificates after transport at **each of the 4,800 labeled cores**.

It also confirms that all 132 newly rejected orbit representatives' old
integer witnesses fail specifically a new union inequality. Mutated primal,
zero dual, overlapping-root and broken-split certificates are rejected.
[audit.py](audit.py) checks 149,504 root instances over all 1,022 labeled
Ramsey graphs on five vertices and three exceptional partitions each. It
builds valid 9- and 11-vertex fixtures that saturate a union bound after
subtracting one exceptional common neighbor, and checks the 47 half-cell
pointwise cases directly. These small fixtures are not target witnesses.

## 6. Reproduction

Checking needs Python 3.11.2 and its standard library only:

```bash
set -o pipefail
python3 ramsey_r55_signature_union_cuts/verify_certificate.py \
  | cmp - ramsey_r55_signature_union_cuts/EXPECTED_OUTPUT.txt
python3 -O ramsey_r55_signature_union_cuts/verify_certificate.py --emit-summary \
  | cmp - ramsey_r55_signature_union_cuts/SUMMARY.tsv
python3 -O ramsey_r55_signature_union_cuts/audit.py \
  | cmp - ramsey_r55_signature_union_cuts/EXPECTED_AUDIT.txt
cd ramsey_r55_signature_union_cuts
sha256sum -c SHA256SUMS
```

Optional regeneration uses NumPy 2.2.6, SciPy 1.15.3 and bundled HiGHS 1.8.0,
pinned in [requirements.txt](requirements.txt):

```bash
task_run=$(mktemp -d /tmp/r55-unions.XXXXXX)
python3 -m venv "$task_run/venv"
"$task_run/venv/bin/pip" install -r ramsey_r55_signature_union_cuts/requirements.txt
"$task_run/venv/bin/python" \
  ramsey_r55_signature_union_cuts/generate_certificate.py > "$task_run/certificate.tsv"
python3 ramsey_r55_signature_union_cuts/verify_certificate.py \
  --certificate "$task_run/certificate.tsv"
```

Verification takes about 18 seconds on the research host; regeneration
takes about five seconds. Regeneration with `-O` reproduced the stored
certificate byte-for-byte. A different valid certificate is acceptable if the exact
checker accepts it. Certificate SHA256:
`94448b3282ad4d5966303a01624f0cfddb78d966751830ffb8160598300f0bd3`.

## 7. Context, trust boundary, and next step

Neighborhood decomposition, Ramsey upper bounds and linear programming are
standard tools; see, for example,
[Angeltveit--McKay, R(5,5)<=46](https://arxiv.org/html/2409.15709v2), especially
Sections 2 and 4. This contribution applies such ideas to the team's
exceptional-degree hard branch and records an exact finite classification
and a forced-half-cell obstruction. No priority claim is made for the
general union-bound or separation principles. The refreshed committed graph
contained the preceding coupled counts but no overlapping union-cut result.

The new proof does not trust SciPy or HiGHS soundness. It does trust the exact
checking programs, Python runtime, and the unformalized graph-theoretic
arguments. The inherited catalog-completeness and hard-branch reductions
remain external dependencies, with pinned upstream inputs and source.
These checks are internal validation, not independent peer review.

The next mathematical boundary is actual compatibility of edges inside and
between the surviving signature cells, not another marginal capacity count.
The half-cell core gives a useful test case for any proposed relaxation.
No larger exceptional stratum, catalog radius, order-five branch or teammate
symmetry search is started here. This pass ends at the complete union-count
classification and its exact integrality obstruction.
