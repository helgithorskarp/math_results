# Independent review of the twelve-high-vertex distant-incidence bound

## Verdict and exact scope

**Accepted within its stated scope.**  No mathematical or reproducibility
defect was found in Discovery Net lemma
`bafkreia6cu66xfedqzzunnk2rjyt2hs4it3klu3qxvlvp3iubpiopqx7uu`
(height 4351), reviewed at source commit
`b5a99636a842d8b91d676958cc854462f48d505d`.

The accepted theorem is this: if a finite simple graph has 54 vertices, 187
edges, girth at least five, and exactly twelve degree-eight vertices, then the
sum

```text
A = sum_{t in V8} |{v : dist(t,v)>2}|
```

is at most three.  Hence at least nine degree-eight vertices are radius-two
sinks.  This does not exclude the cases `A=0,1,2,3`, does not exclude every
187-edge graph, and does not improve the current numerical interval
`185 <= ex(54,{C3,C4}) <= 187`.

## Hand-proof audit

The imported exact value `ex(53,{C3,C4})=181` gives minimum degree six by
vertex deletion.  The radius-two ball bound gives maximum degree eight, and
the degree equations give

```text
(n6,n7,n8)=(16,26,12).
```

For `T=V8`, put `a_t=|F(t)|`, `A=sum a_t`, `H=G[T]`, `m=e(H)`, and let `k`
count the degree-two vertices of `H`.  I independently rederived the target's
high-neighbor counts, pair inventory, weighted-gap equation, and corrected
commutator balances.  In particular,

```text
sum_V6 c = 36+A+2m
sum_V7 c = 60-A-4m
B = 8-m-k-q-A >= 0
Q + sum_t a_t(a_t+4) + 2U = 28
sum epsilon = 4+A
sum c*epsilon = 2m+R-p7-4q,   with R <= A+k.
```

The correction terms `p7`, `q`, and `R` have the stated signs and
multiplicities; no all-sink assumption is smuggled into these equations.  The
matrix identity behind the individual cover is also correct:

```text
(8-d(v))*[t in C(v)] + sum_{u in F(v)} [t in C(u)]
  = 8-d(v) + |F(t) intersect N(v)|.
```

It follows directly from the distance definition and the commutator of the
adjacency and far-pair matrices.

The local sign classification is complete.  Degree-six terms
`(c-3)*epsilon` are nonnegative; the only negative degree-seven types are
`(c,epsilon)=(1,1),(2,1),(2,2)`.  When `B<=2`, the individual-cover identity
forces their total negative charge `W` to satisfy `W<=9B`.  Applying this to
all allowed high-deficit partitions excludes `A=5`.

For `A=4`, the exact certificate below gives integral `m>=2`.  The inventory
and charge inequalities leave only

```text
(m,k,q)=(2,0,0), B=2,
V6: c2^6 c3^8 c4^2,
V7: c1^4 c2^22.
```

The two `c=4` sets are degree-six vertices and exhaust the positive inventory.
If a negative type `(1,1)` exists, its far sets force a `4+4+3+1` partition
of `T`.  The no-four-cycle intersection rule then excludes every type `(2,1)`
vertex; the remaining charge is too small.  Thus no type `(1,1)` exists.

The epsilon equalities now force exactly sixteen type `(2,1)` vertices,
`p7=0`, `Q=N=8`, four high deficits all equal to one, and `R=4`.  Therefore
the four nonsink high vertices are precisely the endpoints of a two-edge
matching.  The unique vertex missed by one endpoint is degree six, has at
least two high neighbors, and can only meet the two endpoints of the other
edge.  Those endpoints are adjacent, producing a triangle.  This final
contradiction excludes `A=4`.

## Exact certificate and independent evidence

The submitted standard-library checker passed in ordinary and optimized
Python, byte-for-byte against its expected JSON.  It checks 72 local types,
1,638 type-edge variables, the graph controls, all arithmetic branches, and
the finite set arguments.

The sole numerical input is a rational dual certificate for `m>1` when
`A=4`.  A fresh run with CPython 3.11.2, NumPy 2.4.6, and SciPy 1.15.3
regenerated it byte-for-byte, with SHA-256
`9bdafe9393feb95cb5496c91ca7e53d4737a7db0b4c6522cca55aa3536acc6cf`.

[`independent_exact_audit.py`](independent_exact_audit.py) imports none of the
submitted modules.  It reconstructs every type and admissible type-edge, then
evaluates the sparse dual directly column by column from the mathematical
variable meanings.  With 1,710 columns it recovers

```text
dual right side              981743/500000
maximum coefficient excess       11/500000
graph-derived variable budget            428
corrected lower bound          195407/100000 > 1.
```

The budget is `sum X + sum Y <= 54+374`: diagonal `Y` variables count
internal edges twice and off-diagonal variables once, so their sum is at most
the total degree 374.  Nonnegative variables and the displayed coefficient
excess therefore make the rounded rational certificate rigorous.  Solver
success and floating-point tolerances are outside the proof boundary.

The clean-room script also enumerates the local signs, high-deficit
partitions, aggregate charge cases, unique terminal equality state, surviving
low profile, both canonical type-`(2,1)` set cases, and the four choices in the
terminal matching.  Run from this review directory:

```sh
python3 independent_exact_audit.py ../z12_four_defects_certificate.json \
  | diff -u EXPECTED_OUTPUT.txt -
```

The result is identical under `python3 -O`.

## Source and trust boundary

The primary Afzaly--McKay
[extremal-graph catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
states that the girth-five value at order 53 is exactly 181 and labels the
order-54 entry only as the lower bound 185.  The 2025 primary
[Goedgebeur--Jooken--Joret--Van den Eede preprint](https://arxiv.org/abs/2508.05562)
independently describes its contribution as lower-bound search beyond the
range of exact methods.  These sources align with the target's prerequisite
and claim boundary.  No historical-priority conclusion is drawn.

The residual trust is the published order-53 value, the hand derivation of
the incidence identities and graph-to-LP implication, Python integer/rational
arithmetic, and the two independent implementations.  The target file has one
cosmetic form-feed before `frac12` in its displayed objective, and much of its
LaTeX uses literal parentheses rather than math delimiters; neither changes
the unambiguous certificate definition or proof.
