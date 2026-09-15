# A complete 468-pattern Parts373 receiving relation

This package freezes a cap-feasible **receiving demand** for a replacement in
Parts's genuine five-chromatic plane graph. It supplies the entire unrestricted
four-colour boundary relation of a 373-point retained host, rather than selected
colourings or a projection onto colour-list signatures. **No replacement or
sub-509 five-chromatic graph is supplied.**

The exact computation finds 468 boundary patterns up to global colour names.
Every pattern has a checked full host colouring. A DRAT-checked completeness
instance excludes any further pattern. A separate checked parent proof and a
literal proper five-colour word certify the positive parent and show that its
original removed module blocks every host pattern.

## Frozen geometry and budget

Use the original Parts509 labels in `points.tsv`. The coordinates are exact
integer coefficients divided by 96 in the basis

```
(1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165))
```

Each row contains eight x coefficients followed by eight y coefficients.
The field is Q(sqrt(3),sqrt(5),sqrt(11)); these eight basis elements are linearly
independent over Q. Thus unequal coefficient rows are distinct physical points.
Both subset-mask multiplication and squarefree-radicand/gcd multiplication
reconstruct and compare all 129,286 pair distances, with no numerical tolerance.

Let

- `L = {0,...,373}`, `S = {374,...,508}`;
- `D = {310} union S`, the removed module of 136 points;
- `H = L minus {310}`, the retained host of 373 points;
- `N = {150,169,287,296}`, the complete neighbourhood of vertex 310.

The boundary consists of **all** H-endpoints of strict unit edges to D:

```
B = [0,150,169,243,244,245,287,296,344,345,346,
     357,358,359,360,361,362,363,364,365,366,367,368]
```

Write `I = B minus N`; this is the original 19-point L/S interface.
The complete graph counts are:

| Object | Physical points | Internal unit edges |
|---|---:|---:|
| Parent G | 509 | 2442 |
| Retained host H | 373 | 1856 |
| Removed module D | 136 | 552 |

There are 34 H--D contacts: 30 to S and four to vertex 310. Vertex 310 is
isolated inside D. The complete graph on B is just the triangle
`{0,150,169}` and 20 isolated vertices. `verify.py` reconstructs every edge and
writes the full labelled decomposition to its output directory.

A replacement X may contain **at most 135 distinct points outside H**:
`373 + 135 = 508`. Equivalently, the graph on B together with X may have at
most 158 points when its only overlap with H is B. Boundary points are already
in H and cost no new physical point. The original D uses 136 new points, so
this asks for a one-point saving in a module with substantial physical extent;
it is not an assumed zero-cost identification or an abstract vertex budget.

## Full relation and its interpretation

In `host_relation.tsv` each row is a 23-character boundary pattern followed by
a 373-character proper colouring in increasing H-label order. The origin is
colour 0. Each pattern is the lexicographically least image under the six
permutations of colours 1,2,3. All patterns use all four colours, so 468 orbits
represent **11,232 labelled boundary assignments**, or 2,808 with origin pinned.
There is no additional restriction on host colourings.

The 468 patterns split as follows:

| Colours on N | Boundary orbits | Distinct I projections | Can add old S? |
|---|---:|---:|---|
| Two | 14 | 6 | No |
| Three | 30 | 14 | No |
| Four | 424 | 424 | Yes |

The two non-rainbow rows have disjoint I projections, giving precisely 20 old
interface patterns. The rainbow sector gives 424 further I patterns, disjoint
from those 20. Thus the whole I projection of H has 444 orbits. Every new I
projection has exactly one lift to B up to global colour names; the old sector
has 44 lifts in total.

`small_extensions.tsv` gives a proper S-colouring for each of the 424 new I
patterns. The verifier checks all 552 S-edges and all 30 contacts and aligns
colour names with the corresponding H witness. This gives **424 directly
checked proper four-colourings of the complete 508-point graph G minus 310**.
The old small part alone therefore leaves every rainbow-sector pattern alive.

For the remaining 44 host patterns, N omits a colour. Assigning an omitted
colour to vertex 310 gives a literal proper colouring of L; the verifier checks
all L-edges. If S extended any such I pattern, that L colouring and the S
colouring would form a proper four-colouring of G, contradicting the checked
parent proof. Hence S blocks all 20 old I patterns and all their 44 B lifts.
For the other 424 patterns, vertex 310 itself cannot receive any of the four
colours. Consequently **the original module D blocks all 468 host patterns**.

This also derives the earlier complete 20-pattern L relation from the new
receiver census: an H colouring extends to L exactly when N is not rainbow.
The computation concerns this specific cut; it does not claim a general
interface-compression theorem or a smaller chromatic construction.

## Exact receiving contract

For a proposed exact point set X, first collision-merge with H and reconstruct
the **complete** unit graph. If every H-neighbour of X is in B, then

```
H union X is four-colourable
    iff R_H(B) intersects R_(B union X)(B).
```

