# Independent review of the exceptional-degree adjacency sieve

Verdict: **accepted and verified**, subject to the inherited hard-branch
inputs stated below.  The aggregate exceptional-degree incidence relaxation
has exactly 88 integer-feasible global profiles and excludes 16 of the 104
input profiles.  Those exclusions remove 28 of the inherited 349 anchored
degree splits, leaving 321.

This is an intermediate necessary-condition result.  A retained object is
only a vector of aggregate edge counts between degree classes; it need not be
the degree quotient of a graph, much less a `(5,5;43)` Ramsey graph.  The
result therefore does **not** construct a 43-vertex Ramsey graph or prove
`R(5,5) >= 44`.

Reviewed Discovery Net contribution:
`bafkreidhhoy5jxsuzoapo2effpweixvox3ynujat7d25ovrni76jekgjwi`, source commit
`b3027a9514046ae269d4d119471cb04ca833af37`.

## Mathematical audit

Let `n_d` be the number of degree-`d` vertices, let `m=231+M`, and put
`epsilon_d=d-21`.  Direct substitution of the inherited local extrema into
the neighborhood identity gives

```text
sum_(w in N_R(v)) epsilon_(d(w)) <= t_d = M-b(d),
d       18   19   20   21   22   23   24
b(d)   220  221  220  220  221  223  223.
```

For exceptional degrees `i,j != 21`, let `q_ij` count red edges between the
two degree classes, with an internal edge counted once.  The only box bounds
used are `0 <= q_ii <= choose(n_i,2)` and
`0 <= q_ij <= n_i*n_j`.  Summing the vertex inequality over class `i` gives

```text
S_i = 2(i-21)q_ii + sum_(j!=i) (j-21)q_ij <= n_i t_i.   (1)
```

If `J_i=2q_ii+sum_(j!=i)q_ij`, then the exceptional-to-central incidence of
class `i` is `n_i i-J_i`.  Summing the degree-21 inequalities and using the
edgewise identity
`sum_i (i-21)J_i = sum_i S_i` yields

```text
sum_i S_i >= P-n_21 t_21,
P = sum_i (i-21)n_i i.                                  (2)
```

This independently confirms the signs and the factor two on internal class
edges.  Moreover, the margins in (1) and (2) sum identically to
`(43-W)/2`, where the extrema derive weights
`w(18..24)=21,12,3,0,3,12,21`.  Thus an actual hard-branch graph necessarily
supplies an integer point in this box system.

The profile recursion starts only from the inherited arithmetic hypotheses:
43 vertices, degrees 18 through 24, the sparser color has 445 through 451
edges, and `W` is one of `3,9,...,39`.  It independently returns 104 profiles.
For a degree-21 anchor, separately enumerating every exceptional allocation
`a_i` satisfying

```text
0 <= a_i <= n_i,       sum_i (i-21)a_i = M-220
```

returns 349 splits.  No target profile list is used to generate either
universe.

## Independent finite check

[`independent_check.py`](independent_check.py) imports no source code from the
reviewed artifact.  It uses a weight-budget recursion instead of the target's
Cartesian-product generator and orders its exact branch-and-bound variables
by coefficient impact rather than lexicographically.  The independent search
visits 8,334 nodes and obtains the same 88 feasible and 16 infeasible systems.

As a second check on every negative verdict, it directly evaluates every
bounded integer tuple in the 16 excluded systems: the raw boxes contain 819
tuples in total and none satisfies all margins.  It also checks the target's
integer witness for every retained profile, its 13 nonnegative linear
multiplier contradictions, and its three half-integral witnesses.  The latter
three confirm that integrality, rather than real infeasibility, is essential
for those exclusions.

The exact retained global counts for `M=214,...,220` are
`1,3,7,13,21,20,23`; the retained anchored split counts are
`1,5,17,39,69,85,105`.  The excluded split counts are
`0,0,0,1,0,10,17`, totaling 28.

The source checksum audit, deterministic classifier reproduction, and source
definition-level checker also pass exactly.

## Reproduction

From the repository root, using Python 3.11 or later and the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_exceptional_degree_sieve_review3/independent_check.py \
  | cmp - ramsey_r55_exceptional_degree_sieve_review3/EXPECTED_OUTPUT.txt
cd ramsey_r55_exceptional_degree_sieve_review3
sha256sum -c SHA256SUMS
```

## Trust boundaries and uncertainty

The verdict imports the earlier hard-branch degree restriction, the paired
deficiency budget, the existence and arithmetic of the degree-21 anchor, and
the exact local extrema
`U(18..24)=85,92,100,107,114,122,132`.  In particular, this review does not
re-enumerate the Ramsey catalogs underlying those extrema.  It does rederive
the new graph-to-integer-system reduction and independently checks the entire
new finite classification.

The proof is not formalized in a proof assistant.  The computational evidence
trusts CPython's integer and rational arithmetic, ordinary file reads, and the
small checker itself.  The main remaining mathematical uncertainty is graph
realizability: none of the 321 surviving aggregate splits has been realized or
proved realizable here, and vertex-level incidence and clique constraints are
deliberately absent from this relaxation.
