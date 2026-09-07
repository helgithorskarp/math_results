# Independent review of the complete E477 marked-pair spindle classification

## Verdict and scope

**Verified, high confidence.**  The reviewed Discovery Net contribution is
`bafkreihm3kmunnnyc7xteqlanufi23lb7sinosf3ncplberixtxmbzzlyu`, *Complete
E477 marked-pair spindle classification excludes every graph through 508
vertices*.

Let `E` be the supplied induced unit-distance graph on 477 vertices and 2,458
edges, with terminals `O,V` at distance `8/3`.  In every subgraph of `E`, the
only distinct pair that can be forced to receive the same colour in all proper
four-colourings is `{O,V}`.  Every marked-pair spindle formed from two
isometric terminal-containing subgraphs of `E`, identifying one terminal and
putting the other terminals at unit distance, has at least 509 vertices if it
is not four-colourable.  Equivalently, every subgraph through 508 vertices of
each normalized full-copy placement is four-colourable.

This is a complete negative result for one construction family.  It is not a
five-chromatic graph below 509 vertices and gives no lower bound for arbitrary
unit-distance graphs in the plane.  It does not address different supports,
attachments with more cross contacts, non-isometric copies, or larger gadget
assemblies.

## Mathematical reduction

The proof has four independent parts.

1. Eighteen checked proper four-colourings of all of `E` give a distinct
   18-colour signature to every vertex except `O,V`.  Restricting these words
   to a subgraph proves that no other pair can be forced equal.
2. For each of 253 distinct nonterminal vertices `v`, a checked proper
   four-colouring of `E-v` gives `O,V` different colours.  Therefore every
   subgraph that still forces `O,V` equal contains those 253 vertices and both
   terminals, hence at least 255 vertices.
3. Up to a global isometry, an attachment is determined by the common
   endpoint in each copy, one of the two intersections of circles of radii
   `8/3` and `1`, and the determinant of the second-copy isometry.  Thus there
   are exactly `2*2*2*2=16` normalized frames.  Exact arithmetic shows that in
   every frame the copies intersect only at the common endpoint and the sole
   cross unit edge joins the other terminals.
4. Two four-colourable halves sharing only `A` and with sole cross edge `XY`
   are non-four-colourable exactly when both halves force `A=X` and `A=Y`.
   If one half permits unequal colours, colour-name permutations fixing `A`
   make `X,Y` different.  The converse is the bridge contradiction.

Consequently a non-four-colourable spindle needs at least

```text
255 + 255 - 1 = 509
```

vertices.  This argument covers vertex- and edge-deleted subgraphs, not merely
induced subgraphs: every positive colouring remains valid after restriction or
edge deletion.

The full 953-vertex spindles are exactly five-chromatic.  A fresh contrary-
terminal proof confirms that every four-colouring of `E` makes `O,V` equal, so
the bridge forbids four colours.  Cloning a checked four-colouring onto the two
halves and recolouring one bridge endpoint gives a checked five-colouring.

## Independent computational audit

The target source was unchanged from its cited commit
`9e7765b8a748642071e2e252218ac425e3846cdf`.  Its checksum manifest passed, its
main verifier reproduced all 16 frames and the 509 lower bound, and ordinary
and optimized controls agreed while rejecting all 14 malformed inputs.

`independent_check.py` imports none of the target verifier, target transform,
or parent radical arithmetic.  It binds the three input files by SHA-256 and
uses these independent choices:

- `Q(sqrt(3),sqrt(11))` is represented by coefficients indexed by the actual
  square-free radicands `1,3,11,33`, with multiplication derived from gcds.
- The two circle intersections are derived directly as
  `(±sqrt(247)/16, ±119/48)`.  For each intersection, the two orthogonal maps
  are reconstructed from determinant `±1`; the target's parity/reflection
  formula is not used.
- Cross distances are expanded as a constant part and a `sqrt(247)` part over
  the base field.  All 3,625,216 noncommon cross pairs are tested exactly.
- All 18 separating words and 253 deletion words are checked edge by edge
  against a freshly reconstructed 2,458-edge induced graph.

The audit found 953 vertices, 4,917 unit edges, one overlap, and one cross edge
in each of all 16 frames.  It also checked 78,672 five-colouring edge
inequalities across those frames.

The parent equality fact was not merely assumed.  I rebuilt its C++17
exhaustive checker in scratch and reproduced the complete contrary-terminal
search: 1,382,032 nodes and 691,060 conflicts.  `drat_recheck.py` then built a
fresh, standard exactly-one-colour CNF from the independent edge generator.
Glucose produced a 46,746,711-byte DRAT proof, and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`.  The CNF and
proof hashes exactly matched the parent validation record.

## Reproduction

The main independent audit needs CPython 3.11 or newer and no third-party
package:

```bash
cd hadwiger_nelson_e477_spindle_classification_review1
sha256sum -c SHA256SUMS
python3 -B independent_check.py
```

The deterministic result is `verification.json`.  The optional fresh proof
replay needs `python-sat==1.9.dev15`, `drat-trim`, and a new scratch directory:

```bash
python3 -B drat_recheck.py \
  --checker /path/to/drat-trim \
  --out /scratch/e477-spindle-drat-recheck
```

Its observed result is recorded in `drat_verification.json`.  The 47 MB proof,
CNF, and log are deliberately omitted from GitHub.

## Trust boundary and literature

The main audit trusts the pinned input bytes, CPython integer/JSON/SHA-256
operations, the finite loops, and the written isometry and colouring
arguments.  The equality replay additionally trusts Glucose only to generate
a proof and the C implementation of `drat-trim` to check it; the solver's
UNSAT return is not trusted.  The field-basis independence follows from the
independent square classes of `3`, `11`, and `247=13*19`.  No proof assistant
was used.

The construction mechanism follows Exoo and Ismailescu's alternate plane-
chromaticity proof: <https://arxiv.org/abs/1805.00157>.  Parts records the
509-vertex construction: <https://arxiv.org/abs/2010.12665>.  Haugland's
August 2026 paper also identifies 509 as the current record comparison:
<https://arxiv.org/abs/2608.04542>.  No novelty or priority claim is made for
the general single-bridge spindle argument.
