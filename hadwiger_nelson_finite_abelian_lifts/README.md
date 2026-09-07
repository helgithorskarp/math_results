# A complete finite abelian Cayley lift obstruction

**No graph improving the 509-vertex benchmark is produced.** This package
classifies a construction mechanism: injective unit-distance realizations in
the Euclidean plane of finite abelian Cayley graphs. It proves that these
graphs are exactly disjoint unions of identical Cartesian products of cycles
and unit segments, and hence have chromatic number at most three. The drawing
need not respect the group action, and nonedges need not have nonunit length.

As a complete target-sized test, define

```text
G_q = Cay((F_(q^2),+), {s : s^(q+1)=1}),   q a prime power, q^2 <= 508.
```

Exactly twelve parameters qualify. Eleven graphs have explicit short
rhombus contradictions to any injective planar unit-distance realization.
The exception is G_3 = C_3 square C_3, which has an exact nine-point drawing
and chromatic number three. The general proof actually excludes every
prime power q other than three, without an order bound.

The mechanism contains an abstract five-chromatic candidate: **G_11 has
121 vertices, 726 edges and chromatic number exactly five**. Its explicit
geometric contradiction explains why it cannot be a planar record graph.

| q | Vertices | Edges | Injective planar unit realization |
|---:|---:|---:|:---|
| 2 | 4 | 6 | Impossible |
| 3 | 9 | 18 | Exact drawing; chromatic number 3 |
| 4 | 16 | 40 | Impossible |
| 5 | 25 | 75 | Impossible |
| 7 | 49 | 196 | Impossible |
| 8 | 64 | 288 | Impossible |
| 9 | 81 | 405 | Impossible |
| 11 | 121 | 726 | Impossible; abstract chromatic number 5 |
| 13 | 169 | 1183 | Impossible |
| 16 | 256 | 2176 | Impossible |
| 17 | 289 | 2601 | Impossible |
| 19 | 361 | 3610 | Impossible |

## Reproduce the proof

From the repository root, CPython 3.11 or later and its standard library
suffice. No solver, network access, source dataset or numerical geometry is
needed for verification.

```sh
python3 hadwiger_nelson_finite_abelian_lifts/verify.py
python3 -O hadwiger_nelson_finite_abelian_lifts/verify.py
python3 hadwiger_nelson_finite_abelian_lifts/controls.py
python3 hadwiger_nelson_finite_abelian_lifts/produce.py \
  --output /tmp/hn-abelian-certificate.json
cmp /tmp/hn-abelian-certificate.json \
  hadwiger_nelson_finite_abelian_lifts/certificate.json
```

`EXPECTED.json` contains the deterministic verifier result. Main counts:
12 cases, 11 exclusions, 933 literal integer rhombus rows, 167586 complete
graph pair tests, all 36 exact drawing pairs for q=3, and 539 RUP additions
for the q=11 lower bound. Normal and optimized runs agree and take about
one second each on the recorded machine.

`controls.py` rejects 19 corruptions. It also independently enumerates all
500 Cayley presentations on all 16 finite abelian group types of orders
2 through 12, including empty connection sets. Full graph four-cycle
matrices over F_101 force collisions in precisely the 337 presentations
that fail the direct-product criterion; 163 pass. This is a finite audit
of the argument, not a substitute for the general proof.

## Files and exact conventions

- `PROOF.md`: the general theorem, exact norm-one specialization, finite
  row certificate, chromatic proof and limitations.
- `certificate.json`: all twelve quotient-field descriptions, full
  norm-one sets, edge counts and eleven additive relations (6465 bytes).
- `q11_four_unsat.drat`: the compact four-colour refutation (12449 bytes).
  Despite the file extension, every addition is checked as RUP; RAT is
  not used. Deletions can safely be ignored by this checker.
