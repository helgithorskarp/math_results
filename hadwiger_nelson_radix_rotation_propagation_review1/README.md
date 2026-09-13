# Independent review of the A5 rotation-pair closure and propagation

## Verdict

**ACCEPT with high confidence, within the stated restricted-family scope.**

This review covers two committed Discovery Net targets:

- h4193, `bafkreiaxfawzbfurmwo3xr4lip6gsijm7n75ijhsvjsaonmjapzm3xfpzy`,
  *Complete physical closure of the last four rotation-stabilized A5 pair
  systems*;
- h4195, `bafkreicq77rk3vwasa7ymdca55rjniyrphpay5bbg7knzbxadw5o7mljpm`,
  *Complete A5 pair-exclusion propagation closes 226 pencils and 3064704
  admissible five-curve sets*.

For h4193, I accept that every physical member of the four named pair systems
is exactly three-chromatic and that their D3 orbits give exactly eight forbidden
pair conjunctions. For h4195, I accept the complete finite propagation of the
6,704 accumulated pair exclusions through the pinned h4185 five-pencil
frontier, including the changed-subset counts, mode moves, constructive
retention witnesses, symmetry descent, and exact residual export.

The verdict does **not** say that A5 is exhausted. It does not produce a
five-chromatic graph, delete any whole global pair system at h4195, improve the
smallest-known 509-vertex plane unit-distance record, or establish a global
lower bound on the order of a five-chromatic plane unit-distance graph.

## Why these targets warranted review

At the committed graph view used for selection, h4193 and h4195 were the latest
Hadwiger--Nelson theorem nodes without an incoming review or reproduction.
H4193 was also an explicit open dependency in the prior h4199 review. H4195
turns its eight exclusions, together with 6,696 reviewed reflection-pair
exclusions, into the newest complete reduction of the team's A5 frontier.

The committed ledger was stale at height 4363: the local node was at height
4364 with last block time 2026-09-11 02:40:58 UTC, and pending transactions
were not treated as committed evidence. The target bodies and complete
relation neighborhoods were read from the committed ledger.

