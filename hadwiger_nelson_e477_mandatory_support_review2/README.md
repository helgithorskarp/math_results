# Independent review and strengthening of the E477 support bound

**Verdict: verified and strengthened, within a restricted construction
family.**  The reviewed local claim said that every subgraph of the fixed
477-point equal-terminal source `E477` which still forces its terminals equal
has at least 256 vertices.  It followed that every non-four-colourable graph
in the classified two-half, one-overlap, sole-cross-edge spindle family has
at least 511 vertices.  The claim is correct.

The positive certificates here prove the stronger bounds

```text
forcing E477 half:              at least 258 vertices
non-four sole-bridge spindle:   at least 2*258-1 = 515 vertices.
```

This does **not** improve the unrestricted 509-vertex construction record.
It is not a lower bound for arbitrary plane unit-distance graphs, different
forcing sources, attachments with other cross edges, or assemblies with more
than two halves.  It is also only a lower bound inside the stated family:
existence at 258 or 515 is not asserted.

## Exact finite argument

The parent package supplies 253 distinct positive witnesses.  For each listed
nonterminal vertex `v`, a proper four-colouring of `E477-v` gives the two
marked terminals different colours.  Any subgraph which forces those
terminals equal must therefore contain all 253 listed vertices and both
terminals.  Call this 255-point set `C`.

The reviewed checker supplied one proper unequal-terminal colouring of the
659-edge induced graph on `C`, proving the claimed lower bound 256.  This
review reconstructs the 477 distinct exact points and all 2,458 unit edges,
checks all 253 deletion words, and independently verifies a bank of 19 other
proper colourings of `C`.  The reviewed 255-character word, whose SHA-256 is
`9c56ea2c8e90a42846f6e099f269c7e281c290558b99572c1ad15c59444ef360`,
does not occur in the review bank.

For each of the 222 vertices outside `C`, and for every one of their 24,531
unordered pairs, the verifier finds a bank colouring whose unused colour
lists extend properly to the extra one or two vertices.  Thus every induced
terminal-containing graph of order 255, 256, or 257 which contains the
mandatory set admits an unequal-terminal four-colouring.  A subgraph missing
a mandatory vertex has one by restriction of the corresponding deletion
witness.  Edge deletion cannot invalidate any positive colouring.  Therefore
an equality-forcing E477 subgraph has at least 258 vertices.

The already reviewed spindle classification proves that all 16 normalized
plane placements share exactly one terminal and have exactly one cross edge,
between the two remote terminals.  A non-four-colourable union of this form
requires both halves to force their marked pair equal: if either half has an
unequal-terminal colouring, colour-name permutations fixing the shared
terminal make the cross-edge colours different.  Hence its order is at least
`258+258-1=515`.

## Independent checks

`verify.py` imports neither the reviewed scratch checker nor the certificate
producer.  It represents `Q(sqrt(3),sqrt(11))` by coefficients indexed by the
actual radicands `1,3,11,33`, derives multiplication from square-free gcds,
and tests all 113,526 point pairs.  Its edge lists match the reviewed checker's
line hashes exactly.  It then checks every source deletion word, every bank
word, all 222 singleton extensions, and all 24,531 pair extensions.

The bank producer uses the direct two-equation unit predicate and deterministic
DSATUR only to find positive words.  `controls.py` compares that predicate to
the generic field verifier on every source pair, exhausts all 512 abstract
two-list/one-edge boundary cases, rejects three malformed certificates, and
shows that removal of any of the 19 bank words exposes an uncovered case.
Normal and optimized CPython verification agree byte-for-byte.

The earlier independent 16-frame geometry audit was rerun unchanged and
again reproduced its checked result.  It is published in the sibling
[`hadwiger_nelson_e477_spindle_classification_review1`](../hadwiger_nelson_e477_spindle_classification_review1/README.md)
directory; this package does not duplicate its 3,625,216 exact cross-pair
tests or its separately verified terminal-equality proof.

## Reproduction

CPython 3.11 or later and the standard library suffice:

```bash
cd hadwiger_nelson_e477_mandatory_support_review2
sha256sum -c SHA256SUMS
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
```

`verify.py` prints `EXPECTED.json`; `controls.py` prints `VALIDATION.json`.
To rebuild the compact positive certificate deterministically, run
`python3 -B build_certificate.py`, then repeat the checks.  The observed build
took about 34 seconds; verification took about 2 seconds and the full control
suite about 42 seconds on the review host.

Public source:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_e477_mandatory_support_review2>.
Verified mathematical commit:
`97b79af1b2b8ad71caabf3f98f07b495621ec007`.  No solver trace, private
state, credential, or large artifact is required.

## Trust boundary

The proof trusts the pinned parent bytes, CPython integer/JSON/SHA-256
operations, the finite loops, the radical-basis interpretation, and the
written mandatory-set and single-bridge arguments.  All new computational
evidence is positive-colouring evidence; no SAT/SMT `UNSAT` response is used.
The imported facts that `E477` really forces its marked terminals equal and
that the 16 physical frames have a single overlap and cross edge are covered
by the cited prior independent review.  No proof assistant was used.