The forward direction is restriction. For the reverse direction, align the
common boundary colours and unite the two proper colourings: all cross edges
have their H-end in B, so none is omitted. Global colour permutations make
the canonical table equivalent to the unrestricted relation.

A successful replacement must reject **all 468** patterns in the actual
receiving frame, use at most 135 new physical points, and admit a checked
proper five-colouring on the entire merged graph. An empty intersection alone
gives the ordinary lower bound five; the five-colour witness is still required
for equality. The parent five-colour word in this package is only a word for
the 509-point parent and is not such a replacement witness.

If new contacts reach H outside B, this 23-pin table is insufficient to decide
the composite: enlarge and completely reclassify the receiving boundary, or
check the full physical graph directly. One surviving boundary word with an
extension suffices to reject a replacement. Rejecting a few words, reproducing
the old S relation, or matching an abstract interface does not pass this gate.

The receiver deletes vertex 310 from L and allows arbitrary exact new points;
it is not the banked fixed-L374 Parts `a=8` pool, a G19 transplant, or a subset
search in an already closed ambient host. Existing criticality, small-swap and
ambient-containment exclusions remain filters on particular replacements.
In particular, deleting one point from D without new geometry simply gives a
one-vertex deletion of the vertex-critical parent. The 135-point allowance is
meaningful physical accounting, not a proof that a suitable replacement exists.

## Reproduction and evidence

Positive checks and regeneration of the exact proof obligations require only
Python 3.11 or later:

```bash
python3 verify.py --out /tmp/parts373-receiver
```

This rebuilds all distances, checks all 468 host words, checks the 424 small-side
words and their complete 508-point unions, checks the parent five-colour word,
and emits `completeness.cnf`, `parent.cnf`, `geometry.json` and a verification
summary matching `expected.json`. The summary explicitly distinguishes these
checks from the negative proof obligations.

To reproduce the independently checked negative evidence:

```bash
python3 certify.py --out /tmp/parts373-receiver \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim --seconds 180
```

Both solver calls must return UNSAT (exit 20), and both independent checks must
exit 0 and print `s VERIFIED`. UNKNOWN or a timeout is not accepted. Each CNF
has exactly one colour per vertex, forbids equal colours on every reconstructed
edge, and pins only vertex 0 to colour 0. The completeness CNF additionally
blocks all six origin-fixing permutations of each listed boundary pattern.
Any proper colouring can be globally renamed to satisfy the pin, so this is
sound and complete for the stated unrestricted relation. The parent CNF has
no boundary-pattern restriction.

| Checked obligation | Variables | Clauses | CNF SHA-256 |
|---|---:|---:|---|
| Complete H boundary relation | 1492 | 12844 | `70204a64d82d5675858cb57c0535449a8cb012e70d2cd9da49b69e0ef83fe7a1` |
| Parent not four-colourable | 2036 | 13332 | `bfad1c1cb96e983bfa83922b63d564da9db3cb9bd36012c15abe89240f227de8` |

The author run used CaDiCaL 1.9.5 and `drat-trim`; solve-plus-check times were
approximately 10 and 72 seconds. `proof_checks.json` pins both binary hashes,
instance/proof hashes, trace sizes and actual checked outcomes. The 7.96 MB
and 36.96 MB binary DRAT traces are preserved in authorized scratch, not Git;
the commands above regenerate and check them. Different solver versions can
produce different valid traces. These are author-side computer-assisted
certificates, not a claim of autonomous independent research review.

Optional re-enumeration uses `python-sat==1.8.dev24` with `cadical195`:

```bash
python3 enumerate.py --out /tmp/parts373-enumeration \
  --seconds 900 --max-patterns 30000
```

The initial enumeration completed in about eight seconds. Witness order may
vary; a complete rerun must reproduce exactly the frozen set of 468 canonical
patterns. The controller preserves partial rows on its finite wall-clock stop
and does not turn an incomplete run into a theorem. Proof verification remains
the preceding separate step.

## Sources and scope

Coordinates are copied byte-for-byte from the repository's
[`points.tsv`](../hadwiger_nelson_parts509_completion_census_degree9/points.tsv),
SHA-256 `f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
The parent five-colour word comes from the
[Parts509 criticality certificate](../hadwiger_nelson_parts509_criticality/certificate.json)
and is checked against the freshly reconstructed strict graph here.
The [20-pattern interface package](../hadwiger_nelson_parts509_interface_lemma/README.md)
and its committed independent review provide historical context; this package
generates and checks its own two negative proof obligations.

[Parts's paper](https://arxiv.org/abs/2010.12665) reports the 509-point/2442-edge
construction. [Haugland v4](https://arxiv.org/html/2608.04542v4) still names 509
as the unrestricted record; its 2131-point construction addresses the different
Moser-spindle-free restriction. Both were checked live on 2026-09-15. This
receiving specification changes neither the record nor the bounds on the
chromatic number of the plane.