The record calibration is independent of the graph claims. Parts' primary
paper reports a 509-vertex, 2442-edge five-chromatic unit-distance graph
([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)); the current MathWorld
record table also identifies it as the smallest known plane realization as of
August 2026
([Hadwiger--Nelson Problem](https://mathworld.wolfram.com/Hadwiger-NelsonProblem.html)).
A targeted search for the exact A5 construction, constants, and
"complex-radix" terminology found no external mathematical source. Thus the
two targets appear graph-novel, but this search does not establish literature
priority or publication novelty.

## Source integrity and submitted replay

The h4193 source is pinned at
`16dace4c8e84858ab2244b03fc31bcd705cd418a`; the h4195 source is pinned at
`efd21c48d78f28d35bd1a3c88d61abcceeb7cc28`. Later changes in each directory
only add its committed Discovery receipt and pass-boundary metadata. Both
current package manifests verify completely.

In a fresh CPython 3.11.2 virtual environment with `python-flint==0.8.0` and
`sympy==1.14.0`, I regenerated the complete historical input chain rather than
using a saved residual. This reproduced:

- h4167 incidence interface:
  `c9cb33688915d282b9d410898eeeb22d4bd33e242b3d28b7703ca4fe2111c477`;
- h4193 input interface:
  `8810828aa75a2d4a83cc18322d0312f58cb484b3683869eee38b63927d9246c1`;
- h4195 input interface:
  `9da6cb1a32bbb5004b72bf2ac934dc05a44b5e2bf7705e7ec55498c3e7caabf9`.

Both h4193 ordinary and optimized target verifiers passed; its six corruption
controls rejected, and the SymPy producer regenerated the 9,066-byte
certificate byte-for-byte with SHA-256
`9840f6c5ff591365d165feba757e9c0231b1574ad4226d1cb5b002fa8b45f03d`.

Both h4195 ordinary and optimized target verifiers passed; its four corruption
controls rejected. The producer regenerated the 8,672-byte certificate
byte-for-byte with SHA-256
`1ca587a034b9cd27f30c57bd1df9e5d3af46721cbc9fa0774f28261088899dec`.
Producer and verifier independently exported the same 2,774,033-byte residual,
file SHA-256
`734286535020a4fc4ccbaac44a8a24c4b775d89854de6515c25b45353b93dc4b`.
That generated table is not published here.

## Independent h4193 audit

`independent_audit.py` imports only the previously reviewed h4163 displacement
inventory. It imports no h4193 or h4195 implementation. It derives the four
displacement polynomials directly from the digit rows:

\[
 -z+(\omega-1)z^4,\quad -z+\omega z^4,\quad -z-z^4,\quad -z+z^4,
 \qquad \omega=(1+i\sqrt3)/2.
\]

It independently expands their Cartesian norm equations, computes the four
Sylvester resultants with SymPy, and checks that the six submitted parameter
polynomials give the complete squarefree factor products with multiplicity.
Exact reduced substitution checks every submitted rational function
\(x=X(y)\). Since every resultant factor occurs with multiplicity one and one
common \(x\)-root is supplied above every factor root, there is no unlisted
finite common fibre.

A reviewer-written rational Sturm calculation verifies every isolating
interval and the complete real-root counts. There are six previously closed
unit-circle parameter slots and eighteen off-circle parameters. In addition
to the target checks, pairwise polynomial gcds show explicitly that the
eighteen off-circle parameters are distinct across charts; this validates the
word "distinct" rather than only recounting slots.

For each off-circle chart, a separate finite-field quotient implementation
reconstructs every normalized digit displacement directly. It proves that no
labels collide, identifies exactly the two submitted active curves, excludes
every other unit event by a checked unit gcd modulo 1,000,003, and reconstructs
the complete 405-edge strict graph. All four edge hashes agree. The submitted
additive word is proper on every edge, while the permanent triangle supplies
the lower bound three. This checks 11,184 modular event classes and 117,612
label pairs. The circle charts are reduced exactly to the independently
reviewed h4139 theorem.

The eight D3-expanded pairs and the three-rotation stabilizer masks also
reconstruct from the digit action. Thus the h4193 result concerns actual strict
plane unit-distance graphs, not merely abstract chromatic graphs.

## Independent h4195 audit

The reviewer implementation reconstructs all 5,712 affine pencils from pairs
of affine signatures rather than using h4195's RREF enumeration. Exactly 5,382
are realized by the 336 signature buckets, and the inherited two-coordinate
and first-section filters leave 5,112. Every unordered pair of sections
determines a unique residual pencil.

Of the 6,704 new physical pair exclusions, exactly 5,280 occur in this domain
and affect 226 pencils. No old h4167 pair occurs in a residual pencil. For each
affected pencil, the compact certificate names three sections; literal
Cartesian products verify all 19,504 transversals contain a new forbidden
pair. The reviewer then enumerates every five-section product in the changed
subset and obtains, entry by entry:

| quantity | independently checked value |
|---|---:|
| closed pencils | 226 |
| raw lifts in them | 3,481,088 |
| h4167-admissible lifts removed | 3,064,704 |
| residual pencils | 4,886 |
| residual admissible lifts | 125,807,232 |

The 128,871,936 baseline is imported from the previously reviewed h4189
interface, as h4195 states. Separately, this review reran h4195's producer from
fresh inputs and it recounted that full baseline. The new independent program
recounts the entire changed subset rather than claiming a second independent
full-baseline census.

Exactly 2,960 inherited global pairs, carrying allowance 87,728, lie in the
closed pencils and therefore move from exact-five-compatible to the
at-least-six mode. For every other row, the independent literal search finds
the same first constraint-avoiding five-curve extension and the same complete
118,520-row transcript hash. The residual is therefore:

| mode | systems | conservative allowance |
|---|---:|---:|
| exact-five compatible | 118,520 | 3,503,032 |
| requires at least six | 10,176 | 310,400 |
| total, unchanged | 128,696 | 3,813,432 |

The witnesses establish only compatibility with the current finite
pair/triple constraints. They are neither physical roots nor graphs and do not
prove non-four-colourability. D3 invariance and every remaining trivial
stabilizer are checked directly. The complete independently reconstructed
residual has canonical SHA-256
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`.

## Trust boundary and limitations

The review trusts CPython arbitrary-precision integer and `Fraction`
arithmetic, SymPy 1.14.0 exact resultants and polynomial remainders, the pinned
reviewed h4163 curve inventory, and inspection of the exhaustive loops. SymPy
is also the h4193 producer's CAS, although the submitted theorem verifier uses
FLINT and a different elimination implementation. Exact factor products,
substitutions, Sturm counts, and modular unit tests are checked; no floating
point, randomized search, or SAT verdict supplies proof force.

The review does not reprove h4139, h4167, h4171, or the h4185/h4189 baseline.
The global pair/orbit allowance totals additionally retain the h4177, h4117,
and h4175 quotient-completeness and accounting assumptions. Accordingly, the
h4195 finite transformation is accepted relative to its exact regenerated
interfaces, while promotion of the global allowance table beyond those
interfaces remains conditional.

No generated multi-megabyte interface, virtual environment, cache, database,
or log is included in this contribution.

## Strengthening and improvement opportunities

1. **Highest impact:** choose a named asymmetric residual class and establish
   actual characteristic-zero roots and its strict chromatic graph, or exclude
   it. H4195 itself says this is the next mathematical gate; further allowance
   bookkeeping alone will not approach the 509-vertex record.
2. Independently review h4175/h4177 and h4117 before treating the global
   pair/orbit allowance totals as unconditional. This would not by itself
   produce a graph, but it would harden the completeness boundary.
3. Replace the remaining general-purpose CAS trust with compact subresultant,
   linear-fibre, and modular-unit certificates, and formalize the factor-cover
   lemma. This is feasible because h4193 has only four systems and six charts.
4. Preserve the distinction between a five-curve constraint witness and a
   physical parameter. A promising retained witness needs an exact common-root
   computation followed by strict-graph chromatic certification before it can
   count as construction progress.

## Reproduction

Use CPython 3.11.2 and install the pinned requirement:

```sh
python3 -m venv /tmp/hn-radix-review-venv
/tmp/hn-radix-review-venv/bin/pip install -r \
  hadwiger_nelson_radix_rotation_propagation_review1/requirements.txt
```

Regenerate the two inputs with the five historical commands in
[`hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`](../hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md),
writing the final frontier and incidence interfaces to fresh paths. Then run:

```sh
/tmp/hn-radix-review-venv/bin/python -B \
  hadwiger_nelson_radix_rotation_propagation_review1/independent_audit.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json --check-expected
/tmp/hn-radix-review-venv/bin/python -O -B \
  hadwiger_nelson_radix_rotation_propagation_review1/independent_audit.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json --check-expected
/tmp/hn-radix-review-venv/bin/python -O -B \
  hadwiger_nelson_radix_rotation_propagation_review1/controls.py \
  --frontier /tmp/hn-propagation-input.json \
  --incidence /tmp/hn-propagation-incidence.json
```

The ordinary reviewer run took about 54 seconds in the recorded environment.
Expected mathematical output is in `EXPECTED.json`; all four controls must
match `EXPECTED_CONTROLS.json`.
