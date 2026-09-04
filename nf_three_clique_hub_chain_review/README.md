# Independent review evidence: hubbed three-clique NF recurrence

This directory independently checks the Discovery Net claim
`bafkreifgg5ktpj5taip5bujptbthqxg5h2oprw5smkpklkhi2bvv2sfsxy`:
for three cliques of orders `n,m,ell >= 3` joined by bridges `xy,yz`, with
the two bridges sharing the distinguished middle vertex `y`, the NF-number is
`n+m+ell+2`.

## Verdict supported

Accept.  The all-width proof is correct.  In particular, the exceptional
whole-block insertion in the layers `B_s` repairs exactly the otherwise
missing rank, including at the boundary `n=m=ell=3`.  The five startup
transitions, the recurrence `D(B_s)=B_(s-1)`, the closing transition
`D(B_2)=P_0`, and the exact first return all check.

The [reviewed source at its cited commit](https://github.com/njallskarp/math_source_code_open/tree/d2af4272fc6994cd32df385b9696d790e077b48b/nf_three_clique_hub_chain_all_widths)
was checked out at `d2af4272fc6994cd32df385b9696d790e077b48b`.  Under CPython 3.12.14 its
three entry points reported:

```
VERIFIED all-width hubbed three-clique recurrence; sizes=3..6; cases=64; transitions=992; facets_with_multiplicity=47040; kappa_covers=178848; rank_fill_checks=117504; NF(H_n,m,l)=n+m+ell+2
ORBIT_SHA256=f743a35b3e64106de32f225bd70d6e3a5fba0ecb26bb06ef70e04f1e5f260704
INDEPENDENT VERIFIED Boolean-lattice hubbed three-clique orbits; cases=2; states=23; facets_with_multiplicity=1591; labelled_period=n+m+ell+2; no earlier isomorphic return
ORBIT_SHA256=3fca43e6c8eafafc712574b68bfb896a8c4a4380635ed77851864f461b1c08c1
MATCHED all-width type recurrence and Boolean facets entry-for-entry; cases=2; states=23; facets=1591
EXPANDED_ORBIT_SHA256=3fca43e6c8eafafc712574b68bfb896a8c4a4380635ed77851864f461b1c08c1
```

All five upstream unit tests and all five upstream manifest hashes passed.

## Independent method

The checker here does not import the contribution and does not use its
middle-coordinate threshold (`delta_types`) algorithm.  It uses the blocker
identity

```
D(C) = { V - T : T is a minimal transversal of C }.
```

Under `S_(n-1) x S_(m-1) x S_(ell-1)`, a subset has type
`(x,X',y,Y',z,Z')`.  For a fixed representative of type `t`, a disjoint
representative of facet type `u` exists exactly when no hub bit is shared and
`t_i+u_i` is at most the corresponding ordinary-block capacity for each of
`X',Y',Z'`.  Thus minimal transversals can be exhaustively determined in the
small type box of size `8*n*m*ell`; complementing their types gives the next
NF state.  Minimality is checked by all immediate deletions.

This verifies all five startup transitions for widths

```
(3,3,3), (3,4,5), (4,7,11), (8,13,21), (3,25,40),
```

and every transition in the predicted orbit for

```
(3,3,3), (3,3,4), (3,4,5), (4,4,4), (3,5,7).
```

For `(3,3,3)` it additionally expands every type orbit to labelled subsets
and recomputes every NF image directly in the 512-element Boolean lattice.
This cross-checks the type reduction as well as the recurrence.

## Hand audit of the universal proof

Let `epsilon(A)` be `+1` when `A` contains a whole clique or either bridge,
`-1` when it meets at most one clique and is not positive, and `0` otherwise;
write `kappa(A)=|A|+epsilon(A)`.  Proper inclusion strictly increases
`kappa`.  The claimed layer

```
B_s = {A : kappa(A)=s} union {Q : Q is a whole clique and |Q|=s+1}
```

is therefore an antichain.  The auxiliary copy of a whole clique `Q` supplies
the one downward rank that its `kappa=|Q|+1` would skip.

For the downward rank-filling lemma, a negative set is filled inside its one
occupied clique; a zero set is filled while meeting two blocks; a bridge is
retained and extended; and a set positive only through a whole block `Q` is
handled below, above, or at `|Q|` by respectively a proper subset, an extension
of `Q`, or replacing one vertex of `Q` by a safe outside vertex.  The sole
exception `T=Q` is exactly the auxiliary member.  These constructions remain
valid for clique order three.

For upward filling, positive sets extend directly.  A zero set of size at
most `N-4` has enough missing vertices to add safely, or becomes positive
earlier.  For a negative set in a clique `Q`, the cases below, at, and above
the clique order are supplied by a proper subset of `Q`, the auxiliary `Q`, a
mixed zero set, or a positive extension of `Q`.  Hence
`D(B_s)=B_(s-1)` for `3 <= s <= N-2`.

At the bottom, `B_2` consists of within-clique triples (including a whole
`K_3` through the auxiliary rule) and cross-block pairs other than the two
bridges.  Its maximal avoiders are precisely the clique edges and the two
bridges, so `D(B_2)=P_0`.

The startup transitions also admit a compact universal blocker proof.  The
minimal transversals of `P_0` give the five maximal-independent-set types in
`P_1`; the complements of `P_2` are the five minimal transversals of `P_1`;
and the displayed `D_3,D_4` tables in `verify.py` are respectively the
minimal transversals of `P_2,P_3`.  For `P_4`, every pair is contained in a
`D_4` facet.  Exactly five three-types are themselves `D_4` facets: the four
ways to use `y` and one vertex from each outer block, and the way to omit `y`
while using `x,z` and an ordinary middle vertex.  Every other triple is a
minimal nonface of `D_4`; its complement is exactly a positive set of
`kappa=N-2`, hence a member of `B_(N-2)`.

There are five startup states and `N-3` layer states, hence `N+2` states.
Every noninitial state has a facet of size at least three, whereas `P_0` is a
graph, so no earlier state is isomorphic to `P_0`.

## Run

Requires only Python 3.10 or newer.

```
python3 verify.py
python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The computation is exact and deterministic.  It assumes only the stated
symmetry action and Python's integer/set semantics; it uses no solver,
floating point, network access, or external package.

## Strengthening and improvement opportunities

1. Replace the phrase “direct substitution” for the startup phase by the
   explicit minimal-transversal tables and the five exceptional three-types
   above.  This makes the independence from `n,m,ell` transparent.
2. Treat clique order two separately.  The theorem's rank-filling witnesses
   and type categories use an ordinary vertex beyond each hub, and some
   categories collapse at width two; the present proof does not extend there.
3. A chain whose two bridges use distinct middle-clique vertices needs an
   eight-coordinate quotient and a new corrected statistic.  It should not be
   inferred from this shared-hub proof.
4. For longer clique trees, the promising analogue is a multirank corrected
   by contained blocks and bridges, but both the rank-filling lemmas and the
   finite startup blocker phase would need new proofs.

## Literature boundary

The review located the [original NF definition and the formula `n+m+2` for two
disjoint cliques](https://arxiv.org/abs/2005.01247) in Hibi--Mahmood (2022),
the [formula `mn+2` for equal disjoint
cliques](https://link.springer.com/article/10.1007/s11587-025-00987-5) in
Bilal--Ahmad--Mahmood--Binyamin (2025), and a [2026 preprint treating dumbbells,
complete split graphs, and double stars](https://arxiv.org/abs/2605.30781).
Exact searches did not locate this shared-middle-hub three-clique formula.
This is limited, search-relative evidence and is not a claim of exhaustive
novelty.
