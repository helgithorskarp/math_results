# One-defect anchor localization and closure of the singleton case

A vertexwise degree identity closes the last disconnected exact-anchor case
in the hard branch of the team's `R(5,5;43)` reduction. In the one-defect
degree profile `20^1 21^42`, the doubly exact vertices are precisely the 22
blue neighbors of the unique degree-20 vertex. Their blue graph is a
`(4,5;22,107)` graph, with vertex-connectivity at least two; their red graph
has vertex-connectivity at least five.

Together with the prior 348-profile result, this proves both-color
connectivity of the exact-anchor set in **all 349 hard-branch split profiles**.
It also gives a short mathematical inconsistency proof for the prior
singleton local-profile SAT formulas. It does **not** exclude the entire
one-defect profile, the hard branch, or any 43-vertex Ramsey graph in general.
No new catalog-radius sweep or SAT solver run is used.

## Definitions and hypotheses

Red edges form a simple graph `G`; blue edges form its complement. A
`(r,s;n,e)` graph has `n` vertices, `e` edges, no clique of order `r`, and
no independent set of order `s`. Write

```text
d(v)   = red degree of v,
t_R(v) = number of red edges induced by N_R(v),
t_B(v) = number of blue edges induced by N_B(v),
D      = {v : (d(v),t_R(v),t_B(v)) = (21,100,100)}.
```

The hard branch of the [local-deficiency dichotomy](../ramsey_r55_local_extremal_deficiency/README.md)
means all local deficiencies are at least seven. Thus

```text
t_R(v) <= U(d(v))-7,     t_B(v) <= U(42-d(v))-7,
U(18),...,U(24) = 85,92,100,107,114,122,132.                (HB)
```

In the one-defect theorem assume `|V(G)|=43`, no monochromatic `K_5`, and
degrees `20^1 21^42`. Denote the exceptional vertex by `z`. Handshaking gives
`m=|E(G)|=451`. Only `U(20)=100`, `U(21)=107`, and `U(22)=114` are needed
for localization. More generally, the localization conclusion holds under
the explicit local caps in (HB), independently of how those caps are obtained.

## A vertexwise conservation identity

For every simple graph on `n` vertices and every vertex `v`,

```text
t_R(v)+t_B(v) = binom(n-1-d(v),2) - m
                 + sum_(w in N_R(v)) d(w).                (1)
```

Proof: set `A=N_R(v)` and `B=N_B(v)`, and let `e(A,B)` count red cross
edges. Partitioning red edges and summing red degrees on `A` gives

```text
m = d(v)+e(A)+e(A,B)+e(B),
sum_(w in A) d(w) = d(v)+2e(A)+e(A,B).
```

Subtract to obtain `e(B)=m-sum_A d(w)+e(A)`. Now
`t_R(v)=e(A)` and `t_B(v)=binom(|B|,2)-e(B)`, proving (1).
This is an elementary counting identity; no historical novelty is claimed.

## Localization theorem

For each `v != z`, all 21 red neighbors have degree 21 except possibly `z`.
Equation (1) therefore reads

```text
t_R(v)+t_B(v) = 210-451+441-1_(vz is red)
             = 200-1_(vz is red).                        (2)
```

Both summands are at most 100 by (HB). If `vz` is blue, (2) forces the pair
`(100,100)`. If `vz` is red, the pair is `(99,100)` or `(100,99)`, so `v`
is not in `D`. Since `z` has degree 20, it is not in `D` either. Consequently

```text
D = N_B(z),                  |D|=22,
V(G) minus (D union {z}) = N_R(z), of order 20.            (3)
```

At `z`, (1) yields `t_R(z)+t_B(z)=231-451+420=200`. The individual upper
bounds 93 and 107 sum to 200, forcing

```text
(t_R(z),t_B(z)) = (93,107),
e_R(N_R(z)) = 93,      e_B(D) = 107,      e_R(D) = 124.   (4)
```

In particular (3) rules out order 23 for `D` in this profile without any
component-catalog calculation. Since all vertices of `D` are blue neighbors
of `z`, their blue graph `H` has no `K_4`; a blue `K_4` there would extend
through `z` to a blue `K_5`. Globally there is no blue independent five-set.
Thus `H` is a `(4,5;22,107)` graph and its complement is a `(5,4;22,124)` graph.

## Connectivity without a local catalog

Suppose a `(r,s)` graph is disconnected and its nonempty components have
independence numbers `a_1,...,a_k`. Independence is additive across
components, so `k>=2`, `a_i>=1`, and `sum a_i <= s-1`. Each component has
order at most `R(r,a_i+1)-1`.

For a `(4,5)` graph, the component order bounds at independence numbers
1, 2, 3 are respectively 3, 8, 17. The possible partitions of the maximal
independence budget four give

```text
partition       1+3   2+2   1+1+2   1+1+1+1
order bound      20    16      14        12.
```

Budgets two or three give smaller bounds. Therefore a disconnected `(4,5)`
graph has at most 20 vertices. For a disconnected `(5,4)` graph the budget
is three, and component order bounds at independence numbers 1, 2 are 4, 13.
The maximal partition bounds are 17 for `1+2` and 12 for `1+1+1`.
Thus a disconnected `(5,4)` graph has at most 17 vertices.

