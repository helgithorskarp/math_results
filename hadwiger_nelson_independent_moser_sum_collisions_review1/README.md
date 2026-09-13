# Independent review: collisions in a three-Moser-spindle sum

## Verdict

**ACCEPT with high confidence** at mathematical target commit
`55f27a5af19948be8ddd9e0d0015b178bdc20936`.
The reviewed package is
[`hadwiger_nelson_independent_moser_sum_collisions`](../hadwiger_nelson_independent_moser_sum_collisions/README.md).

For the displayed seven-point Moser spindle `M` and arbitrary unit complex
numbers `u,v`, let

```text
S(u,v) = M + uM + vM
```

as a set of actual plane points, with every pair at Euclidean distance
exactly one made adjacent. If the formal map from the 343 addresses in
`M^3` to `S(u,v)` is noninjective, the resulting complete strict plane
unit-distance graph has chromatic number exactly four.

Thus any five-chromatic member of this particular construction family must
have all 343 formal points distinct. The injective family remains open. This
is a record-relevant restricted-family exclusion, not a five-chromatic
construction, a proof that any injective member is five-chromatic, or a
global lower bound. The published 509-vertex record is unchanged.

## Mathematical audit

The reduction and every boundary between structural and enumerated cases were
checked independently.

1. A collision has differences `a+ub+vc=0`, where each of `a,b,c` is in
   `M-M`. Exactly one nonzero difference is impossible. Hence every collision
   is covered by the two-nonzero or three-nonzero branch; no sampled-angle
   assumption enters.
2. For three nonzero differences, taking norms gives
   `H=A+B-C` and `Delta=4AB-H^2`. The two displayed solutions for the
   auxiliary direction exhaust the circle intersection: negative `Delta` is
   nonphysical, zero gives one solution, and positive `Delta` gives two.
   A positive element of `Q(sqrt(33))` that is a square in
   `E=Q(i sqrt(3),i sqrt(11))` is already a square in its real subfield, so
   the in-field and genuine quadratic-extension branches are exhaustive.
3. The clean-room checker uses the different representation
   `E=Q(sqrt(33))[alpha]/(alpha^2+3)`. It reconstructs all 34 nonzero spindle
   differences, seven norms, 1,716 in-field phase pairs, 6,528 outside-field
   pairs, 32 nonsquare radicands and 31 extension classes. Its complete
   serialized root-inventory hash exactly matches the target.
4. The 2-adic square test is exact: the chosen `sqrt(33)=1 mod 8` branch is
   Hensel-lifted until the valuation and three odd-unit bits stabilize. Of the
   outside-field pairs, 3,024 embed compatibly into the accepted local
   colouring field; the remaining 3,504 receive explicit positive words.
5. For two nonzero differences, permuting the three summands and applying a
   common unit rotation puts the support in the form
   `B+vM`, `B=M+uM`, with `u` among 30 exact phases. The identity
   `lambda*conj(M)=M` reduces these to 16 conjugation representatives without
   restricting the arbitrary phase `v`.
6. When `v` is outside `E`, the map `B x M -> B+vM` is injective. Every
   non-Cartesian unit contact has the monic quadratic
   `v^2-Tv+J=0`. Its two physical roots have the same complete edge graph:
   any further outside-field contact sharing one root has the same irreducible
   monic quadratic. Grouping by `(T,J)` is therefore exact, not an angular
   sample.
7. Since `B,M` lie in the fixed local integer ring, the residue-sum colouring
   closes `T=0`, trace valuation at least one, and trace valuation `-1` by a
   direct valuation argument. At trace valuation zero, the independently
   audited unit-trace lemma applies: after writing `w=v/T`, its polynomial
   reduces to `Z^2+Z+1`; the two simple residue roots Hensel-lift compatibly
   with conjugation, embedding the whole quadratic field into the four-colour
   local field. Only trace valuation at most `-2` remains finite.
8. The alternate-basis audit reconstructs all 5,064 retained contact
   quadratics, matches the target's complete quadratic-inventory and
   edge-stream hashes, verifies every event edge against its assigned word,
   and checks that every word descends through the fixed two-factor
   collisions. The two roots of each quadratic share that verified graph.

Every support contains the original seven-point, eleven-edge Moser spindle,
so the four-colour upper bounds are exact rather than merely sufficient.

## Reproduction and independent evidence

The target package was replayed with CPython 3.11.2 and g++ 12.2.0. The
204,793-byte certificate has SHA-256
`2795687647a8f8d2b01d6d7c844d3d0d06afd9b3000f5a24341d03b5b3c26765`.
The complete release verifier matched `expected.json` byte-for-byte. A second
complete replay used a native library compiled with undefined-behaviour
sanitization and assertions disabled. Both exact native metric derivations
agreed on all 433,052,116 audited unordered physical pairs:

- 204,010,800 pairs over the 3,504 explicit three-factor supports;
- 229,041,316 pairs over the 5,064 two-factor event graphs.

All 8,568 positive exceptional colourings passed, as did the two malformed
word controls, the collision-disagreement control, every constant-colour
rejection, 1,140 independent rational metric controls, 328 valuation controls
and six native range guards. The package manifest passed.

`independent_audit.py` imports no target code. Besides matching the complete
phase and quadratic inventories, it verifies all 3,504 explicit collision
descents, all 483 used words on the 1,617 Cartesian product edges, every
two-factor event edge, the exact per-case edge histograms, the spindle's
three-colour obstruction and a positive four-colouring. Normal and
assertion-disabled executions agree.

The accepted base-field theorem and its existing external checker were
replayed. The unit-trace theorem had no external review in the committed
Discovery Net view, so this review did not silently inherit it: its
Hensel/conjugation proof was independently checked and all three of its exact
algebra, geometry and alternate-representation suites were replayed.

## Trust boundary and limitations

The universal reduction and local-field arguments are written mathematics,
not proof-assistant formalizations. The independent program replaces the
target's field representation and inventory implementation, but does not
repeat the 204-million-pair three-factor edge census with a third metric.
That physical census is supported by the target's two algebraically distinct
exact metrics, a complete sanitized replay, exact root inventory agreement,
collision-descent checks and positive certificates. Both target metrics share
the exact coordinate generator.

The native verifier uses signed 128-bit integers. Inspection of every
pre-promotion operation and the enforced `10^9` input guards confirms the
claimed degree-three expressions remain far below `2^127`; representative
and full undefined-behaviour-sanitized runs report no issue. No floating
point, solver verdict, omitted private input or uncommitted large certificate
is a proof premise.

Most importantly, this theorem says nothing about injective phase pairs,
other summands, deformations of the spindle, or arbitrary plane
unit-distance graphs. It distinguishes actual exact plane realizations from
formal address graphs by quotienting every collision and enumerating every
strict physical unit pair before applying the positive colour words.

Record calibration uses Parts,
[*Graph minimization*](https://arxiv.org/abs/2010.12665). Haugland's
[2026 construction](https://arxiv.org/abs/2608.04542) has 2,131 vertices
under the additional Moser-spindle-free restriction and does not supersede
the unrestricted 509-vertex benchmark.
