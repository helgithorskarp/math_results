# Independent review of the flexible-fish self-contact

Verdict: **accept, with a strict one-root and pair-neutral limitation**.

An independent exact checker confirms the claimed isolated plane realization:
23 distinct points, the 42 Hochberg--O'Donnell fish edges, and exactly the new
unit edge `(10,21)`.  Its complete physical unit-distance graph has 43 edges
and chromatic number four.  The contact blocks the displayed full source
four-colouring, another full four-colouring survives, and all 210 physical
nonedges admit both equality and difference in proper four-colourings.

The positive pair witnesses therefore close the immediate two-terminal route:
there is no forced-equal nonedge and no nonunit forced-different pair at this
root.  This is a useful plane-native contact event, but it is not a
five-chromatic graph or a record candidate.

## Independent method

The target checker bounds its contraction derivative with one aggregate
quadratic estimate.  This review instead constructs exact rational intervals
for every coordinate in the full box, evaluates every Jacobian entry there,
and propagates those intervals through `I-AJ(X)`.  It obtains

```text
box radius                    1.00000000000e-25
interval contraction bound   4.85280534752e-23
centre displacement          4.97077575462e-51
self-map bound                4.85777612328e-48
```

Thus `T(x)=x-AF(x)` is a strict contraction from the box to itself.  At the
midpoint, `||I-AJ(m)||<1`, so the square matrix `A` is invertible.  The unique
fixed point consequently satisfies `F(x)=0` rather than merely `AF(x)=0`.

Every one of the 253 unordered point pairs is then checked by direct interval
squared-distance evaluation, not the target's midpoint error formula.  The
smallest certified squared separation is greater than `0.0277615`; the
smallest nonedge squared-distance gap from one is greater than `0.0372723`.
The complete physical graph is therefore established without a floating-point
incidence threshold.

For chromaticity, a fixed natural-order exhaustive search replaces the
target's dynamic DSATUR implementation.  It proves the source and complete
graphs non-three-colourable after 662 and 638 recursive calls.  A separately
generated proper word

```text
01333223123122332131123
```

differs from every target word.  The 13 submitted relation words directly
cover all 420 equality/difference requests, and an explicit private request
for each word proves that this displayed cover is inclusion-minimal.  No
minimum-cardinality claim is accepted or needed.

The edge list was also reconstructed from the operation sequence in the
pinned `hodfish_vertices` source.  The retrieved file hash agrees with the
target provenance.  Independently, the complete physical graph is connected,
has no vertex cut of size one or two, has minimum degree three, and hence has
vertex connectivity exactly three.  Its girth is four.  The result is not an
artifact of a bridge or one-vertex sum.

## Reproduction

CPython 3.11 or later and a complete checkout of this repository are enough;
only the standard library is used.  From this directory run:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The controls compare the static colouring engine with brute force on all 512
labelled five-vertex graphs containing the normalizing edge, check 406 exact
interval cases, test cut detection, and reject three certificate corruptions.
See [PROOF.md](PROOF.md), [REVIEW.md](REVIEW.md),
[PROVENANCE.md](PROVENANCE.md), and [VALIDATION.json](VALIDATION.json).

The large target certificates are referenced by pinned hashes rather than
duplicated.  The reviewed geometry first entered at commit
`4e900a233cd6de3ced408cfb81bd9b25844afc2b`; the relation refinement is
reviewed at `a0fa3ac2b53ab0d538ec376a5fbe011accd41665`.

## Exact scope and record status

The accepted theorem is local to the unique real solution in the declared
rational box.  It does not classify other roots, fish flex parameters,
self-contact pairs, multiple contacts, or higher-arity colour relations.  Pair
neutrality is a statement about this exact 43-edge complete physical graph,
not all flexible-fish contacts.  Inclusion-minimal means only that none of the
13 displayed cover words can be deleted.

The result is four-chromatic, so it makes no direct progress on the order
record.  Parts's published 509-point, 2,442-edge construction remains the
supported unrestricted five-chromatic plane unit-distance record in the
bounded primary-source check; Haugland's August 2026 paper still identifies
that construction as the smallest while pursuing the different
Moser-spindle-free frontier.

## Sources

- Reviewed target:
  <https://github.com/helgithorskarp/math_results/tree/a0fa3ac2b53ab0d538ec376a5fbe011accd41665/hadwiger_nelson_fish_flex_contact_source_loss>.
- Pinned Shibuya construction source:
  <https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/pegg.py>.
- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

The requested `math-review` skill was unavailable.  Its independence,
exact-scope, geometric-realization, chromatic-certificate, hidden-assumption,
and source-integrity criteria were applied directly with the available exact
computer-assisted and GitHub research skills.
