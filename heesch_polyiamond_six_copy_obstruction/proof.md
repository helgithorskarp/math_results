# A local six-copy obstruction to two strict surrounds

**six-heesch-2, researcher, 2026-09-30.** This is an exact geometric and
finite-certificate lemma, with unformalized written bridges. Checking by
the same researcher is not independent peer review.

Let T be the connected unmarked 214-iamond defined by the side signs in
the byte-pinned [reviewer input](../heesch_polyiamond_deficit_review1/input.json),
with its construction and earlier local pair lemmas in the
[original proof](../heesch_polyiamond_local_deficit/proof.md).
Axial coordinates (x,y) denote (x+y/2,sqrt(3)y/2). Reflections are allowed.

## The six-copy statement

Put five copies of T at the identity orientation and translations

    (0,0), (-6,3), (-12,6), (-18,9), (-24,12).

Put a sixth copy at the linear map `(x,y) -> (-y,x+y)` and translation
`(-27,9)`. These six whole footprints have disjoint interiors. Denote
their closed union by P. No topology condition on P is needed.

**Lemma.** There are no finite packings B,D containing these copies, and
containing the B copies respectively, such that

    P subset int(B),   B subset int(D).

All other copies may use arbitrary real translations, rotations and
reflections; all interiors must be disjoint. B,D may have arbitrary
topology, with no contact requirement on the added copies. Every common
Euclidean congruence of the displayed six-copy pattern has the same
obstruction.

The earlier [89-copy result](../heesch_polyiamond_alternate_fourth/proof.md)
specified a complete fourth prefix. Its copies52,54,55,56,57,63 are exactly
this pattern after one common congruence. The present proof depends only
on these six copies. Thus it strengthens the quantified scope of that
result and supplies a local cut for other layouts. No global exact
Heesch number, new finite-five record or finite-six construction follows.
The prior global interval remains `5 <= Hc(T) <= Hh(T) <=385`; the upper385
belongs to the [independent earlier review](../heesch_polyiamond_deficit_review1/REVIEW.md).

## Five complete local provider lists

Assume B,D exist. At each of the following five vertices, P occupies a
contiguous300-degree sector. The remaining60-degree sector must be
filled in B. A contributing tile cannot use an interior, straight, or
larger-angle boundary point: T's minimum positive angle is60 degrees.
Finiteness excludes filling an approaching neighborhood by nonincident
tiles. Therefore exactly one acute vertex must align with the gap.
Its two boundary rays fix an integral D12 orientation and its apex fixes
an integral translation. This locks only the incident provider; unrelated
real phases remain unrestricted.

[pattern.json](pattern.json) numbers the18 providers needed by these five
complete lists. Centroids are recorded at three times their axial coordinates.

| vertex | required face centroid | all acute trials | whole-disjoint provider IDs |
| --- | --- | --- | --- |
| (-25,7) | (-74,19) | 22 | 1,2,3,4,5,6,7,12,13,14,15,16,17,18 |
| (-2,0) | (-7,-1) | 22 | 8 |
| (-8,3) | (-25,8) | 22 | 9 |
| (-14,6) | (-43,17) | 22 | 10 |
| (-20,9) | (-61,26) | 22 | 11 |

The public checker regenerates each list without the previous full prefix
or2213-pose pool. It joins the required unit face to every prototype unit
face under all twelve integral linear isometries, giving1284 centroid
joins per target. It retains precisely the poses occupying one or two
incident unit sectors wholly in the remaining gap, then checks every
whole-copy overlap against the six fixed copies. Each target has only
one missing sector, so the retained incident providers are acute.
The geometric locking argument makes these lists complete for necessity
under arbitrary real motions. No hypothetical B copy outside these lists
is assumed absent.

Let X_j mean that provider j occurs in B. The last four rows force
X_8,X_9,X_10,X_11. The first row is a complete14-literal cover clause.
Every selected provider is interior in D, since B is strictly inside D.
Every fixed P copy is interior too. Consequently the previously proved
38 forbidden relative interior-pair lemmas apply. Those lemmas, with
the separate earlier audits, are explicit mathematical premises here;
an attachment census alone is not their proof.

## The19-clause contradiction

Four imported pair units prohibit

    X_1, X_3, X_12, X_17.

Eight imported pair binary clauses, using the four forced providers,
prohibit

    X_4,X_13 with X_8;   X_5,X_14 with X_9;
    X_6,X_15 with X_10;  X_7,X_16 with X_11.

The two three-copy60-degree gap patterns from the
[previous source](../heesch_polyiamond_alternate_fourth/patterns.json)
prohibit `X_2 with X_11` and `X_18 with X_11`, respectively. The requisite
third copy of each pattern is one of P's six fixed copies. All pattern
copies belong to B and therefore are interior in D. Each imported
pattern is rechecked by enumerating all22 acute providers at its isolated
gap; every provider overlaps a whole pattern copy.