Deleting zero or one vertices from `H` leaves at least 21 vertices; deleting
at most four from its complement leaves at least 18. The Ramsey restrictions
are hereditary, so these remaining graphs are connected. Consequently

```text
kappa(blue graph on D) >= 2,
kappa(red graph on D)  >= 5.                             (5)
```

These are lower bounds, not claims of sharpness. The elementary inputs are
`R(4,2)=4`, `R(5,2)=5`, `R(4,3)=9`, `R(5,3)=14`, `R(4,4)=18`.
The three nontrivial values, attributed to Greenwood and Gleason (1955), are
recorded in [Radziszowski's Small Ramsey Numbers, Section 2.1(b)](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The same values give `4<=d_H(v)<=13` and hence red internal degrees 8 through
17: the blue neighbors form a `(3,5)` graph of order at most 13, and the
blue nonneighbors form a `(4,4)` graph of order at most 17.

## Singleton formulas: what is now closed

The prior [singleton reduction and encoder](../ramsey_r55_doubly_exact_anchor_propagation/README.md)
use `u=42`, `C={0,...,20}`, `O={21,...,41}`, and `z=21`. All `u-C` edges are
red and all `u-O` edges blue. The base formula has the global degree multiset
`20^1 21^42`, `e_R(C)=100`, and `e_R(O)=110`. Its local-profile strengthening
also requires every `c in C` to have pair `(100,100)` and `z` to have pair
`(93,107)`.

Here is a direct inconsistency proof using only these stated constraints:

1. By (2), the exact local pair on every `c in C` forces all `z-C` edges blue.
   Also `uz` is blue. Since `d(z)=20`, all `z-(O minus {z})` edges are red.
   Hence `N_B(z)=C union {u}`.
2. The local requirement `t_B(z)=107` gives
   `e_R(C union {u})=binom(22,2)-107=124`.
3. But the base constraints give that same number as `e_R(C)+21=121`.

Equivalently the forced set would give `t_R(u)=124-21=103`, contradicting
the encoded `t_R(u)=100`. This is a hand proof of semantic inconsistency.
It does not require the optional type choices, stabilizer, or the global
absence of monochromatic `K_5` once the displayed degree/local data are assumed.

The closed formulas are the aggregate `--local-profile` formula, all seven
typed `x=0,3,...,18` formulas, and all seven stabilized typed formulas.
Their existing manifests still pin their generated bytes correctly; source
inspection and the existing encoder gate tests supply the CNF-to-graph
bridge. **No solver-generated UNSAT certificate or DRAT proof is claimed.**
The base formula without `--local-profile` is not settled by this argument:
its constraints do not require all of `C` to be doubly exact. Do not report
that relaxation as UNSAT.

The prior profile theorem already proves connectivity for the other 348
split profiles. Applying (3)--(5) to its one remaining escape completes
both-color connectivity for all 349. That combined corollary inherits the
prior extremal-catalog and component-enumeration trust boundaries for the
other profiles. The new one-defect proof itself requires no component catalog.
The old target-specific radius-five/six/seven theorems remain valid finite
catalog-distance results for degree multiset `20^22 21^20`; they are no longer
needed to investigate this eliminated singleton mechanism.

## A reusable degree-neighborhood constraint

For any hard-branch profile, choose the sparser color as red, put `m=231+M`,
and write `epsilon(w)=d(w)-21`. Combining (1) with (HB) gives

```text
sum_(w in N_R(v)) epsilon(w) <= M-b(d(v)),
d             18   19   20   21   22   23   24
b(d)         220  221  220  220  221  223  223.            (6)
```

The slack in (6) is exactly the sum of the two local deficiencies beyond
seven at `v`, not merely an arbitrary inequality slack. This is a vertexwise
degree-correlation constraint suitable for a next structural feasibility
pass. No enumeration using (6) across all profiles is claimed here.

## Reproduction and evidence boundary

From the repository root (Python 3.11.2, standard library only):

```bash
python3 ramsey_r55_one_defect_anchor_localization/verify_localization.py \
  | cmp - ramsey_r55_one_defect_anchor_localization/EXPECTED_OUTPUT.txt
python3 ramsey_r55_doubly_exact_anchor_propagation/singleton_sat.py self-test
cd ramsey_r55_one_defect_anchor_localization
sha256sum -c SHA256SUMS
```

The audit compares (1) with literal induced-edge counts on every labeled
simple graph of orders zero through six, also tests the specialized identity
on an explicit 43-vertex one-defect fixture, enumerates all allowed local
pairs and component-budget partitions, checks the singleton contradiction
and (6), and pins the imported singleton profile/source/manifests by hashes.
The 43-vertex fixture is deliberately **not** a Ramsey graph (it has an
explicit red `K_5`); it tests arithmetic without pretending to solve the target.
The small-graph enumeration is a consistency test, not a substitute for the
universal hand proof. Hashing inherited files is provenance checking, not a
fresh independent proof of their claims. Expected audit runtime is seconds.

This milestone uses the combinatorial counting method and an exact
definition-level code audit. No historical novelty, formal proof-assistant
verification, independent peer review, or improvement of the Ramsey lower
bound is asserted.
