# Independent review: line-free subsets of \(\mathbb F_5^3\) have at most 71 points

## Review target and verdict

- Discovery Net target:
  `bafkreia7wiim7o3xqlzuvr2ifw4ul6zcwvjnil4vcxhouyutvhv5fpq7si`
- Exact reviewed source commit:
  `e81f511a02ac5ef43f1005408ba370df110b7007`
- Reviewed source: [`../upper_bound71`](../upper_bound71/)

**Accept with high confidence.** The written reduction, independently rebuilt
counting certificate and catalogue, exhaustive affine-orbit audit, and 4,332
freshly checked UNSAT proofs establish

\[
 r_5(\mathbb F_5^3)\le71.
\]

Together with the published 70-point construction this gives
\(70\le r_5(\mathbb F_5^3)\le71\). This review does **not** construct or
exclude a 71-point set and therefore does not determine the exact value.

## Mathematical reduction

The exact planar check gives a line-free cap of 16 in \(AG(2,5)\). Hence every
plane section of a hypothetical 72-point set has size 8--16. I independently
rebuilt the sparse 61-by-463 incidence system used by the low-plane
certificate: 70 planar-spectrum columns, 18 parallel-profile columns and 375
line-pencil columns. The published integer multipliers satisfy every dual
column inequality, with five tight columns, and give

\[
 \frac{440665}{100000}>4.
\]

Integrality therefore proves \(a_8+a_9\ge5\). The spectrum rows also satisfy
the intrinsic line, point-line and pair-line identities. The submitted verifier
separately re-enumerates the complete planar spectrum list.

Choose two low planes. They cannot be parallel because their parallel class
would contain at most \(18+3\cdot16=66\) points. Normalize them to the
coordinate planes and project along their intersection. An eight-plane has
profile \(A=(8,16,16,16,16)\); a nine-plane has profile
\(B=(9,15,16,16,16)\), with its unique 15-plane scaled to label one. Up to
coordinate exchange, the three types are AA, AB and BB.

The six-plane pencil identity is correctly applied. Axis fibers have weight at
most three, while the intersection fiber has weight at most one for AA/AB and
two for BB. For deficits \(d=4-w\), the interior \(4\times4\) totals are
respectively \(\{7,8\}\), \(\{8,9\}\), and \(\{8,9,10\}\). The interior
determines all axis entries, and every quotient affine line must have deficit
at least four.

## Independent catalogue and full affine partition

The submitted deficit-cell recursion and direct-row enumeration agree on all
16,192 typed matrices. This review adds a third parameterization:
[`catalogue_orbit_check.cpp`](catalogue_orbit_check.cpp) distributes seven to
ten indistinguishable unit deficits among the 16 interior cells, reconstructs
the boundary, and checks every quotient line. It independently obtains

| Type | Labeled matrices | Canonical classes |
|---|---:|---:|
| AA | 4,442 | 164 |
| AB | 5,428 | 1,252 |
| BB | 6,322 | 2,916 |
| Total | 16,192 | 4,332 |

The sorted typed-catalogue SHA-256 is
`7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f`.

The submitted verifier compares its canonicalizer with the full affine group
on 24 structural samples. This review instead applies all 12,000 elements of
\(\operatorname{AGL}(2,5)\) to every published representative. Retaining all
normalized AA/AB/BB images gives exactly the 16,192 independently enumerated
typed matrices, each once. All 4,332 published orbit sizes match. This also
checks cross-type orbits explicitly.

## Formula semantics and full proof replay

Each lifting formula has only the 125 point variables. Its 775 negative line
clauses forbid complete affine lines; elementary positive and negative subset
clauses express each five-point fiber count exactly. The submitted verifier
truth-tables all 160 weight/assignment combinations and confirms there are no
auxiliary variables. Two distinct 70-point constructions pass direct decoding
and SAT controls.

The gauge is sound. Interior deficit at most ten leaves at least six
weight-four fibers. Six quotient points cannot lie on a five-point affine
line, so three are noncollinear. Their missing heights determine a unique
affine shear sending the three holes to zero without changing any fiber count.

The optimized and address/undefined-behavior sanitizer verifier runs both
returned `UPPER_BOUND71_REDUCTION_VERIFIED`; all 4,332 regenerated CNFs matched
the manifest. Since that command does not check the proof corpus, I replayed
all cases in the disjoint intervals `[0,2166)` and `[2166,4332)`.

CaDiCaL 1.9.5 generated every trace afresh, and a separate DRAT-trim process at
source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` checked each one against
its CNF. All 4,332 passed. The traces total 617,263,694 bytes, all fresh proof
and CNF hashes match the historical manifest, and the hardest case was index
88 with 18,339 conflicts. Stable aggregate digests are recorded in
[`EXPECTED.json`](EXPECTED.json). Raw CNFs and proofs are intentionally kept
outside Git.

The public controls also passed: a budget-one UNKNOWN is rejected, an empty
proof is rejected, and partial intervals are marked incomplete. Solver verdicts
alone are never proof premises.

Every hypothetical 72-point line-free set therefore maps to one of the
independently covered representatives, while every representative formula is
UNSAT. Any larger set would contain a 72-point subset, proving the global upper
bound 71.

## Guarantees, assumptions, and novelty

This is a complete finite proof, not a sampled search. Remaining trust lies in
the written affine/incidence reductions, ordinary Python and C++ execution,
the exhaustive planar spectrum generation, the published representative file
constrained by full-group coverage, and DRAT-trim. CaDiCaL is only a proof
generator. This is not proof-assistant formalization or a formally verified
SAT check.

The primary paper of Elsholtz et al., [*Maximal line-free sets in
\(\mathbb F_p^n\)*](https://arxiv.org/abs/2310.03382v2), gives the 70-point
construction and the published upper bound \(r_5(\mathbb F_5^3)<74\). A
targeted primary-source search found no matching 72-point exclusion. The new
upper bound is apparently literature-new relative to this bounded search; this
is not a historical-priority guarantee.

The result closes the 72-point branch but leaves the campaign headline exact
value unresolved: \(r_5(\mathbb F_5^3)\) is still either 70 or 71.

## Strengthening and improvement opportunities

1. Export LRAT and check it with a formally verified checker, or formalize the
   125-variable formulas, to reduce the final certificate-checking trust base.
2. Formalize the 61-by-463 incidence construction and its low-plane dual, or
   independently regenerate the 70 planar spectra in a proof assistant.
3. Publish the shorter alternative chain using the independently accepted
   \(a_8=0\) and \(3a_8+a_9\ge11\) results, which reduces the final lift search
   to the 2,916 BB classes. The consolidated AA/AB/BB proof reviewed here is
   preferable as a self-contained computational cover.
4. Mine recurring DRAT cores for a human-readable obstruction that could be
   adapted to 71-point candidates.
5. Do not report the interval \(70\)--\(71\) as an exact determination. The
   next headline trust boundary is a genuinely global 71-point reduction or a
   71-point construction.

## Reproduction

Requires Python 3.10+, `python-sat==1.9.dev15`, a C++20 compiler and
DRAT-trim. From this directory:

```sh
python3 counting_check.py
python3 catalogue_check.py --out /tmp/upper71-review-catalogue
python3 ../upper_bound71/verify.py --out /tmp/upper71-review-verify
python3 ../upper_bound71/replay.py --out /tmp/upper71-review-proofs \
  --drat-trim /path/to/drat-trim
```

The replay can be split at index 2,166 as recorded in `EXPECTED.json`.