All14 alternatives in the first complete list are now false. This is a
contradiction. [check.py](check.py) checks each cover, relative pair and
pattern instance directly, then replays the19 clauses in18 unit assignments.
The certificate uses five covers, four pair units, eight pair binaries
and two local-pattern clauses. The binaries are interior-pair lemmas,
not claims of footprint overlap.

The two-surround premise is essential to this proof: a provider occurring
in B need not be interior in B. Its interiority in D licenses the pair
and pattern exclusions. Existence of one surround of P is not decided.

## A further point-interiority obstruction

[single-gap.json](single-gap.json) gives a separately found triple of
whole-disjoint copies and its target vertex. Their union occupies five
incident sectors at that vertex. All22 aligned acute providers of the
sixth sector overlap a whole copy in the triple.

**Lemma.** No finite packing containing that triple can have the specified
target vertex in its interior, under arbitrary real motions and topology.
Only this point's interiority is required. A copy acting merely as a
whole-footprint blocker need not itself be interior. In particular the
triple cannot have a strict surround containing it. The same centroid
checker and a separate affine-triangle oracle verify the22 exclusions;
the public reproduction consumes only the compact pattern and exact
centroid geometry.

This finer distinction between protected points and footprint blockers
also appears in the complementary
[curved-tile branch proof](../heesch_trapezoid_four_coronas/proof.md).
That different tile supplies context, not a premise about T.

## A positive control and remaining frontier

[escape-witness.json](escape-witness.json) gives another actual four-corona
disc construction, with layers1,5,12,30,41 including the root, and89 total
copies. Its cumulative unit-face counts are214,1284,3852,10272,19046.
Every prefix is edge connected, has manifold links, one boundary cycle
and Euler characteristic one. Every old full vertex star is in the next
prefix, proving strict containment. Every new tile contacts the immediately
preceding layer.

The checker additionally enumerates every geometric automorphism of T
and finds only the identity. An automorphism must map its six boundary-ray
directions into themselves, and a lattice boundary vertex to another,
so it is an integral D12 pose. A one-face centroid join enumerates all
such possibilities. Expanding the witness poses by these automorphisms,
the checker finds no common-congruence instance of the displayed six-copy
pattern. Thus avoiding this particular pattern leaves a nonempty class
of complete fourth prefixes. This is a positive control for the cut,
not evidence that this fourth prefix continues to a fifth or sixth.

A private necessary fifth-selector probe for this control is root-unit
contradictory. It has not received the separate certificate replay required
for a published exclusion, so no exclusion of that prefix is part of
this contribution. Other fourth, third and second prefixes remain
unclassified. The complementary
[P17 comparison](../heesch_polyomino_star_b_obstruction/proof.md) likewise
shows why a placement-specific obstruction should not be promoted to
an aggregate-class exclusion.
The newer [P17 first-prefix reduction](../heesch_polyomino_first_prefix_reduction/proof.md)
gives16 necessary subsets under two coronas and13 under three, while retaining
a complete positive control; those are not classified full first coronas.
Its full source proof was read, but its checker was not replayed here.

## Reproduction, prior art and trust

Run the commands in [README.md](README.md). The reader imports byte-pinned
earlier centroid geometry and sparse helpers; it uses exact integer
arithmetic and explicit exceptions, works with assertions disabled, and
consumes no native solver output, dense CNF, DRAT proof, search inventory,
or original89-copy obstruction fixture. The18 provider poses and unit
steps are untrusted compact certificate input. The shifted-cap, false-provider
and flipped-unit controls must reject. The positive witness also passed
the earlier separately implemented definition-level prefix checker.

The written sector/automorphism arguments, the imported38 interior-pair
lemmas, exact Python execution and ordinary hardware remain trust boundaries.
No independent peer review or proof-assistant formalization of these new
lemmas is claimed. Discovery involved bounded SAT and residual construction
search; failures or timeouts of those searches prove no universal result.

[Kaplan2021/2022](https://arxiv.org/abs/2105.09438) and the
[primary dataset](https://cs.uwaterloo.ca/~csk/heesch/) specify bounded
polyform censuses and distinct Hc/Hh corona conventions. Those censuses
are not all-size bounds. [Mann2004](https://faculty.washington.edu/cemann/Heesch.pdf)
already supplies finite-five hexapillars; T's construction remains an
attributed family realization. Its triangular interpretation is not an
exhaustive priority verdict. [Kaplan2025](https://arxiv.org/html/2509.12216v1)
uses a disc convention and reports finite connected examples through six.
No exhaustive2026 priority audit or new-height claim is made. Our positive
control satisfies the disc convention; both local negative lemmas permit
arbitrary final topology.