- `q11_five_colouring.json`: 121 colours in vertex-address order.
- `verify.py`: independent arithmetic, all-pairs graph reconstruction,
  literal integer rhombus identities, exact drawing and RUP checker. It
  imports no producer code.
- `produce.py`: independently regenerates field and relation certificates.
- `pilot.py`: optional capped solver discovery and proof regeneration.
- `VALIDATION.json` and `SHA256SUMS`: compact validation and file digests.

For a field with prime p and degree d, integer address
`a_0 + p*a_1 + ... + p^(d-1)*a_(d-1)` means the polynomial
`a_0 + a_1 X + ... + a_(d-1) X^(d-1)` modulo the listed monic modulus.
Modulus coefficients are stored in ascending degree order. At q=11 this
is X^2+1 over F_11. Colours are integers 0 through 4. All binary proof
data are published as ordinary textual clauses.

## Optional solver reproduction and the frozen pilot

The producer environment used Python 3.11.2, python-sat 1.9.dev15 and
CaDiCaL 1.9.5 on Linux. With that optional dependency installed:

```sh
python3 hadwiger_nelson_finite_abelian_lifts/pilot.py \
  --q11-only --output /tmp/hn-abelian-q11
cmp /tmp/hn-abelian-q11/q11.drat \
  hadwiger_nelson_finite_abelian_lifts/q11_four_unsat.drat
cmp /tmp/hn-abelian-q11/q11_five_colouring.json \
  hadwiger_nelson_finite_abelian_lifts/q11_five_colouring.json
```

The complete optional pilot omits `--q11-only`. It makes one four-colour
query per q with a fixed cap of 100000 conflicts, followed by a capped
five-colouring query for q=11. The original pilot had eight SAT results,
three UNSAT results (q=11,13,17), and one UNKNOWN (q=19, exactly 100000
conflicts). UNKNOWN is not a chromatic conclusion and its cap was not
extended. The q=13 and q=17 traces were independently checked with
drat-trim but are ancillary to the theorem and are not published here.
All geometric exclusions are unconditional regardless of these solver
outcomes; only the compact q=11 chromatic certificate is a proof input.

The initial CaDiCaL proof export omitted an unflushed final block and was
rejected. `pilot.py` explicitly flushes C streams on the recorded POSIX
platform before reading the proof; destroying the solver alone did not
fix this build. The corrected complete q=11 proof and five-colouring both
regenerate byte for byte. A second solver, Glucose 4, produced a different
refutation checked by the same RUP verifier against independently built
edges `(dx*dx+dy*dy) % 11 == 1`. No incomplete proof supports a claim.

## Scope and provenance

This closes injective realizations of the entire stated abstract graphs.
It does not close noninjective graph homomorphisms, chosen subgraphs,
edge-deleted graphs, or infinite additive direction graphs. It is not an
extraction result for a Parts or Haugland host. The ordinary plane target
of a five-chromatic unit-distance graph on at most 508 vertices is open.

Rhombus logic is established methodology; see Alexeev, Mixon and Parshall,
[Section 4](https://arxiv.org/html/2412.11914v2). The distinction from
infinite groups of plane directions is explicit in
[Eng et al.](https://arxiv.org/html/2511.10813v1). No priority claim is made
for those methods or for Cartesian products of unit-distance graphs.
The proof and finite certificates here are self-contained applications to
this construction gate. There are no imported coordinate tables.

Before publication, shared evidence was refreshed through Discovery Net
height 3794. The accepted
[Snail classification review](../hadwiger_nelson_snail_dihedral_review1/REVIEW.md)
and teammate's new
[769-point host closure](../hadwiger_nelson_joint769_order508_closure/README.md)
were inspected and preserved. They are campaign context, not mathematical
premises of this theorem; this milestone remains in the construction lane.

Trust boundaries are the written, unformalized planar rhombus and finite
group arguments; CPython's exact integer/Fraction arithmetic and parsing;
and the small checker implementations. This package has internal
independent checks but is not yet externally reviewed or formalized.
