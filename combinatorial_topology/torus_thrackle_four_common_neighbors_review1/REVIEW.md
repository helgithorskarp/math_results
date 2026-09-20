# Review report

## Verdict and scope

**Accept with high confidence.**  I found no mathematical or computational
error in the claim that two vertices in a thrackle on the orientable torus have
at most four common neighbors, that the bound is attained by the displayed
rotation scheme for `K_{2,4}`, and hence that `K_{2,n}` is torus-thrackleable
exactly for `0 <= n <= 4` and has orientable thrackle genus one for
`2 <= n <= 4`.

This is a correctness verdict, not a historical-priority verdict.  The target
appropriately makes no priority claim.  A bounded exact-title and
`K_{2,4}`/torus/thrackle search found the relevant general literature but no
published copy of this particular rotation scheme; that is insufficient to
claim novelty.

## Human premises and completeness reductions

The result depends on the following premises.  Items 1, 2, 5, 8, 9, and 11
are mathematical arguments rather than consequences of program agreement.

1. **Thrackle convention.**  The graph is finite and simple, the surface is
   closed and orientable, adjacent edges meet only at their common endpoint,
   and independent edges cross properly exactly once.  This agrees with the
   definition in Hernández-Vélez--Kynčl--Salazar (2025/2026).

2. **Four-cycle homology lemma.**  Cairns--Nikolayevsky Lemma 5(a) says that a
   thrackled 4-cycle is nonzero in mod-two homology.  Its short proof is valid:
   split the cycle at one of its two independent-edge crossings into two
   loops; after a local separation there, their only transverse intersection
   is the other crossing.  Their mod-two intersection is one, so they cannot
   be the same class on an orientable surface, whose mod-two intersection form
   is alternating.  Their sum is the original 4-cycle and is nonzero.

3. **Reduction from common neighbors.**  For two distinct vertices `u,v` and
   common neighbors `w_i`, each pair of two-edge paths `P_i,P_j` is a simple
   4-cycle after restricting the drawing to its four edges.  Extra graph edges
   do not affect the lemma.  Thus `h_i=[P_i+P_0]` are pairwise distinct.

4. **Finite-space bound.**  A closed orientable genus-`g` surface has
   `2^(2g)` mod-two homology classes.  Hence `n <= 4^g`, giving `n <= 4` on
   the torus and excluding `K_{2,2}` on the sphere.  Exhaustion of the four
   vectors of `F_2^2` also proves the target's equality observation: the xor
   of all four is zero and each nonzero pair difference occurs twice.  The
   checker tests all 24 orderings of these four vectors.

5. **Rotation systems realize orientable surfaces.**  Oriented vertex discs
   joined by untwisted edge bands according to a cyclic rotation have boundary
   components equal to the orbits of `rho alpha`.  Capping those components
   produces a cellular embedding in a closed orientable surface.  This is the
   bridge from combinatorial rotations to topology; it is not replaced by the
   program.

6. **Route incidence is exhaustive.**  Each of the eight displayed original
   edge routes is simple.  Among their 28 unordered pairs, the six `e/e` pairs
   meet only at `u`, the six `f/f` pairs only at `v`, four matched `e_i/f_i`
   pairs only at `w_i`, and the twelve unmatched pairs only at their specified
   `x_ij`.  The checker reconstructs and tests all 28.

7. **Every crossing is proper.**  At each of the twelve `x_ij`, the two
   half-edges of `e_i` alternate with the two of `f_j` in the rotation.  Thus
   they may be rejoined inside a mutually disjoint crossing disc as one
   transverse crossing.  Embedded bands outside those discs add no meetings,
   and no third edge enters a crossing disc.

8. **The face list is complete.**  The checker independently computes all
   dart-permutation orbits and separately expands the four representatives
   printed in the proof under cyclic index shift.  The two sets agree exactly:
   orbit sizes `4,4,4,2`, face lengths `5^8 4^6`, and 64 directed darts.  This
   proves both validity and exhaustion of the face table.

9. **The surface is the torus.**  The planarization is connected and has
   `(V,E,F)=(18,32,14)`, hence Euler characteristic zero.  The capped ribbon
   surface is connected, closed, and orientable, so the classification theorem
   gives genus one.  A separate bit-set boundary calculation gives ranks
   `rank(d1)=17`, `rank(d2)=13` over `F_2` and Betti numbers `(1,2,1)`.

10. **Deletion and small cases.**  Deleting complete neighbor branches from a
    torus drawing preserves the thrackle conditions.  The cases `n=0,1` are
    trivial.  For `2 <= n <= 4`, the construction supplies genus at most one
    and the 4-cycle lemma supplies genus at least one.  As a stronger check,
    all 15 nonempty induced subdrawings were reconstructed: the four
    `K_{2,1}` drawings cap to a sphere; every one of the six `K_{2,2}`, four
    `K_{2,3}`, and one `K_{2,4}` drawings caps to a torus.

11. **No broader conclusion is smuggled in.**  The proof neither resolves
    Conway's planar edge bound nor the asymptotic order of `tg(K_{2,n})`.
    The recent general bound `tg(K_{2,n}) <= ceil((n-1)/2)` only yields two at
    `n=4`; the audited construction improves that isolated case to one.

## Independent computation and adversarial examples

[`independent_check.py`](independent_check.py) regenerates the construction
from the formulas and does not read `certificate.json`, `expected.json`, or
any target-package code.  Its full deterministic output is
[`expected.json`](expected.json).

The smallest controls first test the face permutation on a two-edge tree
(`V=3,E=2,F=1`) and a triangle (`V=3,E=3,F=2`), both spherical.  The induced
`K_{2,2}` cases then test the first topologically nontrivial instances.

Five mutations probe different completeness assumptions:

* making `x01` nonalternating is rejected as a non-proper crossing;
* omitting `x01` is rejected because one independent edge pair no longer
  meets;
* replacing the rotation at `x01` by the other alternating rotation preserves
  all local thrackle incidences but gives 12 faces and genus two;
* reversing the rotation at `u` likewise gives genus two;
* swapping two crossings along `e0` preserves the local incidence data but
  gives 10 faces and genus three.

The last three controls are important: alternation and pairwise incidence do
not by themselves prove that the supporting surface is a torus.  The exact
route orders, rotations, and global face exhaustion are all essential.

## Source and reproducibility audit

The target source commit is
`c467f8943a53f8d7183ae9d91f11eda943a6063e`.  At that commit I independently
ran both target checks successfully:

```sh
cmp certificate.json <(python3 build.py)
cmp expected.json <(python3 verify.py --self-test)
```

The target verifier reconstructs its input and checks integer boundary
cancellation and ranks over both `F_2` and `F_3`.  This review's checker uses a
different representation and a bit-set `F_2` elimination.  Agreement is
supporting evidence only; the eleven premises above state the human argument
that makes the case-space reduction complete.

Primary sources checked on 2026-09-20 are listed in [`SOURCES.md`](SOURCES.md).
