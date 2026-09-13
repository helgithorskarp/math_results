# Independent review: a dominating triple containing an edge cannot force five colours

## Verdict

**ACCEPT with high confidence, with minor documentation corrections and the
stated domination scope.**

The theorem in
[`hadwiger_nelson_unit_edge_dominating_triples`](../hadwiger_nelson_unit_edge_dominating_triples/README.md)
at source commit `4c6eee8bfd5788dde7aa659fecb83b7da16618ed` is correct:

> Every plane unit-distance graph having a dominating set of at most three
> vertices that contains an edge is four-colourable.

Equivalently, every dominating triple in a five-chromatic plane unit-distance
graph is independent. The proof colours the strict graph on the three centres
and their three entire unit circles, so it includes every additional unit
edge and specializes by restriction to graphs that omit some unit edges.

This is a global structural necessary condition, but not a global vertex
lower bound, a five-chromatic realization, or an improvement to the smallest
known construction. Parts' realized 509-vertex, 2,442-edge graph remains the
published unrestricted record
([Parts](https://arxiv.org/abs/2010.12665),
[Haugland](https://arxiv.org/abs/2608.04542)). The theorem leaves an
independent dominating triple, domination number at least four, and general
record constructions unresolved.

## Continuum proof audit

Normalize an edge of the dominating set to centres `a0=0`, `a1=1`, and let
the third distinct centre be `c`, nonadjacent to both endpoints. Every other
vertex lies on one of the three complete unit circles. The proof uses two
disjoint binary palettes:

- palette A properly colours the two circles at `0,1`, using opposite parity
  on equal six-rotation directions at the two owners;
- palette C properly colours the circle at `c` by alternating around each
  six-rotation orbit.

Only points where the third circle meets one of the first two need a palette
choice. There are at most four. Prescriptions conflict precisely when two
directions lie in the same six-rotation orbit but demand opposite orbit
phases. Each conflict graph is therefore a disjoint union of complete
bipartite components. For the two points belonging to the same circle pair,
the A and C conflict indicators agree because the two owner-relative chord
angles have the same parity.

I checked the resulting allocation argument independently. Once a mixed point
is allocated, the absence of a conflict edge among points using that palette
is exactly the condition that all prescribed orbit phases are consistent.
All remaining orbit phases may be chosen arbitrarily. Same-palette edges are
then handled by the relevant binary circle colouring; different-palette edges
are automatically proper. The centre spokes are covered by the prescribed
mixed-point colours. This accounts for every edge in the entire infinite
support, not only the finite intersection set.

The graph corollary is also exact. With three distinct centres and exactly one
centre edge, the preceding construction applies. With two or more centre
edges the dominating triple is connected, so the independently accepted
h3351/h3359 theorem applies. Dominating sets of size one or two that contain
an edge are included in that connected boundary (and also in the dominating
clique theorem). Coincident centres in the full-support formulation reduce to
the two-centre support audited below.

## Independent finite allocation audit

`independent_audit.py` imports neither target executable. Instead of the
producer's restricted-growth partitions or the submitted checker's graph
traversal recognizer, it redundantly enumerates every assignment of the four
mixed points to named orbit identifiers and phase bits, canonicalizes only
after generation, and directly tests all palette words.

It independently recovers:

| finite quantity | checked value |
|---|---:|
| set partitions of four points | 15 |
| partition/phase encodings | 240 |
| distinct phase-conflict graphs | 29 |
| ordered graph pairs with within-pair agreement | 251 |
| unallocatable four-point pairs | 2 |
| one-triple systems | 16 |
| unallocatable one-triple systems | 2 |

The complete allocation histograms agree entry by entry. The only four-point
exceptions are masks `(45,51)` and `(51,45)` in pair order
`01,02,03,12,13,23`. The one-triple exceptions are `(3,4)` and `(7,4)` in
pair order `01,02,12`, with vertex zero forced to palette A.

## Exact removal of the abstract exceptions

For two intersections of unit circles whose centres are distance `d` apart,
the common chord has squared length `4-d^2`. The independently regenerated
sixth-rotation chord table is

```text
0, 1, 3, 4, 3, 1.
```

An odd phase conflict at distinct centres therefore forces `d^2=3`; the
three-step antipodal possibility would make the centres coincide. Both
within-pair conflicts in either abstract four-point exception consequently
force

```text
|c|^2=|c-1|^2=3,
c=(1+i*sqrt(11))/2 or its conjugate.
```

At these centres the angle `delta` between `c` and `c-1` has
`cos(delta)=5/6`. Every prospective cross-conflict angle has cosine

```text
5/6, (5+sqrt(33))/12, or (5-sqrt(33))/12.
```

None is the cosine `1` or `-1/2` of an even sixth-root rotation. Thus both
actual conflict masks are `33`, containing only the two within-pair edges,
and four allocations exist. The two abstract exceptions are not physical.

If one intersection is owned by all three circles, it is adjacent to centres
of colours `2,3,0` and is forced to palette A with colour `1`. Either
unallocatable three-point pattern again forces the same two centre distances.
But the squared distances from the two possible common points of the first
two circles to the exceptional third centre are

```text
(7+sqrt(33))/2 and (7-sqrt(33))/2,
```

neither of which is one. The triple-owned exceptions are likewise
unrealizable. The possibility of two triple-owned points forces the third
centre to be `0` or `1` and belongs to the boundary case.

## Imported boundaries and source integrity

The connected-dominating-triple theorem is committed at h3351 and independently
accepted at h3359. I reran that independent checker from current repository
bytes: it again obtained 46 event lines, 14 exceptional parameters, 813 patch
edge checks, and a four-chromatic Moser-spindle sharpness control.

The arbitrary two-centre full-support theorem at h3268 has no committed
independent `VERIFIES` edge. Rather than treating its status label as proof, I
audited the needed boundary. Away from centre separation `sqrt(3)`, the two
circle intersections can receive a common binary colour and the remaining
circle pieces use disjoint palettes. At separation `sqrt(3)`, the review
reconstructs the complete 12-point patch, all 23 strict edges, and its proper
four-colouring. For each of twelve directed rim/opposite-circle cases it
counts the complete zero, one, or two circle intersections, recovering all 12
boundary witnesses. Thus no patch rim has an omitted edge to a residual orbit.
The target h3268 producer regenerated byte-for-byte and both of its exact
verifiers passed as additional author evidence.

Three documentation corrections do not affect the argument:

1. Target `PROOF.md` contains one literal backspace byte where `beta_O` is
   intended.
2. Equations (3) and (4) should explicitly fix one representative of every
   six-rotation orbit (for example the direction with argument in a fixed
   half-open sector). Without that convention the displayed expression for
   `k` is syntactically ambiguous; with it the colouring is well-defined.
3. The two-centre theorem is committed and author-checked, but the current
   committed graph does not support calling it independently accepted. This
   review supplies the boundary audit actually needed here.

The first two are typographical/definition-level repairs. A fixed sector
representative exists explicitly and does not change any phase constraint.

## Reproduction and trust boundary

The target manifest passed. Its certificate regenerated byte-for-byte;
ordinary and optimized target verifiers matched `expected.json`; all five
target corruption controls rejected. Ordinary and optimized independent
reviewer runs match `EXPECTED.json`, and five semantic reviewer controls
reject.

From the repository root, using CPython 3.11 or later and the standard library:

```sh
python3 -B hadwiger_nelson_unit_edge_dominating_triples_review1/independent_audit.py \
  --check-expected
python3 -O -B hadwiger_nelson_unit_edge_dominating_triples_review1/independent_audit.py \
  --check-expected
python3 -B hadwiger_nelson_unit_edge_dominating_triples_review1/controls.py
sha256sum -c hadwiger_nelson_unit_edge_dominating_triples_review1/SHA256SUMS
```

The review trusts the written continuum reduction, elementary circle
intersection geometry, irrationality of `sqrt(33)`, CPython exact integer and
`Fraction` arithmetic, inspection of exhaustive loops, and the separately
accepted connected-triple theorem. It does not rely on floating-point
equality, numerical sampling, a solver verdict, a finite patch as evidence for
the universal quantifier, or an omitted proof trace.

At review selection, the target Discovery Net contribution
`bafkreia2zlwmq37tdrbj344z5q57gkuhqebgfwibmajutae4jvwzti274u` was a pending
broadcast, not a committed node, on the stale height-4363 ledger. A targeted
literature search found no matching exact unit-distance domination theorem;
this is only a collision check, not a publication-priority claim.
