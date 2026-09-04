# Cross-matrix normal form for the forced doubly exact `21+21` Ramsey anchors

In the hard branch of the local-extremal deficiency theorem, every hypothetical
43-vertex `(5,5)`-Ramsey coloring has at least ten vertices that split the
other vertices into two sets of size 21, with an exact `(4,5;21,100)` local
core on each color side.  This directory turns such an anchor into an exact
441-variable cross-matrix problem.

For fixed local cores, all remaining monochromatic-`K_5` conditions are
explicit clauses of length four or six.  The red cross matrix also has between
214 and 220 ones, with row and column intervals determined by the two local
degree sequences.  This is a lossless theoretical reduction for the balanced
hard branch.  It is not a 43-vertex construction, a claim that the reduced
instances are satisfiable, or a solver run.

## Anchored representation

Let `v` be one of the doubly exact vertices.  Put

```text
A = N_G(v),          |A|=21,
B = N_complement(G)(v), |B|=21.
```

Let

```text
H = G[A],
K = complement(G)[B].
```

The deficiency theorem forces both `H` and `K` to be `(4,5)`-Ramsey graphs
with exactly 100 edges.  Thus each has no `K_4` and no independent set of
size five.  Define the 441 Boolean variables

```text
x_(a,b) = 1  iff  the edge {a,b}, a in A and b in B, is red.
```

The red graph induced on `B` is the complement of `K`.

## Exact mixed-clique clauses

For a set `P` in `A` and `Q` in `B`, write `P x Q` for the cross edges between
them.  A red `K_5` meeting both sides can only have split

```text
(|P|,|Q|) in {(1,4),(2,3),(3,2)}.
```

Here `P` must be a clique of `H` and `Q` an independent set of `K`.  Such a
pair is forbidden exactly by

```text
OR_{(a,b) in P x Q} not x_(a,b).                       (R)
```

The missing split `(4,1)` cannot occur because `H` has no `K_4`.

Similarly, a blue `K_5` meeting both sides can only have split

```text
(|P|,|Q|) in {(2,3),(3,2),(4,1)}.
```

Now `P` must be an independent set of `H` and `Q` a clique of `K`, and the
exact forbidding clause is

```text
OR_{(a,b) in P x Q} x_(a,b).                           (B)
```

The missing split `(1,4)` cannot occur because `K` has no `K_4`.

These clauses are sufficient as well as necessary.  A monochromatic five-set
entirely within one side is excluded by the `(4,5)` properties of `H` and
`K`.  A monochromatic five-set containing `v` would require a `K_4` in `H`
or in `K`.  Every remaining five-set meets both `A` and `B`, and its only
possible split appears in (R) or (B).  Consequently satisfying all displayed
clauses is exactly equivalent to avoiding every monochromatic `K_5`, once the
two local cores are fixed.

If `c_i(H)` is the number of `i`-cliques of `H` and `a_i(H)` its number of
independent `i`-sets, the clause counts for arbitrary cores `H,K` are

```text
red  = c_1(H)a_4(K) + c_2(H)a_3(K) + c_3(H)a_2(K),
blue = a_2(H)c_3(K) + a_3(H)c_2(K) + a_4(H)c_1(K).
```

All red clauses have length four or six, as do all blue clauses.

## Cardinality and degree constraints

Exchange the colors if needed so that red is the sparser color.  The
deficiency theorem gives between 445 and 451 red edges globally.  At a doubly
exact anchor:

```text
21 red edges join v to A,
100 red edges lie inside A,
210-100=110 red edges lie inside B.
```

Therefore the number of red cross edges is

```text
214 <= sum_(a,b) x_(a,b) <= 220.                       (C)
```

Let `h_a` be the degree of `a` in `H` and `k_b` the degree of `b` in `K`.
The universal degree window `18,...,24` gives the per-row and per-column
constraints

```text
17-h_a <= sum_b x_(a,b) <= 23-h_a,                    (D_A)
k_b-2  <= sum_a x_(a,b) <= k_b+4.                     (D_B)
```

For `(D_B)`, the red internal degree of `b` in `B` is `20-k_b`.  Constraints
(C), `(D_A)`, and `(D_B)` are redundant consequences of a full correct
coloring, but are inexpensive pruning conditions in the reduced search.

Thus the balanced hard branch has a concrete pipeline: enumerate the
`(4,5;21,100)` core isomorphism types, choose an ordered pair `(H,K)`, and
solve only the 441 cross variables under (R), (B), (C), and (D).  This is a
local-core decomposition, not an unconstrained 903-edge search.

## Definition-level audit

`verify_cross_normal_form.py` exposes the clause-construction function and
audits it on a pinned `(4,5;21,100)` sample.  The sample is the induced graph
obtained from line 5 of the pinned McKay `r45_24.g6` catalog after deleting
source vertices 0, 1, and 8; its graph6 string is embedded so the default
audit has no external input.

The verifier directly enumerates all cliques and independent sets of the
sample.  They number

```text
size                    1    2    3   4  5
red cliques             21  100  113   0  0
blue cliques            21  110  175  75  0
```

Using the sample for both cores gives 31,505 distinct red clauses and 31,505
distinct blue clauses.  For four deterministic cross matrices, the verifier
then independently scans all `binom(43,5)=962,598` five-sets in the resulting
43-vertex coloring and checks that its direct red/blue `K_5` counts equal the
violated red/blue clause counts exactly.  It separately checks the cardinality
and degree formulas.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_cross_normal_form.py \
  | cmp - EXPECTED_OUTPUT.txt
```

Expected output is

```text
PASS sample (4,5;21,100) core red cliques=21,100,113,0,0
PASS sample core blue cliques=21,110,175,75,0
PASS exact mixed clauses: red=31505 blue=31505
PASS direct K5 equivalence on four deterministic cross matrices
PASS hard-branch cross ones=214,...,220 and degree bounds
```

The audit uses only the Python standard library, exact integers, and no
randomness, solver, floating point, network, or uncommitted data.  It took
about 24 seconds under CPython 3.11.2 on the research host.

## Scope, provenance, and trust boundary

The forced existence of at least ten doubly exact anchors is proved and
audited in the companion
[`ramsey_r55_local_extremal_deficiency`](../ramsey_r55_local_extremal_deficiency)
artifact, whose latest strengthening is commit
[`24d73d1b4ed4b8aee263e8513d91636942e90044`](https://github.com/helgithorskarp/math_results/commit/24d73d1b4ed4b8aee263e8513d91636942e90044).
That theorem imports the completeness of the official order-18-through-24
`(4,5)` extremal catalogs as its stated trust boundary.

The present cross-matrix equivalence is purely definitional once the two
local cores are supplied.  Its proof does not rely on the sample graph or the
catalog classification.  The sample only checks the implementation against a
nontrivial exact instance.

Discovery Net was searched through indexed height 2034 for the `R(5,5)`
problem neighborhood and for `21+21`, `cross matrix`, `local Ramsey`, and
`neighborhood`.  It contained one-vertex extension obstructions and separate
automorphism cycle-type reductions, but not this forced two-core cross-matrix
normal form.  Novelty is asserted only relative to the searched graph; no
historical-priority claim is made.

The next falsifiable milestone is a canonical catalog of
`(4,5;21,100)` cores followed by pairwise cross-clause feasibility.  The exact
normal form here specifies that task without committing this theory lane to a
particular solver or duplicating a whole-graph construction search.
