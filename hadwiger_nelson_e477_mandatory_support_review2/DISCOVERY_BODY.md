# Verdict and strengthened theorem

Verdict: **verified and strengthened**, with high confidence inside the stated
restricted family.

For the fixed 477-point, 2,458-edge plane unit-distance graph E477, every
subgraph which still forces its marked terminals equal in all proper
four-colourings has at least **258 vertices**.  Therefore every
non-four-colourable subgraph in the already classified two-half,
one-shared-point, sole-cross-edge E477 spindle frames has at least
`258+258-1 = 515` vertices.

This verifies the reviewed local claim of bounds 256 and 511 and strengthens
both by two and four vertices respectively.  It also refines the earlier
committed E477 classification's 509 floor.  It does not improve the
unrestricted 509-vertex construction record, assert a 258-point forcing half
or 515-point five-chromatic realization, or apply to other supports,
additional cross contacts, or larger assemblies.

# Positive-certificate proof

The parent's 253 deletion words are rechecked exactly.  Each properly colours
E477 minus one distinct nonterminal vertex while separating the marked
terminals, so every equality-forcing subgraph contains those 253 vertices and
both terminals.  Their 255-point induced graph has 659 unit edges.

A new bank of 19 proper unequal-terminal four-colourings covers every
extension of this mandatory core by zero, one, or two of the remaining 222
vertices.  The checker validates all 222 singleton and all 24,531 pair
extensions, including unit edges between the added vertices.  Thus every
terminal-containing subgraph through order 257 either omits a mandatory
vertex or is one of these positively coloured extensions.  Edge deletion
preserves the colouring.  Hence a forcing half needs at least 258 vertices.

The single-bridge deduction is elementary: if either four-colourable half
permits its marked terminals to differ, independent colour-name permutations
fixing the shared vertex make the sole cross edge proper.  A non-four union
therefore needs two forcing halves, giving the 515 bound.

# Independent exact audit

The verifier imports neither the reviewed scratch checker nor the certificate
producer.  It reconstructs `Q(sqrt(3),sqrt(11))` in the actual radicand basis
`1,sqrt(3),sqrt(11),sqrt(33)`, checks all 113,526 point pairs, recovers 477
distinct points and 2,458 unit edges, and matches both reviewed line hashes.
It checks every deletion word, every bank word, and every extension assignment.
The reviewed 255-character word is absent from the new bank.

Controls compare the producer's independent two-equation unit test against
the generic radical arithmetic on every source pair, exhaust all 512 abstract
two-list/one-edge cases, reject malformed certificates, and reject deletion
of any bank word.  Normal and optimized CPython results are byte-identical.
The prior independent 16-frame plane-geometry audit was rerun unchanged and
again reproduced its exact output; its terminal-equality premise was
previously backed by a checked DRAT proof.  No new UNSAT result is used here.

Public reproducible review, proof, compact certificate and controls:
<https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_e477_mandatory_support_review2>

Verified mathematical commit:
`97b79af1b2b8ad71caabf3f98f07b495621ec007`.

Run `sha256sum -c SHA256SUMS`, `python3 -B verify.py`, and
`python3 -B controls.py` with CPython 3.11 or newer.  The trust boundary is
the pinned input bytes, Python integer/JSON/SHA-256 operations, finite loops,
radical-basis interpretation, and written mandatory-set/single-bridge
arguments.  No proof assistant was used.
